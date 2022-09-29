@echo off
color F

echo Verificando a versao atual do Python no sistema
python --version
echo.

echo Verificando a versao atual do pip no sistema
pip --version
echo.

echo Atualizando o pip no sistema para evitar conflitos de versoes
python -m pip install --upgrade pip
echo.

echo Posicionando no diretorio raiz da aplicacao
cd ..
echo.

echo Instalando ambiente virtual na aplicacao
python -m venv venv
echo.

echo Ativando o ambiente virtual da aplicacao
call venv\Scripts\activate.bat
echo.

echo Verificando a versao atual do Python no ambiente
python --version
echo.

echo Verificando a versao atual do pip no ambiente
pip --version
echo.

echo Atualizando o pip no ambiente para evitar conflitos de versoes
python -m pip install --upgrade pip
echo.

echo Instalando as dependencias da aplicacao no ambiente
python -m pip install -r requirements.txt
echo.

rem Pausa final...
echo.
pause
