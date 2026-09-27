"""
Fear & Greed Index Mixin
Adds market sentiment filtering to any strategy.

Features:
- Crypto Fear & Greed Index integration (alternative.me API)
- Historical data support for backtesting (CSV file)
- Real-time sentiment data with caching for live/dry-run
- Entry filtering based on market sentiment
- Configurable via hyperopt parameters
- Works in both backtest and live modes

Setup for backtesting:
    1. Download historical data:
       docker exec freqtrade bash -c "curl 'https://api.alternative.me/fng/?limit=365&format=csv' > /freqtrade/user_data/fear_greed_history.csv"
    
    2. The CSV will have columns: timestamp,value,value_classification
       Example: 1732060800,74,Greed

Usage:
    from strategies.base import PerformanceFilterStrategy
    from strategies.mixins import FearGreedMixin
    
    class MyStrategy(PerformanceFilterStrategy, FearGreedMixin):
        def populate_indicators(self, dataframe, metadata):
            # Add Fear & Greed index to dataframe
            dataframe = self.add_fear_greed_to_dataframe(dataframe, metadata)
            return dataframe
        
        def populate_entry_trend(self, dataframe, metadata):
            conditions = []
            
            # Check Fear & Greed
            sentiment_ok = self.check_fear_greed(dataframe)
            if sentiment_ok is not None:
                conditions.append(sentiment_ok)
            
            # ... your other conditions ...
            
            if conditions:
                dataframe.loc[reduce(lambda x, y: x & y, conditions), 'enter_long'] = 1
            return dataframe
"""

from freqtrade.strategy import BooleanParameter, IntParameter
import pandas as pd
import requests
from datetime import datetime, timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class FearGreedMixin:
    """
    Mixin for Fear & Greed Index sentiment filtering.
    
    This mixin provides methods to:
    1. Fetch Fear & Greed Index from alternative.me API
    2. Cache sentiment data to avoid rate limits
    3. Filter trades based on market sentiment
    
    Fear & Greed Index values:
    - 0-24: Extreme Fear (good time to buy)
    - 25-44: Fear
    - 45-55: Neutral
    - 56-75: Greed
    - 76-100: Extreme Greed (good time to sell)
    
    To use: Add this mixin to your strategy class inheritance
    """
    
    # ============================================================
    # FEAR & GREED PARAMETERS (Can be hyperopt optimized)
    # ============================================================
    fear_greed_enabled = BooleanParameter(
        default=False,  # Disabled by default (requires API calls)
        space="buy",
        optimize=True,
        load=True
    )
    
    fear_greed_min = IntParameter(
        0, 50,
        default=25,
        space="buy",
        optimize=True,
        load=True
    )
    
    fear_greed_max = IntParameter(
        50, 100,
        default=75,
        space="buy",
        optimize=True,
        load=True
    )
    
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self._fear_greed_cache = None
        self._fear_greed_cache_time = None
        self._fear_greed_cache_duration = timedelta(hours=1)  # Cache for 1 hour
        self._fear_greed_historical_data = None
        self._historical_data_loaded = False
        
        # Detect run mode
        self.is_backtesting = config.get('runmode') in ['backtest', 'hyperopt']
    
    def load_historical_fear_greed_data(self) -> None:
        """
        Load historical Fear & Greed Index data from CSV file.
        Called once during initialization.
        
        CSV format (from alternative.me API):
        fng_value,fng_classification,date
        18-11-2025,11,Extreme Fear
        17-11-2025,14,Extreme Fear
        
        Note: The API returns CSV with JSON header that we skip.
        """
        if self._historical_data_loaded:
            return
        
        csv_path = Path('/freqtrade/user_data/fear_greed_history.csv')
        
        if not csv_path.exists():
            logger.warning(
                f"⚠️  Fear & Greed historical data not found at {csv_path}. "
                f"Run: docker exec freqtrade bash -c \"curl 'https://api.alternative.me/fng/?limit=365&format=csv' > {csv_path}\""
            )
            self._historical_data_loaded = True
            return
        
        try:
            # Load CSV directly (now cleaned)
            df = pd.read_csv(csv_path)
            
            # Expected columns: fng_value, fng_classification, date
            # Rename to standardized names
            df = df.rename(columns={
                'fng_value': 'date',
                'fng_classification': 'value',
                'date': 'classification'
            })
            
            # But actually the order in file is: date, value, classification
            # So we need to swap back
            df.columns = ['date', 'value', 'classification']
            
            # Convert date from DD-MM-YYYY to datetime
            df['datetime'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
            
            # Set datetime as index for easy lookup
            df = df.set_index('datetime').sort_index()
            
            # Convert value to int
            df['value'] = df['value'].astype(int)
            
            # Store data
            self._fear_greed_historical_data = df
            self._historical_data_loaded = True
            
            logger.info(
                f"✅ Loaded {len(df)} days of Fear & Greed historical data "
                f"({df.index.min().date()} to {df.index.max().date()})"
            )
        
        except Exception as e:
            logger.error(f"❌ Failed to load Fear & Greed historical data: {e}")
            self._historical_data_loaded = True
    
    def get_fear_greed_for_timestamp(self, timestamp: pd.Timestamp) -> int:
        """
        Get Fear & Greed Index for a specific timestamp (backtest mode).
        
        Args:
            timestamp: The timestamp to lookup
            
        Returns:
            int: Fear & Greed Index value (0-100), or None if not found
        """
        if self._fear_greed_historical_data is None:
            return None
        
        try:
            # F&G is daily data - extract just the date
            date_only = timestamp.date()
            
            # Convert to pandas Timestamp at midnight for lookup
            lookup_time = pd.Timestamp(date_only)
            
            # Try exact match first
            if lookup_time in self._fear_greed_historical_data.index:
                return int(self._fear_greed_historical_data.loc[lookup_time, 'value'])
            
            # If no exact match, find nearest date within 1 day
            time_diff = abs(self._fear_greed_historical_data.index - lookup_time)
            nearest_idx = time_diff.argmin()
            
            if time_diff.iloc[nearest_idx] <= pd.Timedelta(days=1):
                value = int(self._fear_greed_historical_data.iloc[nearest_idx]['value'])
                return value
            
            return None
        
        except Exception as e:
            logger.debug(f"Failed to get F&G for timestamp {timestamp}: {e}")
            return None
    
    def get_fear_greed_index(self) -> int:
        """
        Fetch current Fear & Greed Index from API (live/dry-run mode).
        Uses caching to avoid excessive API calls.
        
        Returns:
            int: Fear & Greed Index value (0-100), or None if unavailable
        """
        # Check cache
        if (self._fear_greed_cache is not None and 
            self._fear_greed_cache_time is not None and
            datetime.now() - self._fear_greed_cache_time < self._fear_greed_cache_duration):
            return self._fear_greed_cache
        
        # Fetch from API
        try:
            response = requests.get(
                'https://api.alternative.me/fng/?limit=1',
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            
            if 'data' in data and len(data['data']) > 0:
                fear_greed_value = int(data['data'][0]['value'])
                
                # Update cache
                self._fear_greed_cache = fear_greed_value
                self._fear_greed_cache_time = datetime.now()
                
                logger.info(f"📊 Fear & Greed Index (Live): {fear_greed_value}")
                return fear_greed_value
        
        except Exception as e:
            logger.error(f"❌ Failed to fetch Fear & Greed Index from API: {e}")
            return None
    
    def add_fear_greed_to_dataframe(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Add Fear & Greed Index values to dataframe.
        Call this in your populate_indicators() method.
        
        Args:
            dataframe: Strategy dataframe
            metadata: Pair metadata
            
        Returns:
            dataframe with 'fear_greed_index' column added
        """
        if not self.fear_greed_enabled.value:
            return dataframe
        
        if self.is_backtesting:
            # Backtest mode: Load historical data and map to timestamps
            if not self._historical_data_loaded:
                self.load_historical_fear_greed_data()
            
            if self._fear_greed_historical_data is None:
                logger.warning("⚠️  No historical Fear & Greed data available for backtest")
                dataframe['fear_greed_index'] = None
                return dataframe
            
            # Map each candle timestamp to F&G value
            dataframe['fear_greed_index'] = dataframe['date'].apply(
                lambda x: self.get_fear_greed_for_timestamp(pd.Timestamp(x))
            )
            
            logger.info(
                f"📊 Fear & Greed (Backtest): "
                f"{dataframe['fear_greed_index'].notna().sum()} / {len(dataframe)} candles have F&G data"
            )
        
        else:
            # Live/Dry-run mode: Get current value and apply to all rows
            current_fg = self.get_fear_greed_index()
            dataframe['fear_greed_index'] = current_fg
        
        return dataframe
    
    def check_fear_greed(self, dataframe: pd.DataFrame) -> pd.Series:
        """
        Check if Fear & Greed Index is within acceptable range.
        Call this in your populate_entry_trend() method.
        
        IMPORTANT: You must call add_fear_greed_to_dataframe() in populate_indicators() first!
        
        Supports both normal and reversed ranges:
        - Normal: min=0, max=60 → trade when F&G is 0-60 (buy during fear)
        - Reversed: min=60, max=100 → trade when F&G is 60-100 (buy during greed)
        
        Args:
            dataframe: Strategy dataframe (must have 'fear_greed_index' column)
            
        Returns:
            pd.Series: Boolean series for the condition (or None if disabled)
        """
        if not self.fear_greed_enabled.value:
            return None
        
        if 'fear_greed_index' not in dataframe.columns:
            logger.error(
                "❌ Fear & Greed Index not found in dataframe! "
                "Did you call add_fear_greed_to_dataframe() in populate_indicators()?"
            )
            return None
        
        # Determine if range is reversed (min > max)
        min_val = self.fear_greed_min.value
        max_val = self.fear_greed_max.value
        
        # Check if each row's F&G value is within range
        # If F&G is None (no data), condition is False (blocks trade)
        if min_val <= max_val:
            # Normal range: min to max (e.g., 0-60 for contrarian/fear buying)
            in_range = (
                (dataframe['fear_greed_index'].notna()) &
                (dataframe['fear_greed_index'] >= min_val) &
                (dataframe['fear_greed_index'] <= max_val)
            )
        else:
            # Reversed range: min to 100 OR 0 to max (e.g., 60-100 for greed buying)
            in_range = (
                (dataframe['fear_greed_index'].notna()) &
                (
                    (dataframe['fear_greed_index'] >= min_val) |  # Above min (e.g., >= 60)
                    (dataframe['fear_greed_index'] <= max_val)    # Below max (e.g., <= 100)
                )
            )
        
        # Log summary
        if self.is_backtesting:
            blocked_count = (~in_range).sum()
            total_count = len(dataframe)
            if blocked_count > 0:
                range_desc = (
                    f"[{min_val}, {max_val}]" if min_val <= max_val 
                    else f"[{min_val}, 100] OR [0, {max_val}]"
                )
                logger.info(
                    f"🚫 Fear & Greed Filter: Blocked {blocked_count}/{total_count} candles "
                    f"(range: {range_desc})"
                )
        else:
            # Live mode: log current value
            if len(dataframe) > 0:
                current_fg = dataframe['fear_greed_index'].iloc[-1]
                if pd.isna(current_fg):
                    logger.warning("⚠️  Fear & Greed Index unavailable - BLOCKING trade")
                elif not in_range.iloc[-1]:
                    range_desc = (
                        f"[{min_val}, {max_val}]" if min_val <= max_val 
                        else f"[{min_val}, 100] OR [0, {max_val}]"
                    )
                    logger.info(
                        f"🚫 Fear & Greed ({current_fg:.0f}) outside range "
                        f"{range_desc} - BLOCKING trade"
                    )
        
        return in_range
