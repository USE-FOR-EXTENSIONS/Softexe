"""
AliceBlue API Integration Examples
Demonstrates how to use the AliceBlue API client
"""

from aliceblue_api import AliceBlueAPIClient
from database import DatabaseManager
from risk_manager import RiskManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TradeMirroringEngine:
    """
    Core Trade Mirroring Engine
    Handles automatic mirroring of master trades to follower accounts
    """

    def __init__(self, master_account_id: str, api_key: str, api_secret: str):
        self.master_account_id = master_account_id
        self.api_client = AliceBlueAPIClient(api_key, api_secret)
        self.db = DatabaseManager()
        self.risk_mgr = RiskManager(self.db)
        self.active_trades = {}

    def initialize(self) -> bool:
        """Initialize and authenticate with AliceBlue"""
        logger.info("Initializing Trade Mirroring Engine...")
        
        # Authenticate with API
        if not self.api_client.authenticate():
            logger.error("Failed to authenticate with AliceBlue API")
            return False

        logger.info("✓ Engine initialized and authenticated")
        return True

    def mirror_trade(self, trade_order: dict) -> bool:
        """
        Mirror a single trade from master to all followers
        
        trade_order example:
        {
            'symbol': 'RELIANCE',
            'side': 'BUY',
            'quantity': 100,
            'price': 2500,
            'order_type': 'MARKET'
        }
        """
        try:
            symbol = trade_order['symbol']
            side = trade_order['side']
            quantity = trade_order['quantity']
            price = trade_order.get('price', 0)
            order_type = trade_order['order_type']

            logger.info(f"Mirroring trade: {symbol} {side} {quantity} @ {order_type}")

            # Get all follower accounts
            followers = self.db.get_all_followers(self.master_account_id)
            
            if not followers:
                logger.warning("No follower accounts configured")
                return False

            success_count = 0

            # Mirror to each follower
            for follower in followers:
                follower_id = follower['follower_id']
                lot_multiplier = follower['lot_multiplier']

                # Calculate adjusted quantity
                adjusted_qty = self.risk_mgr.calculate_adjusted_quantity(
                    follower_id,
                    quantity,
                    lot_multiplier
                )

                # Validate against risk limits
                is_valid, validation_msg = self.risk_mgr.validate_trade(
                    follower_id,
                    symbol,
                    adjusted_qty,
                    price
                )

                if not is_valid:
                    logger.warning(f"Trade validation failed for {follower['account_name']}: {validation_msg}")
                    self.risk_mgr.log_intervention(
                        follower_id,
                        'VALIDATION_FAILED',
                        symbol,
                        validation_msg,
                        'TRADE_BLOCKED'
                    )
                    continue

                # Prepare order for follower
                follower_order = {
                    'symbol': symbol,
                    'side': side,
                    'quantity': int(adjusted_qty),
                    'price': price,
                    'order_type': order_type,
                    'account_id': follower['account_id']
                }

                # Place order on follower account
                order_result = self.api_client.place_order(
                    follower['account_id'],
                    follower_order
                )

                if order_result:
                    order_id = order_result.get('order_id')
                    
                    # Record trade in database
                    self.db.record_trade(
                        self.master_account_id,
                        follower_id,
                        symbol,
                        side,
                        adjusted_qty,
                        price,
                        order_type,
                        order_id
                    )

                    logger.info(f"✓ Trade mirrored to {follower['account_name']}: {adjusted_qty} @ {order_type}")
                    success_count += 1
                else:
                    logger.error(f"Failed to place order for {follower['account_name']}")

            return success_count > 0

        except Exception as e:
            logger.error(f"Error mirroring trade: {str(e)}")
            return False

    def modify_trade(self, order_id: str, modifications: dict) -> bool:
        """
        Modify existing trades
        
        modifications example:
        {
            'quantity': 150,
            'price': 2550
        }
        """
        try:
            logger.info(f"Modifying trade {order_id}: {modifications}")

            # Get trade details
            # In real implementation, fetch from database

            # Modify in follower accounts
            followers = self.db.get_all_followers(self.master_account_id)
            
            success_count = 0
            for follower in followers:
                result = self.api_client.modify_order(
                    follower['account_id'],
                    order_id,
                    modifications
                )
                if result:
                    success_count += 1

            return success_count > 0

        except Exception as e:
            logger.error(f"Error modifying trade: {str(e)}")
            return False

    def cancel_trade(self, order_id: str) -> bool:
        """Cancel a trade across all followers"""
        try:
            logger.info(f"Cancelling trade {order_id}")

            followers = self.db.get_all_followers(self.master_account_id)
            success_count = 0

            for follower in followers:
                result = self.api_client.cancel_order(
                    follower['account_id'],
                    order_id
                )
                if result:
                    success_count += 1
                    self.db.log_trade_action(
                        follower['follower_id'],
                        'ORDER_CANCELLED',
                        reason=f"Cancelled order {order_id}"
                    )

            return success_count > 0

        except Exception as e:
            logger.error(f"Error cancelling trade: {str(e)}")
            return False

    def get_master_positions(self) -> list:
        """Get all open positions in master account"""
        try:
            positions = self.api_client.get_positions(self.master_account_id)
            return positions
        except Exception as e:
            logger.error(f"Error getting positions: {str(e)}")
            return []

    def get_follower_positions(self, follower_id: str) -> list:
        """Get positions for specific follower"""
        try:
            follower = self.db.get_all_followers(self.master_account_id)
            for f in follower:
                if f['follower_id'] == follower_id:
                    positions = self.api_client.get_positions(f['account_id'])
                    return positions
            return []
        except Exception as e:
            logger.error(f"Error getting follower positions: {str(e)}")
            return []

    def sync_positions(self) -> bool:
        """Synchronize positions between master and followers"""
        try:
            logger.info("Syncing positions...")

            master_positions = self.get_master_positions()
            followers = self.db.get_all_followers(self.master_account_id)

            for follower in followers:
                follower_positions = self.api_client.get_positions(follower['account_id'])
                
                # Compare and reconcile
                for master_pos in master_positions:
                    symbol = master_pos['symbol']
                    master_qty = master_pos['quantity']
                    
                    # Calculate expected follower quantity
                    expected_qty = master_qty * follower['lot_multiplier']
                    
                    # Find corresponding position in follower
                    follower_pos = None
                    for pos in follower_positions:
                        if pos['symbol'] == symbol:
                            follower_pos = pos
                            break
                    
                    # Log if mismatch
                    if follower_pos:
                        actual_qty = follower_pos['quantity']
                        if actual_qty != expected_qty:
                            logger.warning(
                                f"Position mismatch for {symbol} in {follower['account_name']}: "
                                f"Expected {expected_qty}, Actual {actual_qty}"
                            )

            logger.info("✓ Position sync completed")
            return True

        except Exception as e:
            logger.error(f"Error syncing positions: {str(e)}")
            return False

    def get_performance_report(self, follower_id: str) -> dict:
        """Get performance report for follower"""
        try:
            trades = self.db.get_recent_trades(follower_id, limit=100)
            
            total_pnl = 0
            wins = 0
            losses = 0
            
            for trade in trades:
                pnl = trade.get('pnl', 0)
                total_pnl += pnl
                if pnl > 0:
                    wins += 1
                elif pnl < 0:
                    losses += 1

            report = {
                'follower_id': follower_id,
                'total_trades': len(trades),
                'winning_trades': wins,
                'losing_trades': losses,
                'total_pnl': total_pnl,
                'win_rate': (wins / len(trades) * 100) if trades else 0
            }

            return report

        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return {}


# Example Usage
if __name__ == "__main__":
    # Initialize engine
    engine = TradeMirroringEngine(
        master_account_id="ALB123456",
        api_key="your_api_key_here",
        api_secret="your_api_secret_here"
    )

    # Initialize
    if engine.initialize():
        # Example: Mirror a trade
        trade = {
            'symbol': 'RELIANCE',
            'side': 'BUY',
            'quantity': 100,
            'price': 2500,
            'order_type': 'MARKET'
        }
        
        if engine.mirror_trade(trade):
            logger.info("Trade mirrored successfully!")
            
            # Get positions
            positions = engine.get_master_positions()
            logger.info(f"Master positions: {positions}")
            
            # Sync
            engine.sync_positions()
