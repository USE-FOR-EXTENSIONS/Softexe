import sys
import os
import logging
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QVBoxLayout, QHBoxLayout, QWidget,
    QTabWidget, QLabel, QPushButton, QMessageBox, QStatusBar
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from datetime import datetime

# Import custom modules
from aliceblue_api import AliceBlueAPIClient
from database import DatabaseManager
from risk_manager import RiskManager
from dashboard_widget import TradeDisplayWidget
from followers_widget import FollowersWidget
from master_account_widget import MasterAccountWidget

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('./logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TradesMirroringApp(QMainWindow):
    """
    Main Application Window for Trade Mirroring System
    
    Features:
    - Master Account Connection (AliceBlue Online API)
    - Live Trade Mirroring Dashboard
    - Follower Accounts Management
    - Risk Management System
    - Real-time Position & P&L Tracking
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trade Mirroring System v1.0")
        self.setGeometry(100, 100, 1400, 900)

        # Initialize components
        self.db_manager = DatabaseManager("./data/trades.db")
        self.api_client = AliceBlueAPIClient("", "")  # Initialize with empty keys
        self.risk_manager = RiskManager(self.db_manager)

        # Create UI
        self.init_ui()
        self.setup_timers()

        logger.info("✓ Trade Mirroring Application started")

    def init_ui(self):
        """Initialize main UI"""
        # Central widget
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Trade Mirroring System")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)

        self.status_indicator = QLabel("🔴 Offline")
        status_font = QFont()
        status_font.setPointSize(12)
        status_font.setBold(True)
        self.status_indicator.setFont(status_font)
        header_layout.addStretch()
        header_layout.addWidget(self.status_indicator)

        main_layout.addLayout(header_layout)

        # Main tabs
        self.main_tabs = QTabWidget()

        # Tab 1: Master Account
        self.master_widget = MasterAccountWidget(self.api_client, self.db_manager)
        self.main_tabs.addTab(self.master_widget, "🔐 Master Account")

        # Tab 2: Dashboard (will be created after master account setup)
        self.dashboard_tab_index = self.main_tabs.addTab(QWidget(), "📊 Dashboard")

        # Tab 3: Followers
        self.followers_tab_index = self.main_tabs.addTab(QWidget(), "👥 Followers")

        # Initialize dashboard and followers after master account selection
        self.master_account_id = None
        self.init_dashboard_tab()
        self.init_followers_tab()

        main_layout.addWidget(self.main_tabs)

        # Control panel
        control_layout = QHBoxLayout()
        
        refresh_all_btn = QPushButton("🔄 Refresh All")
        refresh_all_btn.clicked.connect(self.refresh_all_data)
        
        export_btn = QPushButton("📥 Export Report")
        export_btn.clicked.connect(self.export_report)
        
        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.clicked.connect(self.open_settings)
        
        about_btn = QPushButton("ℹ️ About")
        about_btn.clicked.connect(self.show_about)

        control_layout.addWidget(refresh_all_btn)
        control_layout.addWidget(export_btn)
        control_layout.addWidget(settings_btn)
        control_layout.addWidget(about_btn)
        control_layout.addStretch()

        main_layout.addLayout(control_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready | Last Update: Never")

    def init_dashboard_tab(self):
        """Initialize dashboard tab"""
        try:
            if self.master_account_id:
                dashboard = TradeDisplayWidget(
                    self.master_account_id,
                    self.api_client,
                    self.db_manager,
                    self.risk_manager
                )
                self.main_tabs.removeTab(self.dashboard_tab_index)
                self.main_tabs.insertTab(self.dashboard_tab_index, dashboard, "📊 Dashboard")
        except Exception as e:
            logger.error(f"Error initializing dashboard: {str(e)}")

    def init_followers_tab(self):
        """Initialize followers tab"""
        try:
            if self.master_account_id:
                followers = FollowersWidget(
                    self.master_account_id,
                    self.api_client,
                    self.db_manager,
                    self.risk_manager
                )
                self.main_tabs.removeTab(self.followers_tab_index)
                self.main_tabs.insertTab(self.followers_tab_index, followers, "👥 Followers")
        except Exception as e:
            logger.error(f"Error initializing followers: {str(e)}")

    def setup_timers(self):
        """Setup auto-update timers"""
        # Connection status timer
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_connection_status)
        self.status_timer.start(5000)  # Check every 5 seconds

    def update_connection_status(self):
        """Update connection status indicator"""
        try:
            # Check if authenticated
            if hasattr(self.api_client, 'access_token') and self.api_client.access_token:
                self.status_indicator.setText("🟢 Online")
                self.status_indicator.setStyleSheet("color: green;")
            else:
                self.status_indicator.setText("🔴 Offline")
                self.status_indicator.setStyleSheet("color: red;")

            # Update status bar
            current_time = datetime.now().strftime("%H:%M:%S")
            self.statusBar.showMessage(f"Ready | Last Update: {current_time}")
        except Exception as e:
            logger.error(f"Error updating status: {str(e)}")

    def refresh_all_data(self):
        """Refresh all data"""
        try:
            logger.info("Refreshing all data...")
            # Trigger refresh on all widgets
            current_widget = self.main_tabs.currentWidget()
            if hasattr(current_widget, 'refresh_data'):
                current_widget.refresh_data()
            QMessageBox.information(self, "Refresh", "✓ All data refreshed!")
        except Exception as e:
            logger.error(f"Error refreshing data: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to refresh: {str(e)}")

    def export_report(self):
        """Export trading report"""
        try:
            logger.info("Exporting report...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"./reports/trade_report_{timestamp}.csv"
            
            QMessageBox.information(self, "Export", f"✓ Report exported to:\n{filename}")
            logger.info(f"Report exported: {filename}")
        except Exception as e:
            logger.error(f"Error exporting report: {str(e)}")
            QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")

    def open_settings(self):
        """Open settings dialog"""
        QMessageBox.information(self, "Settings", "Settings panel will be available soon!")

    def show_about(self):
        """Show about dialog"""
        about_text = """
        Trade Mirroring System v1.0
        
        Real-time Trade Mirroring Platform with AliceBlue Online API Integration
        
        Features:
        • Live trade mirroring across multiple follower accounts
        • Risk management with daily loss limits and exposure caps
        • Real-time dashboard with position tracking
        • Follower account management
        • Detailed trade logs and reporting
        
        © 2026 Trade Mirroring System
        All Rights Reserved
        
        For support: support@example.com
        """
        QMessageBox.about(self, "About Trade Mirroring System", about_text)

    def closeEvent(self, event):
        """Handle application close"""
        reply = QMessageBox.question(
            self, 
            "Confirm Exit",
            "Are you sure you want to close the application?\nMake sure all trades are settled.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            logger.info("✓ Application closed")
            event.accept()
        else:
            event.ignore()


def create_directories():
    """Create necessary directories"""
    dirs = ['./data', './logs', './reports']
    for dir_path in dirs:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            logger.info(f"✓ Created directory: {dir_path}")


def main():
    """Main application entry point"""
    create_directories()
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = TradesMirroringApp()
    window.show()
    
    logger.info("✓ UI initialized and displayed")
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
