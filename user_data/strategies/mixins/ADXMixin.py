"""
ADX (Average Directional Index) Mixin
Adds trend strength filtering to any strategy.

Features:
- ADX trend strength measurement
- Filters out weak/choppy markets
- Configurable via hyperopt parameters
- Works in both backtest and live modes

Usage:
    from strategies.base import PerformanceFilterStrategy
    from strategies.mixins import ADXMixin
    
    class MyStrategy(PerformanceFilterStrategy, ADXMixin):
        def populate_indicators(self, dataframe, metadata):
            # Add ADX indicators
            dataframe = self.add_adx_indicators(dataframe, metadata)
            return dataframe
        
        def populate_entry_trend(self, dataframe, metadata):
            conditions = []
            
            # Check ADX strength
            adx_strong = self.check_adx_strength(dataframe)
            if adx_strong is not None:
                conditions.append(adx_strong)
            
            # ... your other conditions ...
            
            if conditions:
                dataframe.loc[reduce(lambda x, y: x & y, conditions), 'enter_long'] = 1
            return dataframe
"""

from freqtrade.strategy import BooleanParameter, IntParameter
import pandas as pd
import talib.abstract as ta
import logging

logger = logging.getLogger(__name__)


class ADXMixin:
    """
    Mixin for ADX-based trend strength filtering.
    
    This mixin provides methods to:
    1. Add ADX indicators to dataframe
    2. Check if trend is strong enough (ADX above threshold)
    3. Filter trades based on trend strength
    
    ADX values interpretation:
    - 0-25: Weak/absent trend (choppy, ranging market)
    - 25-50: Strong trend
    - 50-75: Very strong trend
    - 75-100: Extremely strong trend
    
    To use: Add this mixin to your strategy class inheritance
    """
    
    # ============================================================
    # ADX PARAMETERS (Can be hyperopt optimized)
    # ============================================================
    adx_enabled = BooleanParameter(
        default=True,
        space="buy",
        optimize=True,
        load=True
    )
    
    adx_period = IntParameter(
        10, 20,
        default=14,
        space="buy",
        optimize=True,
        load=True
    )
    
    adx_threshold = IntParameter(
        15, 35,
        default=25,
        space="buy",
        optimize=True,
        load=True
    )
    
    def add_adx_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Add ADX indicators to the dataframe.
        Call this in your populate_indicators() method.
        
        Args:
            dataframe: Strategy dataframe
            metadata: Pair metadata
            
        Returns:
            dataframe with ADX indicators added
        """
        if not self.adx_enabled.value:
            return dataframe
        
        # Calculate ADX
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=self.adx_period.value)
        
        # Strong trend flag
        dataframe['adx_strong'] = dataframe['adx'] > self.adx_threshold.value
        
        return dataframe
    
    def check_adx_strength(self, dataframe: pd.DataFrame) -> pd.Series:
        """
        Check if ADX indicates strong trend.
        Call this in your populate_entry_trend() method.
        
        Args:
            dataframe: Strategy dataframe (must have ADX indicators added)
            
        Returns:
            pd.Series: Boolean series for the condition (or None if disabled)
        """
        if not self.adx_enabled.value:
            return None
        
        if 'adx_strong' not in dataframe.columns:
            logger.error("❌ ADX indicators not found! Did you call add_adx_indicators()?")
            return None
        
        return dataframe['adx_strong']
