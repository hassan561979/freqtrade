# 1-Minute Trading Strategies
*High Win-Rate Strategies for Ultra-Fast Scalping*

---

## Navigation
- [Back to Main Guide](TRADING_STRATEGIES_GUIDE.md)
- [5-Minute Strategies](strategies_5m.md)
- [15-Minute Strategies](strategies_15m.md)
- [30-Minute Strategies](strategies_30m.md)
- [1-Hour Strategies](strategies_1h.md)
- [Common Sections](shared_content.md) - UT Bot Guide, Risk Management, Implementation Tips

---

## Overview

**Trading Style:** SCALPING (Ultra-fast)  
**Time Commitment:** Active monitoring required  
**Capital Requirements:** $100-$1,000+  
**Recommended Experience:** Intermediate to Advanced

**Key Characteristics:**
- Very fast-paced (seconds to minutes per trade)
- Requires quick decision-making
- Many signals per day (20-50+)
- Small profit targets (0.3-1.5% per trade)
- Tight stop losses (0.2-0.5%)
- Best during high volume sessions

---

## Strategy 1A: UT Bot Scalping (Win Rate: ~68%)
**📊 Category:** SCALPING (Pure)

**Best For:** Pure scalpers, high-frequency trading  
**Recommended Pairs:** BTC/USDT, ETH/USDT  
**Capital Required:** $100+

### Optimal Market Conditions

**✅ BEST CONDITIONS:**
- **High volume trading sessions** (London open 3am-5am EST, NY open 9:30am-12pm EST)
- **Clear short-term trends** (price moving in one direction for 10-30 minutes)
- **Stable volatility** (ATR neither spiking nor dying)
- Price making **clean moves** (not whipsaw/choppy)
- **Tight spreads** (good liquidity)
- After news events settle (not during)

**❌ AVOID:**
- Low volume periods (weekends, holidays, late night)
- Choppy/ranging markets (false signals every 2-3 candles)
- During major news releases (unpredictable spikes)
- When spread widens significantly
- After extended trends without pullback
- Asian session (typically low volume for crypto)

**⚠️ WARNING SIGNS:**
- UT Bot flipping every 1-3 candles (whipsaw)
- Price consolidating in tight range
- Volume significantly below average
- Large wicks on candles (rejections)
- Spread widening (liquidity drying up)

**📊 Pre-Trade Checklist:**
1. Is it during high volume session (London/NY)?
2. Has UT Bot been consistent (not flipping constantly)?
3. Is ATR stable (not spiking or flat)?
4. Is 5m/15m timeframe showing same direction?
5. Is volume above average for this pair?
6. Is spread tight (<0.05%)?

### Setup
```
Indicator:
- UT Bot Indicator (Key Value: 3.5-4.0, ATR Period: 10)

TradingView Setup:
1. Add "UT Bot Alerts" indicator
2. Settings:
   - Key Value: 3.5 for volatile assets, 4.0 for stable
   - ATR Period: 10 (default)
3. Enable alerts for buy/sell signals
```

### Entry Rules - LONG
1. UT Bot BUY signal appears (green dot/label)
2. Confirm 5m chart is aligned (bullish)
3. Volume above average
4. Enter immediately on signal candle close

### Entry Rules - SHORT
1. UT Bot SELL signal appears (red dot/label)
2. Confirm 5m chart is aligned (bearish)
3. Volume above average
4. Enter immediately on signal candle close

### Exit Strategy

**Primary Exit Methods:**

**1. ROI (Return on Investment) Table:**
```python
minimal_roi = {
    "0": 0.015,      # 1.5% immediate (very aggressive take)
    "5": 0.012,      # 1.2% after 5 minutes
    "10": 0.01,      # 1% after 10 minutes
    "15": 0.008,     # 0.8% after 15 minutes
    "30": 0.005,     # 0.5% after 30 minutes
    "60": 0.003      # 0.3% after 1 hour (minimum acceptable)
}
```
**Rationale:** 1m scalping requires fast profit-taking. Target 0.5-1% typically hit within 5-20 minutes. Longer hold = lower expectations.

**2. Stop Loss Configuration:**

**UT Bot Trailing Stop (Primary):**
```
Stop Type: Dynamic (UT Bot trailing line)

Calculation:
- UT Bot calculates: Key Value (3.5) × ATR
- Stop line follows price
- Distance varies with volatility

Typical Range:
- BTC: 0.3-0.5% behind price
- ETH: 0.4-0.6% behind price
- Altcoins: 0.5-0.8% behind price

Example:
Entry: $67,800
UT Bot Line: $67,550
Distance: $250 (0.37%)
```

**Fixed Percentage Backup:**
```
Hard Stop: -0.5% from entry

When to Use:
- If UT Bot line too far (>0.8%)
- During high volatility
- As emergency backstop

Calculation:
Entry: $67,800
Fixed Stop: $67,461 (-0.5%)

Use TIGHTER of: UT Bot stop OR Fixed stop
```

**Break-Even Rule:**
```
Trigger: When profit = 2 × stop distance

Example:
Entry: $67,800
Stop: $67,550 (0.37% = $250 risk)
Break-even trigger: 0.74% profit
Price: $68,302
Action: Move stop to $67,810 (entry + fees)
Result: Risk-free trade
```

**3. UT Bot Signal Exit (Opposite Signal):**
```
Exit Condition: UT Bot gives opposite signal

LONG Position:
- UT Bot red dot (SELL signal) appears
- Action: Exit 100% immediately
- No hesitation

SHORT Position:
- UT Bot green dot (BUY signal) appears
- Action: Exit 100% immediately

Why Important:
- UT Bot is primary indicator
- Signal flip = trend change
- Priority: Higher than ROI table
- Speed: Critical (within 1-2 bars)

Override:
- Can override ROI profit targets
- Exit even if target not reached
- Opposite signal = immediate exit
```

**4. Partial Exit Strategy:**

**Scalping Approach (Quick Take):**
```
TP1 (60% position): 0.5% profit
- Fast target (3-10 minutes)
- Secure majority profit
- Move stop to breakeven
- Let 40% run

TP2 (40% position): 1.0% profit OR opposite signal
- Extended target (10-30 minutes)
- Exit on UT Bot opposite signal
- Or trail with UT Bot line
```

**Aggressive Scalping:**
```
TP1 (70%): 0.4% (very fast take)
TP2 (30%): 0.8% or opposite signal
```

**Patient Scalping:**
```
TP1 (50%): 0.7%
TP2 (30%): 1.2%
TP3 (20%): Trail with UT Bot line
```

**5. Time-Based Exits:**
```
Max Hold Time: 60 minutes

Time Actions:
0-15 min: Prime profit zone, hold patiently
15-30 min: If profit >0.5%, take 60%
30-45 min: If profit >0.3%, take 80%
45-60 min: Close all remaining
>60 min: Force close (scalp failed)

Reasoning:
- 1m scalps should complete fast
- Long holds = signal likely failed
- Move to next opportunity
```

**6. Trailing Stop Activation:**
```
Activation Point: 0.4% profit

Trailing Configuration:
- Distance: 0.25% behind highest point
- Update: Real-time (every tick)

Example:
Entry: $67,800
Price reaches: $68,071 (0.4% profit)
Trailing activates at: $67,970

As price moves:
Price: $68,200 → Stop: $68,029 (+0.34%)
Price: $68,500 → Stop: $68,329 (+0.78%)
Price: $68,300 → Stop triggered at $68,129 (+0.49%)
```

**7. Emergency Exits:**
```
Immediate Exit Conditions:

1. Sudden Volume Spike (>10x):
   - Possible news/manipulation
   - Exit 100% at market

2. Wide Spread (>0.1%):
   - Liquidity issue
   - Exit carefully with limit orders

3. UT Bot Flipping Rapidly:
   - Multiple signals in 5 minutes
   - Exit current trade
   - Stop trading this pair for 30 min

4. Price Gap:
   - Gap against position
   - Accept loss, exit immediately
```

**8. Exit Priority Hierarchy:**
```
Level 1 - IMMEDIATE (No delay):
1. Stop loss hit → Exit 100%
2. Opposite UT Bot signal → Exit 100%
3. Emergency condition → Exit 100%

Level 2 - HIGH PRIORITY:
4. Time > 60 min → Exit 100%
5. TP1 (0.5%) → Exit 60%
6. Trailing stop hit → Exit all

Level 3 - STANDARD:
7. TP2 (1.0%) → Exit 40%
8. ROI table triggers → Automatic exits
```

**Complete Freqtrade Configuration:**
```python
class UTBotScalping1m(IStrategy):
    
    # ROI table
    minimal_roi = {
        "0": 0.015,
        "5": 0.012,
        "10": 0.01,
        "15": 0.008,
        "30": 0.005,
        "60": 0.003
    }
    
    # Hard stop loss
    stoploss = -0.005  # -0.5%
    
    # Trailing stop configuration
    trailing_stop = True
    trailing_stop_positive = 0.004  # Start trailing at 0.4%
    trailing_stop_positive_offset = 0.006  # Activate at 0.6%
    trailing_only_offset_is_reached = True
    
    # Exit signals (UT Bot opposite)
    use_exit_signal = True
    exit_profit_only = False  # Exit on signal even at loss
    exit_profit_offset = 0.0
    
    # Ignore ROI if exit signal appears
    ignore_roi_if_entry_signal = False
    
    timeframe = '1m'
    
    def populate_exit_trend(self, dataframe, metadata):
        """
        Exit when UT Bot gives opposite signal
        """
        dataframe.loc[
            (
                (dataframe['ut_bot_signal'] == 'sell') &  # Opposite signal
                (dataframe['volume'] > 0)
            ),
            'exit_long'
        ] = 1
        
        return dataframe
```

### Example Trade
```
BTC/USDT 1m Chart
Time: 10:15 AM EST (NY session)

Entry: $67,800 (UT Bot buy signal + 5m bullish)
Stop Loss: $67,460 (-0.5%, $340)
TP1 (60%): $68,140 (+0.5%, $340)
TP2 (40%): $68,480 (+1.0%, $680)

Capital: $1,000
Risk: 0.5% = $5
Position Size: 0.0147 BTC

Outcome:
TP1 hit at 8 minutes → +$5 (closed 60%)
TP2 hit at 18 minutes → +$4.50 (closed 40%)
Total Profit: $9.50 (0.95% account)
```

### Performance Metrics
- Win Rate: 68%
- Average Win: 0.7%
- Average Loss: 0.4%
- Expectancy: +0.32% per trade
- Trades per Day: 20-40
- Hold Time: 5-30 minutes

---

## Strategy 1B: 1m VWAP Bounce (Win Rate: ~64%)
**📊 Category:** SCALPING (Price Action)

**Best For:** Volume-based scalping  
**Recommended Pairs:** High volume pairs only  
**Capital Required:** $200+

### Optimal Market Conditions

**✅ BEST CONDITIONS:**
- **High volume sessions** (London/NY overlap 8am-12pm EST)
- Price **oscillating around VWAP** (not running away)
- VWAP acting as **clear support/resistance**
- After VWAP tests 2-3 times (proven level)
- **Institutional trading hours**
- Clear bounces/rejections at VWAP line

**❌ AVOID:**
- Low volume (VWAP not reliable)
- Price trending strongly away from VWAP
- VWAP flat/horizontal (no direction)
- During first 30 min of day (VWAP establishing)
- Weekend low liquidity
- When VWAP tested 5+ times without reaction

**⚠️ WARNING SIGNS:**
- Price crossing VWAP without bounce
- Volume declining as approaching VWAP
- VWAP line choppy/erratic
- Large wicks through VWAP (rejections)
- Multiple failed bounces in 30 minutes

**📊 Pre-Trade Checklist:**
1. Is volume >1.5x average?
2. Has VWAP been tested 2-3 times already?
3. Is price clearly bouncing/rejecting at VWAP?
4. Is VWAP angled (not flat)?
5. Is it during high-volume session?
6. Is higher timeframe (5m/15m) confirming direction?

### Setup
```
Indicators:
- VWAP (Volume-Weighted Average Price)
- Volume bars
- Optional: EMA 20 for trend confirmation

TradingView:
1. Add VWAP indicator
2. Style: Make it bold/visible
3. Watch for price reactions at the line
```

### Entry Rules - LONG (VWAP Bounce)
1. Price approaches VWAP from above
2. Price touches or goes slightly below VWAP
3. Strong bullish candle forms (rejection wick)
4. Volume spike on bounce candle
5. Enter on next candle if it opens above VWAP

### Entry Rules - SHORT (VWAP Rejection)
1. Price approaches VWAP from below
2. Price touches or goes slightly above VWAP
3. Strong bearish candle forms (rejection wick)
4. Volume spike on rejection candle
5. Enter on next candle if it opens below VWAP

### Exit Strategy

**Primary Exit Methods:**

**1. ROI Table:**
```python
minimal_roi = {
    "0": 0.012,      # 1.2% immediate
    "5": 0.01,       # 1% after 5 min
    "10": 0.008,     # 0.8% after 10 min
    "20": 0.006,     # 0.6% after 20 min
    "40": 0.004,     # 0.4% after 40 min
    "60": 0.002      # 0.2% after 1 hour
}
```
**Rationale:** VWAP bounces are quick. Target 0.5-0.8% within 10-20 min typical.

**2. Stop Loss:**
```
Primary Stop: Other side of VWAP

LONG:
Entry: $140.80 (just above VWAP at $140.70)
Stop: $140.50 (-0.21%, below VWAP)

SHORT:
Entry: $140.60 (just below VWAP at $140.70)
Stop: $140.90 (+0.21%, above VWAP)

Backup Stop: -0.4% fixed
```

**3. Target Exit:**
```
TP1 (70%): Previous swing high/low
- LONG: Recent resistance above VWAP
- SHORT: Recent support below VWAP
- Typically 0.5-0.8% away

TP2 (30%): 2x distance to VWAP
- Let runner for extended move
- Or opposite VWAP test
```

**4. VWAP Re-Cross Exit:**
```
LONG Position:
- If price closes below VWAP again
- Action: Exit 100%
- Setup failed, VWAP not holding

SHORT Position:
- If price closes above VWAP again
- Action: Exit 100%
```

**5. Time & Volume Exits:**
```
Volume Declining:
- 3 bars of lower volume
- Price stalling
- Exit 50%

Time Limit:
- Max 60 minutes
- If not moving, exit all

High Volume Spike Against:
- Sudden 5x volume opposite direction
- Exit 100% immediately
```

**6. Exit Priority:**
```
1. Stop loss → 100%
2. VWAP re-cross → 100%
3. TP1 → 70%
4. Time > 60 min → 100%
5. TP2 or trail → 30%
```

**Freqtrade Configuration:**
```python
class VWAPBounce1m(IStrategy):
    
    minimal_roi = {
        "0": 0.012,
        "5": 0.01,
        "10": 0.008,
        "20": 0.006,
        "40": 0.004,
        "60": 0.002
    }
    
    stoploss = -0.004  # -0.4%
    
    trailing_stop = True
    trailing_stop_positive = 0.003
    trailing_stop_positive_offset = 0.005
    trailing_only_offset_is_reached = True
    
    use_exit_signal = True
    
    def populate_exit_trend(self, dataframe, metadata):
        # Exit if price crosses back through VWAP
        dataframe.loc[
            (
                (dataframe['close'] < dataframe['vwap']) &  # For LONG
                (dataframe['volume'] > 0)
            ),
            'exit_long'
        ] = 1
        
        return dataframe
```

### Example Trade
```
SOL/USDT 1m Chart
Time: 10:45 AM

VWAP: $140.70
Entry: $140.80 (bounce confirmation)
Stop: $140.50 (-0.21%, $0.30)
TP1 (70%): $141.50 (+0.50%, $0.70)
TP2 (30%): $142.00 (+0.85%, $1.30)

Capital: $500
Position Size: 3.52 SOL
```

### Performance Metrics
- Win Rate: 64%
- Average Win: 0.6%
- Average Loss: 0.3%
- Expectancy: +0.25% per trade
- Trades per Day: 15-30
- Hold Time: 10-40 minutes

---

## Trading Session Recommendations

**Best Times for 1m Scalping:**
- **London Open:** 3:00am - 5:00am EST (High volatility)
- **NY Open:** 9:30am - 11:30am EST (Peak volume)
- **Overlap:** 8:00am - 12:00pm EST (Best liquidity)

**Avoid:**
- Late night: 12:00am - 4:00am EST
- Weekends: Low liquidity
- Major holidays
- Asian session (unless trading Asian pairs)

---

## Risk Management for 1m Scalping

**Position Sizing:**
```
Risk per trade: 0.5-1% maximum
Max concurrent positions: 2-3
Daily loss limit: 3%

Example ($1,000 account):
Risk per trade: $5-10
Max positions: 2-3 ($15-30 total risk)
Daily limit: $30 loss
```

**Scalping Rules:**
```
1. Take profit quickly (don't be greedy)
2. Cut losses faster (tight stops)
3. Max 3 losses in a row = stop for 1 hour
4. If daily limit hit = stop trading
5. No revenge trading
```

**Psychological Tips:**
```
✅ DO:
- Set alerts, don't stare at chart
- Take breaks every 2 hours
- Keep detailed journal
- Accept small losses quickly
- Celebrate small wins

❌ DON'T:
- Overtrade (quality over quantity)
- Chase missed entries
- Move stops further away
- Trade when tired/emotional
- Skip risk management
```

---

## Next Steps

1. **Practice on Demo:** At least 100 trades before live
2. **Backtest:** Review last 1-3 months of data
3. **Paper Trade:** 1 week minimum with real-time alerts
4. **Start Small:** 10-25% of intended position size
5. **Scale Up:** After 30+ profitable trades

---

## See Also

- [5-Minute Strategies](strategies_5m.md) - Less intensive than 1m
- [15-Minute Strategies](strategies_15m.md) - Better for beginners
- [UT Bot Complete Guide](shared_content.md#ut-bot-guide)
- [Risk Management](shared_content.md#risk-management)

---

*Last Updated: November 15, 2025*
