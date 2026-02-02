from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QDoubleSpinBox, QDialog, QMessageBox,
    QTabWidget, QHeaderView, QSpinBox, QComboBox
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QFont
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class TradeDisplayWidget(QWidget):
    """Dashboard showing live trade mirroring"""

    def __init__(self, master_account_id: str, api_client, db_manager, risk_manager):
        super().__init__()
        self.master_account_id = master_account_id
        self.api_client = api_client
        self.db = db_manager
        self.risk_mgr = risk_manager
        self.followers = []
        self.current_positions = {}
        self.init_ui()
        self.setup_timers()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("📊 Live Trade Mirroring Dashboard")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Master Account Info
        master_info_layout = QHBoxLayout()
        self.master_status = QLabel(f"🟢 Master Account: {self.master_account_id}")
        master_status_font = QFont()
        master_status_font.setPointSize(11)
        master_status_font.setBold(True)
        self.master_status.setFont(master_status_font)
        master_info_layout.addWidget(self.master_status)
        master_info_layout.addStretch()
        layout.addLayout(master_info_layout)

        # Tabs for different views
        self.tabs = QTabWidget()

        # Tab 1: Live Positions
        self.positions_widget = QWidget()
        self.init_positions_tab()
        self.tabs.addTab(self.positions_widget, "Live Positions")

        # Tab 2: Recent Trades
        self.trades_widget = QWidget()
        self.init_trades_tab()
        self.tabs.addTab(self.trades_widget, "Recent Trades")

        # Tab 3: Risk Status
        self.risk_widget = QWidget()
        self.init_risk_tab()
        self.tabs.addTab(self.risk_widget, "Risk Status")

        layout.addWidget(self.tabs)

        # Control buttons
        control_layout = QHBoxLayout()
        pause_btn = QPushButton("⏸ Pause Mirroring")
        resume_btn = QPushButton("▶ Resume Mirroring")
        refresh_btn = QPushButton("🔄 Refresh")
        pause_btn.clicked.connect(self.pause_mirroring)
        resume_btn.clicked.connect(self.resume_mirroring)
        refresh_btn.clicked.connect(self.refresh_data)
        control_layout.addWidget(pause_btn)
        control_layout.addWidget(resume_btn)
        control_layout.addWidget(refresh_btn)
        control_layout.addStretch()
        layout.addLayout(control_layout)

        self.setLayout(layout)

    def init_positions_tab(self):
        """Initialize positions display tab"""
        layout = QVBoxLayout()

        # Positions table
        self.positions_table = QTableWidget()
        self.positions_table.setColumnCount(9)
        self.positions_table.setHorizontalHeaderLabels([
            "Symbol", "Side", "Qty (Master)", "Qty (Follower)", "Price",
            "LTP", "P&L", "Status", "Last Update"
        ])
        self.positions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.positions_table)

        # Statistics
        stats_layout = QHBoxLayout()
        self.positions_count_label = QLabel("Open Positions: 0")
        self.total_pnl_label = QLabel("Total P&L: ₹0")
        stats_layout.addWidget(self.positions_count_label)
        stats_layout.addWidget(self.total_pnl_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        self.positions_widget.setLayout(layout)

    def init_trades_tab(self):
        """Initialize trades history tab"""
        layout = QVBoxLayout()

        # Filter controls
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Follower:"))
        self.trade_follower_filter = QComboBox()
        self.trade_follower_filter.currentTextChanged.connect(self.refresh_trades)
        filter_layout.addWidget(self.trade_follower_filter)
        filter_layout.addWidget(QLabel("Days:"))
        self.trade_days_filter = QSpinBox()
        self.trade_days_filter.setRange(1, 30)
        self.trade_days_filter.setValue(1)
        self.trade_days_filter.valueChanged.connect(self.refresh_trades)
        filter_layout.addWidget(self.trade_days_filter)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # Trades table
        self.trades_table = QTableWidget()
        self.trades_table.setColumnCount(9)
        self.trades_table.setHorizontalHeaderLabels([
            "Time", "Symbol", "Side", "Qty", "Price", "Follower",
            "Status", "Fill %", "P&L"
        ])
        self.trades_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.trades_table)

        self.trades_widget.setLayout(layout)

    def init_risk_tab(self):
        """Initialize risk management tab"""
        layout = QVBoxLayout()

        # Risk alerts table
        self.risk_table = QTableWidget()
        self.risk_table.setColumnCount(5)
        self.risk_table.setHorizontalHeaderLabels([
            "Follower Account", "Daily Loss Limit", "Current Loss",
            "Exposure Cap", "Status"
        ])
        self.risk_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.risk_table)

        # Intervention logs
        layout.addWidget(QLabel("Recent Interventions:"))
        self.intervention_table = QTableWidget()
        self.intervention_table.setColumnCount(4)
        self.intervention_table.setHorizontalHeaderLabels([
            "Follower", "Type", "Reason", "Time"
        ])
        self.intervention_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.intervention_table)

        self.risk_widget.setLayout(layout)

    def setup_timers(self):
        """Setup auto-refresh timers"""
        # Positions update timer (1 second)
        self.positions_timer = QTimer()
        self.positions_timer.timeout.connect(self.update_positions)
        self.positions_timer.start(1000)

        # Trades update timer (2 seconds)
        self.trades_timer = QTimer()
        self.trades_timer.timeout.connect(self.refresh_trades)
        self.trades_timer.start(2000)

        # Risk status timer (5 seconds)
        self.risk_timer = QTimer()
        self.risk_timer.timeout.connect(self.update_risk_status)
        self.risk_timer.start(5000)

    def update_positions(self):
        """Update live positions from API"""
        try:
            self.followers = self.db.get_all_followers(self.master_account_id)
            if not self.followers:
                self.positions_table.setRowCount(0)
                return

            # Get master positions
            positions = self.api_client.get_positions(self.master_account_id)
            self.positions_table.setRowCount(len(positions))

            total_pnl = 0
            for row, position in enumerate(positions):
                symbol = position.get('symbol', '')
                side = position.get('side', '')
                qty = position.get('quantity', 0)
                price = position.get('price', 0)
                ltp = position.get('ltp', price)
                pnl = (ltp - price) * qty

                total_pnl += pnl

                self.positions_table.setItem(row, 0, QTableWidgetItem(symbol))
                self.positions_table.setItem(row, 1, QTableWidgetItem(side))
                self.positions_table.setItem(row, 2, QTableWidgetItem(str(qty)))

                # Calculate follower quantity
                follower_qty = qty * self.followers[0].get('lot_multiplier', 1) if self.followers else qty
                self.positions_table.setItem(row, 3, QTableWidgetItem(str(int(follower_qty))))
                self.positions_table.setItem(row, 4, QTableWidgetItem(f"₹{price:.2f}"))
                self.positions_table.setItem(row, 5, QTableWidgetItem(f"₹{ltp:.2f}"))

                # P&L with color
                pnl_item = QTableWidgetItem(f"₹{pnl:,.2f}")
                if pnl > 0:
                    pnl_item.setBackground(QColor(144, 238, 144))
                elif pnl < 0:
                    pnl_item.setBackground(QColor(255, 200, 200))
                self.positions_table.setItem(row, 6, pnl_item)

                status_item = QTableWidgetItem("🟢 Active")
                self.positions_table.setItem(row, 7, status_item)
                self.positions_table.setItem(row, 8, QTableWidgetItem(datetime.now().strftime("%H:%M:%S")))

            self.positions_count_label.setText(f"Open Positions: {len(positions)}")
            self.total_pnl_label.setText(f"Total P&L: ₹{total_pnl:,.2f}")

        except Exception as e:
            logger.error(f"Error updating positions: {str(e)}")

    def refresh_trades(self):
        """Refresh recent trades display"""
        try:
            if not self.followers:
                return

            # Get trades for all followers
            all_trades = []
            for follower in self.followers:
                trades = self.db.get_recent_trades(follower['follower_id'], limit=20)
                all_trades.extend(trades)

            all_trades.sort(key=lambda x: x.get('entry_time', ''), reverse=True)
            all_trades = all_trades[:50]

            self.trades_table.setRowCount(len(all_trades))

            for row, trade in enumerate(all_trades):
                self.trades_table.setItem(row, 0, QTableWidgetItem(str(trade.get('entry_time', ''))))
                self.trades_table.setItem(row, 1, QTableWidgetItem(trade.get('symbol', '')))
                self.trades_table.setItem(row, 2, QTableWidgetItem(trade.get('side', '')))
                self.trades_table.setItem(row, 3, QTableWidgetItem(str(trade.get('quantity', 0))))
                self.trades_table.setItem(row, 4, QTableWidgetItem(f"₹{trade.get('price', 0):.2f}"))
                self.trades_table.setItem(row, 5, QTableWidgetItem(str(trade.get('follower_account_id', ''))))
                self.trades_table.setItem(row, 6, QTableWidgetItem(trade.get('status', '')))
                self.trades_table.setItem(row, 7, QTableWidgetItem(f"{trade.get('fill_percentage', 0):.1f}%"))
                self.trades_table.setItem(row, 8, QTableWidgetItem(f"₹{trade.get('pnl', 0):,.2f}"))

        except Exception as e:
            logger.error(f"Error refreshing trades: {str(e)}")

    def update_risk_status(self):
        """Update risk management status"""
        try:
            if not self.followers:
                return

            self.risk_table.setRowCount(len(self.followers))

            for row, follower in enumerate(self.followers):
                risk_summary = self.risk_mgr.get_risk_summary(follower['follower_id'])

                self.risk_table.setItem(row, 0, QTableWidgetItem(follower['account_name']))
                self.risk_table.setItem(row, 1, QTableWidgetItem(f"₹{risk_summary['daily_loss_limit']}"))

                current_loss = risk_summary['current_daily_loss']
                loss_item = QTableWidgetItem(f"₹{current_loss:,.2f}")
                if abs(current_loss) > (float(risk_summary['daily_loss_limit']) * 0.8):
                    loss_item.setBackground(QColor(255, 200, 200))
                self.risk_table.setItem(row, 2, loss_item)

                self.risk_table.setItem(row, 3, QTableWidgetItem("₹100,000"))

                # Status
                status = "🟢 Safe" if abs(current_loss) < float(risk_summary['daily_loss_limit']) else "🔴 Alert"
                status_item = QTableWidgetItem(status)
                self.risk_table.setItem(row, 4, status_item)

        except Exception as e:
            logger.error(f"Error updating risk status: {str(e)}")

    def pause_mirroring(self):
        """Pause trade mirroring"""
        self.positions_timer.stop()
        self.trades_timer.stop()
        QMessageBox.information(self, "Paused", "Trade mirroring paused!")

    def resume_mirroring(self):
        """Resume trade mirroring"""
        self.positions_timer.start()
        self.trades_timer.start()
        QMessageBox.information(self, "Resumed", "Trade mirroring resumed!")

    def refresh_data(self):
        """Manual data refresh"""
        self.update_positions()
        self.refresh_trades()
        self.update_risk_status()
        QMessageBox.information(self, "Refreshed", "Data refreshed successfully!")
