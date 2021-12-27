rem @echo off

rem ativa o ambiente virtual do projeto
cd ..
call venv\Scripts\activate.bat

rem apaga a pasta de distribuicao para nova release
rmdir /s /q dist  1>nul  2>&1

rem monta estrutura para distribuir o pacote de executavel
mkdir dist  1>nul  2>&1
mkdir dist\bin  1>nul  2>&1
mkdir dist\conf  1>nul  2>&1
mkdir dist\logs  1>nul  2>&1
mkdir dist\tmp  1>nul  2>&1
mkdir dist\www  1>nul  2>&1

rem atualiza a lista de dependencias do projeto
python -m pip freeze > requirements.txt
copy requirements.txt dist\  

rem elimina os arquivos de byte-code temporarios
forfiles /p .\src\main /s /m __pycache__ /c "cmd /c rmdir /s /q @file"  1>nul  2>&1

rem compacta o codigo fonte no pacote executavel
python -m zipfile -c dist\bin\infinite.zip src\main\infinite src\main\__main__.py

rem copia para distribuicao os arquivos resources e scripts
copy src\scripts\*.* dist\bin\
copy src\resources\prod\*.* dist\conf\
copy src\resources\README.md dist\

rem executa o programa para testar se tudo ok
cd dist\bin
python infinite.zip -t -c ..\conf


rem instala as dependencias do projeto (ambiente virtual corrente)
rem python -m pip install -r requirements.txt

rem atualiza versao do utilitario pip
rem python -m pip install --upgrade pip

pause