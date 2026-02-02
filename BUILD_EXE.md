# Building Windows EXE

This guide explains how to build a standalone `.exe` file for Windows.

## Option A: GitHub Actions (Recommended - Automatic)

**How it works:**
1. Push code to GitHub
2. GitHub Actions runs automatically on `windows-latest` runner
3. Builds `.exe` and uploads as artifact
4. Available for 30 days for download

**Triggers:**
- Every push to `main` branch
- Every pull request
- Manual trigger via **Actions** tab
- Tag creation (creates Release)

**Download built EXE:**
1. Go to your GitHub repo → **Actions** tab
2. Click latest "Build Windows EXE" run
3. Download artifact `TradeMirrorApp-py3.X.zip`
4. Extract and run `TradeMirrorApp.exe`

---

## Option B: Local Build (Windows Machine)

**Prerequisites:**
- Windows 10 or later
- Python 3.8+
- Git Bash or Command Prompt

**Steps:**

### 1. Clone & Setup
```bash
git clone https://github.com/USE-FOR-EXTENSIONS/Softexe.git
cd Softexe
```

### 2. Run Build Script
```bash
# On Windows CMD:
build_exe.bat

# On Windows PowerShell:
.\build_exe.bat

# On WSL or Git Bash:
bash build_exe.sh
```

### 3. Result
- **One-file mode**: `build/dist/TradeMirrorApp.exe` (single file, ~200MB)
- **Directory mode**: `build/dist/TradeMirrorApp/TradeMirrorApp.exe` (lighter, requires folder)

### 4. Test
```bash
build\dist\TradeMirrorApp.exe
```

---

## Option C: Manual PyInstaller Command

If you prefer direct control:

```bash
# Activate venv
python -m venv venv
venv\Scripts\activate

# Install PyInstaller
pip install pyinstaller

# Build
pyinstaller --noconfirm --onefile --windowed ^
  --name "TradeMirrorApp" ^
  --hidden-import=PyQt5.sip ^
  --hidden-import=PyQt5.QtCore ^
  --hidden-import=PyQt5.QtGui ^
  --hidden-import=PyQt5.QtWidgets ^
  --add-data "data;data" ^
  --add-data "logs;logs" ^
  --add-data "reports;reports" ^
  main.py

# Output: dist\TradeMirrorApp.exe
```

---

## File Size & Performance

| Format | Size | Speed | Notes |
|--------|------|-------|-------|
| **One-file (.exe)** | ~200-250 MB | Slower first-run (unpacks) | Best for distribution |
| **Directory** | ~150-180 MB | Faster | Better for local use |
| **With installer** | ~50-80 MB (installer) | Fast | Best for end-users |

---

## Troubleshooting

### Build Fails: "ModuleNotFoundError: PyQt5"
**Solution:**
```bash
pip install --upgrade PyQt5
pyinstaller --hidden-import=PyQt5.sip ...
```

### EXE Won't Run: "DLL not found"
**Cause:** Missing dependencies  
**Solution:** Use directory format (`--onedir`) to keep DLLs together

### Antivirus Flags EXE
**Normal behavior** for compiled executables. Either:
1. Add to whitelist
2. Sign the EXE (requires certificate)
3. Use installer (more trusted by antivirus)

### Want a Professional Installer?

Use **Inno Setup** (free, Windows):
1. Download from https://jrsoftware.org/isdl.php
2. Create `.iss` script
3. Compile to `.exe` installer

Or **NSIS** (free, Windows):
1. Download from https://nsis.sourceforge.io/
2. Create installer script
3. Compile

---

## Distribution

Once you have the `.exe`:

1. **Share directly:**
   - Upload to GitHub Releases
   - Share via Google Drive, OneDrive, etc.

2. **Create installer:**
   - Wrap with Inno Setup or NSIS
   - Users run installer instead of `.exe`

3. **Portable version:**
   - No installation required
   - Just copy & run `.exe`

---

## Next Steps

1. **Choose build method** (A, B, or C above)
2. **Build EXE** (2-5 minutes)
3. **Test on Windows machine**
4. **Distribute or create installer**
5. **Done!** Users can now run your app

---

## CI/CD Status

Check latest build status: https://github.com/USE-FOR-EXTENSIONS/Softexe/actions

---

For questions, see main README.md or QUICK_START.md
