Criar classe ancestral e aplicar POO nos jobs
    substituir o "duck typing" no scheduler.

Incluir arquivo de controle em todos os jobs
    se j� executou no dia, nem arquivo de log copia...

Mover os arquivos de logging, para n�o deixar acumular na esta��o Dell.
    Logging do InFiniTe e Digital-Clock.

Apos a aplica��o atingir maturidade, desligar o logging dos frameworks.
    loggers:
      schedule:
        level: ERROR
      selenium:
        level: ERROR
      urllib3:
        level: ERROR

Incluir zip do diretorio \dist\*.* no InFiniTe.
    <app>.zip

Criar novo job de manuten��o para apagar logs antigos
    apagar arquivos de controle de dias anteriores (\infinite\temp\*), etc...

Criar novo job para download dos arquivos de resultados das loterias da caixa.
    dia de sorte:  //*[@id="resultados"]/div[2]/ul/li/a
    megasena:      //*[@id="resultados"]/div[2]/ul/li/a
    quina:         //*[@id="resultados"]/div[2]/ul/li/a
    timemania:     //*[@id="resultados"]/div[2]/ul/li/a
    lotomania:     //*[@id="resultados"]/div[2]/ul/li/a
    dupla-sena:    //*[@id="resultados"]/div[2]/ul/li/a 
    lotofacil:     //*[@id="resultados"]/div[2]/ul/li/a

Criar novo job para alertar para vencimentos de ativos como mini �ndices e op��es.
    Indicar pr�ximos ativos a serem negociados apos vencimento e dia/data da troca.

---------------------------------------------------------------------

** Dia 01/Janeiro/2022: revisar feriados B3 no InFiniTe (Python).

Substituir level CRITICAL por FATAL.
