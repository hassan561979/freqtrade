# 5-Minute Trading Strategies
*High Win-Rate Strategies for Scalping & Swing Scalping*

---

## Navigation
- [Back to Main Guide](TRADING_STRATEGIES_GUIDE.md)
- [1-Minute Strategies](strategies_1m.md)
- [15-Minute Strategies](strategies_15m.md)
- [30-Minute Strategies](strategies_30m.md)
- [1-Hour Strategies](strategies_1h.md)
- [Shared Content](shared_content.md) - UT Bot Guide, Risk Management, Implementation Tips

---

## Overview

**Trading Style:** SCALPING / SWING SCALPING  
**Time Commitment:** 4-6 hours/day active monitoring  
**Capital Requirements:** $500-$2,000+  
**Recommended Experience:** Beginner to Advanced

**Key Characteristics:**
- Medium-paced (minutes to hours per trade)
- Balance of frequency and quality
- Multiple signals per day (8-15)
- Profit targets (1.0-2.5% per trade)
- Stop losses (0.5-1.5%)
- Best for trend following and smart money concepts

---

## 5-Minute Strategies

### Strategy 5A: UT Bot + 100 MA (Win Rate: ~72%)
**📊 Category:** SCALPING (Swing Scalping)

**Best For:** Swing scalping, trend following  
**Recommended Pairs:** BTC/USDT, ETH/USDT, BNB/USDT  
**Capital Required:** $1,000+

#### Optimal Market Conditions

**✅ BEST CONDITIONS:**
- **Strong trending markets** (price consistently above/below 100 MA)
- **Clear directional bias** on 15m/30m/1H timeframes
- **Healthy pullbacks** that don't break structure
- Price staying **above 100 MA for uptrends** (below for downtrends)
- **Rising ATR** during trends (momentum building)
- Volume confirming direction (higher on trend moves)

**❌ AVOID:**
- Choppy/ranging markets (price crossing 100 MA frequently)
- When price is flat and 100 MA is horizontal
- During consolidation phases (tight range)
- After extended trends without pullback (exhaustion)
- Low volume grind (weak institutional interest)
- When multiple timeframes are conflicting

**⚠️ WARNING SIGNS:**
- Price repeatedly rejected at 100 MA (trend weakness)
- UT Bot giving opposite signals quickly (whipsaw)
- Volume declining as trend continues
- 100 MA starting to flatten or turn
- ATR contracting (volatility dropping)

**📊 Pre-Trade Checklist:**
1. Is 15m/30m trend aligned with 5m signal?
2. Has price been above/below 100 MA for 2+ hours?
3. Is this a healthy pullback (not breaking structure)?
4. Is there clean space to target (no major resistance nearby)?
5. Is volume supporting the trend direction?

#### Setup
```
Indicators:
- UT Bot (Key Value: 3.5-4.0, ATR Period: 10)
- 100-period Moving Average (EMA/SMA/WMA)
- ATR indicator (for position sizing)
```

#### Entry Rules - LONG
1. Price ABOVE 100 MA (confirms uptrend)
2. UT Bot BUY signal (green dot/label)
3. No recent resistance nearby (<2% away)
4. Enter immediately on signal candle close

#### Entry Rules - SHORT
1. Price BELOW 100 MA (confirms downtrend)
2. UT Bot SELL signal (red dot/label)
3. No recent support nearby (<2% away)
4. Enter immediately on signal candle close

#### Exit Strategy

**Primary Exit Methods:**

**1. ROI (Return on Investment) Table:**
```python
minimal_roi = {
    "0": 0.03,       # 3% immediate (strong move)
    "10": 0.025,     # 2.5% after 10 minutes
    "20": 0.02,      # 2% after 20 minutes
    "30": 0.015,     # 1.5% after 30 minutes
    "60": 0.01,      # 1% after 1 hour
    "120": 0.005     # 0.5% after 2 hours (breakeven+)
}
```
**Why this ROI:** 5m swing scalping targets larger moves. Patient early, then gradual profit taking.

**2. Stop Loss Configuration:**

**Primary Stop - ATR Trailing:**
```python
# Dynamic stop based on volatility
ATR_Period = 14
ATR_Multiplier = 2.0  # Wider for 5m timeframe

Trailing_Stop = Entry_Price - (ATR × 2.0)

Example:
Entry: $67,500
ATR: $200
Initial Stop: $67,500 - ($200 × 2.0) = $67,100 (-0.59%)
```

**Backup Stop - Fixed Percentage:**
- **Hard Stop:** -1.5% (absolute maximum loss)
- **Typical Stop:** -0.8% to -1.2% (depending on ATR)
- **Override:** Use whichever is TIGHTER (ATR or fixed)

**3. Break-Even Strategy:**
```
Trigger: When profit reaches 0.75:1 ratio

Calculation:
Risk: $300 (stop distance)
Breakeven Trigger: $225 profit (0.75 × $300)

Action:
- Move stop to entry price + $10 (cover fees)
- Lock in risk-free trade
- Let rest run to targets
```

**4. Partial Exit Strategy (Multi-Target):**

**Setup A - Conservative (Recommended):**
```
TP1 (50% position): 3:1 risk:reward
- If risk = $300, TP1 = $900 profit
- Entry: $67,500, Stop: $67,200, TP1: $68,400
- Action: Close 50%, move stop to breakeven
- Expected time: 20-60 minutes

TP2 (30% position): 5:1 risk:reward
- TP2 = $1,500 profit
- Entry: $67,500, TP2: $69,000
- Action: Close 30%, trail rest with UT Bot line
- Expected time: 1-3 hours

TP3 (20% position): Let run
- Trail: 0.5% behind price
- Exit: UT Bot opposite signal OR end of day
- Maximum target: 7:1 or higher
```

**Setup B - Aggressive:**
```
TP1 (40%): 2:1 ratio (quick profit)
TP2 (30%): 4:1 ratio
TP3 (20%): 6:1 ratio
TP4 (10%): Trail indefinitely
```

**5. Exit Signal (UT Bot Opposite):**
```
Condition: UT Bot SELL signal (red dot) appears

Actions:
- If in profit >1%: Exit 100% immediately
- If in profit 0.5-1%: Exit 70%, trail 30% tight (0.3%)
- If in profit <0.5%: Exit 50%, hold rest with tight stop
- If at breakeven/loss: Hold unless 100 MA breaks

Priority: HIGH (override ROI if strong signal)
```

**6. 100 MA Exit Rules:**
```
LONG Position:
- Price touches 100 MA from above: Exit 30% (warning)
- Price closes below 100 MA: Exit 70% more (total 100%)
- 100 MA starts flattening: Tighten trail to 0.4%

SHORT Position:
- Price touches 100 MA from below: Exit 30%
- Price closes above 100 MA: Exit 70% more
- 100 MA starts flattening: Tighten trail to 0.4%
```

**7. Time-Based Exit:**
```
Max Trade Duration: 4 hours

Time-Based Actions:
- After 2 hours: Start trailing tighter (0.5% behind)
- After 3 hours: If profit <1%, exit 50%
- After 4 hours: Close remaining position
- Exception: If in strong profit (>2%), extend to 6 hours max
```

**8. Trailing Stop Activation:**
```python
Trailing Configuration:

Activation Point: 0.6% profit
Trailing Distance: 0.4% behind highest point

Example:
Entry: $67,500
Price reaches: $67,905 (0.6% profit) → Trailing activates
Trailing Stop: $67,905 - (0.4%) = $67,633

As price rises:
Price: $68,400 → Stop: $68,126 (locked in +0.93%)
Price: $69,000 → Stop: $68,724 (locked in +1.81%)
```

**9. Volatility-Based Adjustments:**
```
High Volatility (ATR increasing):
- Widen stops by 1.5x
- Take profits earlier (2:1 instead of 3:1)
- Reduce position size on next trade

Low Volatility (ATR decreasing):
- Tighten stops by 0.7x
- Be patient for larger targets (4:1)
- Consider skipping setups (insufficient movement)
```

**10. Emergency Exits:**
```
Immediate Exit Conditions (100% position):
- Sudden volume spike >5x against position
- News event detected (economic calendar)
- Price gaps through stop loss (market order)
- 15m/30m timeframe breaks structure
- Multiple false UT Bot signals in 30 minutes
```

**Exit Priority (Top to Bottom):**
1. Emergency conditions → Exit 100% immediately
2. Hard stop loss (-1.5%) → Exit 100%
3. 100 MA broken against trend → Exit 100%
4. UT Bot opposite signal → Exit per rules above
5. Time limit (4 hours) → Exit per schedule
6. Partial profit targets → Exit per plan
7. ROI table → Automatic profit taking
8. Trailing stop → Lock in gains

**Complete Freqtrade Configuration:**
```python
# Strategy 5A - UT Bot + 100 MA Exit Config

class UTBot100MAStrategy(IStrategy):
    
    minimal_roi = {
        "0": 0.03,
        "10": 0.025,
        "20": 0.02,
        "30": 0.015,
        "60": 0.01,
        "120": 0.005
    }
    
    stoploss = -0.015  # -1.5% hard stop
    
    # Trailing stop configuration
    trailing_stop = True
    trailing_stop_positive = 0.006  # Start trailing at 0.6%
    trailing_stop_positive_offset = 0.008  # Trigger point
    trailing_only_offset_is_reached = True
    
    # Use exit signals from UT Bot
    use_exit_signal = True
    exit_profit_only = False
    exit_profit_offset = 0.0
    
    # Ignore ROI if exit signal appears
    ignore_roi_if_entry_signal = False
    
    # Optional: Partial exits (custom implementation needed)
    # position_adjustment_enable = True
```

**Performance Optimization Tips:**
```
Backtest Adjustments:
1. Test different ATR multipliers (1.5x - 2.5x)
2. Optimize ROI table for your pairs
3. Adjust trailing_stop_positive for volatility
4. Test partial exits vs full exits
5. Compare signal exits vs ROI exits (which performs better)

Live Trading:
1. Start with conservative partial exits (50/30/20)
2. Use tighter stops in choppy markets
3. Be more patient in strong trends (hold to 5:1)
4. Track which exit method works best
5. Adjust based on market conditions
```

#### Example Trade
```
BTC/USDT 5m Chart
Setup: Strong uptrend, price consolidating above 100 MA

Entry: $67,500 (UT Bot buy signal above 100 MA)
Stop Loss: $67,200 (-0.44%, ATR trailing stop)
Break Even: $67,725 (0.75:1, move stop to entry)
TP1 (50%): $68,400 (+1.33%, 3:1 ratio)
TP2 (50%): $69,100 (+2.37%, opposite signal)

Capital: $1,000
Position Size: 0.0148 BTC
Risk: $4.44 (0.44% account)
Reward: $13.32-$23.70
```

#### Performance Metrics
- Win Rate: 72%
- Average Win: 2.1%
- Average Loss: 0.9%
- Expectancy: +1.26% per trade
- Trades per Day: 8-15

---

### Strategy 5B: Order Blocks + Fair Value Gaps (Win Rate: ~68%)
**📊 Category:** SCALPING (Smart Money)

**Best For:** Smart Money Concepts, institutional trading  
**Timeframe:** 5m execution, 15m/30m analysis  
**Capital Required:** $500+

#### Optimal Market Conditions

**✅ BEST CONDITIONS:**
- **After strong impulsive moves** (creates clear FVGs)
- **Clear Break of Structure** on higher timeframes (15m/30m)
- **Trending markets** with defined swing highs/lows
- **High volume breakouts** that leave gaps behind
- Markets showing **institutional behavior** (clean sweeps, decisive moves)
- When price returns to **confluence zones** (OB + FVG overlap)

**❌ AVOID:**
- Slow grinding markets (no clear FVGs form)
- Low volume environments (no institutional footprint)
- Ranging markets with no clear BOS
- When Order Blocks are old (>24 hours)
- Multiple overlapping OBs/FVGs (confusion)
- During major news (price behavior unpredictable)

**⚠️ WARNING SIGNS:**
- Price enters OB/FVG but no reaction (zone invalidated)
- Break of Structure not confirmed with volume
- Price quickly returns through zone (weak hands)
- Multiple false setups in same session
- Conflicting signals across timeframes

**📊 Pre-Trade Checklist:**
1. Is there a clear BOS on 15m/30m timeframe?
2. Has the Order Block been created within last 12 hours?
3. Does FVG overlap with OB (confluence)?
4. Is higher timeframe trend supporting this direction?
5. Has price cleanly entered the zone (no premature entries)?
6. Is volume increasing as price enters zone?

**🔍 MARKET STRUCTURE REQUIREMENTS:**
- **For LONG:** Clear higher highs forming, bullish BOS confirmed
- **For SHORT:** Clear lower lows forming, bearish BOS confirmed
- **Daily/4H bias:** Must align with your trade direction
- **Recent liquidity:** Obvious swing highs/lows swept before move

#### Understanding Core Concepts

**Order Blocks (OB):**
- Zones where institutions placed significant orders
- **Bullish OB**: Last bearish candle before uptrend breakout
- **Bearish OB**: Last bullish candle before downtrend breakdown
- Represents imbalance between buyers/sellers

**Fair Value Gaps (FVG):**
- Price imbalances from aggressive moves
- Three-candle formation: Gap between candle 1 and candle 3 wicks
- Market often returns to "fill" these gaps
- Represents inefficient price discovery

**Break of Structure (BOS):**
- Price breaking recent swing high (bullish) or low (bearish)
- Confirms trend direction change
- Used to validate order block setups

#### Setup Process

**Step 1: Identify Trend (15m/30m chart)**
```
Bullish Trend:
- Series of higher highs (HH) and higher lows (HL)
- BOS: Price breaks above recent swing high

Bearish Trend:
- Series of lower highs (LH) and lower lows (LL)
- BOS: Price breaks below recent swing low
```

**Step 2: Mark Order Blocks (15m chart)**
```
Bullish OB:
- Find last bearish candle before bullish BOS
- Draw box from candle low to candle high
- This is your demand zone

Bearish OB:
- Find last bullish candle before bearish BOS
- Draw box from candle high to candle low
- This is your supply zone
```

**Step 3: Identify Fair Value Gaps (5m chart)**
```
Bullish FVG (imbalanced to upside):
- Candle 1: Bearish or neutral
- Candle 2: Strong bullish move
- Candle 3: Continuation up
- Gap: Candle 1 high < Candle 3 low

Bearish FVG (imbalanced to downside):
- Candle 1: Bullish or neutral
- Candle 2: Strong bearish move
- Candle 3: Continuation down
- Gap: Candle 1 low > Candle 3 high
```

**Step 4: Find Confluence**
- FVG overlaps with Order Block = HIGH probability zone
- Wait for price to retrace into this confluence zone

#### Entry Rules - LONG Example

```
Context:
Daily: Uptrend, price above 200 MA
15m: BOS at $68,000 (breaks previous high)
15m: Bullish OB at $67,200-$67,400 (last red candle)
5m: FVG forms at $67,300-$67,450 during pullback

Entry Setup:
1. Price retraces from $68,000 to $67,350
2. Price enters FVG + OB confluence zone
3. Look for bullish confirmation:
   - Strong buying candle (>70% green body)
   - Volume spike (>1.5x average)
   - Bullish engulfing or pin bar
4. Enter LONG at $67,350 (on confirmation candle close)

Exit:
Stop Loss: $67,150 (-0.30%, below OB low)
TP1 (50%): $67,950 (+0.89%, 1:3 ratio)
TP2 (50%): $68,500 (+1.71%, 1:5.7 ratio)

Position Sizing (for $1000 account, 2% risk):
Risk Amount: $20
Risk per coin: $200
Position Size: 0.1 BTC ($6,735)
```

#### Complete Exit Strategy

**1. ROI (Return on Investment) Table:**
```python
minimal_roi = {
    "0": 0.025,      # 2.5% immediate (strong institutional move)
    "15": 0.02,      # 2% after 15 minutes
    "30": 0.015,     # 1.5% after 30 minutes
    "60": 0.01,      # 1% after 1 hour
    "120": 0.005,    # 0.5% after 2 hours
    "180": 0.003     # 0.3% after 3 hours (minimum acceptable)
}
```
**Rationale:** Smart Money moves are decisive. Big profit potential early, then patience for full move.

**2. Stop Loss Strategy:**

**Zone-Based Stop Loss:**
```
Stop Placement Rules:

LONG:
- Primary: Below Order Block low
- Buffer: -0.1% below OB (avoid wick hunting)
- Backup: Below Fair Value Gap low
- Absolute Max: -0.8% from entry

SHORT:
- Primary: Above Order Block high
- Buffer: +0.1% above OB
- Backup: Above Fair Value Gap high
- Absolute Max: +0.8% from entry

Example (LONG):
OB Low: $67,150
Buffer: $67,150 - ($67,150 × 0.001) = $67,083
Entry: $67,350
Stop: $67,083
Risk: $267 (0.40%)
```

**Stop Loss Adjustment:**
```
Scenario A - Zone Holding:
If price stays in OB/FVG zone for 10+ minutes:
- Tighten stop to entry - 0.2%
- Reason: Taking too long, weak demand

Scenario B - Quick Rejection:
If price drops back into zone within 5 minutes:
- Exit 50% immediately
- Move stop to breakeven on rest
- Reason: Institutions not defending level

Scenario C - Zone Invalidated:
If price breaks through OB/FVG zone downward:
- Exit 100% immediately (market order)
- Reason: Setup failed, structure broken
```

**3. Partial Exit Strategy (Institutional Style):**

**Professional Scaling:**
```
TP1 (40%): 1:3 Risk:Reward
- Target: Recent structure high OR resistance
- Time: 15-45 minutes expected
- Action: Close 40%, move stop to breakeven + fees
- Logic: Lock in quick institutional profit

TP2 (30%): 1:5 Risk:Reward  
- Target: Next major resistance OR FVG from opposite side
- Time: 1-2 hours expected
- Action: Close 30%, trail rest with structure
- Logic: Capture main institutional move

TP3 (20%): 1:7+ Risk:Reward
- Target: Major daily level OR opposite OB
- Time: 2-4 hours expected
- Action: Trail with 15m swing lows, 0.5% distance
- Logic: Catch extended smart money push

TP4 (10%): Runner
- Target: Trail indefinitely
- Exit: 15m BOS against position OR end of session
- Logic: Occasional huge winners (10:1+)
```

**Alternative - Aggressive:**
```
TP1 (50%): 1:2.5 (quick take)
TP2 (30%): 1:4
TP3 (20%): 1:6+
```

**Alternative - Conservative:**
```
TP1 (60%): 1:3 (secure profit)
TP2 (40%): 1:5 (let winners run)
```

**4. Structure-Based Exits:**

**Break of Structure Exit Rules:**
```
LONG Position Exits:

15m BOS Broken (Bearish):
- Exit: 100% immediately
- Reason: Higher timeframe structure failing

New Lower Low Forms:
- Exit: 70% immediately
- Trail: 30% tight (0.3% stop)
- Reason: Trend potentially reversing

5m Creates Bearish OB Above Price:
- Exit: 50%
- Tighten stop on rest to entry
- Reason: Selling pressure building
```

**Fair Value Gap Exits:**
```
If price creates FVG in opposite direction:
- Small FVG (<0.3%): Tighten trail, watch closely
- Medium FVG (0.3-0.5%): Exit 30%, secure profits
- Large FVG (>0.5%): Exit 70%, trend likely reversing
```

**5. Time-Based Management:**

**Optimal Exit Windows:**
```
Minute 0-15: Hold (setup developing)
  - Don't exit early
  - Let institutional orders fill
  - Watch for confirmation

Minute 15-45: Prime profit zone
  - TP1 should hit here
  - Strong trend: hold for TP2
  - Weak momentum: consider scaling out more

Minute 45-120: Extended move
  - TP2 target zone
  - Start trailing aggressively
  - Watch for exhaustion signs

Hour 2-4: Late stage
  - Most trades should be closed
  - If still in: very tight trail (0.3%)
  - Consider taking profits even below TP3

Hour 4+: Force close
  - Max holding period reached
  - Close remaining position
  - Exception: if profit >3%, extend to 6 hours
```

**Session-Based Exits:**
```
London Open (3am EST): Strong moves expected, hold
London/NY Overlap (8am-12pm EST): Peak activity, best exits
NY Afternoon (12pm-4pm EST): Momentum fades, consider closing
Asia Session: Close all positions (low liquidity)
```

**6. Volume-Based Exit Signals:**

**Volume Divergence:**
```
Bullish Divergence (EXIT LONG):
- Price making higher highs
- Volume declining on each push
- Action: Exit 50% immediately, trail rest tight

Volume Climax:
- Sudden volume spike (>5x average)
- Long wicks appearing
- Action: Exit 70%, this might be top

Volume Drying Up:
- 3 consecutive bars with <0.5x average volume
- Price stalling at resistance
- Action: Exit 40%, momentum dying
```

**7. Trailing Stop Configuration:**

**Dynamic Trailing (After TP1 Hit):**
```python
# Structure-Based Trailing

Method 1 - Swing Lows (Recommended):
Trail behind: Most recent 5m swing low (for LONG)
Distance: Swing low - 0.1%
Update: Every time new swing low forms

Example:
Entry: $67,350
Current: $68,200
Last 5m swing low: $67,950
Trailing Stop: $67,882 (locked in +0.79% profit)

Method 2 - Fixed Percentage:
Trailing Distance: 0.5% behind highest point
Activation: After TP1 hit (in profit)
Update: Real-time as new highs made

Method 3 - ATR-Based:
Trailing Distance: 1.5 × ATR behind price
Adaptive to volatility
Wider in volatile markets, tighter in calm markets
```

**8. Confluence Exit Indicators:**

**Multiple Signals = Stronger Exit:**
```
Exit 100% when 3+ signals align:

□ 15m BOS broken
□ New opposite OB formed
□ Volume divergence present  
□ TP2 target reached
□ Time > 2 hours
□ Price at major daily resistance
□ RSI extreme (>75 for LONG)
□ Opposite FVG created

Example:
- TP2 hit ✓
- Time = 90 minutes ✓  
- Volume declining ✓
- Price at daily resistance ✓
→ Exit 100%, don't wait for more
```

**9. Emergency Exit Conditions:**

**Immediate Exit (Market Order):**
```
1. Order Block Breakdown:
   - Price breaks back through OB zone
   - Close 100% immediately
   - Setup invalidated

2. News Event:
   - Unexpected major news
   - High impact economic data
   - Exit before volatility spike

3. Liquidity Sweep:
   - Price spikes through stop, then reverses
   - Suggests stop hunt
   - Re-evaluate, don't re-enter immediately

4. Market Structure Chaos:
   - Multiple timeframes conflicting
   - Erratic price action
   - No clear structure
   - Exit and wait for clarity
```

**10. Exit Priority Hierarchy:**

```
Level 1 - IMMEDIATE EXITS (No hesitation):
1. Stop loss hit
2. Order Block broken through
3. 15m BOS invalidated
4. News event detected

Level 2 - HIGH PRIORITY:
5. Volume climax against position
6. Opposite institutional pattern forming
7. Time limit exceeded (4 hours)
8. Multiple bearish signals (3+)

Level 3 - STANDARD EXITS:
9. TP1/TP2/TP3 targets hit
10. ROI table activated
11. Structure-based trail hit
12. Session ending (close before Asia)

Level 4 - DISCRETIONARY:
13. Profit looks good, secure it
14. Market feels choppy
15. Tired of monitoring
```

**Freqtrade Configuration:**
```python
class OrderBlockFVGStrategy(IStrategy):
    
    minimal_roi = {
        "0": 0.025,
        "15": 0.02,
        "30": 0.015,
        "60": 0.01,
        "120": 0.005,
        "180": 0.003
    }
    
    stoploss = -0.008  # -0.8% maximum
    
    trailing_stop = True
    trailing_stop_positive = 0.008  # Start trailing at 0.8%
    trailing_stop_positive_offset = 0.012  # Activate at 1.2%
    trailing_only_offset_is_reached = True
    
    use_exit_signal = True
    exit_profit_only = False
    
    # Custom exit logic for OB/FVG validation
    def custom_exit(self, pair, trade, current_time, current_rate, **kwargs):
        # Check if OB zone is broken
        # Check if opposite structure forming  
        # Check volume divergence
        # Return True to exit
        pass
```

**Exit Strategy Summary Table:**

| Exit Method | Priority | Timing | Action |
|-------------|----------|--------|--------|
| Stop Loss | HIGHEST | Immediate | 100% exit |
| OB Broken | HIGHEST | Immediate | 100% exit |
| TP1 (1:3) | HIGH | 15-45 min | Close 40% |
| TP2 (1:5) | MEDIUM | 1-2 hours | Close 30% |
| Structure Trail | MEDIUM | Ongoing | Close rest |
| ROI Table | LOW | Time-based | Gradual |
| Time Limit | MEDIUM | 4 hours | Force close |
| Session End | MEDIUM | Asia open | Close all |
```

#### Entry Rules - SHORT Example

```
Context:
Daily: Downtrend, price below 200 MA
15m: BOS at $66,000 (breaks previous low)
15m: Bearish OB at $66,800-$67,000 (last green candle)
5m: FVG forms at $66,700-$66,900 during rally

Entry Setup:
1. Price rallies from $66,000 to $66,850
2. Price enters FVG + OB confluence zone
3. Look for bearish confirmation:
   - Strong selling candle (<30% body from high)
   - Volume spike (>1.5x average)
   - Bearish engulfing or shooting star
4. Enter SHORT at $66,850 (on confirmation candle close)

Exit:
Stop Loss: $67,050 (+0.30%, above OB high)
TP1 (50%): $66,250 (-0.90%, 1:3 ratio)
TP2 (50%): $65,850 (-1.50%, 1:5 ratio)
```

#### Visual Pattern Recognition

```
Bullish Setup (LONG):

Price Action:
    ↑ BOS (Break high)
   ⎡ ⎤  Rally
   ⎢ ⎥
   ⎣ ⎦  Pullback to:
  ╔═══╗  ← FVG (imbalanced area)
  ║OB ║  ← Order Block (last red candle)
  ╚═══╝
    ↑ Entry here (on confirmation)
    
Timeline:
15m: ---- BOS ---- Pullback starts ----
5m:  ---- FVG forms ---- Price enters zone ---- Confirmation ---- ENTER


Bearish Setup (SHORT):

Price Action:
   ⎡ ⎤  Rally into:
   ⎢ ⎥
   ⎣ ⎦
  ╔═══╗  ← Order Block (last green candle)
  ║OB ║  ← FVG (imbalanced area)
  ╚═══╝
    ↓ Entry here (on confirmation)
    ↓ BOS (Break low)
```

#### Key Rules for Success

**DO:**
- ✅ Wait for clear BOS on higher timeframe
- ✅ Only trade when FVG + OB overlap
- ✅ Require strong confirmation candle
- ✅ Use proper risk management (1-2% per trade)
- ✅ Mark all levels before price arrives

**DON'T:**
- ❌ Trade against higher timeframe trend
- ❌ Enter without confirmation
- ❌ Trade old order blocks (>24 hours)
- ❌ Ignore volume confirmation
- ❌ Chase price after it leaves the zone

#### Performance Metrics
- Win Rate: 68%
- Average Win: 1.8%
- Average Loss: 0.6%
- Expectancy: +0.82% per trade
- Trades per Day: 3-6

---

### Strategy 5C: Triple Confirmation System (Win Rate: ~75%)
**📊 Category:** SCALPING (Conservative)

**Best For:** Conservative traders, high accuracy  
**Timeframe:** 5m

#### Optimal Market Conditions

**✅ BEST CONDITIONS:**
- **Clear trending markets** (all 3 indicators align easily)
- **Momentum-driven moves** (not choppy)
- **Active trading sessions** with good volume
- When higher timeframes (15m/30m) show **same direction**
- After **brief consolidation** before trend continuation
- Markets with **clear directional bias**

**❌ AVOID:**
- Ranging/sideways markets (indicators conflict constantly)
- Low volume periods (weak signals)
- When indicators keep flipping (no consensus)
- During consolidation phases (false signals)
- Right after trend exhaustion (late entries)
- When 2 indicators agree but 1 conflicts (wait for all 3)

**⚠️ WARNING SIGNS:**
- One indicator turning before the other two
- Signals align but volume is weak
- Previous signal failed recently (market indecision)
- Indicators showing divergence from price

**📊 Pre-Trade Checklist:**
1. All 3 indicators aligned (UT Bot + Trend A-V2 + QQE MOD)?
2. Is 15m timeframe confirming this direction?
3. Is there adequate volume supporting the move?
4. Are you entering early in the trend (not late)?
5. No conflicting signals on nearby timeframes?

**🎯 SIGNAL QUALITY:**
- **A-Grade:** All 3 align immediately after pullback in strong trend
- **B-Grade:** All 3 align but after extended move
- **C-Grade:** Indicators barely aligned or weak trend
- **Skip:** Any conflict between indicators

#### Setup
```
Indicators:
- UT Bot (Key Value: 3.5)
- Trend Indicator A-V2
- QQE MOD (by Mihkel00)
```

#### Entry Rules - LONG (All 3 Must Align)
1. UT Bot issues BUY signal (green dot)
2. Trend Indicator A-V2 is GREEN
3. QQE MOD histogram is BLUE
4. Enter on signal candle close

#### Entry Rules - SHORT (All 3 Must Align)
1. UT Bot issues SELL signal (red dot)
2. Trend Indicator A-V2 is RED
3. QQE MOD histogram is RED
4. Enter on signal candle close

#### Exit Strategy

**Primary Exit Methods:**

**1. ROI (Return on Investment) Table:**
```python
minimal_roi = {
    "0": 0.02,       # 2% immediate (all 3 indicators aligned)
    "10": 0.015,     # 1.5% after 10 minutes
    "20": 0.012,     # 1.2% after 20 minutes
    "40": 0.01,      # 1% after 40 minutes
    "80": 0.006,     # 0.6% after 1hr 20min
    "120": 0.003     # 0.3% after 2 hours (minimal acceptable)
}
```
**Rationale:** Triple confirmation = high probability. More patient than single indicator strategies.

**2. Stop Loss Strategy:**

**Primary Stop - UT Bot Trailing Stop Line:**
```
Stop Type: Dynamic (follows UT Bot white line)

LONG Position:
- Stop: UT Bot trailing stop line (below price)
- Buffer: -0.1% below line (avoid wicks)
- Typical Distance: 0.4-0.7% from entry

SHORT Position:
- Stop: UT Bot trailing stop line (above price)
- Buffer: +0.1% above line
- Typical Distance: 0.4-0.7% from entry

Advantage: Adapts to volatility automatically
```

**Backup Stop - Fixed Percentage:**
```
Hard Stop: -0.8% from entry

When to Use:
- If UT Bot line too far (>1% away)
- During high volatility (protection)
- Technical glitch with indicator

Rule: Use whichever is TIGHTER
```

**Break-Even Rules:**
```
Trigger: When profit reaches 0.6%

Action:
1. Move stop to entry + $5 (cover fees)
2. Now risk-free trade
3. Let ROI/signals handle the rest

Example:
Entry: $140.50
Profit: $140.50 × 0.006 = $0.843 (+0.6%)
Price: $141.34
Action: Move stop to $140.55
```

**3. Signal-Based Exits:**

**Triple Indicator Exit Signals:**
```
Exit Trigger: When ANY indicator flips

Scenario A - One Indicator Flips:
- Action: Exit 40% immediately
- Move stop to breakeven on rest
- Watch if others follow

Scenario B - Two Indicators Flip:
- Action: Exit 80% immediately  
- Trail rest very tight (0.2%)
- Likely full reversal coming

Scenario C - All Three Flip:
- Action: Exit 100% immediately
- No hesitation
- Full signal reversal confirmed

Priority Order:
1. UT Bot flip = Highest priority (exit 40%)
2. Trend Indicator A-V2 flip = High priority (exit 40% more)
3. QQE MOD flip = Medium priority (exit 20% more)
```

**Individual Indicator Exit Rules:**
```
UT Bot:
- LONG: Red dot appears → Exit 40-50%
- SHORT: Green dot appears → Exit 40-50%

Trend Indicator A-V2:
- LONG: Turns RED → Exit 30-40%
- SHORT: Turns GREEN → Exit 30-40%

QQE MOD:
- LONG: Histogram turns RED → Exit 20-30%
- SHORT: Histogram turns BLUE → Exit 20-30%

Complete Reversal (All 3 Opposite):
- Exit: 100% immediately
- Time: Within 30 seconds of third signal
```

**4. Partial Exit Strategy:**

**Conservative Approach (Recommended):**
```
TP1 (50% position): 2:1 Risk:Reward
- Calculate: Risk × 2 = Reward
- Time: 15-40 minutes expected
- Action: Close 50%, move stop to breakeven
- Example: Risk $7 → TP1 at $14 profit (1%)

TP2 (30% position): 3:1 Risk:Reward
- Calculate: Risk × 3 = Reward
- Time: 40-90 minutes expected
- Action: Close 30%, trail rest with UT Bot line
- Example: Risk $7 → TP2 at $21 profit (1.5%)

TP3 (20% position): Let it run
- Trail: UT Bot line OR fixed 0.5% behind
- Exit: Any indicator flips OR end of day
- Potential: 4:1 to 6:1 or more
```

**Aggressive Approach:**
```
TP1 (40%): 1.5:1 (quick take)
TP2 (30%): 2.5:1
TP3 (20%): 4:1
TP4 (10%): Trail indefinitely
```

**Ultra-Conservative:**
```
TP1 (60%): 2:1 (secure majority)
TP2 (40%): 3:1+ (let rest run)
```

**5. Time-Based Management:**

**Time-Based Actions:**
```
0-20 minutes: HOLD
- Setup developing
- Be patient
- Don't exit early

20-60 minutes: PRIME ZONE
- TP1 should hit here
- Strong trend: hold for TP2
- Weak signals: consider scaling out

60-120 minutes: EXTENDED
- TP2 target zone
- Start watching for indicator flips
- Tighten trailing stop

2-3 hours: LATE STAGE
- Most should be closed
- If still in: very tight trail (0.3%)
- One indicator flip = exit all

3+ hours: FORCE EXIT
- Close remaining position
- Don't hold overnight on 5m trades
- Exception: if profit >2.5%, extend to 4 hours
```

**6. Indicator Strength Analysis:**

**Strong vs Weak Signals:**
```
Strong Signal (Hold Longer):
□ All 3 indicators aligned cleanly
□ UT Bot line steeply angled
□ Trend A-V2 solid color (not flickering)
□ QQE MOD histogram expanding
□ Volume supporting direction
→ Target: 3:1 or higher

Weak Signal (Exit Faster):
□ Indicators barely aligned
□ UT Bot line flat
□ Trend A-V2 flickering
□ QQE MOD histogram shrinking  
□ Low volume
→ Target: 1.5:1 to 2:1, exit early
```

**7. Trailing Stop Configuration:**

**Method 1 - UT Bot Line (Default):**
```python
# Follow UT Bot trailing stop line

LONG:
Trailing_Stop = UT_Bot_Line - (UT_Bot_Line × 0.001)
Update: Every candle close

Example:
Entry: $140.50
Current Price: $142.10 (+1.14%)
UT Bot Line: $141.20
Trailing Stop: $141.06 (locked in +0.40%)

Advantage: Moves with volatility
Disadvantage: Can be wide in volatile markets
```

**Method 2 - Fixed Percentage (After TP1):**
```python
Activation: After TP1 hit (in profit)
Distance: 0.5% behind highest point

Example:
Entry: $140.50
TP1 hit at: $141.90 (closed 50%)
Current high: $142.50
Trailing Stop: $141.79 (locked in +0.92%)

Advantage: Predictable, not too tight
```

**Method 3 - Hybrid (Best of Both):**
```
Use wider of:
- UT Bot line - 0.1%
- Fixed 0.5% behind high

Example:
UT Bot Stop: $141.06
Fixed Stop: $141.79
Actual Stop: $141.79 (wider = safer)
```

**8. Exit Priority Hierarchy:**

```
Level 1 - IMMEDIATE (No questions):
1. Stop loss hit → 100% exit
2. All 3 indicators flip → 100% exit
3. UT Bot line broken by price → 70% exit

Level 2 - HIGH PRIORITY:
4. 2 indicators flip → 80% exit
5. Time limit (3 hours) → Close all remaining
6. TP2 hit + 1 indicator flip → 100% exit

Level 3 - STANDARD:
7. TP1 hit → 50% exit per plan
8. TP2 hit → 30% exit per plan
9. ROI table → Automatic
10. One indicator flip → 40% exit

Level 4 - TRAILING:
11. UT Bot trailing stop
12. Fixed percentage trail  
13. End of trading session
```

**9. Emergency Exits:**

**Immediate Action Required:**
```
1. Indicator Glitch:
   - All indicators show conflicting data
   - Action: Exit 100%, something's wrong

2. Extreme Volatility:
   - Candles >1.5% range appearing
   - Action: Exit 70%, protect capital

3. News Event:
   - Unexpected major news
   - Action: Exit 100% before spike

4. Multiple False Signals:
   - 3+ flip-flops in 30 minutes
   - Action: Exit all, market too choppy
   - Wait for clearer conditions
```

**10. Performance Tracking:**

**Track Which Exit Method Works Best:**
```
Exit Reason Log:

Signal Exits:
- UT Bot flip: Win rate ___%, Avg profit ___
- All 3 flip: Win rate ___%, Avg profit ___

ROI Exits:
- TP1 (2:1): Hit rate ___%, Avg profit ___
- TP2 (3:1): Hit rate ___%, Avg profit ___

Trailing Stops:
- UT Bot trail: Win rate ___%, Avg profit ___
- Fixed trail: Win rate ___%, Avg profit ___

Time Exits:
- 2 hour max: Frequency ___%, Avg profit ___

Adjust Strategy Based on Results:
- If ROI exits perform best → Be more patient
- If signal exits perform best → Exit on first flip
- If trailing stops work well → Hold longer
```

**Complete Freqtrade Configuration:**
```python
class TripleConfirmationStrategy(IStrategy):
    
    # ROI table
    minimal_roi = {
        "0": 0.02,
        "10": 0.015,
        "20": 0.012,
        "40": 0.01,
        "80": 0.006,
        "120": 0.003
    }
    
    # Stop loss
    stoploss = -0.008  # -0.8% hard stop
    
    # Trailing stop
    trailing_stop = True
    trailing_stop_positive = 0.006  # Start at 0.6% profit
    trailing_stop_positive_offset = 0.008  # Activate at 0.8%
    trailing_only_offset_is_reached = True
    
    # Exit signals
    use_exit_signal = True
    exit_profit_only = False
    
    def populate_exit_trend(self, dataframe, metadata):
        dataframe.loc[
            (
                # Any indicator flips opposite
                (dataframe['ut_bot_signal'] == 'sell') |  # UT Bot
                (dataframe['trend_av2'] == 'red') |        # Trend A-V2
                (dataframe['qqe_mod'] == 'red')            # QQE MOD
            ),
            'exit_long'
        ] = 1
        
        return dataframe
    
    def custom_exit(self, pair, trade, current_time, current_rate, **kwargs):
        # Partial exits based on R:R
        profit_ratio = trade.calc_profit_ratio(current_rate)
        
        # Check risk:reward ratios
        risk = abs(trade.stop_loss_pct)
        
        # TP1: 2:1
        if profit_ratio >= (risk * 2):
            return 0.5  # Exit 50%
        
        # TP2: 3:1
        if profit_ratio >= (risk * 3):
            return 0.3  # Exit additional 30%
        
        return None
```

**Exit Strategy Quick Reference:**

| Condition | Action | % Exit |
|-----------|--------|--------|
| Stop loss hit | Exit immediately | 100% |
| All 3 indicators flip | Exit immediately | 100% |
| TP1 (2:1) reached | Take profit | 50% |
| TP2 (3:1) reached | Take profit | 30% |
| 2 indicators flip | Exit mostly | 80% |
| 1 indicator flips | Partial exit | 40% |
| 3 hours elapsed | Force close | 100% |
| UT Bot trail hit | Exit remaining | Rest |

#### Example Trade
```
SOL/USDT 5m Chart

Entry: $140.50
- UT Bot: BUY signal ✓
- Trend A-V2: GREEN ✓
- QQE MOD: BLUE histogram ✓

Stop Loss: $139.80 (-0.50%)
Target: $141.90 (+1.00%, 2:1 ratio)

Capital: $1,000
Risk: $5.00 (0.5%)
Reward: $10.00
```

#### Performance Metrics
- Win Rate: 75%
- Average Win: 1.5%
- Average Loss: 0.6%
- Expectancy: +0.68% per trade
- Trades per Day: 4-8

---



---

## See Also

- [1-Minute Strategies](strategies_1m.md) - Faster scalping
- [15-Minute Strategies](strategies_15m.md) - Day trading approach
- [UT Bot Complete Guide](shared_content.md#ut-bot-guide)
- [Risk Management](shared_content.md#risk-management)

---

*Last Updated: November 16, 2025*
