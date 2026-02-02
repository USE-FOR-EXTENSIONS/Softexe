@echo off
REM Quick one-liner EXE builder - paste and run in Command Prompt

echo Building portable Trade Mirroring App EXE...
python -m venv venv && venv\Scripts\activate.bat && pip install --upgrade pip && pip install pyinstaller -r requirements.txt && pyinstaller --noconfirm --onefile --windowed --name TradeMirrorApp --hidden-import=PyQt5.sip --hidden-import=PyQt5.QtCore --hidden-import=PyQt5.QtGui --hidden-import=PyQt5.QtWidgets --add-data "data;data" --add-data "logs;logs" --collect-all PyQt5 main.py && echo. && echo SUCCESS! Your EXE is at: dist\TradeMirrorApp.exe && pause
