"""
Trade Mirroring System - Utilities Module
Contains helper functions and utilities
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import csv
import os

logger = logging.getLogger(__name__)


def format_currency(amount: float, currency: str = "INR") -> str:
    """Format amount as currency string"""
    if currency == "INR":
        return f"₹{amount:,.2f}"
    return f"{amount:,.2f}"


def calculate_pnl(entry_price: float, current_price: float, quantity: float, side: str) -> Tuple[float, float]:
    """
    Calculate Profit & Loss
    
    Returns: (pnl_amount, pnl_percentage)
    """
    try:
        if side.lower() == 'buy':
            pnl = (current_price - entry_price) * quantity
        else:  # sell
            pnl = (entry_price - current_price) * quantity
        
        pnl_pct = (pnl / (entry_price * quantity)) * 100 if entry_price > 0 else 0
        return pnl, pnl_pct
    except Exception as e:
        logger.error(f"Error calculating P&L: {str(e)}")
        return 0, 0


def validate_api_credentials(api_key: str, api_secret: str) -> Tuple[bool, str]:
    """Validate API credentials format"""
    if not api_key or not api_secret:
        return False, "API Key and Secret are required"
    
    if len(api_key) < 10:
        return False, "API Key seems too short"
    
    if len(api_secret) < 10:
        return False, "API Secret seems too short"
    
    return True, "Credentials format valid"


def export_trades_to_csv(trades: List[Dict], filename: str) -> bool:
    """Export trades to CSV file"""
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        if not trades:
            logger.warning("No trades to export")
            return False
        
        fieldnames = trades[0].keys()
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(trades)
        
        logger.info(f"✓ Trades exported to {filename}")
        return True
    except Exception as e:
        logger.error(f"Error exporting trades: {str(e)}")
        return False


def get_trading_hours() -> Tuple[str, str]:
    """Get NSE trading hours"""
    # NSE Trading: 9:15 AM to 3:30 PM IST
    return "09:15", "15:30"


def is_market_open() -> bool:
    """Check if market is currently open"""
    from datetime import datetime, time
    
    now = datetime.now()
    current_time = now.time()
    
    # Check if weekday (0-4 = Monday-Friday)
    if now.weekday() >= 5:  # Saturday or Sunday
        return False
    
    market_open = time(9, 15)
    market_close = time(15, 30)
    
    return market_open <= current_time <= market_close


def round_to_lot_size(quantity: float, lot_size: float = 1) -> int:
    """Round quantity to nearest lot size"""
    return int((quantity // lot_size) * lot_size)


def calculate_lot_multiplier_adjustment(master_qty: float, follower_qty: float) -> float:
    """Calculate effective lot multiplier from quantities"""
    if master_qty == 0:
        return 0
    return follower_qty / master_qty


def get_market_depth_summary(bid_prices: List[float], ask_prices: List[float]) -> Dict:
    """Analyze market depth"""
    return {
        'best_bid': max(bid_prices) if bid_prices else 0,
        'best_ask': min(ask_prices) if ask_prices else 0,
        'bid_depth': len(bid_prices),
        'ask_depth': len(ask_prices),
        'spread': min(ask_prices) - max(bid_prices) if (bid_prices and ask_prices) else 0
    }


def log_operation(db_manager, account_id: str, operation: str, details: str) -> bool:
    """Log an operation"""
    try:
        return db_manager.log_trade_action(account_id, operation, reason=details)
    except Exception as e:
        logger.error(f"Error logging operation: {str(e)}")
        return False


def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%d-%m-%Y %H:%M:%S")
    except:
        return timestamp


def get_system_info() -> Dict:
    """Get system information"""
    import platform
    import psutil
    
    return {
        'platform': platform.system(),
        'python_version': platform.python_version(),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'timestamp': datetime.now().isoformat()
    }
