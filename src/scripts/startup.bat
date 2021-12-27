@echo off

rem ativa o ambiente virtual do projeto
call ..\venv\Scripts\activate.bat

python infinite.zip -d -c C:\Apps\B3\InFiniTe\conf
