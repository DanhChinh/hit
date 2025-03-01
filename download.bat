@echo off
echo Đang tải và cài đặt Python...
curl -o python_installer.exe https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe
start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1

echo Đang tải và cài đặt Git...
curl -o git_installer.exe https://github.com/git-for-windows/git/releases/download/v2.48.1.windows.1/Git-2.48.1-64-bit.exe
start /wait git_installer.exe /VERYSILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh"

echo Đang clone dự án từ GitHub...
git clone https://github.com/DanhChinh/hit.git

echo install module
cd ".\hit\AI"
pip install -r requirement.txt

echo Tất cả các tác vụ đã hoàn thành!
pause