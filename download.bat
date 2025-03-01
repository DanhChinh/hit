@echo off
echo Download Python...
curl -o python_installer.exe https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe
start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
del python_installer.exe 

:: Tải Git từ trang chính thức
echo Download Git...
powershell -Command "Invoke-WebRequest -Uri https://github.com/git-for-windows/git/releases/download/v2.48.1.windows.1/Git-2.48.1-64-bit.exe -OutFile Git-installer.exe"

:: Cài đặt Git
start /wait Git-installer.exe /SILENT /NORESTART

:: Xóa tệp cài đặt sau khi cài đặt xong
echo Dọn dẹp...
del Git-installer.exe
echo clone https://github.com/DanhChinh/hit.git
git clone https://github.com/DanhChinh/hit.git

echo pip install -r requirement.txt
cd ".\hit\AI"
pip install -r requirement.txt

echo Done!
pause