@echo off

echo Cloning repository...
git clone https://github.com/DanhChinh/hit.git

:: Cài đặt các yêu cầu từ requirement.txt
echo Installing dependencies...
cd ".\hit\AI"

pip install -r requirement.txt