#!/bin/sh
set -e
python ../test.py
./build.sh
./test_upload.sh
start "" "C:\Users\User\AppData\Local\Programs\Opera\launcher.exe" "https://test.pypi.org/manage/projects/"
echo "Waiting for you to check the test upload."
read -p "$*"
./build.sh
read -p "$*"
