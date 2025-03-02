@echo off

:: Tải Python
echo Download Python...
curl -o python_installer.exe https://www.python.org/ftp/python/3.13.2/python-3.13.2-amd64.exe
start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
del python_installer.exe