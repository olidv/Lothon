"""
   Package .
   Module  __main__.py

   Modulo principal do aplicativo InFiniTe, entry-point para execucao de
   tarefas individuais ou pelo agendador utilitario do Python (lib schedule).
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
from infinite.conf import settings
from infinite import scheduler_diario
from infinite import scheduler_mensal


# ----------------------------------------------------------------------------
# CONSTANTES
# ----------------------------------------------------------------------------

# argumentos da linha de comando:
CMD_LINE_ARGS = "dmtc:"

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
          '  python infinite.zip [opcoes]\n'
          '\n'
          'Opcoes Gerais:\n'
          '  -c <path>   Informa o path para os arquivos de configuracao\n'
          '  -d          Agenda as tarefas diarias\n'
          '  -m          Agenda as tarefas mensais\n'
          '  -t          Executa teste de funcionamento\n')


# faz o parsing das opcoes e argumentos da linha de comando:
opts = None
try:
    # se parsing feito com sucesso - programa ira prosseguir:
    opts, args = getopt.getopt(sys.argv[1:], CMD_LINE_ARGS)

except getopt.GetoptError as ex:
    print("Erro no parsing dos argumentos da linha de comando:", repr(ex))
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
opt_diario = False   # Flag para tarefas diarias
opt_mensal = False   # Flag para tarefas mensais
opt_testes = False   # Flag para teste de funcionamento

# identifica o comando/tarefa/job do InFiniTe a ser executado:
for opt, val in opts:
    if opt == '-c':
        opt_cfpath = val
    if opt == '-d':
        opt_diario = True
    elif opt == '-m':
        opt_mensal = True
    elif opt == '-t':
        opt_testes = True

# valida o path para os arquivos de configuracao:
if len(opt_cfpath) == 0:
    opt_cfpath = '.'  # utiliza o proprio diretorio do executavel.


# ----------------------------------------------------------------------------
# LOGGING
# ----------------------------------------------------------------------------

# verifica se conseguiu fazer a configuracao do logging:
if not settings.setup_logging(opt_cfpath):
    print("Erro ao configurar o logging da aplicacao...")
    sys.exit(EXIT_ERROR_CONFIG_LOGGING)  # nao ha porque prosseguir...

# obtem uma instância do logger para o modulo corrente:
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
logger.debug("Argumentos da linha de comando: " + str(opts).strip('[]'))


# ----------------------------------------------------------------------------
# TESTES
# ----------------------------------------------------------------------------

# Rotina de testes:
if opt_testes:
    # aborta o processamento se esta apenas testando:
    logger.info("Modulo main() executado com sucesso! opt_testes = %s", opt_testes)
    sys.exit(EXIT_SUCCESS)


# ----------------------------------------------------------------------------
# STARTUP
# ----------------------------------------------------------------------------

# configura as tarefas no scheduler de acordo com as opcoes de execucao:
if opt_diario:
    logger.debug("Vai iniciar o scheduler diario...")
    # Executa schedulers para agendar as tarefas (jobs)
    sys.exit(scheduler_diario.main())

elif opt_mensal:
    logger.debug("Vai iniciar o scheduler mensal...")
    # Executa schedulers para agendar as tarefas (jobs)
    sys.exit(scheduler_mensal.main())

# se a opcao de execucao fornecida na linha de comando nao foi reconhecida:
else:
    # exibe ao usuario a forma correta de execucao do programa:
    print_usage()
    sys.exit(EXIT_ERROR_NO_ARGS)

# ----------------------------------------------------------------------------
