@echo off
setlocal

if not exist ".\venv\Scripts\activate.bat" (
  call create_venv.bat
)

rem activate virtual env
call .\venv\Scripts\activate.bat

rem run
.\venv\Scripts\python.exe getcal-antlers.py

pause

rem deactivate virtual env
call .\venv\Scripts\deactivate.bat

endlocal
