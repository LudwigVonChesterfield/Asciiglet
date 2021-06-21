python ../test.py
if %ERRORLEVEL% GEQ 1 EXIT /B 1
call build.bat
call test_upload.bat
set \p url=https://test.pypi.org/manage/projects/
start C:\Users\User\AppData\Local\Programs\Opera\launcher.exe
echo "Waiting for you to check the upload on the site."
pause
call upload.bat
pause
