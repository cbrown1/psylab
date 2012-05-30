@echo off

:: A batch script to install a Python module. No further comment...

:: Get Python version
set ver=%1
if %ver%.==. goto NoArg
set maj=%ver:~0,-2%
set min=%ver:~2%

:: Get Package name & version
for /f %%i in ('c:\python%maj%%min%\python.exe setup.py --name') do set packagename=%%i
for /f %%i in ('c:\python%maj%%min%\python.exe setup.py --version') do set packagever=%%i

:: Get architecture
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" goto 64BIT
set arch=win32
goto ENDARCH
:64BIT
set arch=amd64
:ENDARCH

:: Find uninstaller, run it
set package=dist\%packagename%-%packagever%.%arch%-py%ver%.msi
IF EXIST %package% goto ENDUNINSTALLERNAME
set package=dist\%packagename%-%packagever%.%arch%.msi
IF EXIST %package% goto ENDUNINSTALLERNAME
echo No uninstaller found
goto NoUninstaller
:ENDUNINSTALLERNAME
:: Uninstall
msiexec /uninstall %package% /qn
REM (ignore uninstall errors)
echo Uninstalling DONE.
:NoUninstaller

:: Build new installer
echo Building Installer DONE.
c:\python%maj%%min%\python.exe setup.py bdist_msi

:: Find installer, run it
set package=dist\%packagename%-%packagever%.%arch%-py%ver%.msi
IF EXIST %package% goto ENDINSTALLERNAME
set package=dist\%packagename%-%packagever%.%arch%.msi
IF EXIST %package% goto ENDINSTALLERNAME
echo No installer found
goto NoInstaller
:ENDINSTALLERNAME
:: Install
msiexec /i %package% /quiet
if ERRORLEVEL 1 goto InstallError
echo Installing DONE.
goto End1
:NoInstaller
goto End1

:PackageNameError
echo Error getting installer name
goto End1

:BuildingInstallerError
echo Error building
goto End1

:InstallError
echo Error installing
goto End1

:NoArg
echo Pass Python version number as major.minor. Example: reinstall_win.bat 2.7
goto End1

:End1
