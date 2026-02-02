# Trade Mirroring Desktop Application

A professional-grade desktop software for automated trade mirroring with AliceBlue Online API integration. Mirror trades from a master account to multiple follower accounts with advanced risk management.

## 🎯 Key Features

### Dashboard
- **Live Trade Mirroring**: Market, limit, stop, partial fills, cancels, and modifications replicated almost instantly
- **Real-time Position Tracking**: Monitor all open positions across master and follower accounts
- **P&L Dashboard**: Visual representation of profits and losses in INR
- **Trade History**: Detailed logs of all executed trades with status and fill percentages

### Followers Management
- **Multiple Accounts**: Add/remove follower accounts in real-time
- **Account Details**:
  - Account Name
  - Account ID
  - Follower Token
  - Lot Multiplier (adjust trade quantity for each follower)
  - Investment Amount (in INR)
  - Profit/Loss Tracking (in INR)
- **Status Monitoring**: Track active/inactive follower accounts

### Master Account
- **AliceBlue API Integration**: Connect via https://aliceblueonline.com/
- **Account Configuration**: API Key and Secret management
- **Connection Testing**: Verify API connectivity
- **Account Info**: View balance, margin, holdings, and portfolio value

### Risk Management
- **Daily Loss Limits**: Set maximum daily loss per follower account (in INR)
- **Per-Symbol Exposure Caps**: Limit exposure per trading symbol
- **Per-Account Caps**: Maximum trade value per follower account
- **Lot Multipliers**: Adjust trade quantity for each follower
- **Intervention Logs**: Detailed logs of all risk management interventions

## 🏗️ Project Structure

```
Softexe/
├── main.py                      # Main application entry point
├── config.py                    # Configuration settings
├── aliceblue_api.py            # AliceBlue API client
├── database.py                 # SQLite database management
├── risk_manager.py             # Risk management system
├── dashboard_widget.py          # Dashboard UI component
├── followers_widget.py          # Followers management UI
├── master_account_widget.py    # Master account configuration UI
├── requirements.txt            # Python dependencies
├── data/                       # Database storage
│   └── trades.db
├── logs/                       # Application logs
└── reports/                    # Exported reports
```

## 📋 System Requirements

- Python 3.8+
- Windows/Mac/Linux
- AliceBlue Online account with API access
- Internet connection

## 🚀 Installation & Setup

### Option A: Run Python Script (Developers)

#### 1. Clone the Repository
```bash
git clone https://github.com/USE-FOR-EXTENSIONS/Softexe.git
cd Softexe
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Get AliceBlue API Credentials
- Visit https://aliceblueonline.com/
- Register/Login to your account
- Navigate to API Settings
- Generate your API Key and API Secret
- Keep these credentials safe

#### 4. Run the Application
```bash
python main.py
```

### Option B: Use Windows EXE (End Users) ⭐ Recommended

**No Python installation needed!** Works on ANY Windows 10+ computer.

#### How to Get EXE:

**A) Download Pre-Built (Easiest)**
- Visit [GitHub Releases](https://github.com/USE-FOR-EXTENSIONS/Softexe/releases) or [Actions](https://github.com/USE-FOR-EXTENSIONS/Softexe/actions)
- Download `TradeMirrorApp.exe`
- Double-click and run!

**B) Build Yourself (5 minutes)**
1. On Windows PC with Python installed
2. Run: `build_portable_exe.bat`
3. Get your EXE at: `dist\TradeMirrorApp.exe`
4. Share & use anywhere!

See [PORTABLE_EXE.md](PORTABLE_EXE.md) for detailed build instructions.

---

**Quick Comparison:**

| Method | Setup Time | Requirements | Best For |
|--------|-----------|--------------|----------|
| **Python Script** | 5 min | Python 3.8+ | Developers, customization |
| **Windows EXE** | 1 min | Windows 10+ | End users, distribution |
| **Installer (.exe setup)** | 2 min | Windows 10+ | Professional deployment |

## 📖 Usage Guide

### Step 1: Configure Master Account
1. Go to **Master Account** tab
2. Enter your AliceBlue credentials:
   - Account ID
   - Account Name
   - API Key
   - API Secret
3. Click **Connect** to authenticate
4. Set global risk management defaults

### Step 2: Add Follower Accounts
1. Go to **Followers** tab
2. Click **➕ Add Follower**
3. Fill in follower details:
   - Account Name (display name)
   - Account ID (AliceBlue ID)
   - Follower Token (API token)
   - Lot Multiplier (1.0 = same size, 0.5 = half size, 2.0 = double size)
   - Investment Amount (capital allocated)
4. Save and activate

### Step 3: Monitor Dashboard
1. Go to **Dashboard** tab
2. View:
   - **Live Positions**: Real-time open positions with P&L
   - **Recent Trades**: Trade execution history
   - **Risk Status**: Daily loss and exposure status
3. Use Pause/Resume to control mirroring
4. Click Refresh to update data manually

## 🛡️ Risk Management Features

### Daily Loss Limits
- Set maximum acceptable loss per day (in INR)
- Automatically reset at market open
- Triggers alerts when limit approached

### Exposure Management
- Maximum loss per symbol per account
- Per-account caps on trade size
- Real-time position monitoring

### Lot Multipliers
- Adjust trade quantity for each follower
- Useful for managing risk across different account sizes
- Example: Master trades 100 shares, Follower with 0.5x multiplier gets 50 shares

### Intervention Logs
- Detailed record of all risk management actions
- Why each limit was enforced
- Timestamps for audit trail

## 📊 Dashboard Metrics

### Live Positions Tab
- Symbol name
- Buy/Sell side
- Master & Follower quantities
- Entry price and LTP
- Unrealized P&L
- Current status
- Last update time

### Recent Trades Tab
- Execution time
- Symbol
- Quantity and price
- Follower account
- Order status
- Fill percentage
- P&L

### Risk Status Tab
- Daily loss limits per account
- Current daily loss
- Exposure caps
- Risk alerts (Green/Red)
- Intervention history

## 🔧 Configuration

Edit `config.py` to customize:

```python
# AliceBlue API Settings
ALICEBLUE_API_BASE_URL = "https://aliceblueonline.com/"

# Risk Management Defaults
DEFAULT_LOT_MULTIPLIER = 1.0
DAILY_LOSS_LIMIT = 10000  # INR
MAX_EXPOSURE_PER_SYMBOL = 100000  # INR

# Update Intervals (seconds)
TRADE_UPDATE_INTERVAL = 1  # Real-time
ACCOUNT_REFRESH_INTERVAL = 5
POSITION_UPDATE_INTERVAL = 2
```

## 📈 Currency & Units

All amounts are in **Indian Rupees (₹ INR)**:
- Investment amounts
- Profit/Loss figures
- Risk limits
- Position values

## 🐛 Troubleshooting

### "Connection Failed"
- Verify API credentials are correct
- Check internet connection
- Ensure API Key/Secret are not expired
- Check AliceBlue API status

### Trades Not Mirroring
- Verify follower accounts are active
- Check risk limits aren't being exceeded
- Review intervention logs for details
- Refresh the dashboard

### Database Issues
- Check if `data/` directory has write permissions
- Restart application to reset database connection
- Backup `trades.db` before troubleshooting

## 📝 Logging

View application logs in `logs/app.log`:
```bash
tail -f logs/app.log
```

Logs include:
- API connections
- Trade executions
- Risk management interventions
- Database operations
- Application events

## 🔐 Security Notes

⚠️ **Important Security Practices:**

1. **Never share API credentials**
2. **Use strong passwords** for AliceBlue account
3. **Keep API keys private** - regenerate if exposed
4. **Run on secure network** - avoid public WiFi
5. **Regular backups** - backup `data/trades.db`
6. **Monitor activity** - review logs regularly
7. **Set realistic limits** - don't expose more than needed

## 💡 Best Practices

1. **Start small**: Begin with 1-2 follower accounts
2. **Test thoroughly**: Use with small amounts first
3. **Monitor closely**: Watch dashboard during trading hours
4. **Set conservative limits**: Gradual increase as confidence grows
5. **Regular reviews**: Audit trade logs and P&L regularly
6. **Risk management**: Use all available risk features
7. **Keep updated**: Watch for AliceBlue API updates

## 📞 Support

- **Documentation**: See individual module docstrings
- **Logs**: Check `logs/app.log` for detailed information
- **API Docs**: https://aliceblueonline.com/docs
- **Issues**: Contact development team

## 📄 License

This software is proprietary. All rights reserved.

## 🔄 Updates & Roadmap

### v1.0 Features (Current)
- ✅ Master/Follower account management
- ✅ Trade mirroring dashboard
- ✅ Risk management system
- ✅ Database and logging

### v1.1 (Planned)
- [ ] WebSocket real-time updates
- [ ] Mobile companion app
- [ ] Advanced charting
- [ ] Performance analytics

### v2.0 (Planned)
- [ ] Multi-broker support
- [ ] Algorithmic trading
- [ ] ML-based risk prediction
- [ ] Cloud synchronization

## ⚠️ Disclaimer

This software is provided as-is for educational and professional trading purposes. 

**Important:** Always verify all trades manually before execution. The authors are not responsible for:
- Financial losses incurred
- API connectivity issues
- Third-party service outages
- Incorrect trade execution
- Data loss or corruption

Trade responsibly and manage risk carefully.

---

**Version**: 1.0.0  
**Last Updated**: February 2, 2026  
**Author**: Softexe Development Team
