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

echo Recuperando ultimo commit dos arquivos no repositorio GitHub...
cd /D C:\Users\qdev\Loto365\cdn-lothon
git pull origin main
echo.

echo Copiando Arquivos CSV de papites para projeto CDN-Lothon...
copy /Y C:\Apps\Infinite\Lothon\data\palpite\*.csv C:\Users\qdev\Loto365\cdn-lothon\data\palpites
echo.

echo Efetuando commit dos arquivos CSV no repositorio GitHub...
cd /D C:\Users\qdev\Loto365\cdn-lothon
git commit -am "Novos palpites gerados diariamente pelo Lothon."
git push origin main
echo.

echo Ativando o ambiente virtual do Janitor para usar os scripts\*.py:
cd /D C:\Apps\Infinite\Janitor
call venv\Scripts\activate.bat
echo.

echo Capturando as telas de consulta dos palpites da Web...
cd /D C:\Users\qdev\Loto365\cdn-lothon\data\palpites
shot_palpites.py 100
echo.

echo Reduzindo as imagens capturadas para tamanho de mobile...
cd /D C:\Users\qdev\Loto365\cdn-lothon\data\palpites
reduce_palpites.py
echo.

echo Efetuando commit dos arquivos PNG e PDF no repositorio GitHub...
cd /D C:\Users\qdev\Loto365\cdn-lothon
git commit -am "Novos palpites gerados diariamente pelo Lothon."
git push origin main
echo.

echo Preparando recursos para criacao de video e publicacao nas redes sociais...
cd /D C:\Users\qdev\Loto365\docs-templates\Social
social_palpites.py
start .
echo.

echo Copiando Arquivos para publicacao dos palpites do dia...
del /F /Q \\BLACK\Publico\Colethon\Lothon\Social\*.*
copy /Y C:\Users\qdev\Loto365\docs-templates\Social\*.* \\BLACK\Publico\Colethon\Lothon\Social
echo.

echo Criando arquivo flag na pasta compartilhada do Colethon [safeToDelete.tmp]...
touch \\BLACK\Publico\Colethon\safeToDelete.tmp
echo.

echo Removendo arquivo flag local [safeToDelete.tmp]...
del /F /Q C:\Apps\Infinite\Lothon\data\safeToDelete.tmp
echo.

:endbat
rem Pausa final...
echo.
pause
