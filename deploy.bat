python test.py
if %ERRORLEVEL% GEQ 1 EXIT /B 1
call build.bat
call test_upload.bat
pause
