rem limpa as pastas temporarias da aplicacao:
del /f /q D:\Workspace\Python\InFiniTe\logs\*.*  1>nul  2>&1
del /f /q D:\Workspace\Python\InFiniTe\www\*.*   1>nul  2>&1
del /f /q D:\Workspace\Python\InFiniTe\tmp\*.*   1>nul  2>&1

rem limpa as pastas de arquivos dos terminais MT5:
del /f /q C:\Users\qdev\AppData\Roaming\MetaQuotes\Terminal\9AA5A2E564E1326FB93349159C9D30A4\MQL5\Files\*.*  1>nul  2>&1
del /f /q C:\Users\qdev\AppData\Roaming\MetaQuotes\Terminal\9352866EDE8D3BAA5CDBEF2EC84D2C07\MQL5\Files\*.*  1>nul  2>&1
del /f /q C:\Users\qdev\AppData\Roaming\MetaQuotes\Terminal\886B601D7760693D209A707150753C26\MQL5\Files\*.*  1>nul  2>&1

rem copia arquivos de D:\Publico\<corretora> para o terminal da respectiva corretora:
cd D:\Publico

xcopy clear\*.* C:\Users\qdev\AppData\Roaming\MetaQuotes\Terminal\9AA5A2E564E1326FB93349159C9D30A4\MQL5\Files  /E /C /Q /R /Y
xcopy genial\*.* C:\Users\qdev\AppData\Roaming\MetaQuotes\Terminal\9AA5A2E564E1326FB93349159C9D30A4\MQL5\Files  /E /C /Q /R /Y
xcopy modal\*.* C:\Users\qdev\AppData\Roaming\MetaQuotes\Terminal\9352866EDE8D3BAA5CDBEF2EC84D2C07\MQL5\Files  /E /C /Q /R /Y
xcopy xm\*.* C:\Users\qdev\AppData\Roaming\MetaQuotes\Terminal\886B601D7760693D209A707150753C26\MQL5\Files  /E /C /Q /R /Y

rem pause