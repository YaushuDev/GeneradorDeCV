@echo off
echo ========================================
echo   Generador de CV - Build Script
echo ========================================
echo.
echo Generando ejecutable con PyInstaller...
echo.

.venv\Scripts\pyinstaller.exe --name="GeneradorCV" --onefile --console --add-data "templates;templates" --add-data "static;static" --add-data "config;config" --add-data "models;models" --add-data "services;services" --add-data "routes;routes" app.py

echo.
echo ========================================
echo   Build completado!
echo ========================================
echo.
echo El ejecutable se encuentra en: dist\GeneradorCV.exe
echo.
pause
