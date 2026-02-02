# Trade Mirroring Desktop Application Configuration

# AliceBlue API Settings
ALICEBLUE_API_BASE_URL = "https://aliceblueonline.com/"
ALICEBLUE_API_ENDPOINT = "https://aliceblueonline.com/api/"

# Application Settings
APP_NAME = "Trade Mirroring System"
APP_VERSION = "1.0.0"
DEBUG_MODE = False

# Database
DATABASE_PATH = "./data/trades.db"
LOG_PATH = "./logs/"

# Risk Management Default Values
DEFAULT_LOT_MULTIPLIER = 1.0
DAILY_LOSS_LIMIT = 10000  # INR
MAX_EXPOSURE_PER_SYMBOL = 100000  # INR

# UI Settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
THEME = "light"

# API Request Timeout
API_TIMEOUT = 30

# Update Intervals (in seconds)
TRADE_UPDATE_INTERVAL = 1  # Real-time trade mirroring
ACCOUNT_REFRESH_INTERVAL = 5
POSITION_UPDATE_INTERVAL = 2
