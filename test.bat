@echo off
setlocal

rem Contribute to the Owner
rem print text file
set "contributionPath=data\contribution"
set "srcPath1=data\*.pak"
set "srcPath2=data\*.sig"
set "pathFile=path.txt"

set "vngFile1=VNGLogo-WindowsClient.sig"
set "vngFile2=VNGLogo-WindowsClient.pak"

call :ContributionPrint "%contributionPath%"
if errorlevel 1 exit /b 1

call :isDataExist "%srcPath1%" "%srcPath2%"
if errorlevel 1 exit /b 1

call :isPathExist "%pathFile%"
if errorlevel 1 exit /b 1

call :copyFiles "%srcPath1%" "%srcPath2%" "%destinationPath%"
call :removeFiles "%concatPath1%" "%concatPath2%"

pause
exit /b 0

:ContributionPrint
set "path=%~1"
if not exist "%path%" (
    echo Introduction file not found
    exit /b 1
)
type "%path%"
echo Do you wish to continue? (Y/N - Y is default)
set /p signal=
if "%signal%"=="" (set signal=Y)
if /i not "%signal%"=="Y" if /i not "%signal%"=="N" (
    echo Invalid input, please enter Y or N
    goto :ContributionPrint
)
if /i "%signal%"=="N" (
    echo Thank you for using the script. L11tled1no.
    exit /b 1
)
exit /b 0

:isDataExist
set "Path1=%~1"
set "Path2=%~2"
if not exist "%Path1%" (
    echo Data is missing, please download the zip again
    exit /b 1
)
if not exist "%Path2%" (
    echo Data is missing, please download the zip again
    exit /b 1
)
exit /b 0

:isPathExist
set "path=%~1"
if not exist "%path%" (
    echo Path file not found
    exit /b 1
)
set "destinationPath="
for /f "usebackq tokens=*" %%i in ("%path%") do set "destinationPath=%%i"
if not exist "%destinationPath%" (
    echo Destination path not found, please check the path.txt file
    exit /b 1
)
set "concatPath1=%destinationPath%\%vngFile1%"
set "concatPath2=%destinationPath%\%vngFile2%"
exit /b 0

:copyFiles
set "srcPath1=%~1"
set "srcPath2=%~2"
set "destinationPath=%~3"
copy "%srcPath1%" "%destinationPath%"
copy "%srcPath2%" "%destinationPath%"
echo Copy files successfully
exit /b 0

:removeFiles
set "concatPath1=%~1"
set "concatPath2=%~2"
if exist "%concatPath1%" (
    del "%concatPath1%"
    echo Remove %vngFile1% successfully
) else (
    echo File %vngFile1% not found, does not need to remove
)
if exist "%concatPath2%" (
    del "%concatPath2%"
    echo Remove %vngFile2% successfully
) else (
    echo File %vngFile2% not found, does not need to remove
)
exit /b 0