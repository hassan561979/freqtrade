# Freqtrade Strategy Parameters Guide

## Complete Guide to Strategy Configuration and Parameters

This guide explains every parameter used in Freqtrade strategies with detailed examples, use cases, and how they interact with each other.

---

## Table of Contents

1. [ROI (Return on Investment)](#roi-return-on-investment)
2. [Stop Loss](#stop-loss)
3. [Trailing Stop Loss](#trailing-stop-loss)
4. [Exit Signals](#exit-signals)
5. [Timeframe](#timeframe)
6. [Startup Candle Count](#startup-candle-count)
7. [Custom Parameters (Hyperopt)](#custom-parameters-hyperopt)
8. [Entry and Exit Logic](#entry-and-exit-logic)
9. [Parameter Interactions](#parameter-interactions)
10. [Real-World Examples](#real-world-examples)

---

## ROI (Return on Investment)

### What is ROI?

ROI is a **time-based profit target table** that automatically exits trades when specific profit levels are reached at specific times. It's the most reliable exit mechanism in most strategies.

### Configuration

```python
minimal_roi = {
    "0": 0.10,    # 10% profit target at any time
    "30": 0.05,   # 5% profit target after 30 minutes
    "60": 0.03,   # 3% profit target after 60 minutes
    "120": 0.01   # 1% profit target after 120 minutes
}
```

### How It Works

**Time Format:**
- Keys are strings representing **minutes** since trade opened
- "0" = immediate (from trade opening)
- "30" = 30 minutes after entry
- "1440" = 24 hours (1 day)

**Profit Format:**
- Values are **decimals** (not percentages)
- 0.01 = 1% profit
- 0.10 = 10% profit
- 0.005 = 0.5% profit

### Execution Logic

ROI checks happen **on every candle**. Freqtrade exits when:
1. Current profit ≥ ROI target for current trade age
2. Trade age is between two time boundaries

**Example Scenario:**

```python
minimal_roi = {
    "0": 0.015,   # 1.5%
    "5": 0.012,   # 1.2%
    "10": 0.01,   # 1.0%
    "30": 0.005   # 0.5%
}
```

**Trade Timeline:**
- **T=0 min:** Trade opens at $100
- **T=2 min:** Price hits $101.50 (+1.5%) → **EXIT** (ROI "0" triggered)
- OR
- **T=2 min:** Price at $101.30 (+1.3%) → Stay in (not enough for 1.5%)
- **T=7 min:** Price at $101.25 (+1.25%) → **EXIT** (ROI "5" triggered, need only 1.2%)
- OR
- **T=35 min:** Price at $100.55 (+0.55%) → **EXIT** (ROI "30" triggered, need only 0.5%)

### ROI Strategies

#### 1. Aggressive Scalping ROI
```python
minimal_roi = {
    "0": 0.015,    # Take 1.5% immediately
    "3": 0.012,    # 1.2% after 3 min
    "7": 0.01,     # 1.0% after 7 min
    "15": 0.005    # 0.5% after 15 min
}
```
**Use Case:** High-frequency scalping on 1m/5m timeframes
**Pros:** Locks in profits quickly
**Cons:** Misses larger moves

#### 2. Patient Swing Trading ROI
```python
minimal_roi = {
    "0": 0.20,      # 20% anytime
    "1440": 0.10,   # 10% after 1 day
    "2880": 0.05,   # 5% after 2 days
    "4320": 0.02    # 2% after 3 days
}
```
**Use Case:** Swing trading on 1h/4h timeframes
**Pros:** Captures big moves
**Cons:** Longer drawdown exposure

#### 3. Balanced Approach
```python
minimal_roi = {
    "0": 0.08,      # 8% anytime (home run exit)
    "30": 0.04,     # 4% after 30 min
    "60": 0.025,    # 2.5% after 1 hour
    "180": 0.015,   # 1.5% after 3 hours
    "360": 0.01     # 1% after 6 hours
}
```
**Use Case:** Most strategies on 15m/30m timeframes
**Pros:** Balanced risk/reward
**Cons:** May exit too early on strong trends

### ROI Best Practices

✅ **DO:**
- Start with longer time intervals, then optimize
- Use ROI as your primary profit-taking mechanism
- Test different ROI tables with backtesting
- Keep ROI targets realistic (1-10% for most strategies)

❌ **DON'T:**
- Set ROI targets too high (unrealistic expectations)
- Use too many time intervals (5-7 max)
- Expect ROI to catch every move (it's a safety net)
- Disable ROI completely (unless using custom_exit)

### Disabling ROI

```python
minimal_roi = {
    "0": 100  # Effectively disabled (100% profit = never triggers)
}
```

**When to disable:**
- Using custom exit methods only
- Testing pure technical exit signals
- Advanced strategies with dynamic exits

---

## Stop Loss

### What is Stop Loss?

Stop loss is a **hard exit** triggered when trade profit drops below a specified percentage. It's your **capital protection** mechanism.

### Configuration

```python
stoploss = -0.10  # Exit if trade loses 10%
```

### Format

- Always **negative decimal**
- -0.01 = -1% loss
- -0.10 = -10% loss
- -0.005 = -0.5% loss

### How It Works

**Trigger Mechanism:**
1. On every candle (or tick), Freqtrade calculates current trade profit
2. If profit ≤ stoploss value → **IMMEDIATE EXIT**
3. Stop loss executes **before** any other exit logic

**Example:**

```python
stoploss = -0.05  # -5% stop loss
```

**Scenario:**
- Entry: $100
- Stop loss triggers at: $95 or below
- Price drops to $94.50 → **EXIT** (lost 5.5%)

### Stop Loss Strategies

#### 1. Tight Stop Loss (Scalping)
```python
stoploss = -0.005  # -0.5%
```
**Use Case:** 1m scalping, quick exits
**Pros:** Limits losses quickly
**Cons:** Gets hit often on volatile pairs (whipsaws)
**Result:** UTBotScalping1m had 994 stop loss hits in 1 year!

#### 2. Medium Stop Loss (Day Trading)
```python
stoploss = -0.02  # -2%
```
**Use Case:** 5m-30m timeframes
**Pros:** Balanced protection vs. breathing room
**Cons:** Can still lose significant capital
**Best For:** Most strategies

#### 3. Wide Stop Loss (Swing Trading)
```python
stoploss = -0.10  # -10%
```
**Use Case:** 1h-4h timeframes, trend following
**Pros:** Survives volatility, stays in trends
**Cons:** Large drawdowns possible
**Best For:** Strong directional strategies

#### 4. Very Tight Stop Loss (High Win Rate Strategies)
```python
stoploss = -0.002  # -0.2%
```
**Use Case:** Mean reversion, high-probability setups
**Pros:** Minimal losses on wrong trades
**Cons:** Noise can stop you out constantly
**Warning:** Only use with very precise entry signals

### Stop Loss Best Practices

✅ **DO:**
- Set stop loss based on timeframe volatility
- Use wider stops on lower timeframes (more noise)
- Backtest to see how often stop loss triggers
- Adjust based on pair volatility (BTC = tighter, alts = wider)

❌ **DON'T:**
- Use same stop loss for all timeframes
- Set it too tight (death by 1000 cuts)
- Set it too wide (large losses add up)
- Ignore stop loss hit rate in backtests

### Dynamic Stop Loss

You can use ATR (Average True Range) to set dynamic stops:

```python
def custom_stoploss(self, pair: str, trade: 'Trade', current_time: datetime,
                    current_rate: float, current_profit: float, **kwargs) -> float:
    """
    Dynamic stop loss based on ATR
    """
    dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
    last_candle = dataframe.iloc[-1].squeeze()
    
    # Use 2x ATR as stop distance
    atr = last_candle['atr']
    entry_price = trade.open_rate
    stop_distance = (2 * atr) / entry_price
    
    return -stop_distance  # Returns negative value
```

---

## Trailing Stop Loss

### What is Trailing Stop Loss?

Trailing stop is a **dynamic stop loss** that moves up (never down) as price moves in your favor. It **locks in profits** while giving the trade room to grow.

### Configuration

```python
trailing_stop = True                          # Enable trailing stop
trailing_stop_positive = 0.01                 # Trail 1% below peak
trailing_stop_positive_offset = 0.02          # Activate at 2% profit
trailing_only_offset_is_reached = True        # Don't trail until offset hit
```

### Parameters Explained

#### 1. `trailing_stop`
- **Type:** Boolean
- **Default:** False
- **What it does:** Enables/disables trailing stop feature
- **Example:**
  ```python
  trailing_stop = True   # Trailing enabled
  trailing_stop = False  # Only use hard stop loss
  ```

#### 2. `trailing_stop_positive`
- **Type:** Decimal (positive value)
- **What it does:** Distance to trail below highest profit reached
- **Format:** Decimal (0.01 = 1%)
- **Example:**
  ```python
  trailing_stop_positive = 0.01  # Trail 1% below peak
  ```
  - Peak profit: 5% → Trail at 4% (exit if drops to 4%)
  - Peak profit: 10% → Trail at 9% (exit if drops to 9%)

#### 3. `trailing_stop_positive_offset`
- **Type:** Decimal (positive value)
- **What it does:** Minimum profit required to activate trailing
- **Format:** Decimal (0.02 = 2%)
- **Example:**
  ```python
  trailing_stop_positive_offset = 0.02  # Activate at 2% profit
  ```
  - Profit < 2%: Trailing inactive, hard stop loss applies
  - Profit ≥ 2%: Trailing activates

#### 4. `trailing_only_offset_is_reached`
- **Type:** Boolean
- **What it does:** Determines if trailing waits for offset
- **Example:**
  ```python
  trailing_only_offset_is_reached = True   # Wait for offset
  trailing_only_offset_is_reached = False  # Trail from entry
  ```

### How Trailing Stop Works

**Configuration Example:**
```python
stoploss = -0.10                          # -10% hard stop
trailing_stop = True
trailing_stop_positive = 0.005            # 0.5% trail distance
trailing_stop_positive_offset = 0.015     # Activate at 1.5% profit
trailing_only_offset_is_reached = True
```

**Trade Timeline:**

| Time | Price | Profit | Peak Profit | Trailing Stop | Status |
|------|-------|--------|-------------|---------------|--------|
| T=0  | $100.00 | 0% | 0% | -10% ($90) | Hard stop active |
| T=5  | $101.00 | +1% | +1% | -10% ($90) | Still using hard stop (< 1.5% offset) |
| T=10 | $101.60 | +1.6% | +1.6% | +1.1% ($101.10) | **Trailing activated!** (1.6% - 0.5% = 1.1%) |
| T=15 | $102.50 | +2.5% | +2.5% | +2.0% ($102.00) | Trailing moved up (2.5% - 0.5% = 2.0%) |
| T=20 | $102.00 | +2.0% | +2.5% | +2.0% ($102.00) | Price dropped but still above trail |
| T=25 | $101.90 | +1.9% | +2.5% | +2.0% ($102.00) | **EXIT!** (price fell below $102.00) |

**Result:** 
- Locked in +1.9% profit instead of riding it down
- Without trailing: Might have hit ROI or exited at lower profit

### Trailing Stop Strategies

#### 1. Tight Trailing (Lock Profits Quickly)
```python
stoploss = -0.02                          # -2% hard stop
trailing_stop = True
trailing_stop_positive = 0.003            # 0.3% trail (very tight)
trailing_stop_positive_offset = 0.008     # Activate at 0.8%
trailing_only_offset_is_reached = True
```
**Use Case:** Scalping, volatile markets
**Behavior:** Locks in profits aggressively, exits on small pullbacks
**Pros:** Protects gains quickly
**Cons:** Exits on normal retracements

#### 2. Loose Trailing (Let Profits Run)
```python
stoploss = -0.05                          # -5% hard stop
trailing_stop = True
trailing_stop_positive = 0.015            # 1.5% trail (loose)
trailing_stop_positive_offset = 0.03      # Activate at 3%
trailing_only_offset_is_reached = True
```
**Use Case:** Trend following, strong momentum
**Behavior:** Gives trades room to breathe, follows trends
**Pros:** Captures larger moves
**Cons:** Gives back more profit on reversals

#### 3. Aggressive Early Trailing
```python
stoploss = -0.03                          # -3% hard stop
trailing_stop = True
trailing_stop_positive = 0.005            # 0.5% trail
trailing_stop_positive_offset = 0.005     # Activate at just 0.5%!
trailing_only_offset_is_reached = True
```
**Use Case:** High win rate strategies, quick scalps
**Behavior:** Trails almost immediately
**Pros:** Never gives back much profit
**Cons:** May exit too early on breakouts

#### 4. UTBotScalping1m Settings (From Our Strategy)
```python
stoploss = -0.005                         # -0.5% hard stop (very tight!)
trailing_stop = True
trailing_stop_positive = 0.004            # 0.4% trail
trailing_stop_positive_offset = 0.006     # Activate at 0.6%
trailing_only_offset_is_reached = True
```
**Performance:**
- ✅ 430 trailing stop exits
- ✅ 93.7% win rate on trailing exits
- ✅ +14.77 USDT profit from trailing
**Analysis:** Trailing worked VERY well! Only issue was hard stop too tight (-0.5%)

### Trailing vs. Hard Stop

**Comparison:**

| Feature | Hard Stop Loss | Trailing Stop |
|---------|---------------|---------------|
| Movement | Fixed at entry price | Moves up with profit |
| Purpose | Limit losses | Lock in profits |
| When Active | Always | After offset reached |
| Direction | Never changes | Only moves up |
| Best For | Protecting capital | Capturing trends |

**Example:**

```python
# Scenario 1: Hard Stop Only
stoploss = -0.05
trailing_stop = False

Entry: $100
Stop: $95 (fixed)
Price goes to $110 → Drops to $96 → Still in trade (above $95)
Price drops to $94 → EXIT at -6% loss
```

```python
# Scenario 2: Hard Stop + Trailing
stoploss = -0.05
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.02
trailing_only_offset_is_reached = True

Entry: $100
Hard stop: $95
Price goes to $102 → Trailing activates at +2%
Peak: $110 (+10%) → Trailing at $108.90 (10% - 1% = 9%)
Price drops to $108 → EXIT at +8% profit
```

**Result:** Trailing captured +8% vs. potential loss with hard stop only!

### Trailing Stop Best Practices

✅ **DO:**
- Use trailing offset > trailing distance (e.g., 2% offset, 1% trail)
- Test different settings with your strategy
- Use wider trailing on trending markets
- Combine with ROI for multi-exit approach

❌ **DON'T:**
- Trail too tightly (0.1% = constant exits)
- Activate trailing immediately (let trade develop)
- Use same settings for all timeframes
- Forget that trailing only moves UP (never down)

### Common Trailing Issues

**Problem 1: Trailing Exits Too Early**
```python
# Bad: Too tight
trailing_stop_positive = 0.002  # 0.2% trail

# Fix: Widen trail distance
trailing_stop_positive = 0.01   # 1% trail
```

**Problem 2: Trailing Never Activates**
```python
# Bad: Offset too high
trailing_stop_positive_offset = 0.10  # 10% (rarely reached)

# Fix: Lower offset
trailing_stop_positive_offset = 0.02  # 2% (more realistic)
```

**Problem 3: Trailing Gives Back Too Much Profit**
```python
# Bad: Loose trail on scalping
trailing_stop_positive = 0.02  # 2% trail on 1m timeframe

# Fix: Tighter trail for scalping
trailing_stop_positive = 0.005  # 0.5% trail
```

---

## Exit Signals

### What are Exit Signals?

Exit signals are **indicator-based exits** defined in `populate_exit_trend()`. They trigger when technical conditions suggest the trade should close.

### Configuration

```python
use_exit_signal = True              # Enable exit signals
exit_profit_only = False            # Exit even at loss
exit_profit_offset = 0.0            # Minimum profit for exit signal
```

### Parameters Explained

#### 1. `use_exit_signal`
- **Type:** Boolean
- **Default:** False
- **What it does:** Enables signals from populate_exit_trend()
- **Example:**
  ```python
  use_exit_signal = True   # Check exit conditions
  use_exit_signal = False  # Ignore exit signals (ROI/stop only)
  ```

#### 2. `exit_profit_only`
- **Type:** Boolean
- **Default:** False
- **What it does:** Only exit on signal if trade is profitable
- **Example:**
  ```python
  exit_profit_only = True   # Only exit on signal if profit > 0
  exit_profit_only = False  # Exit on signal at any profit/loss
  ```

**Comparison:**

```python
# Dangerous Setting (Current UTBotScalping1m)
use_exit_signal = True
exit_profit_only = False

# Trade at -3% loss, exit signal appears → EXIT at -3% 😱
# Trade at +0.5% profit, exit signal appears → EXIT at +0.5%
```

```python
# Safer Setting
use_exit_signal = True
exit_profit_only = True

# Trade at -3% loss, exit signal appears → IGNORE (wait for stop loss)
# Trade at +2% profit, exit signal appears → EXIT at +2% ✅
```

#### 3. `exit_profit_offset`
- **Type:** Decimal
- **Default:** 0.0
- **What it does:** Minimum profit required for exit signal
- **Example:**
  ```python
  exit_profit_offset = 0.0    # No minimum
  exit_profit_offset = 0.005  # Need 0.5% profit minimum
  exit_profit_offset = 0.02   # Need 2% profit minimum
  ```

**How it works:**
```python
exit_profit_only = True
exit_profit_offset = 0.01  # Need 1% profit

# Scenario:
# Trade at +0.5%, exit signal → IGNORE (< 1%)
# Trade at +1.2%, exit signal → EXIT ✅ (≥ 1%)
# Trade at -2%, exit signal → IGNORE (not profitable)
```

### Exit Signal Implementation

**Example from UTBotScalping1m:**

```python
def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            # Exit when UT Bot flips to sell
            (dataframe['ut_bot_sell'] == True) &
            (dataframe['volume'] > 0)
        ),
        'exit_long'] = 1
    return dataframe
```

**What happens:**
1. Every candle checks if `ut_bot_sell` is True
2. If True + use_exit_signal=True → Exit triggered
3. Exit competes with ROI, trailing, and stop loss
4. **First exit to trigger wins**

### Exit Signal Strategies

#### 1. Disabled Exit Signals (ROI Only)
```python
use_exit_signal = False
```
**Use Case:** When indicator exits are unreliable
**Result:** Only ROI, trailing, and stop loss can exit
**Best For:** Strategies with poor exit signal performance
**UTBotScalping1m:** Should use this! (Exit signals have 3.9% win rate)

#### 2. Profit-Only Exit Signals
```python
use_exit_signal = True
exit_profit_only = True
exit_profit_offset = 0.003  # 0.3% minimum
```
**Use Case:** Conservative exit signal usage
**Result:** Only exits on signals when trade is winning
**Best For:** Most strategies (protects against bad exits)

#### 3. Aggressive Exit Signals (Dangerous!)
```python
use_exit_signal = True
exit_profit_only = False
exit_profit_offset = 0.0
```
**Use Case:** When exit signals are highly accurate
**Result:** Exits immediately on any signal
**Problem:** UTBotScalping1m lost -74.82 USDT this way!
**Warning:** Only use if backtests show >80% win rate on exit signals

#### 4. High Threshold Exit Signals
```python
use_exit_signal = True
exit_profit_only = True
exit_profit_offset = 0.01  # 1% minimum
```
**Use Case:** Only exit on signals after capturing some profit
**Result:** Prevents premature exits, lets ROI handle small profits
**Best For:** Scalping strategies with tight ROI tables

### Exit Signal Analysis (UTBotScalping1m Case Study)

**Current Settings:**
```python
use_exit_signal = True
exit_profit_only = False
exit_profit_offset = 0.0
```

**Backtest Results:**
- Exit signal trades: 2,032 (49% of all trades!)
- Win rate: **3.9%** 😱
- Total P&L: **-74.82 USDT**
- Average loss: -0.037 USDT per trade

**Why it failed:**
1. UT Bot flips frequently on 1m timeframe (noise)
2. Exits at losses (exit_profit_only = False)
3. No profit filter (exit_profit_offset = 0.0)
4. Premature exits on temporary pullbacks

**Fix Options:**

**Option A: Disable Exit Signals**
```python
use_exit_signal = False  # Let ROI and trailing handle exits
```
**Expected improvement:** +74.82 USDT (remove losing exits)

**Option B: Require Profit**
```python
use_exit_signal = True
exit_profit_only = True
exit_profit_offset = 0.003  # 0.3% minimum
```
**Expected improvement:** Significant (only exit winners)

**Option C: Higher Profit Threshold**
```python
use_exit_signal = True
exit_profit_only = True
exit_profit_offset = 0.008  # 0.8% minimum (near ROI levels)
```
**Expected improvement:** Let ROI handle most exits, signals only for trend reversals

### Exit Priority Order

Freqtrade checks exits in this order:

1. **Emergency Stop** (exchange disconnection, etc.)
2. **Force Exit** (manual or time-based)
3. **Stop Loss** (hard or trailing)
4. **ROI** (time-based profit targets)
5. **Exit Signal** (if enabled)
6. **Custom Exit** (if implemented)

**First triggered exit wins** - others are ignored.

**Example:**

```python
# Current state:
# Profit: +1.5%
# ROI at 1.5%: True (would exit)
# Exit signal: True (would exit)
# Trailing stop: +1.0% (would NOT exit)

# Result: ROI exits (checked before exit signal)
```

### Exit Signal Best Practices

✅ **DO:**
- Backtest exit signal performance separately
- Use `exit_profit_only = True` by default
- Add profit offset if signals are unreliable
- Disable if win rate < 50% on exit signals
- Test with and without exit signals

❌ **DON'T:**
- Use `exit_profit_only = False` without testing
- Trust exit signals blindly (check win rate!)
- Exit on weak indicators (RSI alone, single MA cross)
- Forget that ROI is usually more reliable

---

## Timeframe

### What is Timeframe?

Timeframe determines the **candle duration** for your strategy. It affects signal frequency, accuracy, and trading style.

### Configuration

```python
timeframe = '1m'   # 1-minute candles
timeframe = '5m'   # 5-minute candles
timeframe = '1h'   # 1-hour candles
timeframe = '1d'   # Daily candles
```

### Available Timeframes

| Timeframe | Duration | Candles/Day | Use Case |
|-----------|----------|-------------|----------|
| `'1m'` | 1 minute | 1,440 | Ultra-fast scalping |
| `'5m'` | 5 minutes | 288 | Fast scalping |
| `'15m'` | 15 minutes | 96 | Scalping/day trading |
| `'30m'` | 30 minutes | 48 | Day trading |
| `'1h'` | 1 hour | 24 | Swing trading |
| `'4h'` | 4 hours | 6 | Swing trading |
| `'1d'` | 1 day | 1 | Position trading |

### Timeframe Characteristics

#### 1-Minute (1m)
```python
timeframe = '1m'
```
**Characteristics:**
- **Signal frequency:** Very high (100+ trades/day possible)
- **Noise level:** Extreme (random price movements)
- **Win rate:** Usually lower (30-40%)
- **Profit per trade:** Small (0.5-2%)
- **Stop loss:** Very tight (-0.5% to -1%)
- **Advantages:** Many opportunities, quick feedback
- **Disadvantages:** High fees, whipsaws, stress

**Best For:**
- Pure scalpers
- High-frequency strategies
- Market making
- Bots with very precise signals

**Example Strategy:**
```python
timeframe = '1m'
minimal_roi = {
    "0": 0.015,    # 1.5%
    "5": 0.01,     # 1%
    "10": 0.005    # 0.5%
}
stoploss = -0.005  # -0.5%
```

#### 5-Minute (5m)
```python
timeframe = '5m'
```
**Characteristics:**
- **Signal frequency:** High (20-50 trades/day)
- **Noise level:** High (but less than 1m)
- **Win rate:** Moderate (40-50%)
- **Profit per trade:** Small-medium (1-3%)
- **Stop loss:** Tight (-1% to -2%)
- **Advantages:** Good balance, decent signals
- **Disadvantages:** Still affected by noise

**Best For:**
- Scalping with less stress
- Day trading strategies
- Momentum trading
- Most automated strategies

**Example Strategy:**
```python
timeframe = '5m'
minimal_roi = {
    "0": 0.03,     # 3%
    "15": 0.02,    # 2%
    "30": 0.01     # 1%
}
stoploss = -0.015  # -1.5%
```

#### 15-Minute (15m)
```python
timeframe = '15m'
```
**Characteristics:**
- **Signal frequency:** Moderate (10-30 trades/day)
- **Noise level:** Moderate
- **Win rate:** Good (45-55%)
- **Profit per trade:** Medium (2-5%)
- **Stop loss:** Medium (-2% to -3%)
- **Advantages:** Clearer trends, less noise
- **Disadvantages:** Fewer opportunities

**Best For:**
- Day trading
- Trend following
- Breakout strategies
- Most retail traders

**Example Strategy:**
```python
timeframe = '15m'
minimal_roi = {
    "0": 0.05,     # 5%
    "30": 0.03,    # 3%
    "60": 0.015    # 1.5%
}
stoploss = -0.025  # -2.5%
```

#### 1-Hour (1h)
```python
timeframe = '1h'
```
**Characteristics:**
- **Signal frequency:** Low (2-10 trades/day)
- **Noise level:** Low
- **Win rate:** Higher (50-60%)
- **Profit per trade:** Large (5-15%)
- **Stop loss:** Wide (-5% to -10%)
- **Advantages:** Strong signals, lower fees
- **Disadvantages:** Slower feedback, fewer trades

**Best For:**
- Swing trading
- Trend following
- Longer-term positions
- Part-time traders

**Example Strategy:**
```python
timeframe = '1h'
minimal_roi = {
    "0": 0.10,      # 10%
    "180": 0.05,    # 5%
    "360": 0.02     # 2%
}
stoploss = -0.05   # -5%
```

### Multi-Timeframe Analysis

Use multiple timeframes for better signals:

```python
timeframe = '5m'  # Trading timeframe

def informative_pairs(self):
    return [
        ("BTC/USDT", "1h"),  # Higher timeframe for trend
    ]

def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    # Get 1h data for trend direction
    informative_1h = self.dp.get_pair_dataframe(pair=metadata['pair'], timeframe='1h')
    informative_1h['ema_200'] = ta.EMA(informative_1h, timeperiod=200)
    
    # Merge into 5m dataframe
    dataframe = merge_informative_pair(dataframe, informative_1h, self.timeframe, '1h', ffill=True)
    
    # Now dataframe has both 5m candles and 1h EMA
    return dataframe

def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
    dataframe.loc[
        (
            # 5m entry signal
            (dataframe['rsi'] < 30) &
            # But only if 1h trend is up
            (dataframe['close'] > dataframe['ema_200_1h'])
        ),
        'enter_long'] = 1
    return dataframe
```

### Timeframe Impact on Strategy Parameters

Different timeframes need different parameters:

```python
# 1m Scalping
timeframe = '1m'
minimal_roi = {"0": 0.01, "5": 0.005}
stoploss = -0.005
trailing_stop_positive_offset = 0.006
startup_candle_count = 30

# vs.

# 1h Swing Trading
timeframe = '1h'
minimal_roi = {"0": 0.10, "360": 0.02}
stoploss = -0.05
trailing_stop_positive_offset = 0.03
startup_candle_count = 200  # Need more history!
```

### Timeframe Best Practices

✅ **DO:**
- Match ROI/stop loss to timeframe volatility
- Use longer timeframes for trend confirmation
- Increase startup_candle_count for longer timeframes
- Test strategy on multiple timeframes

❌ **DON'T:**
- Use 1m timeframe for slow indicators (200 EMA)
- Use 1h timeframe for scalping strategies
- Forget fees eat profits more on lower timeframes
- Mix timeframe parameters (1m settings on 1h)

---

## Startup Candle Count

### What is Startup Candle Count?

Number of historical candles required before strategy produces valid signals. Needed for indicator calculations.

### Configuration

```python
startup_candle_count: int = 200
```

### How It Works

**Why Needed:**
- Indicators need historical data to calculate
- EMA(200) needs 200 candles minimum
- RSI(14) needs 14 candles minimum
- Strategy needs warm-up period

**Example:**

```python
startup_candle_count = 100

# Freqtrade downloads:
# - Your requested backtest period: 30 days
# - Plus startup period: 100 candles extra
# Total: 30 days + 100 candles of earlier data
```

**Timeline:**
```
<--- 100 candles ---><--------- 30 days --------->
    Startup Period      Actual Backtesting Period
   (no trades here)      (trades can happen)
```

### Calculating Required Startup Candles

**Formula:** Use the **longest indicator period** in your strategy

**Examples:**

```python
# Strategy uses:
# - EMA(50)
# - RSI(14)
# - ATR(10)

# Longest period = 50
startup_candle_count = 50  # Minimum
startup_candle_count = 100  # Recommended (2x longest)
```

```python
# Strategy uses:
# - EMA(200)
# - MACD(12, 26, 9)
# - Bollinger Bands(20)

# Longest period = 200
startup_candle_count = 200  # Minimum
startup_candle_count = 400  # Recommended (2x longest)
```

```python
# UTBotScalping1m uses:
# - ATR(10)
# - Volume MA(20)

# Longest period = 20
startup_candle_count = 30  # Safe (1.5x longest)
```

### Startup Candles by Timeframe

| Timeframe | Typical Startup Count | Reason |
|-----------|----------------------|--------|
| 1m | 30-100 | Fast indicators, less history needed |
| 5m | 50-200 | Moderate indicators |
| 15m | 100-300 | Longer EMAs common |
| 30m | 200-500 | Trend indicators |
| 1h | 200-500 | Often use 200 EMA |
| 4h | 300-600 | Long-term trends |

### Too Few vs. Too Many

**Too Few Startup Candles:**
```python
# Strategy uses EMA(200)
startup_candle_count = 50  # ❌ Too few!

# Result:
# - First 150 candles have invalid EMA values (NaN or wrong)
# - Strategy makes bad trades based on incomplete indicators
# - Backtest shows unrealistic results
```

**Too Many Startup Candles:**
```python
# Strategy uses ATR(10)
startup_candle_count = 1000  # ❌ Overkill!

# Result:
# - Unnecessarily large data download
# - Slower backtesting
# - No benefit (waste of resources)
```

**Just Right:**
```python
# Strategy uses ATR(10) and Volume MA(20)
startup_candle_count = 30  # ✅ Perfect (1.5x longest)
```

### Best Practices

✅ **DO:**
- Set to 2x your longest indicator period
- Use minimum 30 candles even for fast strategies
- Increase for multi-timeframe strategies
- Test that indicators have valid values from start

❌ **DON'T:**
- Use less than longest indicator period
- Use 1000+ unless truly needed
- Forget to update when adding longer indicators
- Assume default (20) is always enough

### Multi-Timeframe Startup

When using higher timeframe data:

```python
timeframe = '5m'  # Trading timeframe

def informative_pairs(self):
    return [
        ("BTC/USDT", "1h"),  # Need 1h data
    ]

# 1h candles need more history
# If using 1h EMA(200), need 200 * 1h = 200 hours
# In 5m candles: 200 hours / (5/60) = 2,400 5m candles!

startup_candle_count = 2500  # Account for 1h EMA(200)
```

---

## Custom Parameters (Hyperopt)

### What are Custom Parameters?

Hyperoptable parameters allow Freqtrade to **optimize** your strategy by testing different values automatically.

### Parameter Types

#### 1. DecimalParameter
```python
ut_key_value = DecimalParameter(
    low=3.0,              # Minimum value to test
    high=5.0,             # Maximum value to test
    decimals=1,           # Precision (3.0, 3.1, 3.2, ...)
    default=3.5,          # Default value
    space="buy"           # Optimization space
)
```

**Use Case:** Multipliers, ratios, percentages

**Examples:**
```python
# ATR multiplier
atr_mult = DecimalParameter(1.0, 5.0, decimals=1, default=2.5, space="buy")

# RSI threshold
rsi_buy = DecimalParameter(20.0, 40.0, decimals=0, default=30.0, space="buy")

# Take profit percentage
tp_percent = DecimalParameter(0.01, 0.05, decimals=3, default=0.025, space="sell")
```

#### 2. IntParameter
```python
ut_atr_period = IntParameter(
    low=5,                # Minimum value
    high=20,              # Maximum value
    default=10,           # Default value
    space="buy"           # Optimization space
)
```

**Use Case:** Indicator periods, lookback windows

**Examples:**
```python
# EMA period
ema_period = IntParameter(50, 200, default=100, space="buy")

# RSI period
rsi_period = IntParameter(7, 21, default=14, space="buy")

# Bollinger Bands period
bb_period = IntParameter(10, 30, default=20, space="buy")
```

#### 3. CategoricalParameter
```python
buy_trigger = CategoricalParameter(
    categories=["rsi", "bb", "macd"],  # Options to test
    default="rsi",                      # Default choice
    space="buy"
)
```

**Use Case:** Choosing between indicators or strategies

**Examples:**
```python
# Entry indicator choice
entry_method = CategoricalParameter(
    ["ema_cross", "rsi_oversold", "bbands_break"],
    default="rsi_oversold",
    space="buy"
)

# Trend filter
trend_filter = CategoricalParameter(
    ["ema_50", "ema_200", "sma_100", "none"],
    default="ema_200",
    space="buy"
)
```

#### 4. BooleanParameter
```python
use_volume_filter = BooleanParameter(
    default=True,
    space="buy"
)
```

**Use Case:** Enable/disable features

**Examples:**
```python
# Volume filter
use_volume = BooleanParameter(default=True, space="buy")

# Trend confirmation
require_uptrend = BooleanParameter(default=False, space="buy")

# Additional filters
check_momentum = BooleanParameter(default=True, space="buy")
```

### Optimization Spaces

| Space | Purpose |
|-------|---------|
| `"buy"` | Entry conditions |
| `"sell"` | Exit conditions |
| `"roi"` | ROI table optimization |
| `"stoploss"` | Stop loss optimization |
| `"trailing"` | Trailing stop optimization |

### Using Parameters in Strategy

```python
class MyStrategy(IStrategy):
    # Define parameters
    rsi_period = IntParameter(7, 21, default=14, space="buy")
    rsi_buy_threshold = DecimalParameter(20.0, 40.0, default=30.0, space="buy")
    use_volume_filter = BooleanParameter(default=True, space="buy")
    
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Use parameter value with .value
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=self.rsi_period.value)
        dataframe['volume_ma'] = dataframe['volume'].rolling(20).mean()
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        
        # Always check RSI
        conditions.append(dataframe['rsi'] < self.rsi_buy_threshold.value)
        
        # Conditionally check volume
        if self.use_volume_filter.value:
            conditions.append(dataframe['volume'] > dataframe['volume_ma'])
        
        # Combine all conditions
        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'enter_long'] = 1
        
        return dataframe
```

### Hyperopt Command

```bash
# Optimize buy parameters
freqtrade hyperopt \
  --strategy MyStrategy \
  --hyperopt-loss SharpeHyperOptLoss \
  --spaces buy \
  --epochs 100

# Optimize everything
freqtrade hyperopt \
  --strategy MyStrategy \
  --hyperopt-loss SharpeHyperOptLoss \
  --spaces buy sell roi stoploss trailing \
  --epochs 500
```

### Best Practices

✅ **DO:**
- Start with reasonable parameter ranges
- Use fewer parameters initially (faster optimization)
- Run at least 100 epochs
- Save results and test on separate data

❌ **DON'T:**
- Over-optimize (curve fitting)
- Use unrealistic parameter ranges
- Trust single hyperopt run
- Skip walk-forward testing

---

## Parameter Interactions

### How Exit Mechanisms Compete

Multiple exit mechanisms can trigger simultaneously. **First one checked wins.**

### Exit Priority (Order of Checking)

```
1. Force Exit (manual/max_open_trades)
   ↓ (if not triggered)
2. Stop Loss (hard or trailing)
   ↓ (if not triggered)
3. ROI
   ↓ (if not triggered)
4. Exit Signal
   ↓ (if not triggered)
5. Custom Exit
   ↓ (if not triggered)
6. Stay in trade
```

### Scenario Examples

#### Scenario 1: ROI vs. Trailing Stop

**Configuration:**
```python
minimal_roi = {"0": 0.02}          # 2% ROI
stoploss = -0.05
trailing_stop = True
trailing_stop_positive = 0.01       # 1% trail
trailing_stop_positive_offset = 0.015  # Activate at 1.5%
```

**Trade Timeline:**
- Entry: $100
- Price: $102 (+2%)
- **Trailing:** Not yet active (need 1.5%)
- **ROI:** ✅ TRIGGERED at 2%
- **Result:** EXIT via ROI at +2%

**Alternative Timeline:**
- Entry: $100
- Price: $103 (+3%)
- **Trailing:** ✅ Active at +2% (3% - 1% = 2%)
- **ROI:** ✅ TRIGGERED at 2%
- **Result:** ROI checked first → EXIT via ROI at +3%

#### Scenario 2: Stop Loss vs. Exit Signal

**Configuration:**
```python
stoploss = -0.02                # -2%
use_exit_signal = True
exit_profit_only = False        # Exit at any profit/loss
```

**Trade Timeline:**
- Entry: $100
- Price drops: $97.50 (-2.5%)
- **Stop Loss:** ✅ TRIGGERED at -2% or worse
- **Exit Signal:** Also triggers (bearish)
- **Result:** Stop loss checked first → EXIT at ~-2%

#### Scenario 3: Multiple Competing Exits

**Configuration:**
```python
minimal_roi = {
    "0": 0.03,      # 3%
    "30": 0.01      # 1% after 30 min
}
stoploss = -0.02
trailing_stop = True
trailing_stop_positive = 0.005
trailing_stop_positive_offset = 0.015
use_exit_signal = True
exit_profit_only = True
exit_profit_offset = 0.005
```

**Complex Timeline:**

| Time | Price | Profit | Stop Check | ROI Check | Trailing Check | Signal Check | Result |
|------|-------|--------|------------|-----------|----------------|--------------|--------|
| T=0 | $100.00 | 0% | Pass (-2%) | Need 3% | Inactive | Not profitable | Hold |
| T=15 | $102.00 | +2% | Pass | Need 3% | Active (+1.5%) | Pass | Hold |
| T=25 | $101.00 | +1% | Pass | Need 3% | ✅ EXIT | N/A | **EXIT +1%** |

**Explanation:** Trailing stop triggered at +1.5% (2% - 0.5%), then price dropped to +1%, hitting the trailing stop.

### ROI + Trailing Best Combo

Most profitable strategies use BOTH:

```python
# Aggressive ROI for home runs
minimal_roi = {
    "0": 0.10,      # 10% immediate (rare but amazing)
    "60": 0.03,     # 3% after 1 hour (good trade)
    "180": 0.015,   # 1.5% after 3 hours (okay trade)
    "360": 0.01     # 1% after 6 hours (minimum acceptable)
}

# Trailing to catch trends
trailing_stop = True
trailing_stop_positive = 0.01       # 1% trail
trailing_stop_positive_offset = 0.02  # Activate at 2%
trailing_only_offset_is_reached = True
```

**How They Work Together:**
- Small profits (0-2%): ROI handles (quick scalps)
- Medium profits (2-10%): Trailing kicks in (locks gains)
- Large profits (10%+): ROI instant exit (home runs)

### Common Conflicts

#### Problem 1: ROI Too Tight
```python
minimal_roi = {"0": 0.005}  # 0.5% immediate
trailing_stop_positive_offset = 0.01  # Needs 1%

# Result: ROI always exits before trailing activates ❌
```

**Fix:**
```python
minimal_roi = {"0": 0.05}   # 5% (higher than offset)
trailing_stop_positive_offset = 0.02  # 2%

# Now trailing can activate and work ✅
```

#### Problem 2: Exit Signals Override Everything
```python
use_exit_signal = True
exit_profit_only = False  # Exits even at loss

# Result: Bad signals exit at -3%, ignoring ROI potential ❌
```

**Fix:**
```python
use_exit_signal = True
exit_profit_only = True
exit_profit_offset = 0.01  # Need 1% minimum

# Now signals only exit winners ✅
```

---

## Real-World Examples

### Example 1: Conservative Swing Trading

**Goal:** Capture larger moves, minimize losses

```python
class ConservativeSwingStrategy(IStrategy):
    # 1h timeframe for clear trends
    timeframe = '1h'
    
    # Patient ROI - wait for bigger moves
    minimal_roi = {
        "0": 0.20,      # 20% home run
        "720": 0.10,    # 10% after 12 hours
        "1440": 0.05,   # 5% after 1 day
        "2880": 0.02    # 2% after 2 days (minimum)
    }
    
    # Wide stop loss - survive volatility
    stoploss = -0.08  # -8%
    
    # Conservative trailing - let profits run
    trailing_stop = True
    trailing_stop_positive = 0.02       # 2% trail (loose)
    trailing_stop_positive_offset = 0.05  # Activate at 5%
    trailing_only_offset_is_reached = True
    
    # Only exit on signals if profitable
    use_exit_signal = True
    exit_profit_only = True
    exit_profit_offset = 0.02  # Need 2% minimum
    
    # Long indicators need history
    startup_candle_count = 200
    
    # Hyperopt parameters
    ema_fast = IntParameter(20, 50, default=30, space="buy")
    ema_slow = IntParameter(100, 200, default=150, space="buy")
```

**Best For:** Patient traders, trending markets, larger accounts

---

### Example 2: Aggressive Scalping

**Goal:** Quick in and out, small consistent profits

```python
class AggressiveScalpingStrategy(IStrategy):
    # 5m timeframe - balance speed and clarity
    timeframe = '5m'
    
    # Quick ROI - take profits fast
    minimal_roi = {
        "0": 0.025,   # 2.5% immediate
        "5": 0.02,    # 2% after 5 min
        "10": 0.015,  # 1.5% after 10 min
        "20": 0.01,   # 1% after 20 min
        "40": 0.005   # 0.5% after 40 min (minimum)
    }
    
    # Tight stop - limit losses quickly
    stoploss = -0.015  # -1.5%
    
    # Aggressive trailing - lock profits immediately
    trailing_stop = True
    trailing_stop_positive = 0.005      # 0.5% trail (tight)
    trailing_stop_positive_offset = 0.01  # Activate at 1%
    trailing_only_offset_is_reached = True
    
    # Disable exit signals - too unreliable on short timeframes
    use_exit_signal = False
    
    # Short indicators
    startup_candle_count = 50
    
    # Hyperopt parameters
    rsi_period = IntParameter(7, 14, default=10, space="buy")
    rsi_buy = DecimalParameter(20.0, 35.0, default=28.0, space="buy")
    rsi_sell = DecimalParameter(65.0, 80.0, default=72.0, space="sell")
```

**Best For:** Active traders, high-volume pairs, automation

---

### Example 3: Balanced Day Trading

**Goal:** 5-10 good trades per day, solid win rate

```python
class BalancedDayTradingStrategy(IStrategy):
    # 15m timeframe - sweet spot
    timeframe = '15m'
    
    # Balanced ROI
    minimal_roi = {
        "0": 0.08,     # 8% home run
        "30": 0.04,    # 4% after 30 min
        "60": 0.025,   # 2.5% after 1 hour
        "120": 0.015,  # 1.5% after 2 hours
        "240": 0.01    # 1% after 4 hours
    }
    
    # Medium stop loss
    stoploss = -0.03  # -3%
    
    # Balanced trailing
    trailing_stop = True
    trailing_stop_positive = 0.01       # 1% trail
    trailing_stop_positive_offset = 0.02  # Activate at 2%
    trailing_only_offset_is_reached = True
    
    # Exit signals only for winners
    use_exit_signal = True
    exit_profit_only = True
    exit_profit_offset = 0.005  # Need 0.5% minimum
    
    # Medium startup
    startup_candle_count = 100
    
    # Multi-timeframe for confirmation
    def informative_pairs(self):
        return [
            (metadata['pair'], '1h')  # Higher timeframe trend
        ]
    
    # Hyperopt parameters
    bb_period = IntParameter(15, 25, default=20, space="buy")
    bb_std = DecimalParameter(1.5, 2.5, decimals=1, default=2.0, space="buy")
    use_volume_filter = BooleanParameter(default=True, space="buy")
```

**Best For:** Most traders, balanced risk/reward, consistent profits

---

## Summary: Quick Reference Table

| Parameter | Type | Example | Use Case |
|-----------|------|---------|----------|
| **minimal_roi** | Dict | `{"0": 0.05, "30": 0.02}` | Time-based profit targets |
| **stoploss** | Float | `-0.05` | Maximum loss before exit |
| **trailing_stop** | Bool | `True` | Enable trailing stop |
| **trailing_stop_positive** | Float | `0.01` | Trail distance (1%) |
| **trailing_stop_positive_offset** | Float | `0.02` | Activation threshold (2%) |
| **trailing_only_offset_is_reached** | Bool | `True` | Wait for offset |
| **use_exit_signal** | Bool | `True` | Enable indicator exits |
| **exit_profit_only** | Bool | `True` | Only exit signals if profit |
| **exit_profit_offset** | Float | `0.005` | Minimum profit for exit signal |
| **timeframe** | String | `'15m'` | Candle duration |
| **startup_candle_count** | Int | `100` | History needed for indicators |

---

## Final Recommendations

### For Beginners
```python
timeframe = '15m'
minimal_roi = {"0": 0.05, "60": 0.02, "180": 0.01}
stoploss = -0.03
trailing_stop = True
trailing_stop_positive = 0.01
trailing_stop_positive_offset = 0.02
use_exit_signal = False  # Learn ROI first
startup_candle_count = 100
```

### For Experienced Traders
```python
# Optimize everything
timeframe = '5m'  # Or your preference
# Use hyperopt to find optimal ROI
# Use hyperopt to find optimal stops
# Test with and without exit signals
# Multi-timeframe confirmation
# Walk-forward testing
```

### For UTBotScalping1m Fix
```python
# Option 1: Disable exit signals
use_exit_signal = False

# Option 2: Require profit
use_exit_signal = True
exit_profit_only = True
exit_profit_offset = 0.005

# Option 3: Widen stops
stoploss = -0.01  # -1% instead of -0.5%

# Option 4: Change timeframe
timeframe = '5m'  # Less noise than 1m
```

---

**End of Guide**

This guide covers all major parameters with examples, use cases, and real-world scenarios. Use it as a reference when configuring your Freqtrade strategies!
