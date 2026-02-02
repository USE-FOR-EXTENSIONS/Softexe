import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    SQLite Database Manager for Trade Mirroring System
    Handles all data persistence
    """

    def __init__(self, db_path: str = "./data/trades.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Master Account Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS master_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT UNIQUE NOT NULL,
                account_name TEXT NOT NULL,
                api_key TEXT NOT NULL,
                api_secret TEXT NOT NULL,
                status TEXT DEFAULT 'inactive',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Follower Accounts Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS follower_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                follower_id TEXT UNIQUE NOT NULL,
                account_name TEXT NOT NULL,
                account_id TEXT NOT NULL,
                follower_token TEXT NOT NULL,
                lot_multiplier REAL DEFAULT 1.0,
                investment_amount REAL DEFAULT 0,
                profit_amount REAL DEFAULT 0,
                currency TEXT DEFAULT 'INR',
                status TEXT DEFAULT 'active',
                master_account_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (master_account_id) REFERENCES master_accounts(account_id)
            )
        ''')

        # Trades Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                master_account_id TEXT NOT NULL,
                follower_account_id TEXT NOT NULL,
                symbol TEXT NOT NULL,
                side TEXT NOT NULL,
                quantity REAL NOT NULL,
                price REAL NOT NULL,
                order_type TEXT NOT NULL,
                order_id TEXT UNIQUE,
                follower_order_id TEXT,
                status TEXT DEFAULT 'pending',
                fill_percentage REAL DEFAULT 0,
                filled_quantity REAL DEFAULT 0,
                entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                close_time TIMESTAMP,
                pnl REAL DEFAULT 0,
                FOREIGN KEY (master_account_id) REFERENCES master_accounts(account_id),
                FOREIGN KEY (follower_account_id) REFERENCES follower_accounts(follower_id)
            )
        ''')

        # Risk Management Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS risk_management (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT UNIQUE NOT NULL,
                daily_loss_limit REAL NOT NULL,
                current_daily_loss REAL DEFAULT 0,
                max_exposure_per_symbol REAL NOT NULL,
                current_exposure REAL DEFAULT 0,
                lot_multiplier REAL DEFAULT 1.0,
                per_account_cap REAL NOT NULL,
                intervention_logs TEXT,
                reset_date DATE,
                FOREIGN KEY (account_id) REFERENCES follower_accounts(follower_id)
            )
        ''')

        # Trade Logs Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS trade_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id TEXT NOT NULL,
                action TEXT NOT NULL,
                symbol TEXT,
                quantity REAL,
                price REAL,
                reason TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES follower_accounts(follower_id)
            )
        ''')

        conn.commit()
        conn.close()
        logger.info("✓ Database initialized successfully")

    def add_master_account(self, account_id: str, account_name: str, api_key: str, api_secret: str) -> bool:
        """Add master account to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO master_accounts (account_id, account_name, api_key, api_secret, status)
                VALUES (?, ?, ?, ?, 'active')
            ''', (account_id, account_name, api_key, api_secret))
            conn.commit()
            conn.close()
            logger.info(f"✓ Master account added: {account_name}")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"Master account already exists: {account_id}")
            return False
        except Exception as e:
            logger.error(f"Error adding master account: {str(e)}")
            return False

    def add_follower_account(self, follower_id: str, account_name: str, account_id: str,
                            follower_token: str, lot_multiplier: float, master_account_id: str) -> bool:
        """Add follower account"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO follower_accounts 
                (follower_id, account_name, account_id, follower_token, lot_multiplier, master_account_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (follower_id, account_name, account_id, follower_token, lot_multiplier, master_account_id))
            conn.commit()
            conn.close()
            logger.info(f"✓ Follower account added: {account_name}")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"Follower account already exists: {follower_id}")
            return False
        except Exception as e:
            logger.error(f"Error adding follower: {str(e)}")
            return False

    def remove_follower_account(self, follower_id: str) -> bool:
        """Remove follower account"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM follower_accounts WHERE follower_id = ?', (follower_id,))
            conn.commit()
            conn.close()
            logger.info(f"✓ Follower account removed: {follower_id}")
            return True
        except Exception as e:
            logger.error(f"Error removing follower: {str(e)}")
            return False

    def get_all_followers(self, master_account_id: str) -> List[Dict]:
        """Get all follower accounts for a master account"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM follower_accounts WHERE master_account_id = ?
            ''', (master_account_id,))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error fetching followers: {str(e)}")
            return []

    def get_master_account(self, account_id: str) -> Optional[Dict]:
        """Get master account details"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM master_accounts WHERE account_id = ?', (account_id,))
            row = cursor.fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            logger.error(f"Error fetching master account: {str(e)}")
            return None

    def record_trade(self, master_account_id: str, follower_account_id: str, symbol: str,
                    side: str, quantity: float, price: float, order_type: str, order_id: str = None) -> bool:
        """Record trade execution"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO trades 
                (master_account_id, follower_account_id, symbol, side, quantity, price, order_type, order_id, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'pending')
            ''', (master_account_id, follower_account_id, symbol, side, quantity, price, order_type, order_id))
            conn.commit()
            conn.close()
            logger.info(f"✓ Trade recorded: {symbol} {side} {quantity}")
            return True
        except Exception as e:
            logger.error(f"Error recording trade: {str(e)}")
            return False

    def update_trade_status(self, order_id: str, status: str, fill_percentage: float = 0) -> bool:
        """Update trade status"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE trades SET status = ?, fill_percentage = ? WHERE order_id = ?
            ''', (status, fill_percentage, order_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error updating trade: {str(e)}")
            return False

    def get_recent_trades(self, follower_id: str, limit: int = 50) -> List[Dict]:
        """Get recent trades for a follower"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM trades WHERE follower_account_id = ?
                ORDER BY entry_time DESC LIMIT ?
            ''', (follower_id, limit))
            rows = cursor.fetchall()
            conn.close()
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error fetching trades: {str(e)}")
            return []

    def log_trade_action(self, account_id: str, action: str, symbol: str = None,
                        quantity: float = None, price: float = None, reason: str = None) -> bool:
        """Log trade actions and interventions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO trade_logs (account_id, action, symbol, quantity, price, reason)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (account_id, action, symbol, quantity, price, reason))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error logging action: {str(e)}")
            return False

    def update_follower_pnl(self, follower_id: str, profit: float) -> bool:
        """Update follower P&L"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE follower_accounts SET profit_amount = profit_amount + ? WHERE follower_id = ?
            ''', (profit, follower_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error updating P&L: {str(e)}")
            return False
