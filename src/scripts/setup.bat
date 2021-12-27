@echo off

rem atualiza o pip para evitar conflitos de versoes:
python -m pip install --upgrade pip
pip --version

rem ativa o ambiente virtual do projeto
call ..\venv\Scripts\activate.bat

rem instala as dependencias do projeto no ambiente:
python -m pip install -r ..\requirements.txt

pause