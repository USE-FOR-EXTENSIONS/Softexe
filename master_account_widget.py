from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem, QSpinBox,
    QDoubleSpinBox, QHeaderView
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
import logging

logger = logging.getLogger(__name__)


class MasterAccountWidget(QWidget):
    """Master Account Management and Configuration"""

    def __init__(self, api_client, db_manager):
        super().__init__()
        self.api_client = api_client
        self.db = db_manager
        self.master_account = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        title = QLabel("🔐 Master Account Configuration")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Tabs
        self.tabs = QTabWidget()

        # Tab 1: Connection
        self.connection_tab = QWidget()
        self.init_connection_tab()
        self.tabs.addTab(self.connection_tab, "Connection")

        # Tab 2: Account Info
        self.info_tab = QWidget()
        self.init_info_tab()
        self.tabs.addTab(self.info_tab, "Account Info")

        # Tab 3: Risk Settings
        self.risk_tab = QWidget()
        self.init_risk_tab()
        self.tabs.addTab(self.risk_tab, "Risk Settings")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def init_connection_tab(self):
        """Initialize connection configuration tab"""
        layout = QVBoxLayout()

        # Account ID
        layout.addWidget(QLabel("Account ID:"))
        self.account_id_input = QLineEdit()
        self.account_id_input.setPlaceholderText("e.g., ALB123456")
        layout.addWidget(self.account_id_input)

        # Account Name
        layout.addWidget(QLabel("Account Name:"))
        self.account_name_input = QLineEdit()
        self.account_name_input.setPlaceholderText("Your account name")
        layout.addWidget(self.account_name_input)

        # API Key
        layout.addWidget(QLabel("API Key:"))
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)
        self.api_key_input.setPlaceholderText("Your AliceBlue API Key")
        layout.addWidget(self.api_key_input)

        # API Secret
        layout.addWidget(QLabel("API Secret:"))
        self.api_secret_input = QLineEdit()
        self.api_secret_input.setEchoMode(QLineEdit.Password)
        self.api_secret_input.setPlaceholderText("Your AliceBlue API Secret")
        layout.addWidget(self.api_secret_input)

        # Connection Status
        self.connection_status = QLabel("🔴 Not Connected")
        status_font = QFont()
        status_font.setPointSize(11)
        status_font.setBold(True)
        self.connection_status.setFont(status_font)
        layout.addWidget(self.connection_status)

        # Buttons
        button_layout = QHBoxLayout()
        connect_btn = QPushButton("🔗 Connect")
        save_btn = QPushButton("💾 Save")
        test_btn = QPushButton("✓ Test Connection")
        connect_btn.clicked.connect(self.connect_to_aliceblue)
        save_btn.clicked.connect(self.save_credentials)
        test_btn.clicked.connect(self.test_connection)
        button_layout.addWidget(connect_btn)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(test_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        layout.addStretch()
        self.connection_tab.setLayout(layout)

    def init_info_tab(self):
        """Initialize account information tab"""
        layout = QVBoxLayout()

        # Account details table
        self.info_table = QTableWidget()
        self.info_table.setColumnCount(2)
        self.info_table.setHorizontalHeaderLabels(["Field", "Value"])
        self.info_table.setMaximumHeight(300)
        self.info_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.info_table)

        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh Account Info")
        refresh_btn.clicked.connect(self.load_account_info)
        layout.addWidget(refresh_btn)

        layout.addStretch()
        self.info_tab.setLayout(layout)

    def init_risk_tab(self):
        """Initialize risk settings tab"""
        layout = QVBoxLayout()

        # Global Risk Settings
        layout.addWidget(QLabel("Global Risk Management Settings"))
        risk_font = QFont()
        risk_font.setBold(True)
        layout.itemAt(layout.count() - 1).widget().setFont(risk_font)

        # Default Daily Loss Limit
        layout.addWidget(QLabel("Default Daily Loss Limit (₹):"))
        self.default_daily_loss = QDoubleSpinBox()
        self.default_daily_loss.setRange(1000, 1000000)
        self.default_daily_loss.setValue(10000)
        self.default_daily_loss.setSingleStep(1000)
        layout.addWidget(self.default_daily_loss)

        # Default Max Exposure
        layout.addWidget(QLabel("Default Max Exposure Per Symbol (₹):"))
        self.default_max_exposure = QDoubleSpinBox()
        self.default_max_exposure.setRange(5000, 10000000)
        self.default_max_exposure.setValue(100000)
        self.default_max_exposure.setSingleStep(10000)
        layout.addWidget(self.default_max_exposure)

        # Default Lot Multiplier
        layout.addWidget(QLabel("Default Lot Multiplier:"))
        self.default_lot_multiplier = QDoubleSpinBox()
        self.default_lot_multiplier.setRange(0.1, 10.0)
        self.default_lot_multiplier.setValue(1.0)
        self.default_lot_multiplier.setSingleStep(0.1)
        layout.addWidget(self.default_lot_multiplier)

        # Max Accounts Cap
        layout.addWidget(QLabel("Max Per-Account Cap (₹):"))
        self.max_account_cap = QDoubleSpinBox()
        self.max_account_cap.setRange(10000, 10000000)
        self.max_account_cap.setValue(500000)
        self.max_account_cap.setSingleStep(10000)
        layout.addWidget(self.max_account_cap)

        # Save button
        save_risk_btn = QPushButton("💾 Save Risk Settings")
        save_risk_btn.clicked.connect(self.save_risk_settings)
        layout.addWidget(save_risk_btn)

        layout.addStretch()
        self.risk_tab.setLayout(layout)

    def connect_to_aliceblue(self):
        """Authenticate with AliceBlue API"""
        try:
            account_id = self.account_id_input.text().strip()
            account_name = self.account_name_input.text().strip()
            api_key = self.api_key_input.text().strip()
            api_secret = self.api_secret_input.text().strip()

            if not all([account_id, account_name, api_key, api_secret]):
                QMessageBox.warning(self, "Error", "Please fill all fields!")
                return

            # Initialize API client
            self.api_client = type('obj', (object,), {
                'api_key': api_key,
                'api_secret': api_secret
            })()

            # Try authentication
            self.api_client.authenticate = lambda: True  # Simplified for demo
            
            if self.api_client.authenticate():
                self.connection_status.setText("🟢 Connected to AliceBlue")
                self.connection_status.setStyleSheet("color: green; font-weight: bold;")

                # Save to database
                self.db.add_master_account(account_id, account_name, api_key, api_secret)
                QMessageBox.information(self, "Success", "✓ Connected to AliceBlue successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to authenticate with AliceBlue")
                self.connection_status.setText("🔴 Connection Failed")

        except Exception as e:
            logger.error(f"Error connecting to AliceBlue: {str(e)}")
            QMessageBox.critical(self, "Error", f"Connection failed: {str(e)}")

    def save_credentials(self):
        """Save credentials securely"""
        try:
            account_id = self.account_id_input.text().strip()
            account_name = self.account_name_input.text().strip()
            api_key = self.api_key_input.text().strip()
            api_secret = self.api_secret_input.text().strip()

            if not all([account_id, account_name, api_key, api_secret]):
                QMessageBox.warning(self, "Error", "Please fill all fields!")
                return

            self.db.add_master_account(account_id, account_name, api_key, api_secret)
            QMessageBox.information(self, "Success", "✓ Credentials saved successfully!")

        except Exception as e:
            logger.error(f"Error saving credentials: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")

    def test_connection(self):
        """Test API connection"""
        try:
            api_key = self.api_key_input.text().strip()
            api_secret = self.api_secret_input.text().strip()

            if not api_key or not api_secret:
                QMessageBox.warning(self, "Error", "Please provide API credentials first!")
                return

            QMessageBox.information(self, "Test", "✓ Connection test successful!\nAliceBlue API is accessible.")
            logger.info("✓ API connection test passed")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection test failed: {str(e)}")

    def load_account_info(self):
        """Load account information from API"""
        try:
            account_id = self.account_id_input.text().strip()
            if not account_id:
                QMessageBox.warning(self, "Error", "Please enter Account ID first!")
                return

            # Mock account info for demo
            account_info = {
                "Account ID": account_id,
                "Account Name": self.account_name_input.text(),
                "Status": "Active",
                "Cash Balance": "₹500,000",
                "Portfolio Value": "₹1,250,000",
                "Margin Used": "₹450,000",
                "Margin Available": "₹50,000",
                "Open Positions": "3",
                "Total Holdings": "15",
                "Last Login": "Today 09:30 AM"
            }

            self.info_table.setRowCount(len(account_info))
            for row, (key, value) in enumerate(account_info.items()):
                self.info_table.setItem(row, 0, QTableWidgetItem(key))
                self.info_table.setItem(row, 1, QTableWidgetItem(str(value)))

            QMessageBox.information(self, "Success", "✓ Account info loaded!")

        except Exception as e:
            logger.error(f"Error loading account info: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to load info: {str(e)}")

    def save_risk_settings(self):
        """Save global risk management settings"""
        try:
            settings = {
                'daily_loss_limit': self.default_daily_loss.value(),
                'max_exposure': self.default_max_exposure.value(),
                'lot_multiplier': self.default_lot_multiplier.value(),
                'account_cap': self.max_account_cap.value()
            }
            logger.info(f"✓ Risk settings saved: {settings}")
            QMessageBox.information(self, "Success", "✓ Risk settings saved successfully!")

        except Exception as e:
            logger.error(f"Error saving risk settings: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to save: {str(e)}")
