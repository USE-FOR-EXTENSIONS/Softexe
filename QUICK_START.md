# Quick Start Guide - Trade Mirroring System

## ⚡ 5-Minute Setup

### Option A: Windows EXE (Easiest - No Python needed!) ⭐

1. **Download EXE** (1 min)
   - Visit [GitHub Releases](https://github.com/USE-FOR-EXTENSIONS/Softexe/releases)
   - Or [GitHub Actions Artifacts](https://github.com/USE-FOR-EXTENSIONS/Softexe/actions)
   - Download `TradeMirrorApp.exe`

2. **Run** (1 min)
   - Double-click `TradeMirrorApp.exe`
   - Done! App launches immediately

3. **Skip to Step 2** (below)

### Option B: Python Script (Developers)

**Install (1 minute)**
```bash
# Mac/Linux
bash install.sh

# Windows
Double-click install.bat
```

**Run**
```bash
python main.py
```

---### 2: Get API Credentials (2 minutes)
1. Visit https://aliceblueonline.com/
2. Login → Settings → API Management
3. Generate API Key and Secret
4. Copy them to notepad

### 3: Launch Application (1 minute)
```bash
python main.py
```

### 4: Connect Master Account (1 minute)
1. Go to **Master Account** tab
2. Paste credentials:
   - Account ID
   - API Key
   - API Secret
3. Click **Connect**

---

## 🎯 First Trade Mirror

### Add Your First Follower (2 minutes)

1. Go to **Followers** tab
2. Click **➕ Add Follower**
3. Fill:
   - Account Name: "Test Follower"
   - Account ID: [Follower's AliceBlue ID]
   - Follower Token: [Follower's API token]
   - Lot Multiplier: **1.0** (same size)
   - Investment: **100000** (₹)
4. Click **Save**

### Start Mirroring (30 seconds)

1. Go to **Dashboard** tab
2. Place a trade in your master account
3. Watch follower automatically mirror it
4. See live P&L in **Live Positions** tab

---

## 📊 Dashboard Quick Reference

### Tabs Explained

**Live Positions**
- Shows active trades
- Real-time P&L
- Master vs Follower quantities

**Recent Trades**
- All executed trades
- Fill percentages
- Execution status

**Risk Status**
- Daily loss tracking
- Exposure monitoring
- Intervention logs

---

## ⚠️ Risk Management Quick Setup

### Default Safe Settings
```
Daily Loss Limit: ₹10,000
Max Per-Symbol: ₹100,000
Lot Multiplier: 1.0x
Per-Account Cap: ₹500,000
```

### Set These
1. Master Account → Risk Settings
2. Enter values above
3. Click **Save**

---

## 🚀 Pro Tips

1. **Start Small**: Use 0.5x multiplier first
2. **Monitor Closely**: Watch dashboard during trading
3. **Set Limits**: Configure all risk parameters
4. **Test First**: Small trades before going live
5. **Review Logs**: Check logs/ directory for issues

---

## 📱 Common Tasks

### Add Another Follower
Followers tab → ➕ Add Follower → Enter details → Save

### Pause Trading
Dashboard → ⏸ Pause Mirroring

### Check P&L
Dashboard → Live Positions → P&L column

### View Errors
Open: logs/app.log

### Export Report
Top menu → 📥 Export Report

---

## ✓ Checklist Before Live Trading

- [ ] API credentials verified
- [ ] Test connection successful
- [ ] Follower accounts added
- [ ] Risk limits configured
- [ ] Small test trade executed
- [ ] Dashboard showing correct data
- [ ] No error messages in logs
- [ ] Database backed up

---

## ❌ If Something Goes Wrong

1. **Check logs**: `logs/app.log`
2. **Restart**: Close and reopen application
3. **Verify**: Test API connection again
4. **Review**: Check risk limits aren't exceeded
5. **Contact**: Email support with log file

---

## 📞 Support Resources

- **Full Guide**: [USER_GUIDE.md](USER_GUIDE.md)
- **API Docs**: https://aliceblueonline.com/docs
- **Technical**: [README.md](README.md)
- **Logs**: `logs/app.log`

---

**Ready to trade!** 🚀

Questions? Check [USER_GUIDE.md](USER_GUIDE.md) for detailed instructions.
