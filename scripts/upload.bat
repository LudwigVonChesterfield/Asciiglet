cd ..
echo "You are about to upload to PyPi."

:choice
set /P c=Are you sure you want to continue[Y/N]?
if /I "%c%" EQU "Y" goto :upload
if /I "%c%" EQU "N" goto :exit
goto :choice

:upload

twine upload dist/*
pause
exit

:exit
exit

cd scripts
