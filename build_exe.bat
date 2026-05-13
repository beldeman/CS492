@echo off
set SCRIPT=app.py
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
pyinstaller --noconfirm --onefile --add-data "templates;templates" --add-data "static;static" %SCRIPT%
echo Build complete. See dist\app.exe
