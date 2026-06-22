@echo off
REM PicX GUI Windows 打包脚本
REM 用于将应用打包为独立的Windows可执行文件

echo.
echo ========================================
echo PicX GUI Windows 打包脚本
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 错误: 未找到Python！
    echo 请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

REM 检查PyInstaller是否安装
python -c "import PyInstaller" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo 正在安装PyInstaller...
    pip install pyinstaller
)

REM 检查libvips是否存在
if not exist "libs\libvips\bin" (
    echo.
    echo ========================================
    echo 警告: 未找到libvips！
    echo ========================================
    echo.
    echo libvips用于支持大图和TIFF格式处理
    echo 如果不需要这些功能，可以继续打包
    echo.
    echo 如需安装libvips:
    echo   1. 运行: python setup_libvips.py
    echo   2. 或手动下载: https://github.com/libvips/libvips/releases
    echo   3. 解压bin目录到: libs\libvips\bin\
    echo.
    set /p continue="是否继续打包（不包含libvips）？(y/N): "
    if /i not "%continue%"=="y" (
        echo 已取消打包
        pause
        exit /b 0
    )
) else (
    echo ✓ 找到libvips，将包含在打包文件中
)

echo.
echo 正在清理旧的构建文件...
if exist "build" (
    rmdir /s /q build
    echo   已删除 build 目录
)
if exist "dist" (
    rmdir /s /q dist
    echo   已删除 dist 目录
)

echo.
echo 正在使用PyInstaller打包...
echo 这可能需要几分钟时间...
echo.

pyinstaller build_windows.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo ✓ 打包完成！
    echo ========================================
    echo.
    echo 可执行文件位于: dist\PicX-GUI\
    echo 主程序: dist\PicX-GUI\PicX-GUI.exe
    echo.
    echo 整个 dist\PicX-GUI 文件夹可以分发给用户
    echo 用户无需安装Python或任何依赖
    echo.
    
    REM 显示打包大小
    for /f %%A in ('powershell -command "(Get-ChildItem -Recurse dist\PicX-GUI | Measure-Object -Property Length -Sum).Sum / 1MB"') do set size=%%A
    echo 打包大小: 约 %size% MB
    echo.
    
    set /p test="是否立即测试运行？(Y/n): "
    if /i not "%test%"=="n" (
        echo.
        echo 正在启动应用...
        start "" "dist\PicX-GUI\PicX-GUI.exe"
    )
    
    echo.
    pause
) else (
    echo.
    echo ========================================
    echo ✗ 打包失败！
    echo ========================================
    echo.
    echo 请检查上面的错误信息
    echo 常见问题:
    echo   1. 缺少依赖: pip install -r requirements.txt
    echo   2. 导入错误: 检查Python代码是否有语法错误
    echo   3. 路径问题: 确保所有文件路径正确
    echo.
    pause
    exit /b 1
)
