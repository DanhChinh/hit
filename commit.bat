@echo off
echo Đang kiểm tra trạng thái Git...
git status

echo Đang thêm các thay đổi vào staging area...
git add .

git config --global user.email "danhchinh2024@gmail.com"
git config --global user.name "chinh.com"

echo Đang commit các thay đổi...
git commit -m "Auto commit: %date% %time%"

echo Đang push các thay đổi lên GitHub...
git push origin main

echo Hoàn thành!
pause