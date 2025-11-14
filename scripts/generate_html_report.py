#!/usr/bin/env python3
"""
Generate HTML report from Freqtrade backtest results
Run inside Docker: docker compose run --rm --entrypoint python freqtrade /freqtrade/user_data/generate_html_report.py
"""

import json
import zipfile
from pathlib import Path
from datetime import datetime

def load_latest_backtest():
    """Load the latest backtest result from ZIP file"""
    results_dir = Path('/freqtrade/user_data/backtest_results')
    
    # Find latest .zip file
    zip_files = list(results_dir.glob('backtest-result-*.zip'))
    if not zip_files:
        print("No backtest results found!")
        return None
    
    latest_zip = max(zip_files, key=lambda p: p.stat().st_mtime)
    print(f"Loading: {latest_zip.name}")
    
    # Extract JSON from ZIP
    with zipfile.ZipFile(latest_zip, 'r') as z:
        json_files = [f for f in z.namelist() if f.endswith('.json') and '_config' not in f and '_market' not in f]
        if not json_files:
            return None
        
        with z.open(json_files[0]) as f:
            data = json.load(f)
    
    return data, latest_zip.stem

def generate_html(data, filename):
    """Generate HTML report from backtest data"""
    
    # Extract strategy data
    strategy_data = data['strategy']['StochCrossStrategy']
    trades = strategy_data['trades']
    
    # Calculate statistics
    total_trades = len(trades)
    winning_trades = strategy_data['wins']
    losing_trades = strategy_data['losses']
    win_rate = strategy_data['winrate']
    
    # Group by pair
    pairs_data = {}
    for trade in trades:
        pair = trade['pair']
        if pair not in pairs_data:
            pairs_data[pair] = {'trades': [], 'wins': 0, 'losses': 0}
        pairs_data[pair]['trades'].append(trade)
        if trade['profit_ratio'] > 0:
            pairs_data[pair]['wins'] += 1
        else:
            pairs_data[pair]['losses'] += 1
    
    # Group by exit reason
    exit_reasons = {}
    for trade in trades:
        reason = trade['exit_reason']
        if reason not in exit_reasons:
            exit_reasons[reason] = {'count': 0, 'profit': 0, 'wins': 0}
        exit_reasons[reason]['count'] += 1
        exit_reasons[reason]['profit'] += trade['profit_abs']
        if trade['profit_ratio'] > 0:
            exit_reasons[reason]['wins'] += 1
    
    # Get top winning and losing trades
    sorted_trades = sorted(trades, key=lambda x: x['profit_ratio'], reverse=True)
    top_wins = sorted_trades[:10]
    top_losses = sorted_trades[-10:][::-1]
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Backtest Results - StochCrossStrategy</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0,0,0,0.15);
        }}
        
        .metric-card.negative {{
            background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        }}
        
        .metric-card.positive {{
            background: linear-gradient(135deg, #55efc4 0%, #00b894 100%);
        }}
        
        .metric-label {{
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            font-weight: 600;
        }}
        
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #2d3436;
        }}
        
        .metric-subtitle {{
            font-size: 0.9em;
            color: #636e72;
            margin-top: 5px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 1.8em;
            color: #2d3436;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        thead {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        th {{
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 1px;
        }}
        
        td {{
            padding: 15px;
            border-bottom: 1px solid #f0f0f0;
        }}
        
        tr:hover {{
            background: #f8f9fa;
        }}
        
        .profit-positive {{
            color: #00b894;
            font-weight: bold;
        }}
        
        .profit-negative {{
            color: #d63031;
            font-weight: bold;
        }}
        
        .badge {{
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .badge-success {{
            background: #00b894;
            color: white;
        }}
        
        .badge-danger {{
            background: #d63031;
            color: white;
        }}
        
        .badge-info {{
            background: #0984e3;
            color: white;
        }}
        
        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #00b894 0%, #55efc4 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
            transition: width 0.5s ease;
        }}
        
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Backtest Results</h1>
            <p>StochCrossStrategy | {strategy_data['backtest_start']} to {strategy_data['backtest_end']}</p>
        </div>
        
        <div class="content">
            <!-- Key Metrics -->
            <div class="metrics-grid">
                <div class="metric-card {'negative' if results_metrics['profit_total'] < 0 else 'positive'}">
                    <div class="metric-label">Total Profit</div>
                    <div class="metric-value">{results_metrics['profit_total']:.2f}%</div>
                    <div class="metric-subtitle">{results_metrics['profit_total_abs']:.2f} USDT</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Total Trades</div>
                    <div class="metric-value">{total_trades}</div>
                    <div class="metric-subtitle">{results_metrics['trades_per_day']:.1f} per day</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Win Rate</div>
                    <div class="metric-value">{win_rate:.1f}%</div>
                    <div class="metric-subtitle">{winning_trades}W / {losing_trades}L</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Max Drawdown</div>
                    <div class="metric-value">{results_metrics['max_drawdown_account']:.2f}%</div>
                    <div class="metric-subtitle">{results_metrics['max_drawdown_abs']:.2f} USDT</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Best Trade</div>
                    <div class="metric-value profit-positive">+{results_metrics['profit_total_max']:.2f}%</div>
                </div>
                
                <div class="metric-card">
                    <div class="metric-label">Worst Trade</div>
                    <div class="metric-value profit-negative">{results_metrics['profit_total_min']:.2f}%</div>
                </div>
            </div>
            
            <!-- Win Rate Progress -->
            <div class="section">
                <h2 class="section-title">Win/Loss Distribution</h2>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {win_rate}%">{winning_trades} Wins ({win_rate:.1f}%)</div>
                </div>
                <div style="display: flex; justify-content: space-between; color: #666; font-size: 0.9em; margin-top: 5px;">
                    <span>Winning Trades: {winning_trades}</span>
                    <span>Losing Trades: {losing_trades}</span>
                </div>
            </div>
            
            <!-- Performance by Pair -->
            <div class="section">
                <h2 class="section-title">Performance by Trading Pair</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Pair</th>
                            <th>Trades</th>
                            <th>Wins</th>
                            <th>Losses</th>
                            <th>Win Rate</th>
                            <th>Total Profit</th>
                            <th>Avg Profit</th>
                        </tr>
                    </thead>
                    <tbody>"""
    
    for pair, data in sorted(pairs_data.items()):
        pair_trades = data['trades']
        pair_wins = data['wins']
        pair_losses = data['losses']
        pair_win_rate = (pair_wins / len(pair_trades) * 100) if pair_trades else 0
        total_profit = sum(t['profit_ratio'] for t in pair_trades) * 100
        avg_profit = total_profit / len(pair_trades) if pair_trades else 0
        profit_class = 'profit-positive' if total_profit > 0 else 'profit-negative'
        
        html += f"""
                        <tr>
                            <td><strong>{pair}</strong></td>
                            <td>{len(pair_trades)}</td>
                            <td>{pair_wins}</td>
                            <td>{pair_losses}</td>
                            <td>{pair_win_rate:.1f}%</td>
                            <td class="{profit_class}">{total_profit:.2f}%</td>
                            <td class="{profit_class}">{avg_profit:.2f}%</td>
                        </tr>"""
    
    html += """
                    </tbody>
                </table>
            </div>
            
            <!-- Exit Reasons -->
            <div class="section">
                <h2 class="section-title">Exit Reasons Analysis</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Exit Reason</th>
                            <th>Count</th>
                            <th>Win Rate</th>
                            <th>Total Profit (USDT)</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>"""
    
    for reason, data in sorted(exit_reasons.items(), key=lambda x: x[1]['profit'], reverse=True):
        reason_win_rate = (data['wins'] / data['count'] * 100) if data['count'] > 0 else 0
        profit_class = 'profit-positive' if data['profit'] > 0 else 'profit-negative'
        badge_class = 'badge-success' if data['profit'] > 0 else 'badge-danger'
        status = '✅ Profitable' if data['profit'] > 0 else '❌ Losing'
        
        html += f"""
                        <tr>
                            <td><strong>{reason}</strong></td>
                            <td>{data['count']}</td>
                            <td>{reason_win_rate:.1f}%</td>
                            <td class="{profit_class}">{data['profit']:.2f}</td>
                            <td><span class="badge {badge_class}">{status}</span></td>
                        </tr>"""
    
    html += """
                    </tbody>
                </table>
            </div>
            
            <!-- Top Winning Trades -->
            <div class="section">
                <h2 class="section-title">🏆 Top 10 Winning Trades</h2>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Pair</th>
                            <th>Entry Date</th>
                            <th>Exit Date</th>
                            <th>Profit %</th>
                            <th>Profit USDT</th>
                            <th>Duration</th>
                            <th>Exit Reason</th>
                        </tr>
                    </thead>
                    <tbody>"""
    
    for idx, trade in enumerate(top_wins, 1):
        profit_pct = trade['profit_ratio'] * 100
        html += f"""
                        <tr>
                            <td>{idx}</td>
                            <td><strong>{trade['pair']}</strong></td>
                            <td>{trade['open_date']}</td>
                            <td>{trade['close_date']}</td>
                            <td class="profit-positive">+{profit_pct:.2f}%</td>
                            <td class="profit-positive">+{trade['profit_abs']:.2f}</td>
                            <td>{trade['trade_duration']} min</td>
                            <td><span class="badge badge-info">{trade['exit_reason']}</span></td>
                        </tr>"""
    
    html += """
                    </tbody>
                </table>
            </div>
            
            <!-- Top Losing Trades -->
            <div class="section">
                <h2 class="section-title">📉 Top 10 Losing Trades</h2>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Pair</th>
                            <th>Entry Date</th>
                            <th>Exit Date</th>
                            <th>Profit %</th>
                            <th>Profit USDT</th>
                            <th>Duration</th>
                            <th>Exit Reason</th>
                        </tr>
                    </thead>
                    <tbody>"""
    
    for idx, trade in enumerate(top_losses, 1):
        profit_pct = trade['profit_ratio'] * 100
        html += f"""
                        <tr>
                            <td>{idx}</td>
                            <td><strong>{trade['pair']}</strong></td>
                            <td>{trade['open_date']}</td>
                            <td>{trade['close_date']}</td>
                            <td class="profit-negative">{profit_pct:.2f}%</td>
                            <td class="profit-negative">{trade['profit_abs']:.2f}</td>
                            <td>{trade['trade_duration']} min</td>
                            <td><span class="badge badge-info">{trade['exit_reason']}</span></td>
                        </tr>"""
    
    html += f"""
                    </tbody>
                </table>
            </div>
            
            <!-- Footer -->
            <div style="text-align: center; padding: 20px; color: #999; border-top: 2px solid #f0f0f0; margin-top: 40px;">
                <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Freqtrade Backtest Report</p>
                <p style="font-size: 0.9em; margin-top: 5px;">File: {filename}</p>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    # Load backtest data
    result = load_latest_backtest()
    if not result:
        print("Failed to load backtest results")
        return
    
    data, filename = result
    
    # Generate HTML
    html = generate_html(data, filename)
    
    # Save to file
    output_file = Path('/freqtrade/user_data/backtest_results/report.html')
    output_file.write_text(html)
    
    print(f"✅ HTML report generated: {output_file}")
    print(f"   Open it in your browser to view the results!")

if __name__ == '__main__':
    main()
