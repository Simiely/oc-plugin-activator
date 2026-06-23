@echo off
REM OC插件快速激活工具 - Windows 打包脚本
REM 双击运行即可生成 exe 文件

echo 正在检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 未检测到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

echo 正在安装 PyInstaller...
pip install pyinstaller

echo.
echo 正在打包程序为 exe...
pyinstaller --onefile --windowed --name "OC插件快速激活工具" oc_tool.py

echo.
echo 打包完成！
echo exe 文件位于 dist 文件夹内。
echo 请将 exe 放在包含 AppData 和 c4doctane 文件夹的目录中运行。
pause
