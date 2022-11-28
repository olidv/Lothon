@echo off
color 1F

rem Printa a apresentacao do Lothon.
echo.
echo  POSTAR PALPITES   [ C:\APPS\INFINITE\LOTHON\BIN\POSTAR_PALPITES.BAT ]
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
echo  ** PREPARANDO P/ POSTAR PALPITES DAS LOTERIAS **
echo  ************************************************
echo.
echo.

echo Efetuando commit no repositorio GitHub dos arquivos CSV de palpites...
cd /D D:\Workspace\United-Sapiens\Loto365\loto365-blogspot
git commit -am "Novos palpites gerados diariamente pelo Lothon."
git push origin main
echo.

rem echo Executando Firefox para verificar Loto365.com.br...
rem start "" "C:\Program Files (x86)\Notepad++\notepad++.exe" "D:\Workspace\United-Sapiens\loto365-blogspot\data\palpites\dia-de-sorte.csv"
rem start "" "C:\Program Files\Mozilla Firefox\firefox.exe" -url "https://www.Loto365.com.br/#palpites"
rem start .
rem echo.

echo Removendo arquivos flag [safeToDelete.tmp]...
del /F /Q C:\Apps\Infinite\Lothon\data\safeToDelete.tmp
echo.

:endbat
rem Pausa final...
rem echo.
rem pause
