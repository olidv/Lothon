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

echo Criando pasta do projeto
mkdir Lothon
echo.

echo Instalando ambiente virtual no projeto
python -m venv Lothon\venv
echo.

echo Posicionando no diretorio raiz do projeto
cd Lothon
echo.

echo Ativando o ambiente virtual do projeto
call venv\Scripts\activate.bat
echo.

echo Instalando as dependencias do projeto no ambiente
@echo on
pip install -U wheel
pip install -U setuptools
pip install -U memory_profiler
pip install -U PyYAML
pip install -U beautifulsoup4
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
pip install -U plotext
@echo off
echo.

echo Atualizando a lista de dependencias do projeto [ requirements ]
python -m pip freeze > requirements.txt
echo.

rem Pausa final...
echo.
pause
