@echo off
cls

echo ZAP - Zippy Asset Packager Installation Setup
echo.

setlocal EnableDelayedExpansion
set "InstallDir=%LOCALAPPDATA%\ZAP"

set "GitHubURL="

:start

set "choice="
set /p "choice=Install ZAP? (Y/N): "

if /I "%choice%"=="N" (
    echo.
    echo Installation cancelled.
    exit /b
)

if /I not "%choice%"=="Y" (
    echo.
    echo Invalid choice. Please enter Y or N.
    goto start
)

echo.
echo Starting installation...
timeout /t 3

echo Installing ZAP to "%InstallDir%"...

if not exist "%InstallDir%" (
    mkdir "%InstallDir%"
)

echo Searching for the latest release of ZAP on GitHub... 
for /f "delims=" %%i in ('powershell -Command "((Invoke-RestMethod 'https://api.github.com/repos/Bkner3/zap/releases') | Where-Object { $_.prerelease -or $_.stable } | Select-Object -First 1).assets | Where-Object { $_.name -like '*zap.exe*' } | Select-Object -ExpandProperty browser_download_url"') do set DOWNLOAD_URL=%%i

echo Downloading ZAP from "%DOWNLOAD_URL%"...
echo.
curl -L -o "%InstallDir%\zap.exe" "%DOWNLOAD_URL%"