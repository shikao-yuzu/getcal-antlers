@echo off
setlocal

set VENV_SCRIPTS=".\venv\Scripts\"

rem create virtual env
python -m venv venv

rem activate virtual env
call %VENV_SCRIPTS%activate.bat

rem install
%VENV_SCRIPTS%python -m pip install --upgrade pip

pip install requests==2.21.0
pip install beautifulsoup4==4.7.1
pip install jaconv==0.2.4

pause

rem deactivate virtual env
call %VENV_SCRIPTS%deactivate.bat

endlocal
