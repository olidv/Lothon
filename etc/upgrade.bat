@echo off

echo Posicionando no diretorio raiz do projeto
cd ..
echo.

echo Atualizando o pip no sistema para evitar conflitos de versoes
python -m pip install --upgrade pip
echo.

echo Verificando a versao atual do pip no sistema
pip --version
echo.

echo Ativa o ambiente virtual do projeto
call venv\Scripts\activate.bat
echo.

echo Atualizando o pip no ambiente para evitar conflitos de versoes
python -m pip install --upgrade pip
echo.

echo Verificando a versao atual do pip no ambiente
pip --version
echo.

echo Instalando as dependencias do projeto no ambiente
python -m pip install -r requirements.txt
echo.

rem Pausa final...
echo.
pause
