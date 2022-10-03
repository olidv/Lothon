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

echo Recuperando ultimo commit dos arquivos CSV, PNG e PDF no repositorio GitHub...
cd /D C:\Users\qdev\Loto365\cdn-lothon
git pull origin main
echo.

echo Executando Firefox para verificar Loto365.com.br e atualizar Google Drive e Redes Sociais...
cd /D C:\Users\qdev\Loto365\docs-templates\Social
start "" "C:\Program Files (x86)\Notepad++\notepad++.exe" "C:\Users\qdev\Loto365\docs-templates\Social\descricao.txt" "C:\Users\qdev\Loto365\cdn-lothon\data\palpites\dia-de-sorte.csv"
start "" "C:\Program Files\Mozilla Firefox\firefox.exe" -url "https://www.Loto365.com.br/#palpites" "https://drive.google.com/drive/folders/1PjOJoHbueNMiNGKJHLP5tC7UEyuRRSvD" "https://web.whatsapp.com/" "https://web.telegram.org/z/#-1488280660" "https://twitter.com/compose/tweet" "https://www.facebook.com/Loto365br" "https://www.instagram.com/loto365br/" "https://studio.youtube.com/channel/UCiiGBkWJiej2eAfwcqiI77A/videos/upload" "https://www.linkedin.com/company/loto365br/?share=true" "https://br.pinterest.com/pin-builder/"
start .
echo.

echo Removendo arquivos flag [safeToDelete.tmp]...
del /F /Q C:\Apps\Infinite\Lothon\data\safeToDelete.tmp
echo.

:endbat
rem Pausa final...
echo.
pause
