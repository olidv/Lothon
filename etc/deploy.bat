@echo off
color E

rem Printa a apresentacao do deploy:
echo.
echo  DEPLOY DO LOTHON   [ D:\WORKSPACE\PYTHON\LOTHON\ETC\DEPLOY.BAT ]
echo.
echo.

echo  *******************************************
echo  **  INICIANDO  IMPLANTACAO  DO  LOTHON.  **
echo  *******************************************
echo.
echo.

echo Posicionando no diretorio raiz da aplicacao
cd /d C:\Apps\B3\Lothon
echo.

echo Limpando as pastas temporarias da aplicacao
rem del /f /q logs\*.*        1>nul  2>&1
rem del /f /q data\caixa\*.*  1>nul  2>&1
del /f /q data\bolao\*.*      1>nul  2>&1
del /f /q data\cache\D_*.csv  1>nul  2>&1
del /f /q data\palpite\*.*    1>nul  2>&1
echo.

echo Posicionando no diretorio do projeto
cd /d D:\Workspace\Python\Lothon\
echo.

echo Copiando os arquivos do projeto
xcopy dist\*.* C:\Apps\B3\Lothon  /E /C /Q /H /R /Y
rem copy /y data\cache\*.* C:\Apps\B3\Lothon\data\cache
rem copy /y data\caixa\*.* C:\Apps\B3\Lothon\data\caixa
echo.

rem Pausa final...
echo.
pause
