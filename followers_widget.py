from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit, QDoubleSpinBox, QDialog, QMessageBox,
    QComboBox, QSpinBox, QHeaderView
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QFont
import logging

logger = logging.getLogger(__name__)


class FollowerDialog(QDialog):
    """Dialog for adding/editing follower accounts"""

    def __init__(self, parent=None, follower_data=None):
        super().__init__(parent)
        self.follower_data = follower_data
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Follower Account" if not self.follower_data else "Edit Follower")
        self.setGeometry(100, 100, 500, 400)

        layout = QVBoxLayout()

        # Account Name
        layout.addWidget(QLabel("Account Name:"))
        self.account_name_input = QLineEdit()
        if self.follower_data:
            self.account_name_input.setText(self.follower_data.get('account_name', ''))
        layout.addWidget(self.account_name_input)

        # Account ID
        layout.addWidget(QLabel("Account ID:"))
        self.account_id_input = QLineEdit()
        if self.follower_data:
            self.account_id_input.setText(self.follower_data.get('account_id', ''))
            self.account_id_input.setReadOnly(True)
        layout.addWidget(self.account_id_input)

        # Follower Token
        layout.addWidget(QLabel("Follower Token:"))
        self.token_input = QLineEdit()
        if self.follower_data:
            self.token_input.setText(self.follower_data.get('follower_token', ''))
        layout.addWidget(self.token_input)

        # Lot Multiplier
        layout.addWidget(QLabel("Lot Multiplier:"))
        self.lot_multiplier_input = QDoubleSpinBox()
        self.lot_multiplier_input.setRange(0.1, 10.0)
        self.lot_multiplier_input.setValue(self.follower_data.get('lot_multiplier', 1.0) if self.follower_data else 1.0)
        self.lot_multiplier_input.setSingleStep(0.1)
        layout.addWidget(self.lot_multiplier_input)

        # Investment Amount
        layout.addWidget(QLabel("Investment Amount (₹):"))
        self.investment_input = QDoubleSpinBox()
        self.investment_input.setRange(0, 10000000)
        self.investment_input.setValue(self.follower_data.get('investment_amount', 0) if self.follower_data else 0)
        self.investment_input.setSingleStep(1000)
        layout.addWidget(self.investment_input)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_data(self):
        return {
            'account_name': self.account_name_input.text(),
            'account_id': self.account_id_input.text(),
            'follower_token': self.token_input.text(),
            'lot_multiplier': self.lot_multiplier_input.value(),
            'investment_amount': self.investment_input.value()
        }


class FollowersWidget(QWidget):
    """Followers Management Panel"""

    follower_updated = pyqtSignal()

    def __init__(self, master_account_id: str, api_client, db_manager, risk_manager):
        super().__init__()
        self.master_account_id = master_account_id
        self.api_client = api_client
        self.db = db_manager
        self.risk_mgr = risk_manager
        self.init_ui()
        self.load_followers()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("Follower Accounts Management")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Control buttons
        control_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Add Follower")
        remove_btn = QPushButton("❌ Remove Selected")
        refresh_btn = QPushButton("🔄 Refresh")
        add_btn.clicked.connect(self.add_follower)
        remove_btn.clicked.connect(self.remove_follower)
        refresh_btn.clicked.connect(self.load_followers)
        control_layout.addWidget(add_btn)
        control_layout.addWidget(remove_btn)
        control_layout.addWidget(refresh_btn)
        control_layout.addStretch()
        layout.addLayout(control_layout)

        # Followers Table
        self.followers_table = QTableWidget()
        self.followers_table.setColumnCount(8)
        self.followers_table.setHorizontalHeaderLabels([
            "Account Name", "Account ID", "Lot Multiplier", 
            "Investment (₹)", "Profit (₹)", "Status", "Actions", "Details"
        ])
        self.followers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.followers_table)

        # Summary Statistics
        stats_layout = QHBoxLayout()
        self.total_followers_label = QLabel("Total Followers: 0")
        self.total_investment_label = QLabel("Total Investment: ₹0")
        self.total_profit_label = QLabel("Total Profit: ₹0")
        stats_layout.addWidget(self.total_followers_label)
        stats_layout.addWidget(self.total_investment_label)
        stats_layout.addWidget(self.total_profit_label)
        layout.addLayout(stats_layout)

        self.setLayout(layout)

    def load_followers(self):
        """Load and display all followers"""
        try:
            followers = self.db.get_all_followers(self.master_account_id)
            self.followers_table.setRowCount(len(followers))

            total_investment = 0
            total_profit = 0

            for row, follower in enumerate(followers):
                self.followers_table.setItem(row, 0, QTableWidgetItem(follower['account_name']))
                self.followers_table.setItem(row, 1, QTableWidgetItem(follower['account_id']))
                self.followers_table.setItem(row, 2, QTableWidgetItem(str(follower['lot_multiplier'])))

                investment = follower.get('investment_amount', 0)
                profit = follower.get('profit_amount', 0)
                total_investment += investment
                total_profit += profit

                self.followers_table.setItem(row, 3, QTableWidgetItem(f"₹{investment:,.2f}"))
                self.followers_table.setItem(row, 4, QTableWidgetItem(f"₹{profit:,.2f}"))

                # Status with color
                status = follower['status']
                status_item = QTableWidgetItem(status)
                if status == 'active':
                    status_item.setBackground(QColor(144, 238, 144))  # Light green
                else:
                    status_item.setBackground(QColor(255, 200, 124))  # Light orange
                self.followers_table.setItem(row, 5, status_item)

                # Action button
                view_btn = QPushButton("View")
                view_btn.clicked.connect(lambda checked, f=follower: self.view_follower(f))
                self.followers_table.setCellWidget(row, 6, view_btn)

            self.total_followers_label.setText(f"Total Followers: {len(followers)}")
            self.total_investment_label.setText(f"Total Investment: ₹{total_investment:,.2f}")
            self.total_profit_label.setText(f"Total Profit: ₹{total_profit:,.2f}")

            logger.info(f"✓ Loaded {len(followers)} followers")
        except Exception as e:
            logger.error(f"Error loading followers: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to load followers: {str(e)}")

    def add_follower(self):
        """Add new follower account"""
        dialog = FollowerDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            try:
                follower_id = f"{self.master_account_id}_FOLLOWER_{len(self.db.get_all_followers(self.master_account_id))}"
                
                success = self.db.add_follower_account(
                    follower_id,
                    data['account_name'],
                    data['account_id'],
                    data['follower_token'],
                    data['lot_multiplier'],
                    self.master_account_id
                )

                if success:
                    # Set up risk management for new follower
                    self.risk_mgr.set_daily_loss_limit(follower_id, 10000)  # Default ₹10,000
                    QMessageBox.information(self, "Success", "Follower account added successfully!")
                    self.load_followers()
                    self.follower_updated.emit()
                else:
                    QMessageBox.warning(self, "Warning", "Follower already exists!")
            except Exception as e:
                logger.error(f"Error adding follower: {str(e)}")
                QMessageBox.critical(self, "Error", f"Failed to add follower: {str(e)}")

    def remove_follower(self):
        """Remove selected follower"""
        current_row = self.followers_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a follower to remove!")
            return

        follower_name = self.followers_table.item(current_row, 0).text()
        reply = QMessageBox.question(self, "Confirm", f"Remove follower '{follower_name}'?")
        if reply == QMessageBox.Yes:
            try:
                # Get follower ID from database
                followers = self.db.get_all_followers(self.master_account_id)
                if current_row < len(followers):
                    self.db.remove_follower_account(followers[current_row]['follower_id'])
                    QMessageBox.information(self, "Success", "Follower removed successfully!")
                    self.load_followers()
                    self.follower_updated.emit()
            except Exception as e:
                logger.error(f"Error removing follower: {str(e)}")
                QMessageBox.critical(self, "Error", f"Failed to remove follower: {str(e)}")

    def view_follower(self, follower):
        """View detailed follower information"""
        trades = self.db.get_recent_trades(follower['follower_id'], limit=10)
        risk_summary = self.risk_mgr.get_risk_summary(follower['follower_id'])

        message = f"""
        Account Name: {follower['account_name']}
        Account ID: {follower['account_id']}
        Lot Multiplier: {follower['lot_multiplier']}x
        Investment: ₹{follower['investment_amount']:,.2f}
        Current Profit: ₹{follower['profit_amount']:,.2f}
        Status: {follower['status']}
        
        Daily Loss Limit: ₹{risk_summary['daily_loss_limit']}
        Current Daily Loss: ₹{risk_summary['current_daily_loss']}
        Total Interventions: {risk_summary['total_interventions']}
        Recent Trades: {len(trades)}
        """

        QMessageBox.information(self, f"Follower Details - {follower['account_name']}", message)
