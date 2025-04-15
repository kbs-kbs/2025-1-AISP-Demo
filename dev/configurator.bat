@echo off
set "version=3.12"
set "path=%USERPROFILE%\AppDasta\Local\Programs\Python\Python%version:.=%"

if exist "%path%" (
(
echo @echo off
echo "%%~dp0python.exe" %%*
) > "%path%\python%version%.bat"
echo You can now use the 'python%version%' command.
) else (
echo Could not find '%path%'.
)