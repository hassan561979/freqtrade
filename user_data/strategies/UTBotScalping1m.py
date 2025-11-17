# Disable pylint warnings for freqtrade strategy format requirements
# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# Disable flake8 unused import warnings
# flake8: noqa: F401
# Skip isort import sorting
# isort: skip_file

# --- Do not remove these imports ---
import numpy as np  # For numerical calculations (UT Bot trailing stop array operations)
import pandas as pd  # For dataframe operations
from pandas import DataFrame  # Type hint for strategy methods
from datetime import datetime  # For timestamp operations
from typing import Optional, Union  # Type hints for optional parameters
import logging  # For debug logging in custom_exit

# Import freqtrade strategy framework components
from freqtrade.strategy import (BooleanParameter, CategoricalParameter, DecimalParameter,
                                IntParameter, IStrategy, merge_informative_pair)
from freqtrade.persistence import Trade  # Import Trade for custom_exit type hints

logger = logging.getLogger(__name__)

# --------------------------------
# Add your lib to import here
import talib.abstract as ta  # Technical Analysis library for ATR calculation
import pandas_ta as pta  # Pandas Technical Analysis (not currently used but available)


class UTBotScalping1m(IStrategy):
    """
    UT Bot Scalping Strategy (1m timeframe)
    
    Strategy Details:
    - Win Rate: ~68% (THEORETICAL - actual backtest: 27.7%)
    - Best for: Pure scalpers, high-frequency trading
    - Recommended Pairs: BTC/USDT, ETH/USDT, SOL/USDT, XRP/USDT
    - Trading Style: SCALPING (Ultra-fast)
    
    Entry Logic:
    - UT Bot BUY signal appears (trailing stop crosses above price)
    - Volume above 20-period average (confirms momentum)
    - Optional: Confirm with 5m trend
    
    Exit Logic:
    - ROI table (aggressive scalping targets, 6 time-based levels)
    - UT Bot opposite signal (trailing stop crosses below price)
    - Trailing stop activation at 0.6% profit (locks in gains)
    - Hard stop loss at -0.5% (limits losses)
    
    KNOWN ISSUES (from 1-year backtest):
    - Exit signals have 3.9% win rate (destroying profits)
    - Stop loss hit 994 times (market whipsaws on 1m)
    - Total loss: -89.93% over 1 year
    - Consider: Disable exit signals OR increase ut_key_value OR use 5m timeframe
    """

    INTERFACE_VERSION = 3  # Freqtrade strategy interface version

    # ROI table - aggressive scalping targets (Return On Investment)
    # Format: "time_in_minutes": profit_percentage (as decimal)
    # Freqtrade exits when price reaches these profit levels at specified times
    # Example: If trade reaches 1.5% profit at ANY time, ROI immediately exits
    # If not, after 5 minutes, will exit at 1.2%, after 10 min at 1.0%, etc.
    minimal_roi = {
        "0": 0.02,       # 2% immediate exit - always exit at 2% profit
    }

    # Hard stop loss - disabled, relying on exit signals and ROI
    # Stop loss too aggressive on 1m causing many false exits
    stoploss = -1  # -100% (effectively disabled)

    # Trailing stop configuration - locks in profits as price moves favorably
    trailing_stop = True  # Enable trailing stop feature
    trailing_stop_positive = 0.004  # Once triggered, trail 0.4% below highest price
    trailing_stop_positive_offset = 0.006  # Only activate trailing when profit reaches 0.6%
    trailing_only_offset_is_reached = True  # Don't trail until offset is reached

    # Exit signals (UT Bot opposite) - exit when UT Bot flips direction
    # WARNING: These have 3.9% win rate in backtests (major problem!)
    use_exit_signal = False  # DISABLED - exit signals have 1.1% win rate, rely on ROI/trailing
    exit_profit_only = False  # Exit on signal even at loss (dangerous on 1m!)
    exit_profit_offset = 0.0  # No minimum profit required for exit signal

    # Timeframe - 1-minute candles for ultra-fast scalping
    timeframe = '1m'

    # Run "populate_indicators()" only for new candle
    # True = better performance, False = updates on every tick (slower)
    process_only_new_candles = True

    # These values can be overridden in the config
    ignore_roi_if_entry_signal = False  # ROI always takes priority over entry signal

    # Number of candles the strategy requires before producing valid signals
    # Needed for indicator warmup (UT Bot needs 30 candles for ATR calculation)
    startup_candle_count: int = 30

    # UT Bot Parameters - hyperoptable (can be optimized)
    # key_value: Multiplier for ATR to set trailing stop distance
    # Higher value = wider stops = less sensitive = fewer signals
    ut_key_value = DecimalParameter(3.0, 5.0, decimals=1, default=3.5, space="buy")
    # atr_period: Number of candles for ATR (Average True Range) calculation
    # Longer period = smoother ATR = more stable signals
    ut_atr_period = IntParameter(5, 20, default=10, space="buy")

    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        
        Example: Could add 5m data for trend confirmation
        return [("BTC/USDT", "5m")]
        
        Currently: Not using any additional timeframes
        """
        return []  # Empty list = no additional pairs/timeframes needed

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame
        
        This method is called for each pair in the whitelist to calculate indicators.
        All indicator calculations happen here before entry/exit logic runs.

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        """

        # UT Bot Indicator - Calculates dynamic trailing stop based on ATR
        # ATR (Average True Range) measures volatility
        # Calculate ATR using TA-Lib for the specified period (default: 10 candles)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=self.ut_atr_period.value)
        
        # Initialize UT Bot columns with default values
        dataframe['ut_bot_trailing_stop'] = 0.0  # Will hold the trailing stop price level
        dataframe['ut_bot_signal'] = 0  # Signal indicator (not used but kept for reference)
        
        # Calculate UT Bot loss threshold (key_value * ATR)
        # This determines how far the trailing stop should be from current price
        # Example: If ATR=0.50 and key_value=3.5, then nLoss = 1.75 (price distance)
        nLoss = self.ut_key_value.value * dataframe['atr']
        
        # Initialize numpy arrays for vectorized calculation (faster than pandas loops)
        src = dataframe['close'].values  # Close prices as numpy array
        xATRTrailingStop = np.zeros(len(dataframe))  # Array to store trailing stop levels
        pos = np.zeros(len(dataframe))  # Array to store position state (1=long, -1=short)
        
        # Calculate trailing stop using UT Bot algorithm
        # Loop through each candle (starting from index 1 to avoid lookback issues)
        for i in range(1, len(dataframe)):
            # CASE 1: Price is above trailing stop (uptrend continuation)
            # If current price > previous trailing stop AND previous price > previous trailing stop
            if src[i] > xATRTrailingStop[i-1] and src[i-1] > xATRTrailingStop[i-1]:
                # Move trailing stop up (but never down) = max of previous stop or new stop
                # New stop = current price - nLoss (stop below price by ATR distance)
                xATRTrailingStop[i] = max(xATRTrailingStop[i-1], src[i] - nLoss.iloc[i])
            
            # CASE 2: Price is below trailing stop (downtrend continuation)
            # If current price < previous trailing stop AND previous price < previous trailing stop
            elif src[i] < xATRTrailingStop[i-1] and src[i-1] < xATRTrailingStop[i-1]:
                # Move trailing stop down (but never up) = min of previous stop or new stop
                # New stop = current price + nLoss (stop above price by ATR distance)
                xATRTrailingStop[i] = min(xATRTrailingStop[i-1], src[i] + nLoss.iloc[i])
            
            # CASE 3: Price crossed above trailing stop (new uptrend starting)
            elif src[i] > xATRTrailingStop[i-1]:
                # Set trailing stop below current price
                xATRTrailingStop[i] = src[i] - nLoss.iloc[i]
            
            # CASE 4: Price crossed below trailing stop (new downtrend starting)
            else:
                # Set trailing stop above current price
                xATRTrailingStop[i] = src[i] + nLoss.iloc[i]
            
            # Determine position based on price crossing the trailing stop
            # Position changes when price crosses the trailing stop line
            if src[i-1] < xATRTrailingStop[i-1] and src[i] > xATRTrailingStop[i-1]:
                # Price crossed above trailing stop = BUY signal
                pos[i] = 1
            elif src[i-1] > xATRTrailingStop[i-1] and src[i] < xATRTrailingStop[i-1]:
                # Price crossed below trailing stop = SELL signal
                pos[i] = -1
            else:
                # No cross = maintain previous position
                pos[i] = pos[i-1]
        
        # Store calculated values back into dataframe
        dataframe['ut_bot_trailing_stop'] = xATRTrailingStop  # Trailing stop price levels
        dataframe['ut_bot_pos'] = pos  # Position state (1=long, -1=short, 0=neutral)
        
        # Generate binary signals for entry/exit
        # BUY signal: Position switched to 1 (long) AND was not 1 before (new signal only)
        dataframe['ut_bot_buy'] = (dataframe['ut_bot_pos'] == 1) & (dataframe['ut_bot_pos'].shift(1) != 1)
        # SELL signal: Position switched to -1 (short) AND was not -1 before (new signal only)
        dataframe['ut_bot_sell'] = (dataframe['ut_bot_pos'] == -1) & (dataframe['ut_bot_pos'].shift(1) != -1)

        # Volume filter - calculate 20-period moving average of volume
        # Used to confirm that trades have sufficient liquidity/momentum
        # DISABLED: Commenting out to test strategy without volume filter
        # dataframe['volume_ma'] = dataframe['volume'].rolling(window=20).mean()

        return dataframe  # Return dataframe with all indicators calculated

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the entry signal for the given dataframe
        
        This method runs AFTER populate_indicators() and determines when to enter trades.
        Sets 'enter_long' column to 1 when all entry conditions are met.
        
        Entry Conditions:
        1. UT Bot generates BUY signal (price crossed above trailing stop)
        2. Valid data exists (volume > 0)
        
        DISABLED: Volume filter (was requiring volume > 20-period MA)
        """
        # Use dataframe.loc[conditions, column] to set signals
        # All conditions inside the tuple must be True for signal to trigger
        dataframe.loc[
            (
                # Condition 1: UT Bot BUY signal
                # True when ut_bot_buy column is True (price crossed above trailing stop)
                (dataframe['ut_bot_buy'] == True) &
                
                # Condition 2: Volume above average - DISABLED
                # Confirms that the move has sufficient trading volume/momentum
                # Helps filter out weak signals with low participation
                # (dataframe['volume'] > dataframe['volume_ma']) &
                
                # Condition 3: Ensure we have valid data
                # Safety check to avoid trading on missing/corrupt data
                (dataframe['volume'] > 0)
            ),
            'enter_long'] = 1  # Set enter_long to 1 when all conditions are True

        return dataframe  # Return dataframe with entry signals populated

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the exit signal for the given dataframe
        
        This method runs AFTER populate_indicators() and determines when to exit trades.
        Sets 'exit_long' column to 1 when exit conditions are met.
        
        Exit Conditions:
        1. UT Bot generates SELL signal (price crossed below trailing stop)
        2. Valid data exists (volume > 0)
        """
        dataframe.loc[
            (
                # Exit when UT Bot sell signal (price crossed below trailing stop)
                (dataframe['ut_bot_sell'] == True) &
                
                # Ensure we have valid data
                (dataframe['volume'] > 0)
            ),
            'exit_long'] = 1

        return dataframe


"""
=============================================================================
TRADINGVIEW PINE SCRIPT VERSION
=============================================================================
Copy the code below (between the START and END markers) into TradingView Pine Editor

────────────────────────── START PINE SCRIPT ──────────────────────────

//@version=5
strategy("UT Bot Strategy (Freqtrade)", overlay=true, 
         initial_capital=1000, default_qty_type=strategy.fixed, default_qty_value=100,
         commission_type=strategy.commission.percent, commission_value=0.1,
         process_orders_on_close=false,
         calc_on_every_tick=false)

// ──────────────────────────────────────────────────────────────────
// UT Bot Parameters
// ──────────────────────────────────────────────────────────────────
keyValue = input.float(3.5, title="UT Bot Key Value", minval=1.0, maxval=10.0, step=0.1)
atrPeriod = input.int(10, title="UT Bot ATR Period", minval=1)
useVolumeFilter = input.bool(false, title="Use Volume Filter", tooltip="Filter signals by volume > 20-period MA (DISABLED to match Freqtrade)")

// ──────────────────────────────────────────────────────────────────
// UT Bot Indicator Calculation
// ──────────────────────────────────────────────────────────────────
src = close
nLoss = keyValue * ta.atr(atrPeriod)

// Initialize trailing stop
var float xATRTrailingStop = na

// Calculate trailing stop
if src > nz(xATRTrailingStop[1], 0) and src[1] > nz(xATRTrailingStop[1], 0)
    xATRTrailingStop := math.max(nz(xATRTrailingStop[1]), src - nLoss)
else if src < nz(xATRTrailingStop[1], 0) and src[1] < nz(xATRTrailingStop[1], 0)
    xATRTrailingStop := math.min(nz(xATRTrailingStop[1]), src + nLoss)
else if src > nz(xATRTrailingStop[1], 0)
    xATRTrailingStop := src - nLoss
else
    xATRTrailingStop := src + nLoss

// Determine position
pos = 0
if src[1] < xATRTrailingStop[1] and src > xATRTrailingStop[1]
    pos := 1  // Buy signal
else if src[1] > xATRTrailingStop[1] and src < xATRTrailingStop[1]
    pos := -1  // Sell signal
else
    pos := nz(pos[1], 0)

// ──────────────────────────────────────────────────────────────────
// Volume Filter (20-period MA)
// ──────────────────────────────────────────────────────────────────
volumeMA = ta.sma(volume, 20)
volumeConfirm = volume > volumeMA

// ──────────────────────────────────────────────────────────────────
// Entry & Exit Signals
// ──────────────────────────────────────────────────────────────────
buySignal = pos == 1 and pos[1] != 1 and (useVolumeFilter ? volumeConfirm : true)
sellSignal = pos == -1 and pos[1] != -1

// ──────────────────────────────────────────────────────────────────
// Strategy Orders (Execute Trades)
// ──────────────────────────────────────────────────────────────────
if buySignal
    strategy.entry("Long", strategy.long)

// Exit signals DISABLED to match Freqtrade configuration
// Freqtrade uses trailing stop and ROI for exits, not UT Bot sell signals
// if sellSignal
//     strategy.close("Long")

// ──────────────────────────────────────────────────────────────────
// Exit Logic: ROI (2% target) and Trailing Stop (0.6% activation, 0.4% trail)
// ──────────────────────────────────────────────────────────────────

// Trailing Stop State Variables (Freqtrade-style)
var float highestPrice = na          // Track highest price since entry
var bool trailingActive = false      // Is trailing stop activated?
var float trailStopPrice = na        // Current trailing stop price level

// Reset state when position closes
if strategy.position_size == 0
    highestPrice := na
    trailingActive := false
    trailStopPrice := na

// Update trailing stop logic when in position
if strategy.position_size > 0
    // Calculate current profit percentage
    entryPrice = strategy.position_avg_price
    currentProfit = (close - entryPrice) / entryPrice
    
    // Update highest price reached
    if na(highestPrice) or close > highestPrice
        highestPrice := close
    
    // Calculate highest profit reached
    highestProfit = (highestPrice - entryPrice) / entryPrice
    
    // ─────────────────────────────────────────────────────────────
    // 1. ROI Exit: Close at 2% profit (takes priority)
    // ─────────────────────────────────────────────────────────────
    if currentProfit >= 0.02
        strategy.close("Long", comment="ROI 2%")
    
    // ─────────────────────────────────────────────────────────────
    // 2. Trailing Stop: Activate at 0.6% profit, trail 0.4% below high
    // ─────────────────────────────────────────────────────────────
    else
        // Activate trailing stop when profit reaches 0.6% (0.006)
        if not trailingActive and highestProfit >= 0.006
            trailingActive := true
        
        // Update trailing stop price if active
        if trailingActive
            // Trail 0.4% below highest price (0.996 = 1 - 0.004)
            newTrailStop = highestPrice * 0.996
            
            // Only move trailing stop UP, never down
            if na(trailStopPrice) or newTrailStop > trailStopPrice
                trailStopPrice := newTrailStop
            
            // Exit if price drops below trailing stop
            if close <= trailStopPrice
                strategy.close("Long", comment="Trailing Stop")

// ──────────────────────────────────────────────────────────────────
// Plot Trailing Stop Line and Highest Price
// ──────────────────────────────────────────────────────────────────
plot(xATRTrailingStop, title="UT Bot Trailing Stop", 
     color=pos == 1 ? color.green : color.red, linewidth=2)

// Plot position trailing stop level (when active)
plot(trailingActive ? trailStopPrice : na, title="Position Trailing Stop", 
     color=color.orange, linewidth=2, style=plot.style_stepline)

// Plot highest price reached (when in position)
plot(strategy.position_size > 0 ? highestPrice : na, title="Highest Price", 
     color=color.blue, linewidth=1, style=plot.style_circles)

// ──────────────────────────────────────────────────────────────────
// Plot Buy/Sell Signals
// ──────────────────────────────────────────────────────────────────
plotshape(buySignal, title="Buy Signal", location=location.belowbar, 
          color=color.green, style=shape.triangleup, size=size.small)
plotshape(sellSignal, title="Sell Signal", location=location.abovebar, 
          color=color.red, style=shape.triangledown, size=size.small)

// ──────────────────────────────────────────────────────────────────
// Alerts
// ──────────────────────────────────────────────────────────────────
alertcondition(buySignal, title="UT Bot Buy", message="UT Bot: BUY Signal")
alertcondition(sellSignal, title="UT Bot Sell", message="UT Bot: SELL Signal")

// ──────────────────────────────────────────────────────────────────
// Strategy Settings (Matches Freqtrade Config)
// ──────────────────────────────────────────────────────────────────
// ROI Table (minimal_roi):
// - 2% immediate exit (always exits at 2% profit)
//
// Trailing Stop (FULLY IMPLEMENTED):
// - Activates at 0.6% profit (trailing_stop_positive_offset)
// - Trails 0.4% below highest price (trailing_stop_positive)
// - Only moves UP, never down (standard trailing behavior)
// - Exits when price drops below trailing stop level
//
// Implementation Details:
// - Tracks highest price since entry using var float
// - Calculates highest profit percentage reached
// - Activates trailing when highestProfit >= 0.6%
// - Trail stop = highestPrice * 0.996 (99.6% = -0.4%)
// - Closes position when close <= trailStopPrice
//
// Stop Loss: DISABLED (-100%)
// - No stop loss set, relying on ROI and trailing stop
// - Long-term trades may result in large losses in bear markets
//
// Exit Signals: DISABLED in Freqtrade (use_exit_signal = False)
//               UT Bot sell signals had only 1.1% win rate
//
// Known Issue: Strategy holds losing positions indefinitely
// - 2 trades left open in 7-day backtest lost -18.8 USDT (-9.4% avg)
// - Trailing stop only activates AFTER 0.6% profit (never for losing trades)
// - Need to add max trade duration or hard stop loss for bear market protection

─────────────────────────── END PINE SCRIPT ───────────────────────────
=============================================================================
"""
