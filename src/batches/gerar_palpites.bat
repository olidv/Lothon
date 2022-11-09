@echo off
color 1F

rem Printa a apresentacao do Lothon.
echo.
echo  GERAR PALPITES   [ C:\APPS\INFINITE\LOTHON\BIN\GERAR_PALPITES.BAT ]
echo.
echo.

rem verifica se o flag indicativo de processamento existe:
if exist C:\Apps\Infinite\Lothon\data\safeToDelete.tmp goto yesfile

:nofile
color C
echo  ************************************************
echo  ** ATENCAO: FLAG safeToDelete NAO ENCONTRADO! **
echo  ************************************************
echo  **    ESTA  ROTINA  BATCH  SERA  ABORTADA.    **
echo  ************************************************
echo.
goto endbat

:yesfile
color B
echo  ************************************************
echo  **  FLAG OK: ARQUIVO safeToDelete ENCONTRADO. **
echo  ************************************************
echo  ** PREPARANDO P/ GERAR PALPITES DAS LOTERIAS. **
echo  ************************************************
echo.
echo.

echo Posicionando no diretorio da aplicacao Lothon para geracao de palpites:
cd /D C:\Apps\Infinite\Lothon\bin
start /b /wait palpites.bat
echo.

echo Copiando Arquivos CSV de palpites para projetos do Lothon...
copy /Y C:\Apps\Infinite\Lothon\data\palpite\*.csv \\BLACK\Publico\Colethon\Lothon\data\palpite\
echo.

echo Criando arquivo flag na pasta compartilhada do Colethon [safeToDelete.tmp]...
touch \\BLACK\Publico\Colethon\safeToDelete.tmp
echo.

echo Removendo arquivo flag local [safeToDelete.tmp]...
del /F /Q C:\Apps\Infinite\Lothon\data\safeToDelete.tmp
echo.

:endbat
rem Pausa final...
rem echo.
rem pause
