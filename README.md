# PizzaShop

This repository contains the first sprint implementation for the PizzaShop user experience, including a friendly site structure, a registration page, and login support.

The application source is organized at the repository root, with `app.py` launching the desktop application.

## What was delivered

- `server.py`: a small Flask app with home, registration, login, and email validation routes.
- `templates/`: HTML templates using a global navigation and local account navigation.
- `static/css/style.css`: consistent typography, spacing, accessible colors, focus styling, and responsive layout.
- `static/js/app.js`: client-side email availability checking and improved registration feedback.

## How to run

1. Create a Python environment if you do not have one:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   .venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
3. Run the desktop application:
   ```bash
   .venv\Scripts\python.exe app.py
   ```

## How to build a Windows executable

1. Install PyInstaller:
   ```bash
   .venv\Scripts\python.exe -m pip install pyinstaller
   ```
2. Build the executable:
   ```bash
   .\build_exe.bat
   ```
3. The executable will appear in `dist\app.exe`.

The built app uses console mode, so a terminal window remains visible while the app is running.

## Notes

- Use `PyInstaller` to bundle `app.py` as an executable.
- The desktop app wrapper uses `pywebview`.

## Notes

- The registration workflow stores user accounts in `%APPDATA%\PizzaShop\users.json` (persistent across app restarts).
- The site structure includes a clear global navigation bar, footer sitemap links, and local account navigation for the registration/login experience.
