@echo off

echo Download Git...
powershell -Command "Invoke-WebRequest -Uri https://github.com/git-for-windows/git/releases/download/v2.48.1.windows.1/Git-2.48.1-64-bit.exe -OutFile Git-installer.exe"

:: Cài đặt Git
start /wait Git-installer.exe /SILENT /NORESTART

:: Kiểm tra nếu cài đặt Git thành công
git --version

:: Xóa tệp cài đặt sau khi cài đặt xong
del Git-installer.exe
