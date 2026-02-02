# Trade Mirroring System - User Guide

## 📚 Table of Contents
1. [Getting Started](#getting-started)
2. [Master Account Setup](#master-account-setup)
3. [Adding Follower Accounts](#adding-follower-accounts)
4. [Dashboard Operations](#dashboard-operations)
5. [Risk Management](#risk-management)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### System Requirements
- Windows 10/11, macOS 10.14+, or Ubuntu 18.04+
- Python 3.8 or higher
- 500 MB free disk space
- Active internet connection
- AliceBlue Online account with API enabled

### Installation Steps

**Windows:**
1. Download and extract the Softexe folder
2. Double-click `install.bat`
3. Wait for dependencies to install
4. Run `python main.py`

**Mac/Linux:**
1. Extract the Softexe folder
2. Open terminal in the folder
3. Run: `bash install.sh`
4. Run: `python main.py`

---

## Master Account Setup

### Step 1: Generate API Credentials

1. Visit https://aliceblueonline.com/
2. Log in to your account
3. Go to **Settings** → **API Management**
4. Click **Generate New API Key**
5. Copy your **API Key** and **API Secret**
6. ⚠️ **Save these securely** - you won't see the secret again

### Step 2: Configure in Application

1. Open Trade Mirroring System
2. Go to **Master Account** tab
3. Click **Connection** subtab
4. Fill in:
   - **Account ID**: Your AliceBlue account ID (e.g., ALB123456)
   - **Account Name**: Display name for your account
   - **API Key**: Paste your API Key
   - **API Secret**: Paste your API Secret

5. Click **Test Connection** to verify
6. Click **Connect** to establish connection
7. Check for green indicator "🟢 Connected to AliceBlue"

### Step 3: Verify Account Information

1. Click **Account Info** subtab
2. Click **Refresh Account Info** button
3. Verify displayed information matches your AliceBlue account

### Step 4: Configure Risk Settings

1. Go to **Risk Settings** subtab
2. Set default values:
   - **Daily Loss Limit**: Maximum loss per day (e.g., ₹10,000)
   - **Max Exposure Per Symbol**: Cap per stock (e.g., ₹100,000)
   - **Default Lot Multiplier**: Base multiplier (usually 1.0)
   - **Max Per-Account Cap**: Limit per follower (e.g., ₹500,000)

3. Click **Save Risk Settings**

---

## Adding Follower Accounts

### Single Follower Account

1. Go to **Followers** tab
2. Click **➕ Add Follower**
3. Fill in follower details:
   - **Account Name**: Custom name (e.g., "Client A Account")
   - **Account ID**: Follower's AliceBlue ID
   - **Follower Token**: API token for follower account
   - **Lot Multiplier**: Quantity multiplier
     - 0.5 = half the master's quantity
     - 1.0 = same quantity as master
     - 2.0 = double the master's quantity
   - **Investment Amount**: Capital allocated (₹)

4. Click **Save**
5. Follower appears in the table

### Follower Lot Multiplier Examples

| Master Order | Multiplier | Follower Order |
|---|---|---|
| Buy 100 shares @ ₹500 | 0.5x | Buy 50 shares @ ₹500 |
| Buy 100 shares @ ₹500 | 1.0x | Buy 100 shares @ ₹500 |
| Buy 100 shares @ ₹500 | 2.0x | Buy 200 shares @ ₹500 |

### Managing Followers

**Edit**: Select follower → Details shown automatically  
**Remove**: Select follower → Click **❌ Remove Selected** → Confirm  
**Refresh**: Click **🔄 Refresh** to reload all followers  
**View Details**: Click **View** button next to any follower

---

## Dashboard Operations

### Live Positions Tab

Shows all open positions:

| Column | Meaning |
|---|---|
| Symbol | Stock symbol (e.g., RELIANCE) |
| Side | Buy or Sell |
| Qty (Master) | Shares held in master account |
| Qty (Follower) | Adjusted quantity in follower account |
| Price | Entry price (₹) |
| LTP | Latest traded price (₹) |
| P&L | Profit or Loss (₹) |
| Status | Trade status (Active/Pending/Closed) |
| Last Update | When data was last refreshed |

**Color Coding:**
- 🟢 Green P&L: Profitable position
- 🔴 Red P&L: Loss-making position

### Recent Trades Tab

View trade execution history with filters:

**Filters:**
- **Follower**: Select specific follower account
- **Days**: Show trades from last X days

**Columns Show:**
- Time of execution
- Stock symbol
- Buy/Sell
- Quantity and price
- Follower account
- Execution status
- Fill percentage (0-100%)
- Realized P&L

### Risk Status Tab

Monitor risk parameters:

**Risk Table:**
- Daily loss limit (₹)
- Current daily loss (₹)
- Exposure caps
- Status indicator (🟢 Safe / 🔴 Alert)

**Intervention Logs:**
Recent risk management actions:
- What type of intervention
- Why it was triggered
- When it occurred

### Control Buttons

- **⏸ Pause Mirroring**: Stop all trade mirroring temporarily
- **▶ Resume Mirroring**: Restart trade mirroring
- **🔄 Refresh**: Manually update all data

---

## Risk Management

### Understanding Risk Limits

#### Daily Loss Limit
- Maximum loss allowed in a single day
- Resets at market open (9:15 AM)
- Example: If limit is ₹10,000 and loss reaches ₹10,000, trading stops

#### Per-Symbol Exposure
- Maximum capital exposed to single stock
- Example: Limit ₹100,000 on INFY means don't trade more than that value

#### Per-Account Cap
- Maximum trade value per follower account
- Example: Cap of ₹500,000 means no single follower exceeds this

#### Lot Multiplier
- Scales trade quantities
- Allows proportional risk across accounts
- Example: 0.5x = half the risk

### Setting Risk Limits

1. Go to **Master Account** tab
2. Click **Risk Settings** subtab
3. Adjust all parameters
4. Click **Save Risk Settings**

### Viewing Risk Alerts

1. Go to **Dashboard** tab
2. Click **Risk Status** subtab
3. Review:
   - Current daily loss percentage
   - Color-coded status
   - Recent interventions

### What Happens When Limits Are Exceeded

When a risk limit is hit:
1. System immediately logs the intervention
2. New trades may be blocked
3. Existing positions may be limited
4. Alert appears in Risk Status tab
5. Email notification (if configured)
6. Details logged in intervention history

---

## Common Trading Scenarios

### Scenario 1: Mirroring with Risk Scaling

**Master Account**: Buy 100 shares RELIANCE @ ₹2000

**Followers** (2 accounts):
- Client A: Multiplier 0.5x → Buys 50 shares
- Client B: Multiplier 1.0x → Buys 100 shares

**Risk Limit**: ₹10,000 daily loss
- Client A can lose max ₹5,000 (50% exposure)
- Client B can lose max ₹10,000 (100% exposure)

### Scenario 2: Stopping on Daily Loss

**Daily Loss Limit**: ₹10,000

1. Morning: Client A loses ₹3,000
2. Noon: Client B loses ₹5,000
3. Total: ₹8,000 (approaching limit)
4. New trade blocked: Would push over limit
5. System pauses new orders
6. Manual review required to continue

### Scenario 3: Per-Symbol Exposure

**Exposure Limit**: ₹100,000 per symbol

- INFY position @ ₹1500 x 50 shares = ₹75,000 ✓ OK
- Want to add @ ₹1500 x 30 shares = ₹45,000
- Total would be ₹120,000 ✗ BLOCKED (exceeds ₹100,000)

---

## Troubleshooting

### Problem: "Connection Failed"

**Causes & Solutions:**
1. **Incorrect credentials**
   - Verify API Key/Secret at aliceblueonline.com
   - Regenerate if needed
   - Paste without extra spaces

2. **Network issues**
   - Check internet connection
   - Try test connection again
   - Check firewall settings

3. **API is down**
   - Visit aliceblueonline.com status page
   - Wait and retry

### Problem: Trades Not Mirroring

**Checklist:**
1. ✓ Master account connected (green indicator)
2. ✓ Follower accounts active
3. ✓ Risk limits not exceeded
4. ✓ Market is open (9:15 AM - 3:30 PM)
5. ✓ Dashboard not paused (click Resume)

**Solution:**
- Go to Dashboard → Risk Status tab
- Check intervention logs
- Review logs/app.log for details

### Problem: High CPU/Memory Usage

**Solution:**
1. Close other applications
2. Reduce dashboard refresh rate (in config.py)
3. Restart application
4. Check system resources: Top or Task Manager

### Problem: Database Locked Error

**Solution:**
1. Close application completely
2. Wait 5 seconds
3. Delete `data/trades.db` (backup first!)
4. Restart application (fresh database created)

### Problem: Follower Account Not Appearing

**Causes:**
1. Follower ID already exists
2. Invalid credentials
3. Database error

**Solution:**
1. Verify follower token is correct
2. Try different account ID
3. Check logs/app.log for errors
4. Restart application

---

## Getting Help

### View Application Logs
```
Open: logs/app.log
```
Contains all operations, errors, and system events

### Check Online Status
Visit: https://aliceblueonline.com/status

### Review Exported Report
```
Open: reports/trade_report_*.csv
```
Detailed trade execution history

---

## Safety Tips

⚠️ **Critical Security Practices:**

1. **Never share API credentials** with anyone
2. **Don't trade with full capital** initially - start small
3. **Monitor actively** during trading hours
4. **Backup database** regularly: `data/trades.db`
5. **Review logs** for suspicious activity
6. **Set conservative limits** initially
7. **Test thoroughly** before going live
8. **Keep software updated**

---

## FAQ

**Q: Can I pause mirroring temporarily?**  
A: Yes, click ⏸ Pause Mirroring button on dashboard

**Q: What's the best lot multiplier?**  
A: Start with 0.5x or 1.0x, adjust based on capital

**Q: How often is data updated?**  
A: Every 1-2 seconds for positions, 5 seconds for accounts

**Q: Can I edit a follower's lot multiplier?**  
A: Yes, it applies to new trades. Old trades unaffected.

**Q: What happens at market close?**  
A: Dashboard continues to show positions. Daily loss limit resets next morning.

**Q: Can I run multiple instances?**  
A: Not recommended - database conflicts. Use one instance per master account.

**Q: How do I recover deleted followers?**  
A: Restore from database backup. No undo feature.

**Q: Is automated trading available?**  
A: v1.0 is manual/mirroring only. Automation planned for v2.0

---

**Document Version**: 1.0  
**Last Updated**: February 2, 2026  
**For Support**: contact@example.com
