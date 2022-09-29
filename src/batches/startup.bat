@echo off

rem Ativa o ambiente virtual da aplicacao:
call ..\venv\Scripts\activate.bat

rem Executa a aplicacao indicando o arquivo de configuracao:
python lothon.zip -c C:\Apps\Infinite\Lothon\conf -a
