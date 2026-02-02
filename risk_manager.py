from typing import Dict, List
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RiskManager:
    """
    Risk Management System for Trade Mirroring
    Handles daily loss limits, exposure caps, and lot multipliers
    """

    def __init__(self, db_manager):
        self.db = db_manager
        self.daily_loss_limits = {}
        self.exposure_tracking = {}
        self.interventions = {}

    def set_daily_loss_limit(self, follower_id: str, limit: float) -> bool:
        """Set daily loss limit for follower account (in INR)"""
        try:
            self.daily_loss_limits[follower_id] = {
                'limit': limit,
                'current_loss': 0,
                'reset_time': datetime.now()
            }
            logger.info(f"✓ Daily loss limit set for {follower_id}: ₹{limit}")
            return True
        except Exception as e:
            logger.error(f"Error setting daily loss limit: {str(e)}")
            return False

    def set_max_exposure(self, follower_id: str, symbol: str, max_exposure: float) -> bool:
        """Set max exposure per symbol (in INR)"""
        try:
            if follower_id not in self.exposure_tracking:
                self.exposure_tracking[follower_id] = {}
            
            self.exposure_tracking[follower_id][symbol] = {
                'max': max_exposure,
                'current': 0
            }
            logger.info(f"✓ Max exposure set for {symbol}: ₹{max_exposure}")
            return True
        except Exception as e:
            logger.error(f"Error setting max exposure: {str(e)}")
            return False

    def check_daily_loss_limit(self, follower_id: str, current_loss: float) -> tuple[bool, str]:
        """
        Check if daily loss limit is exceeded
        Returns: (is_within_limit, message)
        """
        if follower_id not in self.daily_loss_limits:
            return True, "No limit set"

        limit_info = self.daily_loss_limits[follower_id]
        
        # Reset if new day
        if datetime.now().date() > limit_info['reset_time'].date():
            limit_info['current_loss'] = 0
            limit_info['reset_time'] = datetime.now()

        if abs(current_loss) >= limit_info['limit']:
            self.db.log_trade_action(
                follower_id, 
                'LIMIT_EXCEEDED',
                reason=f"Daily loss limit exceeded: ₹{current_loss}"
            )
            logger.warning(f"⚠ Daily loss limit exceeded for {follower_id}")
            return False, f"Daily loss limit exceeded: ₹{current_loss} / ₹{limit_info['limit']}"
        
        return True, "Within limit"

    def check_exposure_limit(self, follower_id: str, symbol: str, position_value: float) -> tuple[bool, str]:
        """
        Check if exposure limit for symbol is exceeded
        Returns: (is_within_limit, message)
        """
        if follower_id not in self.exposure_tracking or symbol not in self.exposure_tracking[follower_id]:
            return True, "No limit set"

        exposure_info = self.exposure_tracking[follower_id][symbol]
        
        if position_value >= exposure_info['max']:
            self.db.log_trade_action(
                follower_id,
                'EXPOSURE_LIMIT_EXCEEDED',
                symbol=symbol,
                reason=f"Max exposure exceeded for {symbol}"
            )
            logger.warning(f"⚠ Exposure limit exceeded for {symbol}")
            return False, f"Exposure limit exceeded: ₹{position_value} / ₹{exposure_info['max']}"

        exposure_info['current'] = position_value
        return True, "Within limit"

    def calculate_adjusted_quantity(self, follower_id: str, master_quantity: float, 
                                   lot_multiplier: float, account_cap: float = None) -> float:
        """
        Calculate adjusted quantity for follower based on lot multiplier
        
        Args:
            follower_id: Follower account ID
            master_quantity: Original quantity from master
            lot_multiplier: Multiplier for quantity (e.g., 0.5, 1.0, 2.0)
            account_cap: Optional per-account cap
        """
        try:
            adjusted_qty = master_quantity * lot_multiplier
            
            # Apply per-account cap if provided
            if account_cap:
                adjusted_qty = min(adjusted_qty, account_cap)
            
            # Ensure minimum quantity
            adjusted_qty = max(adjusted_qty, 1)
            
            logger.info(f"✓ Adjusted quantity: {master_quantity} → {adjusted_qty} (multiplier: {lot_multiplier})")
            return adjusted_qty
        except Exception as e:
            logger.error(f"Error calculating adjusted quantity: {str(e)}")
            return master_quantity

    def validate_trade(self, follower_id: str, symbol: str, quantity: float, 
                      price: float, account_cap: float = None) -> tuple[bool, str]:
        """
        Validate trade against all risk management rules
        Returns: (is_valid, message)
        """
        # Check daily loss limit
        is_within_daily, daily_msg = self.check_daily_loss_limit(follower_id, 0)
        if not is_within_daily:
            return False, daily_msg

        # Check exposure limit
        position_value = quantity * price
        is_within_exposure, exposure_msg = self.check_exposure_limit(follower_id, symbol, position_value)
        if not is_within_exposure:
            return False, exposure_msg

        # Check per-account cap
        if account_cap and position_value > account_cap:
            msg = f"Position exceeds account cap: ₹{position_value} / ₹{account_cap}"
            self.db.log_trade_action(follower_id, 'CAP_EXCEEDED', symbol=symbol, reason=msg)
            return False, msg

        return True, "Trade validation passed"

    def log_intervention(self, follower_id: str, intervention_type: str, 
                        symbol: str, reason: str, action_taken: str) -> bool:
        """Log risk management intervention"""
        try:
            if follower_id not in self.interventions:
                self.interventions[follower_id] = []

            intervention = {
                'type': intervention_type,
                'symbol': symbol,
                'reason': reason,
                'action': action_taken,
                'timestamp': datetime.now().isoformat()
            }
            
            self.interventions[follower_id].append(intervention)
            self.db.log_trade_action(follower_id, intervention_type, symbol=symbol, reason=reason)
            
            logger.info(f"✓ Intervention logged: {intervention_type} - {reason}")
            return True
        except Exception as e:
            logger.error(f"Error logging intervention: {str(e)}")
            return False

    def get_intervention_logs(self, follower_id: str) -> List[Dict]:
        """Get all interventions for a follower"""
        return self.interventions.get(follower_id, [])

    def get_risk_summary(self, follower_id: str) -> Dict:
        """Get risk management summary for follower"""
        try:
            daily_limit = self.daily_loss_limits.get(follower_id, {})
            exposure = self.exposure_tracking.get(follower_id, {})
            interventions = self.interventions.get(follower_id, [])

            return {
                'follower_id': follower_id,
                'daily_loss_limit': daily_limit.get('limit', 'Not set'),
                'current_daily_loss': daily_limit.get('current_loss', 0),
                'exposures': exposure,
                'total_interventions': len(interventions),
                'recent_interventions': interventions[-5:] if interventions else []
            }
        except Exception as e:
            logger.error(f"Error getting risk summary: {str(e)}")
            return {}
