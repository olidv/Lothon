@echo off
color F

echo Posicionando no diretorio raiz do projeto
cd ..
echo.

echo Verificando a versao atual do Python no sistema
python --version
echo.

echo Atualizando o pip no sistema para evitar conflitos de versoes
python -m pip install --upgrade pip
echo.

echo Verificando a versao atual do pip no sistema
pip --version
echo.

echo Ativando o ambiente virtual do projeto
call venv\Scripts\activate.bat
echo.

echo Verificando a versao atual do Python no ambiente
python --version
echo.

echo Atualizando o pip no ambiente para evitar conflitos de versoes
python -m pip install --upgrade pip
echo.

echo Verificando a versao atual do pip no ambiente
pip --version
echo.

echo Instalando as dependencias do projeto no ambiente
@echo on
pip install -U numpy
pip install -U pandas
pip install -U patsy
pip install -U matplotlib
pip install -U bokeh
pip install -U scipy
pip install -U statsmodels
pip install -U seaborn
pip install -U scikit-learn
pip install -U pingouin
pip install -U jupyterlab
@echo off
echo.

echo Atualizando a lista de dependencias do projeto [ requirements ]
python -m pip freeze > requirements.txt
echo.

rem Pausa final...
echo.
pause
