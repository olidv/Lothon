@echo off
color 1F

echo Posicionando no diretorio raiz do projeto
cd ..
echo.

echo Ativando o ambiente virtual do projeto
call venv\Scripts\activate.bat
echo.

echo Executando o JupyterLab:
jupyter-lab
echo.
