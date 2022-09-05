@echo off

echo Posicionando no diretorio raiz do projeto
cd ..
echo.

echo Limpando as pastas temporarias do projeto
del /f /q data\bolao\*.*    1>nul  2>&1
del /f /q data\cache\*.*    1>nul  2>&1
del /f /q data\palpite\*.*  1>nul  2>&1
del /f /q logs\*.*          1>nul  2>&1
del /f /q www\*.*           1>nul  2>&1
del /f /q tmp\*.*           1>nul  2>&1
echo.

rem Pausa final...
rem echo.
rem pause
