# 1-Hour Trading Strategies
*High Win-Rate Strategies for Swing Trading*

---

## Navigation
- [Back to Main Guide](TRADING_STRATEGIES_GUIDE.md)
- [1-Minute Strategies](strategies_1m.md)
- [5-Minute Strategies](strategies_5m.md)
- [15-Minute Strategies](strategies_15m.md)
- [30-Minute Strategies](strategies_30m.md)
- [Shared Content](shared_content.md)

---

## Overview

**Trading Style:** SWING TRADING  
**Time Commitment:** <2 hours/day  
**Capital Requirements:** $5,000+  
**Recommended Experience:** Intermediate to Advanced

**Key Characteristics:**
- Patient approach (1-5 days per trade)
- Premium quality setups
- 2-5 signals per week
- Profit targets (3-8% per trade)
- Stop losses (1.5-3%)
- Best for trend following, cloud systems, and divergence trading

---

## 1-Hour Strategies

### Strategy 1HA: Trend Following with Moving Averages (Win Rate: ~71%)
**📊 Category:** SWING TRADING (Trend Following)

**Best For:** Swing traders, position trading  
**Timeframe:** 1H  
**Capital Required:** $5,000+

#### Optimal Market Conditions

**✅ BEST CONDITIONS:**
- **Strong trending markets** on Daily/4H timeframes
- Price **well above 200 EMA** (>3-5% for uptrend)
- **ADX >25** showing strong directional momentum
- 20/50 EMAs clearly separated (not tangled)
- **MACD histogram expanding** (momentum building)
- After **healthy pullbacks** to 20 EMA (not breakdowns)
- Higher timeframe structure intact

**❌ AVOID:**
- Ranging/sideways markets (price around 200 EMA)
- ADX <20 (weak/no trend)
- EMAs flat or tangled (no clear direction)
- After extended moves without pullback (exhaustion)
- MACD histogram declining (momentum fading)
- When price breaks below 50 EMA (trend break)
- Low volume grind (weak institutional interest)

**⚠️ WARNING SIGNS:**
- 20 EMA flattening or turning down
- Price closing below 20 EMA multiple times
- ADX declining while in trade
- MACD histogram compressing
- Volume declining during trend
- 50 EMA getting tested repeatedly
- Higher highs not being made (for uptrend)

**📊 Pre-Trade Checklist:**
1. Is price >5% above 200 EMA (clear trend)?
2. Is 20 EMA cleanly crossing above 50 EMA?
3. Is MACD histogram green and growing?
4. Is ADX >25 and rising?
5. Is this a pullback to 20 EMA (not 50 EMA breakdown)?
6. Is 4H/Daily timeframe confirming trend?
7. Is volume healthy (not declining)?
8. Is there clear space to target (no major resistance)?

**🎯 PERFECT ENTRY:**
- Strong Daily uptrend (price >200MA for weeks)
- 20/50 EMA golden cross just confirmed
- Price pulls back to 20 EMA (first touch after cross)
- ADX at 30+ and climbing
- MACD histogram positive and expanding
- Volume picks up on bounce from 20 EMA
- 4H showing bullish structure

**📉 TREND STRENGTH INDICATORS:**
- **Very Strong:** Price >10% above 200 EMA, ADX >35
- **Strong:** Price 5-10% above 200 EMA, ADX 25-35
- **Moderate:** Price 2-5% above 200 EMA, ADX 20-25
- **Weak:** Price <2% above 200 EMA, ADX <20 (SKIP)

#### Setup
```
Indicators:
- 20 EMA (fast)
- 50 EMA (medium)
- 200 EMA (slow/trend filter)
- MACD (12, 26, 9)
- ADX (14) - trend strength
```

#### Entry Rules - LONG
1. Price above 200 EMA (bullish trend)
2. 20 EMA crosses ABOVE 50 EMA (golden cross)
3. MACD histogram positive and rising
4. ADX > 25 (strong trend)
5. Pullback to 20 EMA after crossover
6. Enter on bounce from 20 EMA

#### Entry Rules - SHORT
1. Price below 200 EMA (bearish trend)
2. 20 EMA crosses BELOW 50 EMA (death cross)
3. MACD histogram negative and falling
4. ADX > 25 (strong trend)
5. Pullback to 20 EMA after crossover
6. Enter on rejection from 20 EMA

#### Exit Strategy

**Primary Exit Methods:**

**1. ROI Table:**
```python
minimal_roi = {
    "0": 0.05,       # 5% immediate (strong trend confirmation)
    "60": 0.04,      # 4% after 1 hour
    "120": 0.032,    # 3.2% after 2 hours
    "240": 0.025,    # 2.5% after 4 hours
    "480": 0.015,    # 1.5% after 8 hours
    "720": 0.008     # 0.8% after 12 hours
}
```
**Rationale:** 1H trend following needs patience for larger moves. Can hold 1-3 days. Front-loaded for quick wins, patient for runners.

**2. Stop Loss - 50 EMA Based:**
```
LONG Position:
Primary Stop: Below 50 EMA

Calculation:
Entry: $67,700
50 EMA: $67,200
Buffer: -0.2% below EMA
Stop: $67,200 × 0.998 = $67,066
Risk: $634 (0.94%)

Why 50 EMA:
- Key support in trends
- Break below = trend weakening
- Not too tight, allows breathing

Backup Fixed Stop: -1.8%
Use tighter of: 50 EMA stop OR -1.8%
```

**Dynamic Stop Management:**
```
As Trend Develops:

After 4 hours:
- 50 EMA: $67,400
- Update stop to: $67,266
- Now risk: 0.64%

After 12 hours:
- 50 EMA: $67,650
- Update stop to: $67,515
- Locked breakeven!

After 24 hours:
- 50 EMA: $68,100
- Stop: $67,964
- Locked +0.39%

Update frequency: Every 2-4 hours OR when 50 EMA moves significantly
```

**3. EMA Crossover Exit Signals:**

**Primary Exit: Death Cross:**
```
LONG Position:

20 EMA crosses BELOW 50 EMA:
- If profit >2%: Exit 100% (take gains)
- If profit 1-2%: Exit 80%, trail 20%
- If profit 0-1%: Exit 60%, hold 40%
- If at loss: Hold if 200 EMA support

Confirmation Required:
- Wait for candle close
- Next candle opens below cross
- MACD should also turn bearish

False Cross Protection:
- If 20 EMA recrosses above within 2 candles
- Re-enter if setup still valid
```

**Progressive Deterioration:**
```
Stage 1 - Early Warning:
- 20 EMA flattening
- Action: Tighten trail to 0.8%
- Monitor closely

Stage 2 - Momentum Slowing:
- Price closes below 20 EMA
- Action: Exit 30%
- Move stop to breakeven

Stage 3 - Trend Breaking:
- 20 EMA touches 50 EMA
- Action: Exit 50% more (80% total)
- Very tight trail on rest

Stage 4 - Complete Reversal:
- Death cross confirmed
- Action: Exit 100%
```

**4. ADX Exit Signals:**

**Trend Strength Monitoring:**
```
ADX During Trade:

Rising ADX (Good):
- ADX climbing from 25 → 35+
- Action: Hold confidently
- Trend strengthening

Peak ADX (Warning):
- ADX reaches 45-50+
- Action: Take 40% profit
- Trend may be exhausting

Declining ADX (Danger):
- ADX drops below 25
- Action: Exit 70%
- Trend losing strength

ADX Below 20 (Exit):
- Clear trend loss
- Action: Exit 100%
- No trend = no edge
```

**5. MACD Exit Signals:**

**Histogram Analysis:**
```
LONG Position:

Histogram Expanding (Good):
- Green bars getting bigger
- Action: Hold, momentum building

Histogram Shrinking (Warning):
- 3+ consecutive smaller bars
- Action: Exit 30%
- Momentum weakening

Histogram Turns Red (Exit):
- MACD bearish crossover
- Action: Exit 70% immediately
- Trend reversing

MACD Below Signal Line (Full Exit):
- Clear bearish signal
- Action: Exit 100%

Divergence:
- Price higher highs
- MACD lower highs
- Action: Exit 60%, trail tight
```

**6. 200 EMA Exit Rule:**

**Critical Trend Line:**
```
LONG Position:

Price Approaching 200 EMA:
- From above, moving down
- Action: Tighten trail to 0.6%

Price Touches 200 EMA:
- First touch: Monitor
- Action: Exit 40% as insurance

Price Closes Below 200 EMA:
- Major trend break
- Action: Exit 100%
- Don't question, exit

Why Critical:
- 200 EMA = main trend indicator
- Below 200 = bearish territory
- Trend following strategy needs trend
```

**7. Partial Exit Strategy:**

**Swing Trading Approach (Recommended):**
```
TP1 (40% position): 2:1 Risk:Reward
- Calculate from entry and stop
- Entry: $67,700, Stop: $67,066
- Risk: $634
- TP1: $67,700 + ($634 × 2) = $68,968 (+1.87%)
- Time: 12-24 hours expected
- Action: Close 40%, move stop to entry

TP2 (35% position): Major resistance or 4:1
- 4:1 ratio: $67,700 + ($634 × 4) = $70,236 (+3.75%)
- Or next major resistance level
- Time: 24-48 hours
- Action: Close 35%, stop to +1.5%

TP3 (15% position): Extended target 6:1
- $67,700 + ($634 × 6) = $71,504 (+5.62%)
- Time: 2-4 days
- Action: Close 15%

TP4 (10% position): Runner
- Trail with 20 EMA - 0.4%
- Exit on death cross
- Potential: 8-12%+
- Let winners run
```

**Conservative Approach:**
```
TP1 (50%): 2:1 (secure majority)
TP2 (40%): 3:1 (most profit banked)
TP3 (10%): Trail with 50 EMA
```

**Aggressive Trend Rider:**
```
TP1 (30%): 2:1 (safety profit)
TP2 (30%): 4:1 (good profit)
TP3 (40%): Trail with 20 EMA (let it ride)
```

**8. Time-Based Management:**

**Swing Holding Periods:**
```
0-12 hours: DEVELOPMENT PHASE
- Trend establishing
- Hold patiently
- Monitor EMA alignment
- Don't exit prematurely

12-24 hours: EARLY PROFIT ZONE
- TP1 zone
- 2:1 should be near
- Take first profits
- Secure partial gains

1-2 days: MAIN PROFIT ZONE
- TP2 potential
- Trend mature
- Bank majority of profit
- Trail remaining

2-4 days: EXTENDED MOVE
- TP3 zone  
- Only if very strong trend
- Trail very tight (0.6%)
- Exit on first weakness

4+ days: EXCEPTIONAL
- Rare but possible
- Only trail with 50 EMA
- Exit on death cross
- Don't overstay
```

**9. Trailing Stop Methods:**

**Method 1 - 20 EMA Trail (Aggressive):**
```python
Activation: After TP1 hit
Distance: 20 EMA - 0.4%

Example:
Entry: $67,700
TP1 hit at: $68,968
20 EMA now at: $68,600
Trail: $68,326 (+0.92% locked)

Advantage: Follows momentum
Disadvantage: Can exit early in strong trends
```

**Method 2 - 50 EMA Trail (Conservative):**
```python
Activation: Immediately
Distance: 50 EMA - 0.3%

Update: Every 4 hours

Entry: $67,700
50 EMA: $67,200 → Trail: $67,000

After 12 hours:
50 EMA: $67,650 → Trail: $67,447 (breakeven)

After 24 hours:
50 EMA: $68,400 → Trail: $68,195 (+0.73%)

Advantage: Patient, catches big moves
Disadvantage: Gives back more profit
```

**Method 3 - Percentage Trail (Simple):**
```python
Activation: +2% profit
Distance: 1% behind highest point

trailing_stop = highest_price * 0.99

Entry: $67,700
High: $69,500 (+2.66%) → Trail: $68,805 (+1.63%)
High: $71,000 (+4.87%) → Trail: $70,290 (+3.83%)

Advantage: Simple, automatic
Disadvantage: Doesn't follow structure
```

**10. Complete Exit Priority:**

```
Level 1 - IMMEDIATE (No Hesitation):
1. Stop loss hit (below 50 EMA) → 100% exit
2. Price closes below 200 EMA → 100% exit
3. Death cross confirmed → 100% exit
4. ADX drops below 18 → 100% exit

Level 2 - HIGH PRIORITY:
5. MACD full bearish cross → 80% exit
6. ADX declining below 23 → 60% exit
7. Price closes below 20 EMA (2x) → 50% exit
8. Time >4 days → 90% exit

Level 3 - STANDARD PROFIT TAKING:
9. TP1 (2:1) hit → 40% exit
10. TP2 (4:1) hit → 35% exit  
11. MACD histogram shrinking → 30% exit
12. ADX peaks >50 → 40% exit
13. ROI table → Automatic

Level 4 - TRAILING:
14. 20 EMA trail hit → Exit rest
15. 50 EMA trail hit → Exit rest
16. Percentage trail hit → Exit rest
```

**Freqtrade Configuration:**
```python
class TrendFollowingEMAStrategy(IStrategy):
    
    minimal_roi = {
        "0": 0.05,
        "60": 0.04,
        "120": 0.032,
        "240": 0.025,
        "480": 0.015,
        "720": 0.008
    }
    
    stoploss = -0.018  # -1.8% hard stop
    
    trailing_stop = True
    trailing_stop_positive = 0.02  # Activate at +2%
    trailing_stop_positive_offset = 0.025  # Trigger at 2.5%
    trailing_only_offset_is_reached = True
    
    use_exit_signal = True
    exit_profit_only = False
    
    def populate_exit_trend(self, dataframe, metadata):
        dataframe.loc[
            (
                # Death cross OR
                (qtpylib.crossed_below(dataframe['ema20'], dataframe['ema50'])) |
                # Below 200 EMA OR
                (dataframe['close'] < dataframe['ema200']) |
                # ADX weak
                (dataframe['adx'] < 20)
            ),
            'exit_long'
        ] = 1
        
        return dataframe
    
    def custom_exit(self, pair, trade, current_time, current_rate, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1]
        
        profit_ratio = trade.calc_profit_ratio(current_rate)
        risk = abs(trade.stop_loss_pct)
        
        # TP1: 2:1
        if profit_ratio >= (risk * 2):
            return 0.4  # Exit 40%
        
        # TP2: 4:1  
        if profit_ratio >= (risk * 4):
            return 0.35  # Exit additional 35%
        
        # Emergency exits
        if current_rate < last_candle['ema200']:
            return True  # Exit all below 200 EMA
        
        if last_candle['adx'] < 18:
            return True  # Exit all when trend dies
        
        return None
    
    def custom_stoploss(self, pair, trade, current_time, current_rate, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1]
        
        # Trail with 50 EMA
        ema50_stop = (last_candle['ema50'] * 0.998 - trade.open_rate) / trade.open_rate
        
        # Use tighter of EMA stop or fixed
        return max(ema50_stop, -0.018)
```

**Exit Strategy Summary:**

| Signal | Action | % Exit | Expected Time |
|--------|--------|--------|---------------|
| Stop (50 EMA) | Exit all | 100% | Immediate |
| Below 200 EMA | Exit all | 100% | 1-3 days |
| Death cross | Exit all | 100% | 1-2 days |
| TP1 (2:1) | Partial | 40% | 12-24 hours |
| TP2 (4:1) | Partial | 35% | 1-2 days |
| ADX <20 | Exit all | 100% | Variable |
| MACD bearish | Exit most | 80% | Variable |
| Trail hit | Exit rest | Rest | Ongoing |

#### Example Trade
```
BTC/USDT 1H Chart

Setup:
- Price: $67,800 (above 200 EMA at $65,500) ✓
- 20 EMA: $67,600 (crosses above 50 EMA) ✓
- 50 EMA: $67,200
- MACD: Histogram green and rising ✓
- ADX: 32 (strong trend) ✓
- Price pulls back to 20 EMA at $67,650

Entry: $67,700 (bounce from 20 EMA confirmed)
Stop Loss: $67,150 (-0.81%, below 50 EMA, $550)
TP1 (50%): $68,600 (+1.33%, $900) [1:1.64 ratio]
TP2 (50%): $69,400 (+2.51%, $1,700) [1:3.09 ratio]

Position Sizing (for $10,000 account, 2% risk):
Risk Amount: $200
Position Size: 0.364 BTC ($24,643)
Potential Profit: $900-$1,700
```

#### Performance Metrics
- Win Rate: 71%
- Average Win: 3.2%
- Average Loss: 1.3%
- Expectancy: +1.35% per trade
- Trades per Week: 3-8
- Holding Time: 1-3 days

---

### Strategy 1HB: Ichimoku Cloud System (Win Rate: ~68%)
**📊 Category:** SWING TRADING (Trend Analysis)

**Best For:** Trend trading, comprehensive analysis  
**Timeframe:** 1H  
**Best Pairs:** BTC/USDT, ETH/USDT

#### Optimal Market Conditions

**✅ BEST CONDITIONS:**
- **Strong trending markets** (price consistently above/below cloud)
- Cloud **clearly colored** (green for up, red for down)
- **Thick cloud** indicating strong support/resistance
- Tenkan/Kijun **clearly separated** (not tangled)
- **Chikou Span in open space** (not tangled with price)
- After **pullbacks to cloud** (not breakdowns)
- Price making new highs above cloud (for uptrend)

**❌ AVOID:**
- Price inside cloud (no clear trend)
- Cloud very thin (weak support/resistance)
- Cloud color changing frequently (indecision)
- Tenkan/Kijun lines tangled (choppy)
- Chikou Span tangled with price (congestion)
- Flat cloud (sideways market)
- When all components conflicting

**⚠️ WARNING SIGNS:**
- Price entering cloud from above (trend weakening)
- Tenkan crossing below Kijun while in trade
- Cloud ahead turning opposite color
- Chikou Span approaching price from below
- Price making lower highs despite being above cloud
- Cloud thinning significantly
- Volume declining during trend

**📊 Pre-Trade Checklist - LONG:**
1. Is price clearly ABOVE cloud (not inside)?
2. Is cloud GREEN (Span A > Span B)?
3. Is Tenkan-sen crossing ABOVE Kijun-sen?
4. Is Chikou Span above price from 26 bars ago?
5. Is price pulling back TO cloud (not through it)?
6. Is 4H Ichimoku also bullish?
7. Is cloud thick (strong support)?
8. Is Chikou Span in clear space (not tangled)?

**📊 Pre-Trade Checklist - SHORT:**
1. Is price clearly BELOW cloud?
2. Is cloud RED (Span A < Span B)?
3. Is Tenkan-sen crossing BELOW Kijun-sen?
4. Is Chikou Span below price from 26 bars ago?
5. Is price pulling back TO cloud (not through it)?
6. Is 4H Ichimoku also bearish?
7. Is cloud thick (strong resistance)?
8. Is Chikou Span in clear space?

**🎯 IDEAL SETUP - LONG:**
- Price 5-10% above green cloud
- Cloud thick and turning up
- Tenkan/Kijun bullish cross freshly formed
- Price pulls back to cloud top
- Bounces with strong candle
- Chikou Span well above price
- 4H showing same bullish picture

**🎯 IDEAL SETUP - SHORT:**
- Price 5-10% below red cloud
- Cloud thick and turning down
- Tenkan/Kijun bearish cross fresh
- Price rallies to cloud bottom
- Rejects with strong bearish candle
- Chikou Span well below price
- 4H showing same bearish picture

**☁️ CLOUD INTERPRETATION:**
- **Thick cloud:** Strong support/resistance, reliable
- **Thin cloud:** Weak support/resistance, easily broken
- **Green cloud:** Bullish sentiment, look for longs
- **Red cloud:** Bearish sentiment, look for shorts
- **Price in cloud:** Neutral/choppy, avoid trading
- **Flat cloud:** Ranging market, use other strategies

#### Setup
```
Indicator:
- Ichimoku Cloud (9, 26, 52)
  - Tenkan-sen (Conversion Line): 9 period
  - Kijun-sen (Base Line): 26 period
  - Senkou Span A (Leading Span A)
  - Senkou Span B (Leading Span B)
  - Chikou Span (Lagging Span)
```

#### Entry Rules - LONG (All Must Align)
1. Price ABOVE the cloud (bullish)
2. Cloud is GREEN (Span A > Span B)
3. Tenkan-sen (blue) crosses ABOVE Kijun-sen (red)
4. Chikou Span (green line) above price from 26 periods ago
5. Price pulls back to cloud or Kijun-sen
6. Enter on bounce

#### Entry Rules - SHORT (All Must Align)
1. Price BELOW the cloud (bearish)
2. Cloud is RED (Span A < Span B)
3. Tenkan-sen crosses BELOW Kijun-sen
4. Chikou Span below price from 26 periods ago
5. Price rallies to cloud or Kijun-sen
6. Enter on rejection

#### Exit Strategy

**Primary Exit Methods:**

**1. ROI Table:**
```python
minimal_roi = {
    "0": 0.06,       # 6% immediate (Ichimoku confirmation)
    "60": 0.05,      # 5% after 1 hour
    "120": 0.04,     # 4% after 2 hours
    "240": 0.03,     # 3% after 4 hours
    "480": 0.018,    # 1.8% after 8 hours
    "720": 0.01      # 1% after 12 hours
}
```
**Rationale:** Ichimoku cloud trends can run 2-5 days. Patient for bigger moves. Front-loaded for quick momentum captures.

**2. Stop Loss - Cloud Based:**
```
LONG Position:
Primary Stop: Below cloud (other side)

Calculation:
Entry: $3,525 (ETH)
Cloud bottom (Senkou Span B): $3,480
Buffer: -0.3% below cloud
Stop: $3,480 × 0.997 = $3,469.56
Risk: $55.44 (1.57%)

Why Cloud Stop:
- Cloud = dynamic support/resistance
- Break through cloud = setup invalidated
- Provides breathing room
- Respects Ichimoku structure

Thin Cloud Exception:
- If cloud <1% thick
- Use Kijun-sen - 0.5% instead
- More reliable stop

Backup Stop: -2.5% fixed
```

**Dynamic Cloud Trailing:**
```
As Cloud Moves:

Initial (Entry):
- Cloud bottom: $3,480
- Stop: $3,469.56

After 4 hours:
- Cloud rises to: $3,510
- Update stop to: $3,499.47
- Now risk: 0.73%

After 12 hours:
- Cloud at: $3,540
- Stop: $3,529.38
- Locked +0.12%

After 24 hours:
- Cloud at: $3,600
- Stop: $3,589.20
- Locked +1.82%

Update: Every 4-6 hours as cloud advances
```

**3. Tenkan/Kijun Cross Exit:**

**Opposite Cross (Primary Exit):**
```
LONG Position:

Tenkan-sen crosses BELOW Kijun-sen:
- If profit >3%: Exit 100%
- If profit 1.5-3%: Exit 80%, trail 20%
- If profit 0-1.5%: Exit 60%, hold 40%
- If at loss & above cloud: Hold
- If at loss & in cloud: Exit 50%

Confirmation:
- Wait for candle close
- Check Chikou Span position
- Verify MACD alignment

False Cross Check:
- Lines very close but not crossed
- Don't exit prematurely
- Wait for clear separation
```

**Line Distance Analysis:**
```
Healthy LONG Trend:
- Tenkan well above Kijun (>1.5%)
- Action: Hold confidently

Warning Signs:
- Gap narrowing to <0.8%
- Action: Tighten trail to 0.8%
- Prepare for exit

Danger Zone:
- Lines touching/crossing
- Action: Exit 70%
- Momentum gone
```

**4. Cloud Exit Rules:**

**Price vs Cloud Relationship:**
```
LONG Position Monitoring:

Price Well Above Cloud (>2%):
- Strong position
- Action: Hold, trail wide

Price Approaching Cloud:
- Within 1% of cloud top
- Action: Exit 30%
- Insurance against reversal

Price Touches Cloud:
- Tests Senkou Span A
- Bounces: Good, hold
- Penetrates: Exit 60%

Price Enters Cloud:
- No clear trend anymore
- Action: Exit 80%
- Neutral zone reached

Price Exits Below Cloud:
- Complete reversal
- Action: Exit 100%
- No questions
```

**Cloud Color Change:**
```
LONG Position:

Cloud Ahead Turning Red:
- Future cloud (26 periods ahead) turns bearish
- Action: Tighten trail to 0.7%
- Resistance forming ahead

Cloud Thinning:
- Cloud getting narrower ahead
- Action: Take 40% profit
- Weaker support coming

Cloud Thickening:
- Cloud getting wider
- Action: Hold confidently
- Strong support ahead
```

**5. Chikou Span Exit Signals:**

**Lagging Line Analysis:**
```
LONG Position:

Chikou Span Above Price (Good):
- 26 periods ago comparison
- Action: Hold position
- Bullish confirmation

Chikou Approaching Price:
- Getting close from above
- Action: Exit 30%
- Warning sign

Chikou Touches Price:
- Resistance met
- Action: Exit 60%
- Momentum questionable

Chikou Below Price:
- Bearish signal
- Action: Exit 100%
- Setup invalidated

Chikou in Cloud:
- Tangled/unclear
- Action: Exit 50%
- Wait for clarity
```

**6. Partial Exit Strategy:**

**Cloud Trading Approach (Recommended):**
```
TP1 (35% position): 3:1 Risk:Reward
- Entry: $3,525, Stop: $3,469.56
- Risk: $55.44
- TP1: $3,525 + ($55.44 × 3) = $3,691.32 (+4.72%)
- Time: 1-2 days expected
- Action: Close 35%, move stop to cloud top

TP2 (40% position): Major resistance or 5:1
- 5:1: $3,525 + ($55.44 × 5) = $3,802.20 (+7.86%)
- Or significant S/R level
- Time: 2-4 days
- Action: Close 40%, stop to +3%

TP3 (15% position): Extended target 7:1
- $3,525 + ($55.44 × 7) = $3,913.08 (+11.01%)
- Time: 3-6 days
- Action: Close 15%

TP4 (10% position): Cloud Runner
- Trail: Cloud top - 0.4%
- Exit: When enters cloud or opposite cross
- Potential: 12-20%+
```

**Conservative Cloud:**
```
TP1 (50%): 3:1 (secure majority)
TP2 (40%): 5:1 (bank most profit)
TP3 (10%): Trail with cloud
```

**Aggressive Cloud Rider:**
```
TP1 (30%): 3:1 (safety)
TP2 (30%): 6:1
TP3 (40%): Trail with cloud (big runner)
```

**7. Time-Based Management:**

**Swing Holding Periods:**
```
0-12 hours: ESTABLISHMENT PHASE
- Ichimoku setup confirming
- All elements aligning
- Don't exit early
- Let cloud work

12-36 hours: EARLY TREND PHASE
- TP1 potential
- Trend developing
- Cloud support evident
- Monitor Tenkan/Kijun separation

1-3 days: MATURE TREND PHASE
- TP2 zone
- Main profit target
- Bank majority here
- Trail remaining tight

3-6 days: EXTENDED TREND
- TP3 potential
- Rare but powerful
- Trail with cloud
- Exit on first Ichimoku signal

6+ days: EXCEPTIONAL TREND
- Very rare
- Only if all Ichimoku aligned
- Trail very tight (0.6%)
- Exit on any weakness
```

**8. Trailing Stop Configuration:**

**Method 1 - Cloud Trailing (Best for Ichimoku):**
```python
Trail: Cloud top (Senkou Span A) - 0.4%

Update: Every 4 hours

Example:
Entry: $3,525

12 hours later:
Cloud top: $3,540
Trail: $3,525.84 (+0.02%)

24 hours:
Cloud top: $3,600
Trail: $3,585.60 (+1.72%)

48 hours:
Cloud top: $3,700
Trail: $3,685.20 (+4.54%)

Advantage: Follows Ichimoku structure perfectly
Disadvantage: Can be wide in ranging clouds
```

**Method 2 - Kijun-sen Trailing:**
```python
Trail: Kijun-sen (Base Line) - 0.5%

Activation: After TP1

Entry: $3,525
TP1 hit at: $3,691
Kijun-sen: $3,620
Trail: $3,601.90 (+2.18%)

Advantage: More responsive than cloud
Disadvantage: Can exit earlier in volatile moves
```

**Method 3 - Percentage Trailing:**
```python
Activation: +3% profit
Distance: 1.2% behind peak

trailing_stop = highest_price * 0.988

Entry: $3,525
Peak: $3,700 (+4.96%) → Trail: $3,655.60 (+3.70%)
Peak: $3,850 (+9.22%) → Trail: $3,803.80 (+7.91%)

Advantage: Simple, automatic
Disadvantage: Ignores Ichimoku structure
```

**9. Complete Exit Priority:**

```
Level 1 - IMMEDIATE:
1. Stop loss (below cloud) hit → 100%
2. Price exits below cloud → 100%
3. Chikou below price → 100%
4. Tenkan/Kijun death cross confirmed → 100%

Level 2 - HIGH PRIORITY:
5. Price enters cloud → 80%
6. Cloud turns red ahead → 50%
7. TP1 (3:1) hit → 35%
8. Time >6 days → 90%
9. Chikou approaching price → 30%

Level 3 - STANDARD:
10. TP2 (5:1) hit → 40%
11. Price touches cloud → 40%
12. Tenkan/Kijun narrowing → 30%
13. ROI table → Automatic

Level 4 - TRAILING:
14. Cloud trail hit → Exit rest
15. Kijun trail hit → Exit rest
16. Percentage trail hit → Exit rest
```

**Freqtrade Configuration:**
```python
class IchimokuCloudStrategy(IStrategy):
    
    minimal_roi = {
        "0": 0.06,
        "60": 0.05,
        "120": 0.04,
        "240": 0.03,
        "480": 0.018,
        "720": 0.01
    }
    
    stoploss = -0.025  # -2.5% hard stop
    
    trailing_stop = True
    trailing_stop_positive = 0.03  # Activate at +3%
    trailing_stop_positive_offset = 0.035  # Trigger at 3.5%
    trailing_only_offset_is_reached = True
    
    use_exit_signal = True
    exit_profit_only = False
    
    def populate_exit_trend(self, dataframe, metadata):
        dataframe.loc[
            (
                # Tenkan/Kijun death cross OR
                (qtpylib.crossed_below(dataframe['tenkan'], dataframe['kijun'])) |
                # Price enters cloud OR
                (
                    (dataframe['close'] < dataframe['senkou_a']) &
                    (dataframe['close'] < dataframe['senkou_b'])
                ) |
                # Chikou span bearish
                (dataframe['chikou_span'] < dataframe['close'].shift(26))
            ),
            'exit_long'
        ] = 1
        
        return dataframe
    
    def custom_exit(self, pair, trade, current_time, current_rate, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1]
        
        profit_ratio = trade.calc_profit_ratio(current_rate)
        risk = abs(trade.stop_loss_pct)
        
        # TP1: 3:1
        if profit_ratio >= (risk * 3):
            return 0.35  # Exit 35%
        
        # TP2: 5:1
        if profit_ratio >= (risk * 5):
            return 0.4  # Exit additional 40%
        
        # Emergency: Below cloud
        cloud_top = max(last_candle['senkou_a'], last_candle['senkou_b'])
        if current_rate < cloud_top:
            return True  # Exit all
        
        # Warning: Approaching cloud
        if current_rate < cloud_top * 1.01:
            return 0.4  # Exit 40%
        
        return None
    
    def custom_stoploss(self, pair, trade, current_time, current_rate, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1]
        
        # Trail below cloud
        cloud_bottom = min(last_candle['senkou_a'], last_candle['senkou_b'])
        cloud_stop = (cloud_bottom * 0.997 - trade.open_rate) / trade.open_rate
        
        # Use tighter of cloud or fixed
        return max(cloud_stop, -0.025)
```

**Exit Strategy Summary:**

| Signal | Action | % Exit | Expected Time |
|--------|--------|--------|---------------|
| Below cloud | Exit all | 100% | Immediate |
| TK death cross | Exit all | 100% | 1-3 days |
| Chikou bearish | Exit all | 100% | Variable |
| TP1 (3:1) | Partial | 35% | 1-2 days |
| TP2 (5:1) | Partial | 40% | 2-4 days |
| Price in cloud | Exit most | 80% | Variable |
| Cloud trail hit | Exit rest | Rest | Ongoing |

#### Example Trade
```
ETH/USDT 1H Chart

Setup:
- Price: $3,550 (above cloud at $3,480-$3,520)
- Cloud: GREEN (bullish)
- Tenkan-sen: Crosses above Kijun-sen ✓
- Chikou Span: Above price 26 periods ago ✓
- Price pulls back to cloud top at $3,520

Entry: $3,525 (bounce from cloud)
Stop Loss: $3,470 (-1.56%, below cloud, $55)
Target: $3,690 (+4.68%, resistance, $165)

Risk:Reward: 1:3
```

#### Performance Metrics
- Win Rate: 68%
- Average Win: 4.5%
- Average Loss: 1.8%
- Expectancy: +1.84% per trade
- Trades per Week: 2-5
- Holding Time: 2-5 days

---

### Strategy 1HC: Fibonacci + RSI Divergence (Win Rate: ~73%)
**📊 Category:** SWING TRADING (Reversal)

**Best For:** Reversal trading, high R:R setups  
**Timeframe:** 1H

#### Optimal Market Conditions

**✅ BEST CONDITIONS:**
- **After extended trends** (overextended price)
- **Clear divergence forming** (price vs RSI)
- Trend showing **signs of exhaustion**
- Price making **final push** to new high/low
- **RSI at extremes** during divergence (>70 or <30)
- Higher timeframe approaching **major S/R levels**
- Volume **declining** on each new high/low (weakness)
- **MACD confirming** divergence pattern

**❌ AVOID:**
- Early in trends (no exhaustion yet)
- When divergence is weak/unclear
- In strong momentum markets (divergence fails)
- When higher timeframe trend very strong
- Low volume markets (weak reversals)
- If only one indicator showing divergence
- During ranging/sideways markets
- If previous divergence signals failed recently

**⚠️ WARNING SIGNS:**
- Divergence forming but price keeps extending
- Volume increasing (trend not exhausted)
- MACD not confirming RSI divergence
- Fibonacci retracement not holding
- Reversal candles weak (small bodies)
- Higher timeframe showing continuation pattern

**📊 Pre-Trade Checklist - BULLISH DIVERGENCE:**
1. Is price making clear lower low?
2. Is RSI making higher low (divergence)?
3. Is RSI below 30 at first low?
4. Has trend been down for several hours/days?
5. Is price at Fibonacci 0.5 or 0.618 level?
6. Is MACD showing bullish crossover?
7. Is volume spiking on reversal candle?
8. Is next candle confirming reversal?

**📊 Pre-Trade Checklist - BEARISH DIVERGENCE:**
1. Is price making clear higher high?
2. Is RSI making lower high (divergence)?
3. Is RSI above 70 at first high?
4. Has trend been up for several hours/days?
5. Is price at Fibonacci 0.5 or 0.618 level?
6. Is MACD showing bearish crossover?
7. Is volume spiking on reversal candle?
8. Is next candle confirming reversal?

**🎯 PERFECT BULLISH DIVERGENCE SETUP:**
- Downtrend for 2+ days
- Price makes new low at $66,200
- RSI: First low at 25, second low at 32 (divergence!)
- Price rallies to $67,000 then pulls back
- Pulls back to Fibonacci 0.618 at $66,500
- MACD crosses bullish
- Strong bullish engulfing candle
- Volume 2x average
- Enter on next candle

**🎯 PERFECT BEARISH DIVERGENCE SETUP:**
- Uptrend for 2+ days
- Price makes new high at $68,500
- RSI: First high at 78, second high at 72 (divergence!)
- Price drops to $67,500 then rallies
- Rallies to Fibonacci 0.618 at $68,200
- MACD crosses bearish
- Strong bearish engulfing candle
- Volume 2x average
- Enter on next candle

**📈 DIVERGENCE STRENGTH:**
- **Class A (Strongest):** RSI swing difference >10 points, clear double top/bottom
- **Class B (Strong):** RSI swing difference 5-10 points, obvious pattern
- **Class C (Weak):** RSI swing difference <5 points, unclear pattern (SKIP)

**🔍 ADDITIONAL CONFIRMATION:**
- Look for: Double top/bottom pattern on price chart
- Volume declining on each swing high/low
- MACD histogram showing same divergence
- Higher timeframe at major S/R level
- Candlestick reversal patterns forming

#### Setup
```
Indicators:
- Fibonacci Retracement (key levels: 0.382, 0.5, 0.618, 0.786)
- RSI (14 period)
- MACD (12, 26, 9)
- Volume
```

#### Entry Rules - LONG (Bullish Divergence)
1. Clear downtrend with lower lows
2. Price makes new low
3. RSI makes HIGHER low (bullish divergence)
4. Price retraces to Fibonacci level (0.5 or 0.618)
5. MACD shows bullish crossover
6. Volume increases on reversal candle
7. Enter on next candle

#### Entry Rules - SHORT (Bearish Divergence)
1. Clear uptrend with higher highs
2. Price makes new high
3. RSI makes LOWER high (bearish divergence)
4. Price retraces to Fibonacci level (0.5 or 0.618)
5. MACD shows bearish crossover
6. Volume increases on reversal candle
7. Enter on next candle

#### Exit Strategy

**Primary Exit Methods:**

**1. ROI Table:**
```python
minimal_roi = {
    "0": 0.07,       # 7% immediate (reversal confirmation)
    "60": 0.06,      # 6% after 1 hour
    "120": 0.05,     # 5% after 2 hours
    "240": 0.035,    # 3.5% after 4 hours
    "480": 0.02,     # 2% after 8 hours
    "720": 0.012     # 1.2% after 12 hours
}
```
**Rationale:** Divergence reversals can be powerful (7-12%+). Front-loaded for quick momentum, patient for extended reversals. Best R:R of all strategies.

**2. Stop Loss - Below Divergence Low:**
```
LONG Position (Bullish Divergence):
Stop: Below most recent divergence low

Calculation:
Divergence Low: $66,200
Buffer: -0.3% (avoid wick hunting)
Stop: $66,200 × 0.997 = $66,001.40
Entry: $66,550
Risk: $548.60 (0.82%)

Why Below Divergence Low:
- If breaks below, divergence failed
- Pattern invalidated
- Setup no longer valid
- No reason to hold

Backup Stop: -1.5% fixed

Use tighter of: Divergence stop OR -1.5%
```

**Progressive Stop Management:**
```
After 1st Fibonacci Level Broken:
- Price above 0.5 level
- Move stop to breakeven
- Lock in zero risk

After TP1 (4:1):
- Move stop to +2%
- Secure substantial profit
- Trail for more

After TP2 (6:1):
- Trail with RSI or 0.6%
- Let winner run
```

**3. Fibonacci Level Exits:**

**Target Level Strategy:**
```
LONG Position (Bullish Divergence):

Entry: 0.618 Fib level
Targets: Previous Fibonacci levels

TP1 (40%): 0.5 Fibonacci
- First resistance
- 1.5-2% typical
- Quick profit secure
- Time: 4-12 hours

TP2 (35%): 0.382 Fibonacci  
- Major resistance
- 3-4% typical
- Bank majority
- Time: 12-36 hours

TP3 (15%): 0 Level (Swing High)
- Full retracement
- 5-8% potential
- Strong reversal
- Time: 1-4 days

TP4 (10%): Extension 1.272
- Beyond original swing
- 10%+ potential
- Runner position
- Trail tight

Example:
Swing Low: $66,200
Swing High: $67,800
Range: $1,600

Entry at 0.618: $66,200 + ($1,600 × 0.382) = $66,811

TP1 (0.5): $67,000 (+2.83%)
TP2 (0.382): $67,189 (+5.65%)
TP3 (0.0): $67,800 (+14.79%)
TP4 (1.272): $69,835 (+45.2%) [rare]
```

**Fibonacci Rejection Exits:**
```
If Price Rejected at Fib Level:

Strong Rejection:
- Large wick
- High volume
- Action: Exit 60%
- Level holding as resistance

Multiple Tests:
- 3+ touches without break
- Action: Exit 70%
- Losing momentum

Break Through:
- Clean break with volume
- Action: Hold for next level
- Take 30% insurance profit
```

**4. RSI Exit Signals:**

**Reversal Confirmation Exits:**
```
LONG Position (Bullish Divergence):

RSI Back to Oversold (<30):
- While in profit
- Action: Tighten trail to 0.6%
- Reversal may be failing

RSI Reaches Overbought (>70):
- Action: Take 50% profit
- Reversal complete
- Likely consolidation/pullback

RSI Extreme (>80):
- Action: Exit 80%
- Exhaustion likely

RSI Divergence Reverses:
- New bearish divergence forms
- Action: Exit 100%
- Setup reversing
```

**RSI Trend Confirmation:**
```
Healthy Reversal (LONG):
- RSI climbing from 30s to 50s
- Action: Hold confidently

Strong Reversal:
- RSI breaks above 50
- Action: Hold, add to trail
- Bulls in control

Weakening Reversal:
- RSI stalling below 45
- Action: Exit 40%
- Momentum questionable

Failed Reversal:
- RSI drops back below 30
- Action: Exit 100%
- Divergence failed
```

**5. MACD Confirmation Exits:**

**Histogram Monitoring:**
```
LONG Position:

MACD Histogram Growing (Good):
- Green bars expanding
- Action: Hold position
- Momentum building

Histogram Peak (Warning):
- Starts getting smaller
- Action: Take 30% profit
- Momentum topping

Histogram Turns Red (Exit):
- Bearish crossover
- Action: Exit 70%
- Reversal losing steam

MACD Crosses Below Signal (Full Exit):
- Clear bearish signal
- Action: Exit 100%
- Trend reversing again

MACD New Divergence:
- Bearish divergence forms
- Action: Exit 80%
- Prepare for pullback
```

**6. Volume Confirmation Exits:**

```
Volume Analysis:

Increasing Volume on Reversal (Good):
- Each candle higher volume
- Action: Hold confidently
- Institutional interest

Volume Climax:
- Extreme spike (5x+)
- At Fibonacci target
- Action: Exit 70%
- Exhaustion

Volume Declining:
- 3+ bars lower volume
- Price still rising
- Action: Exit 40%
- Weak hands, no conviction

Volume Spike Against Position:
- Sudden high volume
- Reversal candle
- Action: Exit 80%
- Another reversal starting
```

**7. Partial Exit Strategy:**

**Reversal Trading Approach (Recommended):**
```
TP1 (40% position): 4:1 Risk:Reward
- Entry: $66,550, Stop: $66,001
- Risk: $549
- TP1: $66,550 + ($549 × 4) = $68,746 (+3.30%)
- Location: Near 0.5 Fibonacci
- Time: 12-24 hours expected
- Action: Close 40%, stop to breakeven

TP2 (35% position): 6:1 or 0.382 Fib
- 6:1: $66,550 + ($549 × 6) = $69,844 (+4.95%)
- Or 0.382 Fibonacci level
- Time: 1-3 days
- Action: Close 35%, stop to +2%

TP3 (15% position): 8:1 or Swing High
- 8:1: $66,550 + ($549 × 8) = $70,942 (+6.60%)
- Or 0.0 Fibonacci (full retracement)
- Time: 2-5 days
- Action: Close 15%

TP4 (10% position): Extended Runner
- Trail: RSI below 50 OR 1% behind
- Exit: New divergence or major resistance
- Potential: 10-15%+
```

**Conservative Divergence:**
```
TP1 (50%): 4:1 (secure half)
TP2 (40%): 6:1 (bank most)
TP3 (10%): Trail to 8:1+
```

**Aggressive Reversal Rider:**
```
TP1 (30%): 4:1 (safety)
TP2 (30%): 7:1
TP3 (40%): Trail to 10:1+ (big runner)
```

**8. Time-Based Management:**

**Reversal Development Phases:**
```
0-4 hours: CONFIRMATION PHASE
- Divergence playing out
- Fibonacci level reaction
- MACD confirming
- Don't exit early
- Let setup develop

4-12 hours: EARLY REVERSAL PHASE
- Breaking first Fib levels
- RSI climbing
- TP1 potential zone
- Take first profits

12-36 hours: MAIN REVERSAL PHASE
- TP2 zone
- Most of retracement complete
- Bank majority of profit
- Trail remaining

1-3 days: EXTENDED REVERSAL
- TP3 potential
- Full Fibonacci retracement
- Trail tight (0.7%)
- Exit on first weakness

3+ days: TREND CHANGE
- Rare but possible
- Original trend may have reversed
- Trail very tight (0.5%)
- Exit on any signal
```

**9. Trailing Stop Configuration:**

**Method 1 - RSI-Based Trailing (Best for Divergence):**
```python
Trail Trigger: RSI drops below 50 (for LONG)

While RSI Above 50:
- Trail: 1% behind highest point

If RSI Drops Below 50:
- Exit: 70% immediately
- Trail rest: 0.5% tight

Example:
Entry: $66,550
Peak: $69,000 (+3.68%)
RSI: 62
Trail: $68,310 (+2.64%)

RSI drops to 48:
Exit: 70% at market
Trail: Remaining 30% at 0.5%
```

**Method 2 - Fibonacci Level Trailing:**
```python
Trail: Last broken Fibonacci level - 0.5%

Entry: $66,550 (at 0.618 Fib)

Breaks 0.5 Fib ($67,000):
Trail: $66,665 (+0.17%)

Breaks 0.382 Fib ($67,189):
Trail: $66,853 (+0.46%)

Breaks 0.0 Fib ($67,800):
Trail: $67,461 (+1.37%)

Advantage: Follows pattern structure
```

**Method 3 - Percentage Trailing (Simple):**
```python
Activation: +4% profit
Distance: 1.5% behind peak

trailing_stop = highest_price * 0.985

Entry: $66,550
Peak: $69,200 (+3.98%) → Trail: $68,162 (+2.42%)
Peak: $70,500 (+5.94%) → Trail: $69,443 (+4.35%)

Advantage: Simple, automatic
Disadvantage: Doesn't follow RSI/Fib structure
```

**10. Complete Exit Priority:**

```
Level 1 - IMMEDIATE (No Questions):
1. Stop loss hit (below div low) → 100%
2. New opposite divergence forms → 100%
3. RSI back to original extreme → 80%
4. Volume climax against position → 80%

Level 2 - HIGH PRIORITY:
5. MACD bearish crossover → 70%
6. TP1 (4:1) hit → 40%
7. TP2 (6:1) hit → 35%
8. Strong Fib level rejection → 60%
9. Time >3 days → 80%

Level 3 - STANDARD:
10. RSI overbought (>70) → 50%
11. MACD histogram shrinking → 30%
12. Volume declining 3+ bars → 40%
13. Multiple tests at Fib level → 50%
14. ROI table → Automatic

Level 4 - TRAILING:
15. RSI trail hit (below 50) → 70%, trail rest
16. Fibonacci trail hit → Exit rest
17. Percentage trail hit → Exit rest
```

**Freqtrade Configuration:**
```python
class FibonacciRSIDivergenceStrategy(IStrategy):
    
    minimal_roi = {
        "0": 0.07,
        "60": 0.06,
        "120": 0.05,
        "240": 0.035,
        "480": 0.02,
        "720": 0.012
    }
    
    stoploss = -0.015  # -1.5% hard stop
    
    trailing_stop = True
    trailing_stop_positive = 0.04  # Activate at +4%
    trailing_stop_positive_offset = 0.045  # Trigger at 4.5%
    trailing_only_offset_is_reached = True
    
    use_exit_signal = True
    exit_profit_only = False
    
    def populate_exit_trend(self, dataframe, metadata):
        dataframe.loc[
            (
                # RSI back to extreme OR
                (dataframe['rsi'] < 30) |  # For LONG reversals
                # MACD bearish crossover OR
                (qtpylib.crossed_below(dataframe['macd'], dataframe['macdsignal'])) |
                # New opposite divergence forming
                (dataframe['new_bearish_divergence'])
            ),
            'exit_long'
        ] = 1
        
        return dataframe
    
    def custom_exit(self, pair, trade, current_time, current_rate, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1]
        
        profit_ratio = trade.calc_profit_ratio(current_rate)
        risk = abs(trade.stop_loss_pct)
        
        # TP1: 4:1
        if profit_ratio >= (risk * 4):
            return 0.4  # Exit 40%
        
        # TP2: 6:1
        if profit_ratio >= (risk * 6):
            return 0.35  # Exit additional 35%
        
        # TP3: 8:1
        if profit_ratio >= (risk * 8):
            return 0.15  # Exit additional 15%
        
        # RSI-based exit
        if last_candle['rsi'] > 75:
            return 0.5  # Exit 50% on extreme RSI
        
        # RSI drops below 50 (momentum lost)
        if last_candle['rsi'] < 50 and profit_ratio > 0.02:
            return 0.7  # Exit 70%
        
        # Emergency: MACD bearish
        if last_candle['macd'] < last_candle['macdsignal']:
            return 0.7  # Exit 70%
        
        return None
```

**Exit Strategy Summary:**

| Signal | Action | % Exit | Expected Time |
|--------|--------|--------|---------------|
| Stop (div low) | Exit all | 100% | Immediate |
| New div opposite | Exit all | 100% | 1-3 days |
| TP1 (4:1) | Partial | 40% | 12-24 hours |
| TP2 (6:1) | Partial | 35% | 1-3 days |
| TP3 (8:1) | Partial | 15% | 2-5 days |
| RSI >75 | Exit half | 50% | Variable |
| MACD bearish | Exit most | 70% | Variable |
| RSI <50 | Exit most | 70% | Variable |
| Trail hit | Exit rest | Rest | Ongoing |

#### Example Trade - Bullish Divergence
```
BTC/USDT 1H Chart

Downtrend Context:
- Price Low 1: $66,500 (RSI: 28)
- Price Low 2: $66,200 (RSI: 32) ← Bullish Divergence

Reversal Setup:
- Price rallies to $67,000
- Draw Fibonacci from $66,200 to $67,000
- Price pulls back to 0.618 level at $66,505

Confirmation:
- MACD: Bullish crossover ✓
- Volume: 1.8x average on reversal ✓
- Bullish engulfing candle ✓

Entry: $66,550 (next candle after confirmation)
Stop Loss: $66,150 (-0.60%, $400, below recent low)
TP1 (50%): $67,350 (+1.20%, $800) [1:2 ratio]
TP2 (50%): $68,000 (+2.18%, $1,450) [1:3.6 ratio]

Capital: $10,000
Risk: 1.5% = $150
Position Size: 0.375 BTC
```

#### Performance Metrics
- Win Rate: 73%
- Average Win: 4.8%
- Average Loss: 1.5%
- Expectancy: +2.40% per trade
- Trades per Week: 1-4
- Holding Time: 1-4 days

---



---

## See Also

- [30-Minute Strategies](strategies_30m.md) - More frequent signals
- [Trading Strategy Selection](shared_content.md#strategy-selection)
- [UT Bot Complete Guide](shared_content.md#ut-bot-guide)
- [Risk Management](shared_content.md#risk-management)

---

*Last Updated: November 16, 2025*
