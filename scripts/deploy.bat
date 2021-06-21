python ../test.py
if %ERRORLEVEL% GEQ 1 EXIT /B 1
call build.bat
call test_upload.bat
start "" "C:\Users\User\AppData\Local\Programs\Opera\launcher.exe" "https://test.pypi.org/manage/projects/"
echo "Waiting for you to check the test upload."
pause
call build.bat
pause
