"""
   Test Package
   Module  __main__.py

   Modulo principal do aplicativo Lothon, entry-point para execucao de
   tarefas individuais ou pelo notebook do Jupyter (import lib).
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import sys
import getopt
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.conf import settings
from lothon.process import analisar_sorteios, simular_jogos, gerar_boloes, \
                           conferir_apostas, exportar_arquivos

# ----------------------------------------------------------------------------
# CONSTANTES
# ----------------------------------------------------------------------------

# argumentos da linha de comando:
CMD_LINE_ARGS = "c:asbrot"

# Possiveis erros que podem ocorrer na execucao da aplicacao para retorno no sys.exit():
EXIT_ERROR_INVALID_ARGS = 1
EXIT_ERROR_NO_ARGS = 2
EXIT_ERROR_CONFIG_LOGGING = 3
EXIT_ERROR_CONFIG_INI = 4
EXIT_ERROR_MAIN = "O modulo '__main__.py' nao pode ser carregado por outro modulo!"

EXIT_SUCCESS = 0  # informa que na verdade nao ocorreu erro, executou com sucesso.


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# Este modulo nao pode ser carregado por outro modulo
if __name__ != '__main__':
    sys.exit(EXIT_ERROR_MAIN)
# prossegue somente se este programa foi executado como entry-point...


# ----------------------------------------------------------------------------
# ARGUMENTOS DE LINHA DE COMANDO
# ----------------------------------------------------------------------------

# exibe ao usuario a forma correta de execucao do programa:
def print_usage():
    print('\n'
          'Uso:\n'
          '  python lothon.zip [opcoes]\n'
          '\n'
          'Opcoes Gerais:\n'
          '  -c <path>   Informa o path para os arquivos de configuracao\n'
          '  -a          Efetua analise dos dados de sorteios das loterias\n'
          '  -s          Simula varios jogos para validar estrategias\n'
          '  -b          Gera boloes de apostas para loterias da Caixa\n'
          '  -r          Confere as apostas com os resultados das loterias\n'
          '  -o          Exporta arquivos CSV com dezenas sorteadas dos concursos\n'
          '  -t <proc>   Executa teste de funcionamento de algum processo\n')


# faz o parsing das opcoes e argumentos da linha de comando:
opts = None
try:
    # se parsing feito com sucesso - programa ira prosseguir:
    opts, args = getopt.getopt(sys.argv[1:], CMD_LINE_ARGS)

except getopt.GetoptError as ex:
    print(f"Erro no parsing dos argumentos da linha de comando: {repr(ex)}")
    # exibe ao usuario a forma correta de execucao do programa:
    print_usage()
    sys.exit(EXIT_ERROR_INVALID_ARGS)  # aborta apos avisar usuario

# se nenhuma opcao de execucao foi fornecida na linha de comando:
if (opts is None) or (len(opts) == 0):
    print("Erro no parsing dos argumentos da linha de comando...")
    # exibe ao usuario a forma correta de execucao do programa:
    print_usage()
    sys.exit(EXIT_ERROR_NO_ARGS)  # nao ha porque prosseguir...

# comandos e opcoes de execucao:
opt_cfpath = ''      # path para os arquivos de configuracao
opt_anlise = False   # Flag para analise de dados dos sorteios
opt_simula = False   # Flag para simulacao de jogos estrategicos
opt_boloes = False   # Flag para geracao de boloes de apostas
opt_result = False   # Flag para conferencia das apostas
opt_output = False   # Flag para exportacao de arquivos CSV (output)
opt_testef = False   # Flag para teste de funcionamento
opt_tstprc = ''      # id do processo a ser executado para testes
opt_valido = False   # Flag para identificar se argumentos estao ok

# identifica o comando/tarefa/job do Lothon a ser executado:
for opt, val in opts:
    if opt == '-c':
        opt_cfpath = val
        # valida o path para os arquivos de configuracao:
        if len(opt_cfpath) == 0:
            opt_cfpath = '.'  # utiliza o proprio diretorio do executavel.
    elif opt == '-a':
        opt_anlise = True
        opt_valido = True
    elif opt == '-s':
        opt_simula = True
        opt_valido = True
    elif opt == '-b':
        opt_boloes = True
        opt_valido = True
    elif opt == '-r':
        opt_result = True
        opt_valido = True
    elif opt == '-o':
        opt_output = True
        opt_valido = True
    elif opt == '-t':
        opt_testef = True
        opt_tstprc = val
        opt_valido = True

# se nenhuma opcao de execucao fornecida na linha de comando foi reconhecida:
if not opt_valido:
    # exibe ao usuario a forma correta de execucao do programa:
    print_usage()
    sys.exit(EXIT_ERROR_NO_ARGS)


# ----------------------------------------------------------------------------
# LOGGING
# ----------------------------------------------------------------------------

# verifica se conseguiu fazer a configuracao do logging:
if not settings.setup_logging(opt_cfpath):
    print("Erro ao configurar o logging da aplicacao...")
    sys.exit(EXIT_ERROR_CONFIG_LOGGING)  # nao ha porque prosseguir...

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)
logger.info("O logging foi configurado com sucesso para a aplicacao.")


# ----------------------------------------------------------------------------
# SETTINGS
# ----------------------------------------------------------------------------

# verifica se conseguiu fazer a leitura do arquivo de configuracao INI:
if not settings.setup_config(opt_cfpath):
    logger.critical("Execucao da aplicacao foi interrompida.")
    sys.exit(EXIT_ERROR_CONFIG_INI)  # aborta se nao puder carregar INI

# tudo ok, prossegue entao com o processamento:
logger.info("Aplicacao configurada e inicializada com sucesso.")
logger.debug(f"Argumentos da linha de comando: {str(opts).strip('[]')}")


# ----------------------------------------------------------------------------
# TESTES
# ----------------------------------------------------------------------------

# Rotina de testes - processo exclusivo em relacao aos outros processos:
if opt_testef:
    # Informa que tudo ok ate aqui, Lothon funcionando normalmente:
    logger.info(f"Modulo main() executado com sucesso! opt_testef = {opt_testef}")
    # finaliza por aqui o processamento se esta apenas testando (exclusivo):
    sys.exit(EXIT_SUCCESS)


# ----------------------------------------------------------------------------
# STARTUP
# ----------------------------------------------------------------------------

# Opcao para executar a analise dos dados de sorteios das loterias:
if opt_anlise:
    logger.debug("Vai iniciar a analise dos dados de sorteios das loterias...")
    analisar_sorteios.run()

# Opcao para executar a simulacao de varios jogos para validar estrategias:
if opt_simula:
    logger.debug("Vai iniciar a simulacao de varios jogos para validar estrategias...")
    simular_jogos.run()

# Opcao para executar a geracao de boloes de apostas para as loterias:
if opt_boloes:
    logger.debug("Vai iniciar a geracao de boloes de apostas para as loterias...")
    gerar_boloes.run()

# Opcao para executar a conferencia das apostas com os resultados das loterias:
if opt_result:
    logger.debug("Vai iniciar a conferencia das apostas com os resultados das loterias...")
    conferir_apostas.run()

# Opcao para executar a exportacao de arquivos CSV com dezenas sorteadas dos concursos:
if opt_output:
    logger.debug("Vai iniciar a exportacao de arquivos CSV com dezenas sorteadas dos concursos...")
    exportar_arquivos.run()

# finaliza o processamento informando que tudo foi ok:
sys.exit(EXIT_SUCCESS)


# ----------------------------------------------------------------------------
