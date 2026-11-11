@echo off
setlocal
if "%~1"=="run" goto run
call "%~dp0build.bat"
if errorlevel 1 exit /b 1
:run
"%~dp0Program\QEMU\qemu-system-x86_64.exe" -hda "%~dp0build\nova-os-26h2.img" -m 128 -boot c -vga std