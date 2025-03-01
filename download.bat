@echo off

:: Tải Python
echo Download Python...
curl -o python_installer.exe https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe
start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
del python_installer.exe

:: Kiểm tra nếu cài đặt Python thành công
python --version
if %errorlevel% neq 0 (
    echo Python installation failed.
    pause
    exit /b
)

:: Tải Git từ trang chính thức
echo Download Git...
powershell -Command "Invoke-WebRequest -Uri https://github.com/git-for-windows/git/releases/download/v2.48.1.windows.1/Git-2.48.1-64-bit.exe -OutFile Git-installer.exe"

:: Cài đặt Git
start /wait Git-installer.exe /SILENT /NORESTART

:: Kiểm tra nếu cài đặt Git thành công
git --version
if %errorlevel% neq 0 (
    echo Git installation failed.
    pause
    exit /b
)

:: Xóa tệp cài đặt sau khi cài đặt xong
del Git-installer.exe

:: Clone repository
echo Cloning repository...
git clone https://github.com/DanhChinh/hit.git

:: Cài đặt các yêu cầu từ requirement.txt
echo Installing dependencies...
cd ".\hit\AI"
if exist requirement.txt (
    pip install -r requirement.txt
) else (
    echo requirement.txt not found.
    pause
    exit /b
)

echo Done!
pause
