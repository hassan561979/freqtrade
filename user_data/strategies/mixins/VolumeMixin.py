"""
Volume Mixin
Adds volume-based filtering to any strategy.

Features:
- Volume spike detection (current volume vs. rolling average)
- Above-average volume filtering
- Configurable via hyperopt parameters
- Works in both backtest and live modes

Usage:
    from strategies.base import PerformanceFilterStrategy
    from strategies.mixins import VolumeMixin
    
    class MyStrategy(PerformanceFilterStrategy, VolumeMixin):
        def populate_indicators(self, dataframe, metadata):
            # Add volume indicators
            dataframe = self.add_volume_indicators(dataframe, metadata)
            return dataframe
        
        def populate_entry_trend(self, dataframe, metadata):
            conditions = []
            
            # Check volume
            volume_ok = self.check_volume_spike(dataframe)
            if volume_ok is not None:
                conditions.append(volume_ok)
            
            # ... your other conditions ...
            
            if conditions:
                dataframe.loc[reduce(lambda x, y: x & y, conditions), 'enter_long'] = 1
            return dataframe
"""

from freqtrade.strategy import BooleanParameter, DecimalParameter, IntParameter
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class VolumeMixin:
    """
    Mixin for volume-based filtering.
    
    This mixin provides methods to:
    1. Add volume indicators to dataframe
    2. Check for volume spikes
    3. Filter trades based on volume conditions
    
    To use: Add this mixin to your strategy class inheritance
    """
    
    # ============================================================
    # VOLUME PARAMETERS (Can be hyperopt optimized)
    # ============================================================
    volume_check_enabled = BooleanParameter(
        default=True,
        space="buy",
        optimize=True,
        load=True
    )
    
    volume_multiplier = DecimalParameter(
        1.0, 3.0,
        default=1.5,
        decimals=1,
        space="buy",
        optimize=True,
        load=True
    )
    
    volume_lookback_period = IntParameter(
        10, 50,
        default=20,
        space="buy",
        optimize=True,
        load=True
    )
    
    def add_volume_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        """
        Add volume indicators to the dataframe.
        Call this in your populate_indicators() method.
        
        Args:
            dataframe: Strategy dataframe
            metadata: Pair metadata
            
        Returns:
            dataframe with volume indicators added
        """
        if not self.volume_check_enabled.value:
            return dataframe
        
        # Calculate rolling average volume
        dataframe['volume_mean'] = dataframe['volume'].rolling(
            window=self.volume_lookback_period.value
        ).mean()
        
        # Volume spike: current volume vs. average
        dataframe['volume_spike'] = dataframe['volume'] > (
            dataframe['volume_mean'] * self.volume_multiplier.value
        )
        
        return dataframe
    
    def check_volume_spike(self, dataframe: pd.DataFrame) -> pd.Series:
        """
        Check if current volume is above threshold.
        Call this in your populate_entry_trend() method.
        
        Args:
            dataframe: Strategy dataframe (must have volume indicators added)
            
        Returns:
            pd.Series: Boolean series for the condition (or None if disabled)
        """
        if not self.volume_check_enabled.value:
            return None
        
        if 'volume_spike' not in dataframe.columns:
            logger.error("❌ Volume indicators not found! Did you call add_volume_indicators()?")
            return None
        
        return dataframe['volume_spike']
