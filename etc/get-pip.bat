@echo off

echo Obtendo ultima versao do pip para Windows
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
echo.

echo Instalando o pip no sistema
python get-pip.py

echo Verificando a versao atual do pip no sistema
pip --version
echo.

rem Pausa final...
echo.
pause
