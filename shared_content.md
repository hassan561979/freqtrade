# Shared Trading Content
*Common Resources for All Timeframes*

---

## Navigation
- [Back to Main Guide](TRADING_STRATEGIES_GUIDE.md)
- [1-Minute Strategies](strategies_1m.md)
- [5-Minute Strategies](strategies_5m.md)
- [15-Minute Strategies](strategies_15m.md)
- [30-Minute Strategies](strategies_30m.md)
- [1-Hour Strategies](strategies_1h.md)

---

## Table of Contents
1. [UT Bot Indicator Guide](#ut-bot-indicator-guide)
2. [Risk Management](#risk-management)
3. [Implementation Tips](#implementation-tips)
4. [Strategy Selection Guide](#strategy-selection-guide)

---


### What is UT Bot?

The UT Bot (Universal Trend Bot) is a powerful trend-following indicator that combines **Average True Range (ATR)** calculations with intelligent trailing stop technology to generate precise buy and sell signals.

### How UT Bot Works

**Core Components:**
1. **ATR Calculation**: Measures market volatility over a specified period (default: 10 periods)
2. **Trailing Stop Formula**: `Trailing Stop = Key Value × ATR`
3. **Dynamic Stop Level**: Moves with price action while maintaining distance proportional to volatility

**Key Settings:**
- **Key Value**: ATR multiplier determining sensitivity
  - Original HPotter setting: 3.5 multiplier, 5 ATR period
  - Crypto trading: 3.5-4.0 (higher volatility)
  - Forex/Stocks: 2.5-3.0 (lower volatility)

**Signal Generation:**
- **Long Signal**: EMA crosses above ATR trailing stop
- **Short Signal**: EMA crosses below ATR trailing stop

**Important Characteristics:**
- ✅ No repainting - signals confirm on bar close
- ✅ Clear visual signals (green/red dots)
- ✅ Built-in trailing stop (white line)
- ⚠️ Requires context and judgment (not purely mechanical)

---



---


## Risk Management

### Position Sizing Formula

**Standard Formula:**
```
Position Size = (Account Balance × Risk %) / (Entry Price - Stop Loss Price)

Example:
Account: $10,000
Risk per trade: 2% = $200
Entry: $67,500
Stop Loss: $67,000
Risk per coin: $500

Position Size = $200 / $500 = 0.4 BTC
Dollar Value = 0.4 × $67,500 = $27,000
```

### Risk Per Trade Guidelines

**Conservative (Beginner):**
- Risk: 0.5-1% per trade
- Max open trades: 2-3
- Total risk exposure: 1.5-3%

**Moderate (Intermediate):**
- Risk: 1-2% per trade
- Max open trades: 3-5
- Total risk exposure: 3-10%

**Aggressive (Advanced):**
- Risk: 2-3% per trade
- Max open trades: 5-8
- Total risk exposure: 10-24%

### Stop Loss Strategies

**1. ATR-Based Stop:**
```
Stop Distance = Entry - (ATR × Multiplier)

Conservative: 1.5 × ATR
Moderate: 2.0 × ATR
Wide: 2.5 × ATR
```

**2. Support/Resistance Stop:**
```
LONG: Place stop below recent support/swing low
SHORT: Place stop above recent resistance/swing high

Buffer: Add 0.1-0.3% beyond level to avoid stop hunting
```

**3. Percentage Stop:**
```
Fixed percentage from entry:
Scalping (1m-5m): 0.3-0.8%
Day trading (15m-1H): 1.0-2.0%
Swing trading (4H-Daily): 2.0-5.0%
```

### Take Profit Strategies

**Scaled Exit Method (Recommended):**
```
TP1 (30-50%): 1:1 or 1:2 ratio → Move stop to break-even
TP2 (25-35%): 1:3 or 1:4 ratio → Secure major profit
TP3 (20-25%): Trail or 1:5+ ratio → Let winners run
```

**Example:**
```
Entry: $67,500
Stop: $67,000 (risk = $500)
TP1 (50%): $68,500 (1:2, reward = $1,000)
TP2 (30%): $69,500 (1:4, reward = $2,000)
TP3 (20%): Trail with 1H EMA

If all targets hit:
Total Profit = (0.5 × $1,000) + (0.3 × $2,000) + (0.2 × $3,000+)
             = $500 + $600 + $600+
             = $1,700+ (3.4:1 average)
```

### Daily Loss Limit

**Rule:** Stop trading if you hit daily loss limit

**Formula:**
```
Daily Loss Limit = Account × Daily Risk %

Conservative: 2-3% of account
Moderate: 3-5% of account
Aggressive: 5-8% of account

Example ($10,000 account, 3% daily limit):
Daily Loss Limit = $300

If you lose:
Trade 1: -$150
Trade 2: -$100
Total: -$250 (83% of limit)
Action: Take only 1 more high-probability trade OR stop for the day
```

### Weekly/Monthly Limits

**Weekly Loss Limit:** 10-15% of account  
**Monthly Loss Limit:** 20-30% of account  

**If exceeded:**
- Stop trading for remainder of period
- Review all trades
- Identify mistakes
- Adjust strategy if needed
- Consider reducing position size

### Leverage Guidelines

**Spot Trading (No Leverage):**
- Safest option
- No liquidation risk
- Best for beginners
- Required capital: 100% of position

**Low Leverage (2x-3x):**
- Moderate risk
- Capital efficiency
- Liquidation possible but unlikely with proper stops
- Required capital: 33-50% of position

**Medium Leverage (5x-10x):**
- High risk
- Advanced traders only
- Tight stop losses required
- Required capital: 10-20% of position

**High Leverage (>10x):**
- Extreme risk
- Expert traders only
- Not recommended for most strategies
- Required capital: <10% of position

**Leverage Example:**
```
Account: $10,000
Trade Setup: BTC at $67,500
Risk: 2% = $200
Stop Loss: 1% away

Spot Trading:
Max Position = $10,000 (0.148 BTC)
Loss if stopped = $200

5x Leverage:
Margin Required = $2,000
Position Value = $10,000 (0.148 BTC)
Loss if stopped = $200
Extra capital available = $8,000 for other trades

Warning: 5x means a 20% move against you = liquidation
Always use stops!
```

---

## Implementation Tips

### Backtesting Requirements

Before trading any strategy live:

**Minimum Standards:**
- Backtest period: 3-6 months minimum
- Number of trades: 100+ samples
- Win rate: >55% for discretionary, >60% for mechanical
- Risk:Reward: >1:1.5 average
- Maximum drawdown: <20%

**Process:**
```
1. Historical Data Collection
   - Get clean OHLCV data for your timeframe
   - Include at least 6 months of data
   - Test on multiple market conditions (trending, ranging, volatile)

2. Manual Backtesting
   - Go candle by candle
   - Mark every setup
   - Record all trades (wins and losses)
   - Calculate metrics

3. Forward Testing (Paper Trading)
   - Trade strategy live without real money
   - Minimum 1 month or 30+ trades
   - Document every trade with screenshots
   - Compare to backtest results

4. Live Trading (Small Size)
   - Start with 10-25% of intended position size
   - Gradually increase as confidence grows
   - Maintain same risk:reward ratios
   - Track psychological factors
```

### Trade Journal Template

**Required Fields:**
```
Date/Time: [timestamp]
Pair: [BTC/USDT]
Timeframe: [15m]
Strategy: [UT Bot + 100 MA]
Setup Quality: [A/B/C grade]

ENTRY:
Price: [$67,500]
Reasoning: [UT Bot buy signal above 100 MA, volume spike]
Position Size: [0.148 BTC]
Risk Amount: [$200]

EXIT:
Stop Loss: [$67,200]
TP1: [$68,400]
TP2: [$69,100]

RESULT:
Exit Price: [$68,600]
P/L: [+$1,100]
R:R: [1:5.5]
Outcome: [Winner/Loser]
Mistakes: [None / Entered too late / etc.]

EMOTIONAL STATE:
Before: [Calm / Anxious / Excited]
During: [Patient / Impatient / Fearful]
After: [Satisfied / Frustrated / Overconfident]

SCREENSHOTS:
[Attach chart screenshots at entry and exit]
```

### Common Mistakes to Avoid

**1. Overtrading**
```
Problem: Taking too many low-quality setups
Solution:
- Wait for A-grade setups only
- Max 3-5 trades per day (5m-15m)
- Max 1-2 trades per day (1H-4H)
- If you lose 2 in a row, stop for the day
```

**2. Moving Stop Loss**
```
Problem: Moving stop further away when price approaches
Solution:
- Set stop and NEVER move it wider
- Only move stop to break-even or trail profits
- If you're tempted to move it, close the trade
```

**3. Revenge Trading**
```
Problem: Trying to "get back" money after a loss
Solution:
- Take a 30-minute break after any loss
- Review what went wrong
- Stick to your trading plan
- Remember: losses are part of the game
```

**4. Ignoring Risk Management**
```
Problem: Taking trades without proper position sizing
Solution:
- Calculate position size BEFORE every trade
- Never risk more than your limit
- Use a position size calculator
- No exceptions!
```

**5. FOMO (Fear of Missing Out)**
```
Problem: Chasing price after missing entry
Solution:
- If you miss entry, wait for next setup
- Never enter in the middle of a move
- There's always another opportunity
- Patience = Profitability
```

### Platform Setup

**Recommended Platforms:**

**Trading:**
- Binance (Best for crypto, low fees)
- Bybit (Good leverage options)
- Coinbase (Best for US traders)

**Charting:**
- TradingView (Industry standard)
  - Pro+ Plan recommended
  - Custom indicators
  - Multi-timeframe analysis

**Bots:**
- Freqtrade (Open source, Python)
- 3Commas (User-friendly, cloud-based)
- Cryptohopper (Automated strategies)

**Alert System:**
```
TradingView Alerts Setup:
1. Create alert on indicator signal
2. Set to "Only Once" per bar close
3. Connect to:
   - Email
   - SMS (via Zapier)
   - Telegram bot
   - Discord webhook
```

### Performance Tracking

**Weekly Review Checklist:**
```
□ Total trades taken: ___
□ Win rate: ___% (target: >60%)
□ Average win: ___% 
□ Average loss: ___%
□ Largest win: ___%
□ Largest loss: ___%
□ Total P/L: $___ (___%)
□ Best trading day: ___
□ Worst trading day: ___
□ Mistakes made: [list]
□ Lessons learned: [list]
□ Strategy adjustments needed: [Y/N]
```

**Monthly Goals:**
```
Account Start: $___
Account End: $___
Target: ___% (realistic: 5-15% per month)
Actual: ___%

Max Drawdown: ___%
Sharpe Ratio: ___
Number of Trading Days: ___

Top 3 Winners:
1. [Pair, %, reason]
2. [Pair, %, reason]
3. [Pair, %, reason]

Top 3 Losers:
1. [Pair, %, reason]
2. [Pair, %, reason]
3. [Pair, %, reason]

What worked: [list]
What didn't work: [list]
Next month focus: [list]
```

---

## Strategy Selection Guide

**Choose Based on:**

**Time Available:**
- <2 hours/day: 1H strategies
- 2-4 hours/day: 30m strategies
- 4-6 hours/day: 15m strategies
- Full-time: 5m or 1m strategies

**Capital Size:**
- <$500: 1m-5m (smaller positions, frequent trades)
- $500-$2,000: 5m-15m (balanced approach)
- $2,000-$10,000: 15m-30m (fewer, higher quality trades)
- >$10,000: 30m-1H (position trading)

**Risk Tolerance:**
- Conservative: 30m-1H strategies, 0.5-1% risk
- Moderate: 15m-30m strategies, 1-2% risk
- Aggressive: 5m-15m strategies, 2-3% risk

**Experience Level:**
- Beginner: Start with 15m-30m, simple indicators
- Intermediate: 5m-1H, multiple indicators
- Advanced: Any timeframe, complex setups

---

## Final Recommendations

**Best Strategies by Win Rate:**
1. Strategy 30A (Multi-Timeframe): 74% win rate
2. Strategy 1HC (Fibonacci + RSI Div): 73% win rate
3. Strategy 5C (Triple Confirmation): 75% win rate
4. Strategy 5A (UT Bot + 100 MA): 72% win rate

**Best Strategies by R:R:**
1. Strategy 1HC: Average 1:4.2 ratio
2. Strategy 30A: Average 1:3.9 ratio
3. Strategy 1HB: Average 1:3.0 ratio
4. Strategy 5A: Average 1:2.8 ratio

**Best Strategies for Beginners:**
1. Strategy 5A (UT Bot + 100 MA): Clear signals, simple rules
2. Strategy 15A (Multi-Indicator): Well-defined conditions
3. Strategy 30B (Support/Resistance): Easy to understand

**Best Strategies for Advanced:**
1. Strategy 30A (Multi-Timeframe): Complex analysis, high accuracy
2. Strategy 5B (Order Blocks + FVG): Institutional concepts
3. Strategy 1HC (Fibonacci + Divergence): Pattern recognition

---

## Disclaimer

**Important:** 
- Past performance does not guarantee future results
- All win rates and metrics are based on backtested data
- Real trading results may vary significantly
- Never trade with money you cannot afford to lose
- Always practice on demo accounts first
- Consider seeking professional financial advice
- Cryptocurrency markets are highly volatile
- No strategy is 100% profitable

**Risk Warning:**
Trading cryptocurrencies involves substantial risk of loss. You should only trade with risk capital that you can afford to lose. The strategies outlined here are for educational purposes only and do not constitute financial advice.

---

*Document Version: 1.0*  
*Last Updated: November 15, 2025*  
*For updates and community discussion: [Your Platform/Link]*
