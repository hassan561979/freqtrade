"""
Base Strategy with Performance Filtering
Inherit from this class to automatically get performance tracking in both live and backtest modes.

Usage:
    from strategies.base import PerformanceFilterStrategy
    
    class MyStrategy(PerformanceFilterStrategy):
        # Your strategy code here
        # Performance tracking is automatic!
"""

from freqtrade.strategy import IStrategy, BooleanParameter, DecimalParameter, IntParameter
from freqtrade.persistence import Trade
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Dynamic lookback periods based on timeframe
PERFORMANCE_LOOKBACK = {
    '1m':  {'trades': 20, 'hours': 12},
    '5m':  {'trades': 15, 'hours': 24},
    '15m': {'trades': 12, 'hours': 48},
    '30m': {'trades': 10, 'hours': 72},
    '1h':  {'trades': 10, 'hours': 168},
    '4h':  {'trades': 8,  'hours': 336},
    '1d':  {'trades': 5,  'hours': 720},
}


class PerformanceFilterStrategy(IStrategy):
    """
    Base strategy class with built-in performance tracking.
    
    Features:
    - Tracks win rate per trading pair
    - Works in both backtest and live/dry-run modes (unified approach!)
    - Automatically blocks underperforming pairs
    - Configurable via hyperopt parameters
    
    To use: Inherit from this class instead of IStrategy
    """
    
    # ============================================================
    # PERFORMANCE FILTER PARAMETERS (Can be hyperopt optimized)
    # ============================================================
    performance_filter_enabled = BooleanParameter(
        default=True, 
        space="buy",
        optimize=True,
        load=True
    )
    
    min_win_rate = DecimalParameter(
        0.3, 0.6, 
        default=0.4, 
        decimals=2,
        space="buy",
        optimize=True,
        load=True
    )
    
    min_trades_required = IntParameter(
        5, 20, 
        default=10, 
        space="buy",
        optimize=True,
        load=True
    )
    
    cooldown_after_loss_enabled = BooleanParameter(
        default=False, 
        space="buy",
        optimize=True,
        load=True
    )
    
    cooldown_hours = IntParameter(
        1, 24, 
        default=4, 
        space="buy",
        optimize=True,
        load=True
    )
    
    def __init__(self, config: dict) -> None:
        super().__init__(config)
        
        # Detect run mode (for logging purposes)
        self.is_backtesting = config.get('runmode') in ['backtest', 'hyperopt']
        
        logger.info(f"🎯 Performance Filter initialized (Mode: {'Backtest' if self.is_backtesting else 'Live/Dry-run'})")
        
        # Note: In backtest, Freqtrade creates in-memory SQLite database
        # So we can use Trade.get_trades() in BOTH modes!
        # No need for separate in-memory tracking
    
    def bot_start(self, **kwargs) -> None:
        """Called when bot starts"""
        if self.performance_filter_enabled.value:
            logger.info(
                f"✅ Performance Filter ENABLED - "
                f"Min Win Rate: {self.min_win_rate.value:.1%}, "
                f"Min Trades: {self.min_trades_required.value}"
            )
        else:
            logger.info("⚠️  Performance Filter DISABLED")
    
    def get_pair_performance(self, pair: str) -> dict:
        """
        Get recent performance for a specific pair.
        ✅ Works in BOTH backtest and live/dry-run modes!
        
        Freqtrade creates an in-memory SQLite database in backtest mode,
        so we can use Trade.get_trades() for both modes - no separate tracking needed!
        
        Args:
            pair: Trading pair (e.g., "BTC/USDT")
            
        Returns:
            dict with keys:
                - win_rate: Win rate as decimal (0.45 = 45%)
                - total_profit: Total profit percentage
                - avg_profit: Average profit per trade
                - trade_count: Number of trades analyzed
                - winning_trades: Number of winning trades
                - losing_trades: Number of losing trades
                - allow_trade: True if pair passes filter
                - reason: Explanation of decision
        """
        lookback_config = PERFORMANCE_LOOKBACK.get(self.timeframe, {'trades': 10, 'hours': 24})
        
        # Query closed trades from database (works in BOTH backtest and live!)
        try:
            trades = Trade.get_trades([
                Trade.pair == pair,
                Trade.is_open.is_(False),
                Trade.close_date >= datetime.now() - timedelta(hours=lookback_config['hours'])
            ]).order_by(Trade.close_date.desc()).limit(lookback_config['trades']).all()
        except Exception as e:
            # If database not ready (very early in backtest), allow all trades
            logger.debug(f"Could not query trades for {pair}: {e}")
            return {
                'win_rate': None,
                'total_profit': 0,
                'trade_count': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'avg_profit': 0,
                'allow_trade': True,
                'reason': 'database_not_ready'
            }
        
        # Check if we have enough history
        if len(trades) < self.min_trades_required.value:
            return {
                'win_rate': None,
                'total_profit': 0,
                'trade_count': len(trades),
                'winning_trades': 0,
                'losing_trades': 0,
                'avg_profit': 0,
                'allow_trade': True,
                'reason': 'insufficient_history'
            }
        
        # Calculate statistics
        winning_trades = [t for t in trades if t.close_profit > 0]
        losing_trades = [t for t in trades if t.close_profit <= 0]
        
        win_rate = len(winning_trades) / len(trades)
        total_profit_pct = sum(t.close_profit for t in trades) * 100
        avg_profit = total_profit_pct / len(trades)
        
        # Decision: Allow trade if win rate is acceptable
        allow_trade = win_rate >= self.min_win_rate.value
        
        return {
            'win_rate': win_rate,
            'total_profit': total_profit_pct,
            'avg_profit': avg_profit,
            'trade_count': len(trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'allow_trade': allow_trade,
            'reason': 'win_rate_ok' if allow_trade else 'win_rate_too_low'
        }
    
    def is_pair_in_cooldown(self, pair: str) -> bool:
        """
        Check if pair is in cooldown period after recent loss.
        ✅ Works in BOTH backtest and live/dry-run modes!
        
        Args:
            pair: Trading pair (e.g., "BTC/USDT")
            
        Returns:
            True if pair should be blocked (in cooldown), False otherwise
        """
        if not self.cooldown_after_loss_enabled.value:
            return False
        
        try:
            # Query last closed trade (works in both backtest and live!)
            last_trade = Trade.get_trades([
                Trade.pair == pair,
                Trade.is_open.is_(False)
            ]).order_by(Trade.close_date.desc()).first()
            
            if not last_trade:
                return False
            
            # If last trade was a loss, check cooldown
            if last_trade.close_profit < 0:
                time_since_close = datetime.now() - last_trade.close_date
                
                if time_since_close.total_seconds() < (self.cooldown_hours.value * 3600):
                    logger.info(
                        f"⏸️  {pair}: In cooldown for "
                        f"{self.cooldown_hours.value - time_since_close.total_seconds()/3600:.1f}h "
                        f"after loss of {last_trade.close_profit*100:.2f}%"
                    )
                    return True
        except Exception as e:
            # If database query fails, don't block (fail-safe)
            logger.debug(f"Cooldown check failed for {pair}: {e}")
            return False
        
        return False
    
    def should_allow_trade(self, pair: str) -> tuple[bool, str]:
        """
        Main filter method: Check if trade should be allowed for this pair.
        Call this in your populate_entry_trend() method.
        
        Args:
            pair: Trading pair (e.g., "BTC/USDT")
            
        Returns:
            tuple: (allow: bool, reason: str)
        """
        if not self.performance_filter_enabled.value:
            return True, "filter_disabled"
        
        # Check cooldown
        if self.is_pair_in_cooldown(pair):
            return False, "cooldown_period"
        
        # Check performance
        perf = self.get_pair_performance(pair)
        
        if not perf['allow_trade']:
            logger.info(
                f"❌ {pair}: Performance filter BLOCKED - "
                f"Win rate: {perf['win_rate']:.1%} (min: {self.min_win_rate.value:.1%}), "
                f"Recent profit: {perf['total_profit']:.2f}%, "
                f"Last {perf['trade_count']} trades: {perf['winning_trades']}W/{perf['losing_trades']}L"
            )
            return False, perf['reason']
        
        return True, "performance_ok"
