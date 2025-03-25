@echo off
chcp 65001 > nul
echo ==================================================
echo 渔网分割功能测试（无UI窗口模式）
echo ==================================================
echo.

cd /d %~dp0..

echo 开始测试... %date% %time%
echo 当前目录: %cd%
echo --------------------------------------------------

python test_scripts/test_fishnet_no_ui.py

echo.
echo 测试完成
echo.
echo 按任意键退出...
pause > nul 