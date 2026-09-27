"""
Higher Timeframe (HTF) Trend Mixin
Adds dynamic higher timeframe trend checking to any strategy.

Features:
- Automatically selects appropriate HTF based on strategy timeframe
- Multiple trend detection methods: EMA, SuperTrend, PSAR
- Configurable via hyperopt parameters
- Works in both backtest and live modes

Usage:
    from strategies.base import PerformanceFilterStrategy
    from strategies.mixins import HTFTrendMixin
    
    class MyStrategy(PerformanceFilterStrategy, HTFTrendMixin):
        # Choose trend method (override in your strategy)
        htf_trend_method = CategoricalParameter(['ema', 'supertrend', 'psar'], default='supertrend', ...)
        
        def populate_indicators(self, dataframe, metadata):
            # Add HTF trend indicators
            dataframe = self.add_htf_trend_indicators(dataframe, metadata)
            return dataframe
        
        def populate_entry_trend(self, dataframe, metadata):
            conditions = []
            
            # Check HTF trend
            htf_bullish = self.check_htf_trend(dataframe, direction='bullish')
            if htf_bullish is not None:
                conditions.append(htf_bullish)
            
            # ... your other conditions ...
            
            if conditions:
                dataframe.loc[reduce(lambda x, y: x & y, conditions), 'enter_long'] = 1
            return dataframe
"""

from freqtrade.strategy import BooleanParameter, IntParameter, CategoricalParameter, DecimalParameter
import pandas as pd
import talib.abstract as ta
import logging
from functools import reduce
import subprocess
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Dynamic HTF mapping based on strategy timeframe
HTF_MAPPING = {
    '1m':  '15m',
    '5m':  '15m',
    '15m': '1h',
    '30m': '4h',
    '1h':  '4h',
    '4h':  '1d',
}


class HTFTrendMixin:
    """
    Mixin for Higher Timeframe (HTF) trend checking.
    
    This mixin provides methods to:
    1. Add HTF trend indicators to dataframe
    2. Check if HTF trend is bullish or bearish
    3. Automatically select appropriate HTF based on strategy timeframe
    
    To use: Add this mixin to your strategy class inheritance
    """
    
    # ============================================================
    # HTF TREND PARAMETERS (Can be hyperopt optimized)
    # ============================================================
    htf_trend_enabled = BooleanParameter(
        default=True,
        space="buy",
        optimize=True,
        load=True
    )
    
    # Choose trend detection method
    htf_trend_method = CategoricalParameter(
        ['ema', 'supertrend', 'psar'],
        default='supertrend',
        space="buy",
        optimize=True,
        load=True
    )
    
    # === EMA Parameters ===
    htf_fast_ema = IntParameter(
        8, 21,
        default=12,
        space="buy",
        optimize=True,
        load=True
    )
    
    htf_slow_ema = IntParameter(
        21, 50,
        default=26,
        space="buy",
        optimize=True,
        load=True
    )
    
    htf_require_strong_trend = BooleanParameter(
        default=False,
        space="buy",
        optimize=True,
        load=True
    )
    
    # === SuperTrend Parameters ===
    htf_supertrend_period = IntParameter(
        7, 14,
        default=10,
        space="buy",
        optimize=True,
        load=True
    )
    
    htf_supertrend_multiplier = DecimalParameter(
        1.0, 5.0,
        default=3.0,
        decimals=1,
        space="buy",
        optimize=True,
        load=True
    )
    
    # === PSAR Parameters ===
    htf_psar_acceleration = DecimalParameter(
        0.01, 0.05,
        default=0.02,
        decimals=2,
        space="buy",
        optimize=True,
        load=True
    )
    
    htf_psar_maximum = DecimalParameter(
        0.1, 0.3,
        default=0.2,
        decimals=1,
        space="buy",
        optimize=True,
        load=True
    )
    
    def get_higher_timeframe(self) -> str:
        """
        Get the appropriate higher timeframe for this strategy.
        
        Returns:
            str: Higher timeframe (e.g., "5m" for 1m strategy)
        """
        htf = HTF_MAPPING.get(self.timeframe)
        
        if htf is None:
            logger.warning(
                f"⚠️  No HTF mapping for timeframe {self.timeframe}. "
                f"HTF trend check will be disabled."
            )
            return None
        
        logger.info(f"📊 HTF Trend: Using {htf} for {self.timeframe} strategy")
        return htf
    
    def download_htf_data_for_pairs(self, pairs: list, htf: str, timerange: str = None) -> bool:
        """
        Download HTF data for multiple pairs before backtesting starts.
        Should be called from informative_pairs() to ensure data is available.
        
        Args:
            pairs: List of trading pairs (e.g., ["BTC/USDT", "ETH/USDT"])
            htf: Higher timeframe (e.g., "5m")
            timerange: Optional timerange string (e.g., "20250628-20250716")
            
        Returns:
            bool: True if download was successful for all pairs
        """
        try:
            # Check if we're in backtest mode
            if not hasattr(self, 'dp') or self.dp is None:
                return False
            
            # Get timerange from config if not provided
            if timerange is None:
                # Try to get from strategy config
                config = getattr(self, 'config', {})
                timerange = config.get('timerange', None)
            
            if timerange is None:
                logger.info(f"⚠️  No timerange specified, skipping HTF data download")
                return False
            
            # Parse timerange to add 2-day buffer for startup period
            try:
                # Format: YYYYMMDD-YYYYMMDD
                if '-' in timerange:
                    start_str, end_str = timerange.split('-')
                    start_date = datetime.strptime(start_str, '%Y%m%d') - timedelta(days=2)
                    start_str = start_date.strftime('%Y%m%d')
                else:
                    logger.warning(f"⚠️  Invalid timerange format: {timerange}")
                    return False
            except Exception as e:
                logger.error(f"❌ Failed to parse timerange {timerange}: {e}")
                return False
            
            logger.info(f"📥 Downloading {htf} data for {len(pairs)} pairs ({start_str} to {end_str})...")
            
            # Build command to download data for all pairs
            cmd = [
                'freqtrade', 'download-data',
                '--exchange', 'binance',
                '--pairs'] + pairs + [
                '--timeframe', htf,
                '--timerange', f'{start_str}-{end_str}',
                '--prepend'
            ]
            
            # Execute download command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout for multiple pairs
            )
            
            if result.returncode == 0:
                logger.info(f"✅ Successfully downloaded {htf} data for all pairs")
                return True
            else:
                logger.error(f"❌ Failed to download {htf} data: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"❌ Download timeout for {htf} data")
            return False
        except Exception as e:
            logger.error(f"❌ Error downloading {htf} data: {e}")
            return False
    
    def check_and_download_htf_data(self, pairs: list, htf: str) -> None:
        """
        Check if HTF data exists for pairs and download if missing.
        Called from informative_pairs() to pre-download data before backtesting.
        
        Args:
            pairs: List of trading pairs
            htf: Higher timeframe
        """
        try:
            # Check if any pair is missing HTF data
            missing_pairs = []
            
            for pair in pairs:
                try:
                    htf_df = self.dp.get_pair_dataframe(pair=pair, timeframe=htf)
                    if htf_df is None or htf_df.empty:
                        missing_pairs.append(pair)
                except Exception:
                    missing_pairs.append(pair)
            
            # Download missing data if needed
            if missing_pairs:
                logger.info(f"⚠️  Missing {htf} data for {len(missing_pairs)} pairs, downloading...")
                self.download_htf_data_for_pairs(missing_pairs, htf)
            else:
                logger.info(f"✅ All pairs have {htf} data available")
                
        except Exception as e:
            logger.error(f"❌ Error checking HTF data: {e}")
    
    def calculate_supertrend(self, dataframe: pd.DataFrame, period: int, multiplier: float) -> pd.DataFrame:
        """
        Calculate SuperTrend indicator.
        
        Args:
            dataframe: OHLCV dataframe
            period: ATR period
            multiplier: ATR multiplier
            
        Returns:
            dataframe with supertrend columns added
        """
        # Calculate ATR
        atr = ta.ATR(dataframe, timeperiod=period)
        
        # Calculate basic upper and lower bands
        hl_avg = (dataframe['high'] + dataframe['low']) / 2
        upper_band = hl_avg + (multiplier * atr)
        lower_band = hl_avg - (multiplier * atr)
        
        # Initialize supertrend
        supertrend = pd.Series(index=dataframe.index, dtype='float64')
        direction = pd.Series(index=dataframe.index, dtype='int64')
        
        # First value
        supertrend.iloc[0] = lower_band.iloc[0]
        direction.iloc[0] = 1  # 1 = bullish, -1 = bearish
        
        # Calculate supertrend
        for i in range(1, len(dataframe)):
            if dataframe['close'].iloc[i] > supertrend.iloc[i-1]:
                direction.iloc[i] = 1
                supertrend.iloc[i] = max(lower_band.iloc[i], supertrend.iloc[i-1])
            elif dataframe['close'].iloc[i] < supertrend.iloc[i-1]:
                direction.iloc[i] = -1
                supertrend.iloc[i] = min(upper_band.iloc[i], supertrend.iloc[i-1])
            else:
                direction.iloc[i] = direction.iloc[i-1]
                if direction.iloc[i] == 1:
                    supertrend.iloc[i] = max(lower_band.iloc[i], supertrend.iloc[i-1])
                else:
                    supertrend.iloc[i] = min(upper_band.iloc[i], supertrend.iloc[i-1])
        
        dataframe['supertrend'] = supertrend
        dataframe['supertrend_direction'] = direction
        
        return dataframe
    
    def add_htf_trend_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Add HTF trend indicators to the dataframe.
        Call this in your populate_indicators() method.
        
        Args:
            dataframe: Strategy dataframe
            metadata: Pair metadata
            
        Returns:
            dataframe with HTF trend indicators added
        """
        if not self.htf_trend_enabled.value:
            return dataframe
        
        htf = self.get_higher_timeframe()
        
        if htf is None:
            return dataframe
        
        # Get HTF dataframe
        try:
            htf_dataframe = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe=htf)
        except Exception as e:
            logger.error(f"❌ Failed to get HTF dataframe for {metadata['pair']}: {e}")
            return dataframe
        
        # If HTF data is missing, warn and return
        if htf_dataframe is None or htf_dataframe.empty:
            logger.error(f"❌ HTF data unavailable for {metadata['pair']}. Download {htf} data before running backtest.")
            return dataframe
        
        # Calculate trend based on selected method
        method = self.htf_trend_method.value
        
        if method == 'ema':
            # EMA Crossover method
            htf_dataframe['ema_fast'] = htf_dataframe['close'].ewm(
                span=self.htf_fast_ema.value, adjust=False
            ).mean()
            htf_dataframe['ema_slow'] = htf_dataframe['close'].ewm(
                span=self.htf_slow_ema.value, adjust=False
            ).mean()
            
            htf_dataframe['trend_bullish'] = htf_dataframe['ema_fast'] > htf_dataframe['ema_slow']
            htf_dataframe['trend_bearish'] = htf_dataframe['ema_fast'] < htf_dataframe['ema_slow']
            
            # Strong trend: price also above/below both EMAs
            if self.htf_require_strong_trend.value:
                htf_dataframe['trend_bullish'] = (
                    htf_dataframe['trend_bullish'] &
                    (htf_dataframe['close'] > htf_dataframe['ema_fast']) &
                    (htf_dataframe['close'] > htf_dataframe['ema_slow'])
                )
                htf_dataframe['trend_bearish'] = (
                    htf_dataframe['trend_bearish'] &
                    (htf_dataframe['close'] < htf_dataframe['ema_fast']) &
                    (htf_dataframe['close'] < htf_dataframe['ema_slow'])
                )
        
        elif method == 'supertrend':
            # SuperTrend method
            htf_dataframe = self.calculate_supertrend(
                htf_dataframe,
                period=self.htf_supertrend_period.value,
                multiplier=self.htf_supertrend_multiplier.value
            )
            
            htf_dataframe['trend_bullish'] = htf_dataframe['supertrend_direction'] == 1
            htf_dataframe['trend_bearish'] = htf_dataframe['supertrend_direction'] == -1
        
        elif method == 'psar':
            # PSAR method
            psar = ta.SAR(
                htf_dataframe,
                acceleration=self.htf_psar_acceleration.value,
                maximum=self.htf_psar_maximum.value
            )
            
            htf_dataframe['psar'] = psar
            
            # Bullish: PSAR below price
            # Bearish: PSAR above price
            htf_dataframe['trend_bullish'] = htf_dataframe['psar'] < htf_dataframe['close']
            htf_dataframe['trend_bearish'] = htf_dataframe['psar'] > htf_dataframe['close']
        
        else:
            logger.error(f"❌ Unknown trend method: {method}")
            return dataframe
        
        # Merge HTF data back to strategy timeframe
        htf_dataframe = htf_dataframe[['date', 'trend_bullish', 'trend_bearish']].copy()
        htf_dataframe.columns = ['date', 'htf_trend_bullish', 'htf_trend_bearish']
        
        # Merge and forward-fill
        dataframe = pd.merge(
            dataframe,
            htf_dataframe,
            on='date',
            how='left'
        )
        
        dataframe['htf_trend_bullish'] = dataframe['htf_trend_bullish'].fillna(method='ffill')
        dataframe['htf_trend_bearish'] = dataframe['htf_trend_bearish'].fillna(method='ffill')
        
        # Fill any remaining NaN with False
        dataframe['htf_trend_bullish'] = dataframe['htf_trend_bullish'].fillna(False)
        dataframe['htf_trend_bearish'] = dataframe['htf_trend_bearish'].fillna(False)
        
        logger.info(f"📊 HTF Trend Method: {method.upper()}")
        
        return dataframe
    
    def check_htf_trend(self, dataframe: pd.DataFrame, direction: str = 'bullish') -> pd.Series:
        """
        Check if HTF trend matches the desired direction.
        Call this in your populate_entry_trend() method.
        
        Args:
            dataframe: Strategy dataframe (must have HTF indicators added)
            direction: 'bullish' or 'bearish'
            
        Returns:
            pd.Series: Boolean series for the condition (or None if disabled)
        """
        if not self.htf_trend_enabled.value:
            return None
        
        if direction == 'bullish':
            if 'htf_trend_bullish' not in dataframe.columns:
                logger.error("❌ HTF indicators not found! Did you call add_htf_trend_indicators()?")
                return None
            return dataframe['htf_trend_bullish']
        
        elif direction == 'bearish':
            if 'htf_trend_bearish' not in dataframe.columns:
                logger.error("❌ HTF indicators not found! Did you call add_htf_trend_indicators()?")
                return None
            return dataframe['htf_trend_bearish']
        
        else:
            logger.error(f"❌ Invalid direction: {direction}. Use 'bullish' or 'bearish'.")
            return None
