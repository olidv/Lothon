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
del /f /q logs\*.*         1>nul  2>&1
del /f /q data\caixa\*.*   1>nul  2>&1
del /f /q data\input\*.*   1>nul  2>&1
del /f /q data\output\*.*  1>nul  2>&1
echo.

echo Posicionando no diretorio do projeto
cd /d D:\Workspace\Python\Lothon\
echo.

echo Copiando os arquivos do projeto
xcopy dist\*.* C:\Apps\B3\Lothon  /E /C /Q /H /R /Y
echo.

rem Pausa final...
echo.
pause
