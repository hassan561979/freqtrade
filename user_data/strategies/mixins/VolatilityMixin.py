"""
Volatility Mixin
Adds volatility-based filtering to any strategy.

Features:
- ATR (Average True Range) volatility measurement
- Filters out low/high volatility periods
- Configurable via hyperopt parameters
- Works in both backtest and live modes

Usage:
    from strategies.base import PerformanceFilterStrategy
    from strategies.mixins import VolatilityMixin
    
    class MyStrategy(PerformanceFilterStrategy, VolatilityMixin):
        def populate_indicators(self, dataframe, metadata):
            # Add volatility indicators
            dataframe = self.add_volatility_indicators(dataframe, metadata)
            return dataframe
        
        def populate_entry_trend(self, dataframe, metadata):
            conditions = []
            
            # Check volatility
            volatility_ok = self.check_volatility(dataframe)
            if volatility_ok is not None:
                conditions.append(volatility_ok)
            
            # ... your other conditions ...
            
            if conditions:
                dataframe.loc[reduce(lambda x, y: x & y, conditions), 'enter_long'] = 1
            return dataframe
"""

from freqtrade.strategy import BooleanParameter, DecimalParameter, IntParameter
import pandas as pd
import talib.abstract as ta
import logging

logger = logging.getLogger(__name__)


class VolatilityMixin:
    """
    Mixin for volatility-based filtering using ATR.
    
    This mixin provides methods to:
    1. Add ATR indicators to dataframe
    2. Check if volatility is within acceptable range
    3. Filter trades based on volatility conditions
    
    ATR measures market volatility:
    - Low ATR: Quiet, ranging market (low opportunity, tight stops)
    - High ATR: Volatile, trending market (high opportunity, wider stops)
    
    To use: Add this mixin to your strategy class inheritance
    """
    
    # ============================================================
    # VOLATILITY PARAMETERS (Can be hyperopt optimized)
    # ============================================================
    volatility_check_enabled = BooleanParameter(
        default=True,
        space="buy",
        optimize=True,
        load=True
    )
    
    atr_period = IntParameter(
        10, 20,
        default=14,
        space="buy",
        optimize=True,
        load=True
    )
    
    # Minimum ATR as percentage of price (filter out dead markets)
    min_atr_pct = DecimalParameter(
        0.5, 2.0,
        default=1.0,
        decimals=1,
        space="buy",
        optimize=True,
        load=True
    )
    
    # Maximum ATR as percentage of price (filter out overly volatile markets)
    max_atr_pct = DecimalParameter(
        3.0, 10.0,
        default=5.0,
        decimals=1,
        space="buy",
        optimize=True,
        load=True
    )
    
    def add_volatility_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Add volatility indicators to the dataframe.
        Call this in your populate_indicators() method.
        
        Args:
            dataframe: Strategy dataframe
            metadata: Pair metadata
            
        Returns:
            dataframe with volatility indicators added
        """
        if not self.volatility_check_enabled.value:
            return dataframe
        
        # Calculate ATR
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=self.atr_period.value)
        
        # ATR as percentage of current price
        dataframe['atr_pct'] = (dataframe['atr'] / dataframe['close']) * 100
        
        # Volatility within acceptable range
        dataframe['volatility_ok'] = (
            (dataframe['atr_pct'] >= self.min_atr_pct.value) &
            (dataframe['atr_pct'] <= self.max_atr_pct.value)
        )
        
        return dataframe
    
    def check_volatility(self, dataframe: pd.DataFrame) -> pd.Series:
        """
        Check if volatility is within acceptable range.
        Call this in your populate_entry_trend() method.
        
        Args:
            dataframe: Strategy dataframe (must have volatility indicators added)
            
        Returns:
            pd.Series: Boolean series for the condition (or None if disabled)
        """
        if not self.volatility_check_enabled.value:
            return None
        
        if 'volatility_ok' not in dataframe.columns:
            logger.error("❌ Volatility indicators not found! Did you call add_volatility_indicators()?")
            return None
        
        return dataframe['volatility_ok']
