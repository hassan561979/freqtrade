"""
Support & Resistance Mixin
Adds support/resistance level detection to any strategy.

Features:
- Pivot point calculation for support/resistance levels
- Entry filtering near support levels (for longs)
- Configurable distance thresholds via hyperopt
- Works in both backtest and live modes

Usage:
    from strategies.base import PerformanceFilterStrategy
    from strategies.mixins import SupportResistanceMixin
    
    class MyStrategy(PerformanceFilterStrategy, SupportResistanceMixin):
        def populate_indicators(self, dataframe, metadata):
            # Add support/resistance indicators
            dataframe = self.add_support_resistance_indicators(dataframe, metadata)
            return dataframe
        
        def populate_entry_trend(self, dataframe, metadata):
            conditions = []
            
            # Check if near support
            near_support = self.check_near_support(dataframe)
            if near_support is not None:
                conditions.append(near_support)
            
            # ... your other conditions ...
            
            if conditions:
                dataframe.loc[reduce(lambda x, y: x & y, conditions), 'enter_long'] = 1
            return dataframe
"""

from freqtrade.strategy import BooleanParameter, DecimalParameter, IntParameter
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class SupportResistanceMixin:
    """
    Mixin for support/resistance level detection.
    
    This mixin provides methods to:
    1. Calculate pivot points for support/resistance levels
    2. Check if price is near support (good entry for longs)
    3. Filter trades based on proximity to key levels
    
    Pivot Points:
    - Support 1: Good entry zone for longs
    - Support 2: Strong support level
    - Resistance 1: First target/exit
    - Resistance 2: Second target/exit
    
    To use: Add this mixin to your strategy class inheritance
    """
    
    # ============================================================
    # SUPPORT/RESISTANCE PARAMETERS (Can be hyperopt optimized)
    # ============================================================
    sr_check_enabled = BooleanParameter(
        default=False,  # Disabled by default (advanced feature)
        space="buy",
        optimize=True,
        load=True
    )
    
    sr_lookback_period = IntParameter(
        10, 30,
        default=20,
        space="buy",
        optimize=True,
        load=True
    )
    
    # Maximum distance from support as percentage (e.g., 2% = within 2% of support)
    sr_distance_pct = DecimalParameter(
        0.5, 3.0,
        default=1.5,
        decimals=1,
        space="buy",
        optimize=True,
        load=True
    )
    
    def add_support_resistance_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Add support/resistance indicators to the dataframe.
        Call this in your populate_indicators() method.
        
        Args:
            dataframe: Strategy dataframe
            metadata: Pair metadata
            
        Returns:
            dataframe with support/resistance indicators added
        """
        if not self.sr_check_enabled.value:
            return dataframe
        
        # Calculate pivot points using rolling high/low
        lookback = self.sr_lookback_period.value
        
        dataframe['pivot_high'] = dataframe['high'].rolling(window=lookback).max()
        dataframe['pivot_low'] = dataframe['low'].rolling(window=lookback).min()
        
        # Pivot Point (PP) = (High + Low + Close) / 3
        dataframe['pivot'] = (dataframe['high'] + dataframe['low'] + dataframe['close']) / 3
        
        # Support and Resistance levels
        dataframe['support1'] = (2 * dataframe['pivot']) - dataframe['pivot_high']
        dataframe['support2'] = dataframe['pivot'] - (dataframe['pivot_high'] - dataframe['pivot_low'])
        dataframe['resistance1'] = (2 * dataframe['pivot']) - dataframe['pivot_low']
        dataframe['resistance2'] = dataframe['pivot'] + (dataframe['pivot_high'] - dataframe['pivot_low'])
        
        # Distance from support1 (as percentage)
        dataframe['dist_from_support1'] = ((dataframe['close'] - dataframe['support1']) / dataframe['close']) * 100
        
        # Near support flag (within threshold distance)
        dataframe['near_support'] = (
            (dataframe['dist_from_support1'] >= 0) &  # Above support
            (dataframe['dist_from_support1'] <= self.sr_distance_pct.value)  # Within threshold
        )
        
        return dataframe
    
    def check_near_support(self, dataframe: pd.DataFrame) -> pd.Series:
        """
        Check if price is near support level (good entry for longs).
        Call this in your populate_entry_trend() method.
        
        Args:
            dataframe: Strategy dataframe (must have S/R indicators added)
            
        Returns:
            pd.Series: Boolean series for the condition (or None if disabled)
        """
        if not self.sr_check_enabled.value:
            return None
        
        if 'near_support' not in dataframe.columns:
            logger.error("❌ Support/Resistance indicators not found! Did you call add_support_resistance_indicators()?")
            return None
        
        return dataframe['near_support']
