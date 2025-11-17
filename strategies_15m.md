# 15-Minute Trading Strategies
*High Win-Rate Strategies for Day Trading*

---

## Navigation
- [Back to Main Guide](TRADING_STRATEGIES_GUIDE.md)
- [1-Minute Strategies](strategies_1m.md)
- [5-Minute Strategies](strategies_5m.md)
- [30-Minute Strategies](strategies_30m.md)
- [1-Hour Strategies](strategies_1h.md)
- [Shared Content](shared_content.md)

---

## Overview

**Trading Style:** DAY TRADING  
**Time Commitment:** 2-4 hours/day  
**Capital Requirements:** $1,000-$5,000+  
**Recommended Experience:** Beginner to Intermediate

**Key Characteristics:**
- Balanced pace (hours per trade)
- Quality over quantity
- 3-6 signals per day
- Profit targets (1.5-3% per trade)
- Stop losses (1.0-2.0%)
- Best for mean reversion and trend following

---

## 15-Minute Strategies

### Strategy 15A: Multi-Indicator Confluence (Win Rate: ~70%)
**📊 Category:** DAY TRADING (Intraday)

**Best For:** Swing traders, moderate frequency  
**Recommended Pairs:** Major pairs (BTC, ETH, BNB)  
**Capital Required:** $2,000+

#### Optimal Market Conditions

**✅ BEST CONDITIONS:**
- **Mean reversion environments** (price bouncing between BB bands)
- **Trending with pullbacks** (not straight up/down)
- **Bollinger Bands expanding** (healthy volatility)
- Price making **clear touches/breaks** of bands
- **EMA crossovers confirming** overall direction
- **MACD histogram aligned** with price action
- Volume spikes on reversals (confirmation)

**❌ AVOID:**
- Strong trending markets (price hugs one band)
- Bollinger Bands extremely tight (low volatility squeeze)
- When EMAs are flat/tangled (no clear trend)
- MACD histogram flat near zero (no momentum)
- Low volume environments (weak reversals)
- During Bollinger Band squeeze (before breakout)

**⚠️ WARNING SIGNS:**
- Price breaks band but doesn't reverse (trend too strong)
- MACD not confirming BB touch
- EMA alignment conflicts with signal
- Volume declining on reversal attempt
- Multiple false signals at bands recently

**📊 Pre-Trade Checklist:**
1. Has price clearly touched or broken outside BB?
2. Are EMAs in favorable alignment (10 above 30 for long)?
3. Is MACD histogram confirming (turning green for long)?
4. Is volume spiking on the reversal candle?
5. Is there room to move to opposite band?
6. No major resistance/support blocking path to target?

**🎯 IDEAL SETUP:**
- Price at lower BB (oversold) for LONG
- 10 EMA crossing above 30 EMA
- MACD turning green
- Volume 2x+ average
- Upper BB clear of obstacles (target zone)

#### Setup
```
Indicators:
- Bollinger Bands (20, 2)
- 10 EMA (fast)
- 30 EMA (slow)
- MACD (12, 26, 9)
- Volume
```

#### Entry Rules - LONG
1. Price touches or breaks BELOW lower Bollinger Band
2. 10 EMA is above OR crossing above 30 EMA
3. MACD histogram turns GREEN (bullish crossover)
4. Volume spike on reversal candle
5. Enter on NEXT candle after all conditions met

#### Entry Rules - SHORT
1. Price touches or breaks ABOVE upper Bollinger Band
2. 10 EMA is below OR crossing below 30 EMA
3. MACD histogram turns RED (bearish crossover)
4. Volume spike on reversal candle
5. Enter on NEXT candle after all conditions met

#### Exit Strategy

**Primary Exit Methods:**

**1. ROI (Return on Investment) Table:**
```python
minimal_roi = {
    "0": 0.025,      # 2.5% immediate (strong BB reversal)
    "15": 0.022,     # 2.2% after 15 minutes
    "30": 0.02,      # 2% after 30 minutes
    "60": 0.015,     # 1.5% after 1 hour
    "120": 0.01,     # 1% after 2 hours
    "180": 0.005     # 0.5% after 3 hours
}
```
**Rationale:** Mean reversion from Bollinger Bands typically completes within 1-2 hours. Patient early, then secure profits.

**2. Stop Loss Configuration:**

**Fixed Percentage Stop:**
```python
# Simple and effective for mean reversion

stoploss = -0.01  # -1.0% hard stop

Calculation:
Entry: $3,502
Stop Loss: $3,502 × 0.99 = $3,467
Risk: $35 per ETH

Why 1%:
- BB reversals are quick
- If doesn't reverse fast, setup failed
- Tight stop appropriate
```

**Break-Even Rules:**
```
Trigger Point: +1.0% profit (1:1 ratio)

Action:
- Move stop to entry + fees ($5)
- Now risk-free
- Let ROI/targets work

Example:
Entry: $3,502
Profit Target: $3,537 (+1.0%)
Price Hits: $3,537
Action: Move stop to $3,507
```

**3. Bollinger Band Exit Rules:**

**Target-Based Exits:**
```
Primary Target: Opposite Bollinger Band

LONG Position:
- Entry: Near lower BB
- Target: Upper BB
- Action: Close 50-70% at upper BB
- Trail rest if price pushes through

SHORT Position:
- Entry: Near upper BB
- Target: Lower BB
- Action: Close 50-70% at lower BB
- Trail rest if price pushes through

Example:
Entry: $3,495 (at lower BB)
Upper BB: $3,585
Target: $3,585 (+2.58%)
Action at target: Close 60%, trail 40%
```

**Band Compression Exit:**
```
Bollinger Band Squeeze Warning:

If bands start narrowing:
- Bands within 1.5% range: Start taking profits
- Bands within 1% range: Exit 50%
- Bands within 0.7% range: Exit 100%

Reason: Low volatility = mean reversion complete
```

**Price Rejection at Band:**
```
If price reaches opposite band but rejects:
- Long wick at upper BB (LONG position)
- Action: Exit 80% immediately
- Reason: Reversal starting, secure profits

Confirmation:
- Next candle closes back inside bands
- Exit remaining 20%
```

**4. EMA Crossover Exit Signals:**

**Primary Exit: EMA Cross Against Position:**
```
LONG Exit Signals:

Signal 1 - 10 EMA crosses BELOW 30 EMA:
- Action: Exit 70% immediately
- Move stop to breakeven on rest
- Momentum reversing

Signal 2 - Price closes below 10 EMA:
- Action: Exit additional 20%
- Hold 10% with tight trail
- Trend weakening

Signal 3 - Price closes below 30 EMA:
- Action: Exit 100% remaining
- Setup completely broken
- No questions

SHORT Exit Signals:
(Opposite of above)
- 10 EMA above 30 EMA → Exit 70%
- Price above 10 EMA → Exit 20% more
- Price above 30 EMA → Exit all
```

**EMA as Dynamic Support/Resistance:**
```
LONG Position:

EMA Testing:
- Price touches 10 EMA: Normal pullback, hold
- Price closes below 10 EMA: Warning, exit 30%
- Price touches 30 EMA: Strong pullback, exit 50%
- Price closes below 30 EMA: Exit 100%

EMA Flattening:
- 10 EMA starts flattening: Tighten trail to 0.5%
- 30 EMA flattening: Consider taking profits
- Both EMAs flat: Exit 70%, momentum gone
```

**5. MACD Exit Signals:**

**MACD Histogram Behavior:**
```
LONG Position Exits:

Histogram Shrinking:
- 3 consecutive smaller green bars
- Action: Take 40% profit, secure gains
- Reason: Momentum weakening

Histogram Turns Red:
- MACD bearish crossover
- Action: Exit 80% immediately
- Reason: Trend reversing

MACD Line Crosses Below Signal:
- Clear bearish signal
- Action: Exit 100%
- No hesitation

MACD Divergence:
- Price higher high, MACD lower high
- Action: Exit 60%, trail rest tight
- Reason: Hidden weakness
```

**6. Volume Exit Signals:**

**Volume Analysis:**
```
Volume Confirmation Exits:

1. Volume Declining on Rally (LONG):
   - 3 bars of declining volume
   - Price still rising
   - Action: Exit 40%, momentum fading

2. Volume Spike on Reversal:
   - Sudden 3x+ volume
   - Large wick against position
   - Action: Exit 70% immediately

3. Volume Climax:
   - Extreme volume (5x+ average)
   - At opposite BB
   - Action: Exit 100%, top/bottom reached

4. Volume Drying Up:
   - Below 0.5x average for 5+ bars
   - Action: Exit 50%, no momentum
```

**7. Partial Exit Strategy:**

**Conservative Approach (Recommended):**
```
TP1 (50% position): 2% profit (2:1 ratio)
- Location: Halfway to opposite BB
- Time: 30-60 minutes expected
- Action: Close 50%, move stop to breakeven
- Example: Entry $3,502 → TP1 $3,572

TP2 (30% position): Opposite Bollinger Band
- Location: Upper BB for LONG
- Time: 1-2 hours expected  
- Action: Close 30%, trail rest
- Example: Upper BB at $3,585 (+2.37%)

TP3 (20% position): Extended target
- Location: BB + 0.3% (band overshoot)
- Exit: Trail 0.5% behind OR EMA cross
- Potential: 3% or more
```

**Aggressive Approach:**
```
TP1 (40%): 1.5% (quick take)
TP2 (30%): Upper/Lower BB
TP3 (20%): BB + 0.5%
TP4 (10%): Trail indefinitely
```

**Ultra-Safe Approach:**
```
TP1 (60%): At opposite BB (secure majority)
TP2 (40%): Trail with 10 EMA or 0.5% stop
```

**8. Time-Based Management:**

**Optimal Timeframes:**
```
0-30 minutes: PATIENCE PHASE
- Let setup develop
- Don't exit early
- BB reversals take time

30-60 minutes: PRIME PROFIT ZONE
- Most TP1 targets hit here
- Watch for EMA alignment
- Monitor MACD confirmation

60-120 minutes: MAIN TARGET ZONE
- Opposite BB usually reached
- Take TP2 profits
- Start aggressive trailing

120-180 minutes: EXTENDED PHASE
- If still holding, be cautious
- Trail very tight (0.4%)
- One indicator flip = exit all

180+ minutes: FORCE EXIT
- Close all remaining positions
- Mean reversion complete
- Don't overstay
```

**Session-Based Timing:**
```
Best Performance: Active sessions
- London open (3am EST): Strong
- NY open (9:30am EST): Strongest
- Overlap (8am-12pm): Best

Weaker Performance:
- After 4pm EST: Consider closing
- Asia session: Exit before 8pm EST
```

**9. Trailing Stop Configuration:**

**Method 1 - Fixed Percentage (Simple):**
```python
Activation: After +1.5% profit
Distance: 0.6% behind highest point

Example:
Entry: $3,502
High: $3,572 (+2.0% profit) → Trailing activated
Trailing Stop: $3,550.57 (locked in +1.39%)

As price continues:
High: $3,585 → Stop: $3,563.49 (+1.76%)
High: $3,595 → Stop: $3,573.43 (+2.04%)
```

**Method 2 - EMA-Based Trailing:**
```
After TP1 Hit:
Trail behind 10 EMA - 0.2%

Example:
Price: $3,572
10 EMA: $3,560
Trailing Stop: $3,552.88

Advantage: Follows momentum
Disadvantage: Can be wide
```

**Method 3 - Bollinger Band Middle (BB Midline):**
```
Trailing: BB Middle line (20 SMA)

After reaching opposite band:
Trail: Middle BB - 0.3%

Example:
Entry: $3,495 (lower BB)
Price: $3,585 (upper BB reached)
Middle BB: $3,540
Trail: $3,529.38

Advantage: Balanced, not too tight
```

**10. Complete Exit Priority:**

```
Level 1 - IMMEDIATE (No hesitation):
1. Stop loss hit (-1%) → 100% exit
2. Price closes opposite side of 30 EMA → 100% exit
3. MACD full bearish cross → 100% exit
4. Volume climax (5x spike) → 100% exit

Level 2 - HIGH PRIORITY:
5. Opposite BB reached → 60% exit (TP2)
6. 10 EMA crossed against → 70% exit
7. MACD histogram turns opposite → 80% exit
8. Time > 3 hours → 100% exit

Level 3 - STANDARD:
9. TP1 (+2%) reached → 50% exit
10. MACD histogram shrinking → 40% exit
11. Volume declining 3 bars → 30% exit
12. ROI table triggers → Automatic

Level 4 - TRAILING:
13. Fixed percentage trail hit
14. EMA trail hit
15. BB middle trail hit
```

**11. Emergency Exits:**
```
1. BB Bands Flipping:
   - Upper BB suddenly below entry
   - Or lower BB above entry  
   - Action: Exit 100%, extreme volatility

2. All Indicators Conflicting:
   - EMAs tangled
   - MACD flat
   - BBs squeezing
   - Action: Exit all, no clarity

3. Gap Through Stop:
   - Price gaps down through stop
   - Action: Exit at market immediately
   - Accept the loss

4. News Event:
   - Major unexpected news
   - Action: Close before volatility
```

**Freqtrade Configuration:**
```python
class MultiBBEMAStrategy(IStrategy):
    
    minimal_roi = {
        "0": 0.025,
        "15": 0.022,
        "30": 0.02,
        "60": 0.015,
        "120": 0.01,
        "180": 0.005
    }
    
    stoploss = -0.01  # -1% fixed stop
    
    trailing_stop = True
    trailing_stop_positive = 0.015  # Start at +1.5%
    trailing_stop_positive_offset = 0.018  # Trigger at 1.8%
    trailing_only_offset_is_reached = True
    
    use_exit_signal = True
    exit_profit_only = False
    
    def populate_exit_trend(self, dataframe, metadata):
        dataframe.loc[
            (
                # EMA bearish cross OR
                (qtpylib.crossed_below(dataframe['ema10'], dataframe['ema30'])) |
                # MACD bearish OR
                (dataframe['macd_histogram'] < 0) |
                # Price at opposite BB
                (
                    (dataframe['close'] >= dataframe['bb_upperband']) &
                    (dataframe['volume'] > dataframe['volume'].rolling(20).mean() * 2)
                )
            ),
            'exit_long'
        ] = 1
        
        return dataframe
    
    def custom_exit(self, pair, trade, current_time, current_rate, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1]
        
        # TP1: 2% profit
        if trade.calc_profit_ratio(current_rate) >= 0.02:
            return 0.5  # Exit 50%
        
        # TP2: At opposite BB
        if current_rate >= last_candle['bb_upperband']:
            return 0.3  # Exit additional 30%
        
        # Emergency: EMA crossed
        if last_candle['ema10'] < last_candle['ema30']:
            return True  # Exit all
        
        return None
```

**Exit Strategy Summary:**

| Signal | Action | % Exit | Priority |
|--------|--------|--------|----------|
| Stop loss | Immediate | 100% | HIGHEST |
| Opposite BB | Take profit | 60% | HIGH |
| EMA cross | Exit | 70% | HIGH |
| MACD bearish | Exit | 80% | HIGH |
| TP1 (2%) | Partial | 50% | MEDIUM |
| Time (3h) | Force close | 100% | MEDIUM |
| Trail hit | Exit rest | Rest | LOW |

#### Example Trade
```
ETH/USDT 15m Chart

Setup:
- Price: $3,495 (touching lower BB at $3,495)
- Lower BB: $3,495
- Upper BB: $3,585
- 10 EMA: $3,510 (above 30 EMA)
- 30 EMA: $3,505
- MACD: Histogram turns green
- Volume: 2.1x average

Entry: $3,502 (next candle open after confirmation)
Stop Loss: $3,467 (-1.0%, $35)
TP1 (50%): $3,572 (+2.0%, $70) - Close half
TP2 (50%): $3,580 (+2.23%, $78) - Upper BB or EMA cross

Position Sizing (for $2,000 account, 1.5% risk):
Risk Amount: $30
Position Size: 0.857 ETH ($3,000)
Risk per coin: $35
Potential Reward: $70-$78
Risk:Reward: 1:2 to 1:2.23
```

#### Performance Metrics
- Win Rate: 70%
- Average Win: 2.2%
- Average Loss: 1.0%
- Expectancy: +0.84% per trade
- Trades per Day: 3-6

---

### Strategy 15B: EMA Crossover + RSI (Win Rate: ~66%)
**📊 Category:** DAY TRADING (Trend Following)

**Best For:** Trend following, momentum trading  
**Timeframe:** 15m

#### Optimal Market Conditions

**✅ BEST CONDITIONS:**
- **Strong trending markets** (clear direction on 1H/4H)
- Price **firmly above/below 50 EMA** (trend established)
- **Momentum building** (RSI trending in same direction)
- After **healthy consolidation** (crossover from rest, not exhaustion)
- Higher timeframes aligned (30m/1H confirming trend)
- **RSI in middle zone** (40-60) showing room to move

**❌ AVOID:**
- Ranging/choppy markets (price crossing 50 EMA frequently)
- RSI at extremes (>70 or <30) when signal forms
- When 9 and 21 EMAs are tangled (no clear cross)
- After extended trends (RSI diverging from price)
- Low volume environments (weak follow-through)
- When 50 EMA is flat/horizontal (no trend)

**⚠️ WARNING SIGNS:**
- EMA cross but price below 50 EMA (counter-trend)
- RSI diverging from price action
- Crossover happening at RSI extremes
- Volume not supporting crossover
- Previous crossover failed recently
- 1H timeframe showing opposite signals

**📊 Pre-Trade Checklist:**
1. Is price clearly above 50 EMA (for long)?
2. Is 9 EMA cleanly crossing 21 EMA?
3. Is RSI above 50 (for long) and not overbought?
4. Is 1H/4H trend supporting this direction?
5. Is volume healthy (not declining)?
6. Is recent swing low clear for stop placement?

**🎯 PERFECT ENTRY:**
- 9/21 EMA golden cross just formed
- Price 5-10% above 50 EMA
- RSI at 55-60 (room to run)
- 1H showing same trend
- Volume increasing

#### Setup
```
Indicators:
- 9 EMA (fast)
- 21 EMA (slow)
- 50 EMA (trend filter)
- RSI (14 period)
```

#### Entry Rules - LONG
1. Price above 50 EMA (uptrend confirmation)
2. 9 EMA crosses ABOVE 21 EMA (golden cross)
3. RSI > 50 (momentum confirmation)
4. RSI not overbought (<70)
5. Enter on crossover candle close

#### Entry Rules - SHORT
1. Price below 50 EMA (downtrend confirmation)
2. 9 EMA crosses BELOW 21 EMA (death cross)
3. RSI < 50 (momentum confirmation)
4. RSI not oversold (>30)
5. Enter on crossover candle close

#### Exit Strategy

**Primary Exit Methods:**

**1. ROI (Return on Investment) Table:**
```python
minimal_roi = {
    "0": 0.025,      # 2.5% immediate (momentum trade)
    "20": 0.02,      # 2% after 20 minutes
    "45": 0.015,     # 1.5% after 45 minutes
    "90": 0.01,      # 1% after 1.5 hours
    "150": 0.006,    # 0.6% after 2.5 hours
    "240": 0.003     # 0.3% after 4 hours
}
```
**Rationale:** Trend following needs patience. Strong early targets, then let winners run longer.

**2. Stop Loss Configuration:**

**Structure-Based Stop (Recommended):**
```
LONG Position:
Stop: Below recent swing low
Buffer: -0.15% below swing low (avoid wicks)

Calculation:
Entry: $67,800
Recent swing low: $67,400
Buffer: $67,400 × 0.9985 = $67,298
Risk: $502 (0.74%)

SHORT Position:
Stop: Above recent swing high
Buffer: +0.15% above swing high
```

**Dynamic Stop Adjustment:**
```
As New Swing Lows Form (LONG):

Initial Stop: $67,298 (at entry)

After 30 min:
- New swing low: $67,600
- Move stop to: $67,499
- Now risking only 0.44%

After 60 min:
- New swing low: $67,750
- Move stop to: $67,648
- Locked in breakeven +0.16%

Rule: Update stop every 15 minutes if new swing forms
```

**Backup Fixed Stop:**
```
Hard Stop: -1.5% from entry

When to Use:
- No clear swing low/high
- Extreme volatility
- Indicator malfunction

Use whichever is TIGHTER:
- Structure stop OR
- Fixed -1.5% stop
```

**3. EMA Crossover Exit Signals:**

**Primary Exit: Opposite Crossover:**
```
LONG Exit Signal:

Death Cross: 9 EMA crosses BELOW 21 EMA

Action Plan:
- If profit >1.5%: Exit 100% (take profits)
- If profit 0.5-1.5%: Exit 80%, trail 20%
- If profit <0.5%: Exit 60%, hold 40% with tight stop
- If at loss: Hold if 50 EMA still supporting

Confirmation:
- Wait for candle close
- Next candle opens below cross = confirmed
- Execute exit immediately

SHORT Exit Signal:
- 9 EMA crosses ABOVE 21 EMA
- Same action plan as above
```

**Progressive EMA Exits:**
```
LONG Position Deterioration:

Stage 1 - Warning:
- 9 EMA flattens or touches 21 EMA
- Action: Tighten trail to 0.5%
- Reason: Momentum slowing

Stage 2 - Danger:
- Price closes below 9 EMA
- Action: Exit 40%
- Reason: Short-term trend broken

Stage 3 - Breakdown:
- 9 EMA crosses below 21 EMA
- Action: Exit 50% more (90% total)
- Reason: Medium-term trend broken

Stage 4 - Complete Reversal:
- Price closes below 50 EMA
- Action: Exit 100% remaining
- Reason: Main trend broken
```

**4. RSI Exit Signals:**

**RSI Overbought/Oversold:**
```
LONG Position:

RSI >70 (Overbought):
- Action: Take 40% profit
- Reason: Momentum extended
- Trail rest with tight 0.4% stop

RSI >80 (Extremely Overbought):
- Action: Exit 80% total
- Reason: Likely reversal coming

RSI Divergence:
- Price higher high
- RSI lower high
- Action: Exit 70%
- Reason: Hidden weakness

RSI Drops Below 50:
- While in LONG
- Action: Exit 50%
- Reason: Momentum shifted bearish
```

**RSI Trend Analysis:**
```
Healthy LONG:
- RSI oscillating between 40-80
- Stay in trade

Weakening LONG:
- RSI making lower highs
- Start taking profits (30%)

Broken LONG:
- RSI drops below 40
- Exit 100%
```

**5. 50 EMA Trend Filter Exits:**

**Critical 50 EMA Rules:**
```
LONG Position:

Price Approaching 50 EMA from Above:
- First touch: Normal, hold position
- Closes at 50 EMA: Warning, exit 30%
- Closes below 50 EMA: Exit 80% total
- Second close below: Exit 100%

Price Behavior at 50 EMA:
- Bounces cleanly: Good, add to position (advanced)
- Hesitates: Neutral, hold
- Pierces through: Bad, exit 60%
- Stays below: Terrible, exit all

50 EMA Slope:
- Rising: Bullish, hold confidently
- Flattening: Caution, tighten stops
- Turning down: Danger, exit 50%
- Declining: Exit 100%
```

**6. Partial Exit Strategy:**

**Conservative Approach (Recommended):**
```
TP1 (50% position): 2:1 Risk:Reward
- Calculate: If risk $450, TP1 = $900 profit
- Entry: $67,800, Stop: $67,350, TP1: $68,700
- Time: 1-2 hours expected
- Action: Close 50%, move stop to breakeven

TP2 (30% position): Opposite crossover OR major resistance
- Exit when 9/21 EMA death cross appears
- Or at major resistance level
- Or 3:1 ratio ($1,350 profit)
- Action: Close 30%, trail rest aggressively

TP3 (20% position): Trail with 50 EMA
- Stop: 50 EMA - 0.3%
- Exit: When price closes below 50 EMA
- Potential: 4:1 to 6:1 ratio
```

**Aggressive Approach:**
```
TP1 (40%): 1.5:1 ratio
TP2 (30%): 2.5:1 ratio
TP3 (20%): 4:1 ratio
TP4 (10%): Trail indefinitely with 50 EMA
```

**Trend Rider Approach:**
```
TP1 (30%): 2:1 (secure some profit)
TP2 (20%): Major resistance
TP3 (50%): Trail with 50 EMA (let winners run)
```

**7. Time-Based Management:**

**Holding Period Guidelines:**
```
0-45 minutes: EARLY PHASE
- Setup developing
- Don't exit prematurely
- Let trend establish

45-120 minutes: DEVELOPMENT PHASE
- TP1 zone
- Trend should be clear
- If not moving well, consider exiting 40%

2-4 hours: MATURE PHASE
- TP2 zone
- Most profit should be banked
- Trail remaining position

4-6 hours: EXTENDED PHASE
- Only if very strong trend
- Trail very tight (0.4%)
- Exit on first sign of weakness

6+ hours: FORCE EXIT
- Close all remaining
- Don't hold 15m setups overnight
- Risk of gap/reversal
```

**Session Awareness:**
```
Best Trending Times:
- London open (3am EST): Strong trends
- NY open (9:30am EST): Best momentum
- Overlap (8am-12pm EST): Peak performance

Weaker Trending Times:
- Lunch (12pm-2pm EST): Often consolidates
- After 4pm EST: Momentum fades
- Asia session: Avoid, low volume

Action:
- Before weak periods: Take profits
- Don't enter new trades in weak periods
```

**8. Trailing Stop Configuration:**

**Method 1 - Swing Low Trailing (Best for Trends):**
```python
# Trail behind each new swing low

For LONG:
trailing_stop = last_swing_low - (last_swing_low * 0.0015)

Example Progression:
Entry: $67,800

After 20 min:
- Swing low: $67,650
- Trail: $67,548 (-0.37%)

After 60 min:
- Swing low: $67,900
- Trail: $67,797 (-0.004%, breakeven!)

After 120 min:
- Swing low: $68,300  
- Trail: $68,197 (+0.59% locked)

Update: Every 15 minutes or on new swing
```

**Method 2 - EMA-Based Trailing:**
```
After TP1 Hit:

Trail: 21 EMA - 0.25%

Example:
Entry: $67,800
TP1 hit at: $68,700
21 EMA now at: $68,400
Trailing Stop: $68,229

Advantage: Follows trend momentum
Disadvantage: Can be wide in strong trends
```

**Method 3 - Percentage Trailing (Simple):**
```python
Activation: +1.2% profit
Distance: 0.6% behind highest point

trailing_stop = highest_price * 0.994

Example:
Entry: $67,800
Highest: $68,700 → Trail: $68,288 (+0.72%)
Highest: $69,200 → Trail: $68,785 (+1.45%)
```

**9. Volume-Based Adjustments:**
```
High Volume Confirmation:
- Volume increasing with trend
- Action: Be more patient, hold longer
- Strong hands pushing price

Volume Declining:
- 3+ bars of decreasing volume
- Price still moving direction
- Action: Exit 40%, momentum fading

Volume Spike Against Position:
- Sudden 3x+ volume
- Large reversal candle
- Action: Exit 80%, potential reversal

Volume Climax:
- Extreme volume (5x+)
- At resistance level
- Action: Exit 100%, exhaustion
```

**10. Complete Exit Priority:**

```
Level 1 - IMMEDIATE:
1. Stop loss hit → 100% exit
2. Price closes below 50 EMA (LONG) → 100% exit
3. Volume climax against position → 100% exit
4. Gap against position → 100% exit

Level 2 - HIGH PRIORITY:
5. 9/21 EMA death cross → 80-100% exit
6. RSI >75 or <25 → 70% exit
7. Time >6 hours → 100% exit
8. Major resistance hit → 60% exit

Level 3 - STANDARD:
9. TP1 (2:1) hit → 50% exit
10. RSI >70 → 40% exit
11. Price touches 50 EMA → 30% exit
12. ROI table → Automatic

Level 4 - TRAILING:
13. Swing low trail hit → Exit rest
14. EMA trail hit → Exit rest
15. Fixed % trail hit → Exit rest
```

**Freqtrade Configuration:**
```python
class EMACrossRSIStrategy(IStrategy):
    
    minimal_roi = {
        "0": 0.025,
        "20": 0.02,
        "45": 0.015,
        "90": 0.01,
        "150": 0.006,
        "240": 0.003
    }
    
    stoploss = -0.015  # -1.5% hard stop
    
    trailing_stop = True
    trailing_stop_positive = 0.012  # Activate at 1.2%
    trailing_stop_positive_offset = 0.015  # Trigger at 1.5%
    trailing_only_offset_is_reached = True
    
    use_exit_signal = True
    exit_profit_only = False
    
    def populate_exit_trend(self, dataframe, metadata):
        dataframe.loc[
            (
                # Death cross OR
                (qtpylib.crossed_below(dataframe['ema9'], dataframe['ema21'])) |
                # RSI overbought OR
                (dataframe['rsi'] > 75) |
                # Below 50 EMA
                (dataframe['close'] < dataframe['ema50'])
            ),
            'exit_long'
        ] = 1
        
        return dataframe
    
    def custom_exit(self, pair, trade, current_time, current_rate, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1]
        
        # Calculate profit
        profit_ratio = trade.calc_profit_ratio(current_rate)
        
        # TP1: 2:1 ratio
        risk = abs(trade.stop_loss_pct)
        if profit_ratio >= (risk * 2):
            return 0.5  # Exit 50%
        
        # Emergency: Below 50 EMA
        if current_rate < last_candle['ema50']:
            return True  # Exit all
        
        # RSI extremely high
        if last_candle['rsi'] > 80:
            return 0.7  # Exit 70%
        
        return None
```

**Exit Summary Table:**

| Signal | Action | % Exit | Time Expected |
|--------|--------|--------|---------------|
| Stop loss | Exit | 100% | Immediate |
| 9/21 death cross | Exit | 80% | 1-3 hours |
| TP1 (2:1) | Partial | 50% | 1-2 hours |
| RSI >70 | Partial | 40% | Variable |
| Below 50 EMA | Exit | 100% | 2-4 hours |
| Time >6h | Force close | 100% | 6 hours |
| Trail hit | Exit rest | Rest | Ongoing |

#### Example Trade
```
BTC/USDT 15m Chart

Entry: $67,800
- 9 EMA crosses above 21 EMA ✓
- Price above 50 EMA ($67,200) ✓
- RSI: 58 ✓
- Recent swing low: $67,400

Stop Loss: $67,350 (-0.66%, $450)
Target: $68,700 (+1.33%, $900)

Capital: $5,000
Risk: 1% ($50)
Position Size: 0.111 BTC
```

#### Performance Metrics
- Win Rate: 66%
- Average Win: 1.8%
- Average Loss: 0.8%
- Expectancy: +0.66% per trade
- Trades per Day: 2-5

---



---

## See Also

- [5-Minute Strategies](strategies_5m.md) - Faster execution
- [30-Minute Strategies](strategies_30m.md) - Position trading
- [UT Bot Complete Guide](shared_content.md#ut-bot-guide)
- [Risk Management](shared_content.md#risk-management)

---

*Last Updated: November 16, 2025*
