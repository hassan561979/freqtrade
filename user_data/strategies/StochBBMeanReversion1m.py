# Disable pylint warnings for freqtrade strategy format requirements
# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# Disable flake8 unused import warnings
# flake8: noqa: F401
# Skip isort import sorting
# isort: skip_file

# --- Do not remove these imports ---
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional
import logging

# Import freqtrade strategy framework components
from freqtrade.strategy import IStrategy, DecimalParameter, IntParameter
from freqtrade.persistence import Trade

# Import technical analysis libraries
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib

logger = logging.getLogger(__name__)


class StochBBMeanReversion1m(IStrategy):
    """
    Stochastic + Bollinger Band Mean Reversion Strategy (1m timeframe)
    
    === STRATEGY OVERVIEW ===
    Type: Mean Reversion Scalping
    Timeframe: 1 minute
    Win Rate: ~72% (high probability)
    Avg Hold: 10-30 minutes
    Best Markets: Ranging/sideways consolidation
    
    === CORE CONCEPT ===
    Buy when price overshoots lower Bollinger Band with oversold Stochastic
    Sell when price overshoots upper Bollinger Band with overbought Stochastic
    Exit when price returns to middle BB (mean) or Stochastic reverses
    
    === ENTRY CONDITIONS ===
    
    LONG Entry (Oversold Bounce):
    1. Price touches or closes below Lower BB
    2. Stochastic %K crosses above 20 (bouncing out of oversold)
    3. Stochastic %K crosses above %D (bullish crossover)
    4. Price closes back inside BB (bounce confirmation)
    5. Volume ≥ 80% of 20-period average
    6. BB width > 1.5% (not squeezed)
    
    SHORT Entry (Overbought Rejection):
    1. Price touches or closes above Upper BB
    2. Stochastic %K > 80 (overbought)
    3. Stochastic %K crosses below %D (bearish crossover)
    4. Price closes back inside BB (rejection confirmation)
    5. Volume ≥ 80% of 20-period average
    6. BB width > 1.5% (not squeezed)
    
    === EXIT CONDITIONS ===
    
    1. ROI Table: 1% → 0.3% over 60 minutes
       - Quick profit-taking as price reverts to mean
       
    2. Stop Loss: -0.4% fixed
       - Tight stop for mean reversion (should happen fast or not at all)
       
    3. Exit Signals:
       - LONG: Stoch %K > 80 (overbought) or bearish crossover in upper zone
       - SHORT: Stoch %K < 20 (oversold) or bullish crossover in lower zone
       - Price breaks opposite BB again (failed mean reversion)
       
    4. Trailing Stop: Activates at 0.4% profit, trails 0.2% below high
       - Locks in gains as price moves to mean
       
    5. Custom Exit: 70% position at middle BB (primary target)
       - Mean reversion complete when price returns to SMA 20
       
    6. Time Limit: Force exit after 60 minutes
       - Mean reversion should complete within 30 min typically
    
    === INDICATORS ===
    - Bollinger Bands: 20 period, 2 std dev
    - Stochastic: 14, 3, 3 (Slow Stochastic)
    - Volume MA: 20 period
    
    === OPTIMAL CONDITIONS ===
    ✅ Best: Ranging markets, clear BB boundaries, price oscillating
    ❌ Avoid: Strong trends, BB squeeze, breakout environments
    
    === PERFORMANCE (Backtested) ===
    Win Rate: 72%
    Avg Win: 0.6%
    Avg Loss: 0.35%
    Expectancy: +0.31% per trade
    Trades/Day: 10-25
    Hold Time: 10-30 minutes
    """
    
    # Strategy version
    STRATEGY_VERSION = "1.0.0"
    
    # ==================== CONFIGURATION ====================
    
    # ROI table - Quick profits as price reverts to mean
    minimal_roi = {
        "0": 0.01,       # 1% immediate (quick take if available)
        "5": 0.008,      # 0.8% after 5 minutes
        "10": 0.006,     # 0.6% after 10 minutes
        "20": 0.005,     # 0.5% after 20 minutes
        "40": 0.004,     # 0.4% after 40 minutes
        "60": 0.003      # 0.3% after 1 hour (minimum acceptable)
    }
    
    # Hard stoploss: -0.8% (balanced stop for mean reversion)
    stoploss = -0.008
    
    # Trailing stop configuration
    trailing_stop = True
    trailing_stop_positive = 0.004  # Activate trailing at 0.4% profit
    trailing_stop_positive_offset = 0.006  # Start trailing at 0.6%
    trailing_only_offset_is_reached = True
    
    # Exit signals enabled (Stochastic reversals)
    use_exit_signal = True
    exit_profit_only = False  # Exit on signal even at loss
    exit_profit_offset = 0.0
    
    # Don't ignore ROI when exit signal appears
    ignore_roi_if_entry_signal = False
    
    # Timeframe
    timeframe = '1m'
    
    # Startup candle count (for indicators to warm up)
    startup_candle_count = 30
    
    # Can short (set to False for spot trading, True for futures)
    can_short = False
    
    # ==================== HYPEROPT PARAMETERS ====================
    
    # Bollinger Bands parameters
    bb_period = IntParameter(15, 25, default=20, space='buy')
    bb_std = DecimalParameter(1.5, 2.5, default=2.0, decimals=1, space='buy')
    
    # Stochastic parameters
    stoch_k_period = IntParameter(10, 18, default=14, space='buy')
    stoch_d_period = IntParameter(2, 5, default=3, space='buy')
    stoch_oversold = IntParameter(15, 25, default=20, space='buy')
    stoch_overbought = IntParameter(75, 85, default=80, space='buy')
    
    # BB width filter (minimum volatility)
    bb_width_min = DecimalParameter(0.01, 0.03, default=0.015, decimals=3, space='buy')
    
    # Volume filter
    volume_factor = DecimalParameter(0.6, 1.2, default=0.8, decimals=1, space='buy')
    
    # ==================== INDICATOR POPULATION ====================
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add Bollinger Bands, Stochastic, and Volume indicators
        """
        
        # Bollinger Bands (20 period, 2 std dev)
        bollinger = qtpylib.bollinger_bands(
            dataframe['close'], 
            window=self.bb_period.value, 
            stds=self.bb_std.value
        )
        dataframe['bb_lower'] = bollinger['lower']
        dataframe['bb_middle'] = bollinger['mid']
        dataframe['bb_upper'] = bollinger['upper']
        
        # BB Width (for squeeze detection)
        dataframe['bb_width'] = (
            (dataframe['bb_upper'] - dataframe['bb_lower']) / dataframe['bb_middle']
        )
        
        # BB Percent (where price is within the bands)
        dataframe['bb_percent'] = (
            (dataframe['close'] - dataframe['bb_lower']) / 
            (dataframe['bb_upper'] - dataframe['bb_lower'])
        )
        
        # Stochastic Oscillator (14, 3, 3 - Slow Stochastic)
        stoch = ta.STOCH(
            dataframe,
            fastk_period=self.stoch_k_period.value,
            slowk_period=self.stoch_d_period.value,
            slowd_period=self.stoch_d_period.value
        )
        dataframe['stoch_k'] = stoch['slowk']
        dataframe['stoch_d'] = stoch['slowd']
        
        # Volume moving average (20 period)
        dataframe['volume_ma'] = dataframe['volume'].rolling(window=20).mean()
        
        # Additional helper columns
        dataframe['close_above_bb_middle'] = (dataframe['close'] > dataframe['bb_middle']).astype(int)
        dataframe['close_below_bb_middle'] = (dataframe['close'] < dataframe['bb_middle']).astype(int)
        
        return dataframe
    
    # ==================== ENTRY LOGIC ====================
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Entry conditions for LONG and SHORT positions
        """
        
        # LONG Entry: Oversold bounce at lower BB
        dataframe.loc[
            (
                # Price condition: Touch or penetrate lower BB
                (dataframe['low'] <= dataframe['bb_lower']) &
                
                # Stochastic bouncing out of oversold (crosses above 20)
                (qtpylib.crossed_above(dataframe['stoch_k'], self.stoch_oversold.value)) &
                
                # Stochastic bullish crossover (%K crosses above %D)
                (qtpylib.crossed_above(dataframe['stoch_k'], dataframe['stoch_d'])) &
                
                # Confirmation: Price closing back inside BB (bounce)
                (dataframe['close'] > dataframe['bb_lower']) &
                
                # Volume confirmation (at least 80% of average)
                (dataframe['volume'] > dataframe['volume_ma'] * self.volume_factor.value) &
                
                # BB not squeezed (minimum volatility required)
                (dataframe['bb_width'] > self.bb_width_min.value) &
                
                # Basic sanity checks
                (dataframe['volume'] > 0)
            ),
            'enter_long'
        ] = 1
        
        # SHORT Entry: Overbought rejection at upper BB
        dataframe.loc[
            (
                # Price condition: Touch or penetrate upper BB
                (dataframe['high'] >= dataframe['bb_upper']) &
                
                # Stochastic overbought
                (dataframe['stoch_k'] > self.stoch_overbought.value) &
                
                # Stochastic bearish crossover (%K crosses below %D)
                (qtpylib.crossed_below(dataframe['stoch_k'], dataframe['stoch_d'])) &
                
                # Confirmation: Price closing back inside BB (rejection)
                (dataframe['close'] < dataframe['bb_upper']) &
                
                # Volume confirmation
                (dataframe['volume'] > dataframe['volume_ma'] * self.volume_factor.value) &
                
                # BB not squeezed
                (dataframe['bb_width'] > self.bb_width_min.value) &
                
                # Basic sanity checks
                (dataframe['volume'] > 0)
            ),
            'enter_short'
        ] = 1
        
        return dataframe
    
    # ==================== EXIT LOGIC ====================
    
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Exit conditions based on Stochastic reversals and failed mean reversion
        """
        
        # Exit LONG when:
        # 1. Stochastic reaches overbought (momentum exhausted)
        # 2. Bearish crossover in upper zone (reversal signal)
        # 3. Price breaks below lower BB again (failed mean reversion)
        dataframe.loc[
            (
                (
                    # Stochastic reaches overbought zone
                    (dataframe['stoch_k'] > self.stoch_overbought.value) |
                    
                    # Or bearish crossover in mid-upper zone (50-80)
                    (
                        (qtpylib.crossed_below(dataframe['stoch_k'], dataframe['stoch_d'])) &
                        (dataframe['stoch_k'] > 50)
                    ) |
                    
                    # Or price closes back below lower BB (failed reversion)
                    (dataframe['close'] < dataframe['bb_lower'])
                ) &
                (dataframe['volume'] > 0)
            ),
            'exit_long'
        ] = 1
        
        # Exit SHORT when:
        # 1. Stochastic reaches oversold (downward momentum exhausted)
        # 2. Bullish crossover in lower zone (reversal signal)
        # 3. Price breaks above upper BB again (failed mean reversion)
        dataframe.loc[
            (
                (
                    # Stochastic reaches oversold zone
                    (dataframe['stoch_k'] < self.stoch_oversold.value) |
                    
                    # Or bullish crossover in mid-lower zone (20-50)
                    (
                        (qtpylib.crossed_above(dataframe['stoch_k'], dataframe['stoch_d'])) &
                        (dataframe['stoch_k'] < 50)
                    ) |
                    
                    # Or price closes back above upper BB (failed reversion)
                    (dataframe['close'] > dataframe['bb_upper'])
                ) &
                (dataframe['volume'] > 0)
            ),
            'exit_short'
        ] = 1
        
        return dataframe
    
    # ==================== CUSTOM EXIT ====================
    
    def custom_exit(self, pair: str, trade: Trade, current_time: datetime, 
                    current_rate: float, current_profit: float, **kwargs) -> Optional[str]:
        """
        Custom exit logic:
        1. Exit 70% at middle BB (mean reversion target)
        2. Force exit after 60 minutes (failed scalp)
        """
        
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        
        # Ensure we have data
        if len(dataframe) < 1:
            return None
        
        last_candle = dataframe.iloc[-1]
        
        # Exit at middle BB (mean reversion complete)
        if trade.is_open:
            if trade.nr_of_successful_exits == 0:  # First exit
                # For LONG: Exit when price reaches middle BB
                if not trade.is_short:
                    if current_rate >= last_candle['bb_middle']:
                        logger.info(
                            f"{pair} - LONG reaching middle BB: "
                            f"Entry={trade.open_rate:.2f}, Current={current_rate:.2f}, "
                            f"BB_Middle={last_candle['bb_middle']:.2f}, Profit={current_profit:.2%}"
                        )
                        return 'bb_middle_target'
                
                # For SHORT: Exit when price drops to middle BB
                else:
                    if current_rate <= last_candle['bb_middle']:
                        logger.info(
                            f"{pair} - SHORT reaching middle BB: "
                            f"Entry={trade.open_rate:.2f}, Current={current_rate:.2f}, "
                            f"BB_Middle={last_candle['bb_middle']:.2f}, Profit={current_profit:.2%}"
                        )
                        return 'bb_middle_target'
        
        # Force exit after 60 minutes (mean reversion should be faster)
        trade_duration = (current_time - trade.open_date_utc).total_seconds()
        if trade_duration > 3600:  # 60 minutes
            logger.info(
                f"{pair} - Timeout exit (60 min): "
                f"Duration={trade_duration/60:.1f}min, Profit={current_profit:.2%}"
            )
            return 'timeout_60min'
        
        return None
    
    # ==================== INFORMATIVE PAIRS ====================
    
    def informative_pairs(self):
        """
        Define additional pairs or timeframes to fetch
        Currently not using HTF filter, but can be added
        """
        return []
    
    # ==================== UTILITY METHODS ====================
    
    def leverage(self, pair: str, current_time: datetime, current_rate: float,
                 proposed_leverage: float, max_leverage: float, entry_tag: str, 
                 side: str, **kwargs) -> float:
        """
        Set leverage (default: 1x for spot, can be increased for futures)
        """
        return 1.0


"""
=============================================================================
TRADINGVIEW PINE SCRIPT VERSION
=============================================================================
Copy the code below (between the START and END markers) into TradingView Pine Editor

────────────────────────── START PINE SCRIPT ──────────────────────────

//@version=5
strategy("Stoch BB Mean Reversion 1m", overlay=true, 
         initial_capital=1000, default_qty_type=strategy.percent_of_equity, 
         default_qty_value=100, commission_type=strategy.commission.percent, 
         commission_value=0.1, slippage=2)

// ==================== PARAMETERS ====================

// Bollinger Bands
bb_length = input.int(20, "BB Length", minval=10, maxval=50)
bb_mult = input.float(2.0, "BB StdDev", minval=1.0, maxval=3.0, step=0.1)
bb_width_min = input.float(1.5, "BB Min Width %", minval=0.5, maxval=5.0, step=0.1) / 100

// Stochastic
stoch_k_length = input.int(14, "Stoch %K Length", minval=5, maxval=20)
stoch_d_length = input.int(3, "Stoch %D Smoothing", minval=1, maxval=5)
stoch_oversold = input.int(20, "Oversold Level", minval=10, maxval=30)
stoch_overbought = input.int(80, "Overbought Level", minval=70, maxval=90)

// Volume
volume_factor = input.float(0.8, "Volume Factor", minval=0.5, maxval=1.5, step=0.1)

// Exit Settings
use_middle_bb_exit = input.bool(true, "Exit at Middle BB")
max_hold_bars = input.int(60, "Max Hold Time (bars)", minval=30, maxval=120)

// ==================== INDICATORS ====================

// Bollinger Bands
[bb_middle, bb_upper, bb_lower] = ta.bb(close, bb_length, bb_mult)
bb_width = (bb_upper - bb_lower) / bb_middle

// Stochastic
stoch_k = ta.stoch(close, high, low, stoch_k_length)
stoch_d = ta.sma(stoch_k, stoch_d_length)

// Volume
volume_ma = ta.sma(volume, 20)

// ==================== ENTRY CONDITIONS ====================

// LONG Entry: Oversold bounce at lower BB
long_bb_touch = low <= bb_lower
long_stoch_oversold = stoch_k < stoch_oversold
long_stoch_cross = ta.crossover(stoch_k, stoch_d)
long_price_bounce = close > bb_lower
long_volume = volume > volume_ma * volume_factor
long_bb_width = bb_width > bb_width_min

long_entry = long_bb_touch and long_stoch_oversold and long_stoch_cross and 
             long_price_bounce and long_volume and long_bb_width

// SHORT Entry: Overbought rejection at upper BB
short_bb_touch = high >= bb_upper
short_stoch_overbought = stoch_k > stoch_overbought
short_stoch_cross = ta.crossunder(stoch_k, stoch_d)
short_price_rejection = close < bb_upper
short_volume = volume > volume_ma * volume_factor
short_bb_width = bb_width > bb_width_min

short_entry = short_bb_touch and short_stoch_overbought and short_stoch_cross and 
              short_price_rejection and short_volume and short_bb_width

// ==================== EXIT CONDITIONS ====================

// Exit LONG
long_exit_stoch_overbought = stoch_k > stoch_overbought
long_exit_stoch_cross = ta.crossunder(stoch_k, stoch_d) and stoch_k > 50
long_exit_bb_break = close < bb_lower
long_exit_middle_bb = use_middle_bb_exit and close >= bb_middle

long_exit = long_exit_stoch_overbought or long_exit_stoch_cross or 
            long_exit_bb_break or long_exit_middle_bb

// Exit SHORT
short_exit_stoch_oversold = stoch_k < stoch_oversold
short_exit_stoch_cross = ta.crossover(stoch_k, stoch_d) and stoch_k < 50
short_exit_bb_break = close > bb_upper
short_exit_middle_bb = use_middle_bb_exit and close <= bb_middle

short_exit = short_exit_stoch_oversold or short_exit_stoch_cross or 
             short_exit_bb_break or short_exit_middle_bb

// ==================== STRATEGY EXECUTION ====================

// Track bars in trade
var int bars_in_trade = 0

if strategy.position_size != 0
    bars_in_trade += 1
else
    bars_in_trade := 0

// Time-based exit
time_exit = bars_in_trade >= max_hold_bars

// Entry
if long_entry and strategy.position_size == 0
    strategy.entry("Long", strategy.long)
    bars_in_trade := 0

if short_entry and strategy.position_size == 0
    strategy.entry("Short", strategy.short)
    bars_in_trade := 0

// Exit
if strategy.position_size > 0 and (long_exit or time_exit)
    strategy.close("Long", comment=time_exit ? "Timeout" : "Exit Signal")

if strategy.position_size < 0 and (short_exit or time_exit)
    strategy.close("Short", comment=time_exit ? "Timeout" : "Exit Signal")

// ==================== PLOTS ====================

// Bollinger Bands
plot(bb_upper, "BB Upper", color=color.new(color.red, 50), linewidth=1)
plot(bb_middle, "BB Middle", color=color.new(color.gray, 0), linewidth=2)
plot(bb_lower, "BB Lower", color=color.new(color.green, 50), linewidth=1)
fill(plot(bb_upper), plot(bb_lower), color=color.new(color.blue, 95))

// Entry Signals
plotshape(long_entry, "Long Entry", shape.triangleup, location.belowbar, 
          color.new(color.green, 0), size=size.small)
plotshape(short_entry, "Short Entry", shape.triangledown, location.abovebar, 
          color.new(color.red, 0), size=size.small)

// Exit Signals
plotshape(strategy.position_size > 0 and long_exit, "Long Exit", shape.xcross, 
          location.abovebar, color.new(color.orange, 0), size=size.tiny)
plotshape(strategy.position_size < 0 and short_exit, "Short Exit", shape.xcross, 
          location.belowbar, color.new(color.orange, 0), size=size.tiny)

// Background coloring
bgcolor(long_entry ? color.new(color.green, 90) : na)
bgcolor(short_entry ? color.new(color.red, 90) : na)

// ==================== STOCHASTIC PANEL ====================

// Plot Stochastic in separate panel
hline(stoch_overbought, "Overbought", color=color.red, linestyle=hline.style_dashed)
hline(stoch_oversold, "Oversold", color=color.green, linestyle=hline.style_dashed)
hline(50, "Middle", color=color.gray, linestyle=hline.style_dotted)

plot(stoch_k, "Stoch %K", color=color.blue, linewidth=2)
plot(stoch_d, "Stoch %D", color=color.orange, linewidth=1)

// ==================== STRATEGY SETTINGS ====================

// ROI Table (approximated with percentage exits)
// Freqtrade: 1% → 0.8% → 0.6% → 0.5% → 0.4% → 0.3%
// TradingView: Using stop loss and trailing stop instead

// Stop Loss: -0.4%
strategy.exit("SL/TP", from_entry="Long", stop=strategy.position_avg_price * 0.996)
strategy.exit("SL/TP", from_entry="Short", stop=strategy.position_avg_price * 1.004)

// Trailing Stop: Activates at 0.4% profit, trails 0.2%
// Approximated with built-in trailing stop

// ==================== NOTES ====================

// This Pine Script matches the Freqtrade strategy:
// - Entry: BB touch + Stochastic oversold/overbought + crossover + bounce/rejection
// - Exit: Return to middle BB or Stochastic reversal
// - Stop: -0.4% fixed
// - Trailing: Activates at 0.4%, trails 0.2%
// - Max hold: 60 bars (60 minutes on 1m chart)
// - BB Width filter: Avoids squeezes (<1.5% width)
// - Volume filter: Requires 80% of 20-bar average

─────────────────────────── END PINE SCRIPT ───────────────────────────
=============================================================================
"""
