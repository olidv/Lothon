@echo off
color 1F

rem Ativa o ambiente virtual da aplicacao:
call ..\venv\Scripts\activate.bat

rem Executa a aplicacao indicando o arquivo de configuracao:
python lothon.zip -c C:\Apps\Loto365\Lothon\conf -o
