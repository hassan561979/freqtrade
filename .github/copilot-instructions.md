# Freqtrade Project - Copilot Instructions

## Project Overview
This is a Freqtrade trading bot project running in Docker with custom strategies for cryptocurrency trading on Binance.

## Docker Setup
- **Container name**: `freqtrade`
- **Image**: `freqtradeorg/freqtrade:stable`
- **User data mount**: `/Users/mac-lab/Documents/my/freqtrade/user_data` → `/freqtrade/user_data`
- **Always use Docker**: Run all freqtrade commands inside the container using `docker exec freqtrade <command>`

## Custom Backtest Visualization

### Background
We created both a static HTML report generator and a dynamic Flask-based web server to visualize backtest results with better formatting and filtering capabilities than the default Freqtrade output.

### Dynamic Report Server (Recommended)
**Location**: `user_data/report_server.py`

**Features**:
- Flask web server running on port 8081
- Real-time data loading from latest backtest
- Manual refresh button (auto-refresh disabled)
- All features from static report plus dynamic updates
- Access at: http://localhost:8081/backtest_report

**Running the Server**:
```bash
# Quick start/restart using the shell script
./user_data/start_report_server.sh
```

**Script content** (`start_report_server.sh`):
```bash
#!/bin/bash
# Start/Restart Backtest Report Server
# This script kills any existing server and starts a fresh one

echo "🔄 Stopping existing report server..."
docker exec freqtrade pkill -f report_server.py 2>/dev/null || true

echo "⏳ Waiting for process to stop..."
sleep 2

echo "🚀 Starting report server..."
docker exec freqtrade bash -c "cd /freqtrade/user_data && python report_server.py > /tmp/report_server.log 2>&1 &"

echo "⏳ Waiting for server to start..."
sleep 3

echo "✅ Report server started!"
echo "📊 Access at: http://localhost:8081/backtest_report"
echo ""
echo "📋 To check server logs:"
echo "   docker exec freqtrade tail -f /tmp/report_server.log"
echo ""
echo "🛑 To stop the server:"
echo "   docker exec freqtrade pkill -f report_server.py"
```

**Manual Commands**:
```bash
# Start server manually
docker exec freqtrade bash -c "cd /freqtrade/user_data && python report_server.py > /tmp/report_server.log 2>&1 &"

# Check logs
docker exec freqtrade tail -f /tmp/report_server.log

# Stop server
docker exec freqtrade pkill -f report_server.py
```

**Important Notes**:
- Flask runs with `debug=True` for auto-reload on code changes
- Server must be restarted after modifying `report_server.py`
- Port 8081 is exposed in `docker-compose.yml`
- API endpoint available at: http://localhost:8081/api/backtest_data

### Static Report Generator (Legacy)
**Location**: `user_data/generate_report.py`

**Features**:
- Reads from `.last_result.json` to automatically find the latest backtest
- Extracts data from ZIP files containing JSON results
- Generates styled HTML report with:
  - Key metrics cards (profit, trades, win rate, drawdown)
  - Performance by trading pair
  - Exit reasons analysis
  - Top 10 winning and losing trades
  - Interactive coin filter dropdown
  - Color-coded profit/loss indicators

**Key Implementation Details**:
1. **Profit Calculation Fix**: Freqtrade stores `profit_total` as decimal (0.13 = 13%), so we multiply by 100 for percentage display:
   ```python
   profit_total_pct = strategy_data['profit_total'] * 100
   ```

2. **Show All Trades**: Changed from showing last 50 trades to all trades:
   ```python
   # Before: for i, trade in enumerate(trades[-50:], 1):
   # After:
   for i, trade in enumerate(trades, 1):
   ```

3. **Latest Backtest Reference**: Uses `.last_result.json` instead of finding newest file by timestamp:
   ```python
   last_result = json.load(open('backtest_results/.last_result.json'))
   latest_file = last_result['latest_backtest']
   ```

4. **Coin Filter**: Added JavaScript dropdown to filter trades by trading pair (SOL/USDT, XRP/USDT, All Pairs)

### Running the Report Generator
```bash
# Generate and open report
docker exec -w /freqtrade/user_data freqtrade python generate_report.py && \
sleep 1 && \
open /Users/mac-lab/Documents/my/freqtrade/user_data/backtest_results/backtest_report.html
```

**Output**: `user_data/backtest_results/backtest_report.html`

### Browser Caching Issues
If the HTML report shows old data:
```bash
# Delete cached HTML file before regenerating
docker exec freqtrade rm -f /freqtrade/user_data/backtest_results/backtest_report.html
```

## Backtest Date Range Configuration

### The Startup Period Problem
Freqtrade requires a **30-candle startup period** (for 30m timeframe = 15 hours) to calculate indicators before the first trade. This delays the actual backtest start time.

**Example**:
- Request backtest from: `2025-10-15 00:00:00`
- Data downloaded from: `2025-10-15 00:00:00`
- Actual backtest starts: `2025-10-15 15:00:00` (15 hours later)

### Solution: Download Earlier Data
To start backtesting at the exact date you want, download data from **2 days earlier** to provide buffer for the startup period:

```bash
# To backtest from Oct 15 - Nov 12
# Download data from Oct 13 (2 days earlier)
docker exec freqtrade freqtrade download-data \
  --exchange binance \
  --pairs SOL/USDT XRP/USDT \
  --timeframe 30m \
  --timerange 20251013-20251113 \
  --prepend

# Then run backtest with desired date range
docker exec freqtrade freqtrade backtesting \
  --strategy StochCrossStrategy \
  --timerange 20251015-20251112 \
  --cache none
```

**Important flags**:
- `--prepend`: Adds earlier data to existing files (instead of overwriting)
- `--cache none`: Forces fresh calculation (avoids reusing cached results)

### Verifying Start Time
Check the backtest output for:
```
Backtesting from: 2025-10-15 00:00:00  ← Should match your desired start
Backtesting to: 2025-11-12 00:00:00
```

If it shows `15:00:00` instead of `00:00:00`, you need to download more historical data.

## Git Configuration

### Strategy Files and .gitignore
By default, `user_data/*` is excluded from git tracking in `.gitignore`. To track strategy files:

**Option 1 - Track all strategy files** (Recommended):
Add to `.gitignore`:
```
!user_data/strategies/*.py
```

**Option 2 - Force add specific file**:
```bash
git add -f user_data/strategies/StochCrossStrategy.py
```

## Current Strategy: StochCrossStrategy

**Location**: `user_data/strategies/StochCrossStrategy.py`

**Logic**:
- **Entry**: When Stochastic K line crosses above D line
- **Exit**: When Stochastic K line crosses below D line
- **Parameters**: 
  - stoch_k = 14
  - stoch_smooth_k = 1
  - stoch_d = 3
- **ROI**: 4% immediate, 2% at 30min, 1% at 60min
- **Stoploss**: -10%
- **Timeframe**: 30m

**Current Performance** (Oct 15 - Nov 12, 2025):
- Total trades: 543
- Win rate: 27.6%
- Total profit: -13.09% (-130.886 USDT)
- ROI exits: +101.82 USDT (profitable)
- Exit signals: -232.71 USDT (losing)

**Performance Analysis**:
- ROI exits are working well (100% win rate)
- Exit signals are the main source of losses (14.2% win rate)
- Strategy needs improvement, possibly by adjusting exit signal logic or Stochastic parameters

## Common Commands

### Data Download
```bash
docker exec freqtrade freqtrade download-data \
  --exchange binance \
  --pairs SOL/USDT XRP/USDT \
  --timeframe 30m \
  --timerange 20251013-20251113
```

### Run Backtest
```bash
docker exec freqtrade freqtrade backtesting \
  --strategy StochCrossStrategy \
  --timerange 20251015-20251112
```

### Start Report Server
```bash
./user_data/start_report_server.sh
```

### Generate Static Report (Legacy)
```bash
docker exec -w /freqtrade/user_data freqtrade python generate_report.py
```

### Check Backtest Results
```bash
# List backtest files
docker exec freqtrade ls -lh /freqtrade/user_data/backtest_results/

# View latest result reference
docker exec freqtrade cat /freqtrade/user_data/backtest_results/.last_result.json
```

## Troubleshooting

### Report Shows Wrong Data
1. Delete cached HTML: `docker exec freqtrade rm -f /freqtrade/user_data/backtest_results/backtest_report.html`
2. Regenerate report: `docker exec -w /freqtrade/user_data freqtrade python generate_report.py`

### Backtest Starts Too Late
1. Download data from 2 days earlier with `--prepend` flag
2. Run backtest with `--cache none` to force recalculation

### Strategy Not Tracked by Git
1. Check `.gitignore` for `user_data/*` exclusion
2. Add exception: `!user_data/strategies/*.py`
3. Or force add: `git add -f user_data/strategies/YourStrategy.py`

### Docker Container Not Running
```bash
# Start the container
docker compose up -d

# Check status
docker ps | grep freqtrade
```

## Development Workflow

1. **Create/modify strategy** in `user_data/strategies/`
2. **Download data** with 2-day buffer for startup period
3. **Run backtest** with `--cache none` for fresh results
4. **Generate HTML report** with `generate_report.py`
5. **Analyze results** in the browser (check exit reasons, win rates by pair)
6. **Iterate** on strategy parameters based on analysis
7. **Commit changes** to git (remember to track strategy files)

## Key Learnings

1. **Always use Docker**: All freqtrade operations must run inside the container
2. **Startup period matters**: Download data 2 days earlier than your desired backtest start
3. **Browser caching**: Delete HTML file if report shows stale data
4. **Profit calculation**: Freqtrade stores decimals, multiply by 100 for percentages
5. **Cache awareness**: Use `--cache none` when you need fresh backtest calculations
6. **Git tracking**: User data is ignored by default, add exceptions for files you want to track
