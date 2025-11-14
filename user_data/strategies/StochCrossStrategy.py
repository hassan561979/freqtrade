# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these imports ---
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, timezone
from pandas import DataFrame
from typing import Optional, Union
from functools import reduce

from freqtrade.strategy import (
    IStrategy,
    Trade,
    Order,
    PairLocks,
    informative,
    BooleanParameter,
    CategoricalParameter,
    DecimalParameter,
    IntParameter,
    RealParameter,
    timeframe_to_minutes,
    timeframe_to_next_date,
    timeframe_to_prev_date,
    merge_informative_pair,
    stoploss_from_absolute,
    stoploss_from_open,
)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
from technical import qtpylib


class StochCrossStrategy(IStrategy):
    """
    Stochastic Crossover Strategy
    
    Buy Signal: Stochastic K line crosses above D line
    Sell Signal: Stochastic K line crosses below D line
    
    This is a simple momentum-based strategy using Stochastic oscillator crossovers.
    """

    # Strategy interface version
    INTERFACE_VERSION = 3

    # Can this strategy go short?
    can_short: bool = False

    # Minimal ROI designed for the strategy
    # This attribute will be overridden if the config file contains "minimal_roi"
    minimal_roi = {
        "60": 0.01,   # Exit with 1% profit after 60 minutes
        "30": 0.02,   # Exit with 2% profit after 30 minutes
        "0": 0.04,    # Exit with 4% profit immediately if possible
    }

    # Optimal stoploss designed for the strategy
    stoploss = -0.10  # Stop loss at -10%

    # Trailing stoploss
    trailing_stop = False
    # trailing_only_offset_is_reached = False
    # trailing_stop_positive = 0.01
    # trailing_stop_positive_offset = 0.0

    # Optimal timeframe for the strategy
    timeframe = "1m"

    # Run "populate_indicators()" only for new candle
    process_only_new_candles = True

    # These values can be overridden in the config
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Hyperoptable parameters for Stochastic (matching TradingView script)
    # K Period - period for stochastic calculation
    stoch_k = IntParameter(low=5, high=21, default=14, space="buy", optimize=True, load=True)
    # Smooth K - smoothing for %K line
    stoch_smooth_k = IntParameter(low=1, high=7, default=1, space="buy", optimize=True, load=True)
    # D Period - smoothing period for %D line
    stoch_d = IntParameter(low=1, high=14, default=3, space="buy", optimize=True, load=True)

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    # Optional order type mapping
    order_types = {
        "entry": "limit",
        "exit": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    # Optional order time in force
    order_time_in_force = {"entry": "GTC", "exit": "GTC"}

    # Plot configuration for visualization
    plot_config = {
        "main_plot": {},
        "subplots": {
            "Stochastic": {
                "k": {"color": "blue"},
                "d": {"color": "orange"},
            },
        },
    }

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        """
        return []

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds Stochastic oscillator to the given DataFrame
        Matches TradingView Pine Script calculation:
        k = ta.sma(ta.stoch(close, high, low, k_period), smooth_k)
        d = ta.sma(k, d_period)
        
        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for the strategies
        """

        # Calculate Stochastic oscillator
        # Using standard STOCH which returns slowk and slowd as tuple
        # fastk_period: period for raw %K calculation
        # slowk_period: smoothing period for %K (SMA of raw %K)
        # slowd_period: smoothing period for %D (SMA of smoothed %K)
        slowk, slowd = ta.STOCH(
            dataframe['high'],
            dataframe['low'],
            dataframe['close'],
            fastk_period=self.stoch_k.value,
            slowk_period=self.stoch_smooth_k.value,
            slowk_matype=0,
            slowd_period=self.stoch_d.value,
            slowd_matype=0
        )
        
        # Assign %K and %D (matching TradingView's logic)
        dataframe['k'] = slowk
        dataframe['d'] = slowd

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the entry signal for the given dataframe
        
        Buy Signal: K crosses above D (ta.crossover(k, d))
        
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with entry columns populated
        """
        
        dataframe.loc[
            (
                # Buy when K crosses above D
                (qtpylib.crossed_above(dataframe['k'], dataframe['d'])) &
                # Make sure Volume is not 0
                (dataframe['volume'] > 0)
            ),
            'enter_long'
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the exit signal for the given dataframe
        
        Sell Signal: K crosses below D (ta.crossunder(k, d))
        
        :param dataframe: DataFrame
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with exit columns populated
        """
        
        dataframe.loc[
            (
                # Sell when K crosses below D
                (qtpylib.crossed_below(dataframe['k'], dataframe['d'])) &
                # Make sure Volume is not 0
                (dataframe['volume'] > 0)
            ),
            'exit_long'
        ] = 1

        return dataframe
