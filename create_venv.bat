@echo off
setlocal

rem create virtual env
python -m venv venv

rem activate virtual env
call .\venv\Scripts\activate.bat

rem install
.\venv\Scripts\python -m pip install --upgrade pip
pip install requests
pip install beautifulsoup4

pause

rem deactivate virtual env
call .\venv\Scripts\deactivate.bat

endlocal
