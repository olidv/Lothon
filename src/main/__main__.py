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
from lothon.process import analisar_sorteios, gerar_boloes, conferir_apostas, simular_jogos

# ----------------------------------------------------------------------------
# CONSTANTES
# ----------------------------------------------------------------------------

# argumentos da linha de comando:
CMD_LINE_ARGS = "tabrsc:"

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
          '  -t          Executa teste de funcionamento\n'
          '  -a          Efetua analise dos dados de sorteios das loterias\n'
          '  -b          Gera boloes de apostas para loterias da Caixa\n'
          '  -r          Confere as apostas com os resultados das loterias\n'
          '  -s          Simula varios jogos para validar estrategias\n'
          '  -c <path>   Informa o path para os arquivos de configuracao\n')


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
opt_testes = False   # Flag para teste de funcionamento
opt_anlise = False   # Flag para analise de dados dos sorteios
opt_boloes = False   # Flag para geracao de boloes de apostas
opt_result = False   # Flag para conferencia das apostas
opt_simula = False   # Flag para simulacao de jogos estrategicos
opt_cfpath = ''      # path para os arquivos de configuracao

# identifica o comando/tarefa/job do Lothon a ser executado:
for opt, val in opts:
    if opt == '-t':
        opt_testes = True
    elif opt == '-a':
        opt_anlise = True
    elif opt == '-b':
        opt_boloes = True
    elif opt == '-r':
        opt_result = True
    elif opt == '-s':
        opt_simula = True
    elif opt == '-c':
        opt_cfpath = val

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

# Opcao para executar a analise dos dados de sorteios das loterias:
if opt_anlise:
    logger.debug("Vai iniciar a analise dos dados de sorteios das loterias...")
    analisar_sorteios.run()

# Opcao para executar a geracao de boloes de apostas para as loterias:
elif opt_boloes:
    logger.debug("Vai iniciar a geracao de boloes de apostas para as loterias...")
    gerar_boloes.run()

# Opcao para executar a conferencia das apostas com os resultados das loterias:
elif opt_result:
    logger.debug("Vai iniciar a conferencia das apostas com os resultados das loterias...")
    conferir_apostas.run()

# Opcao para executar a simulacao de varios jogos para validar estrategias:
elif opt_simula:
    logger.debug("Vai iniciar a simulacao de varios jogos para validar estrategias...")
    simular_jogos.run()

# se a opcao de execucao fornecida na linha de comando nao foi reconhecida:
else:
    # exibe ao usuario a forma correta de execucao do programa:
    print_usage()
    sys.exit(EXIT_ERROR_NO_ARGS)

# ----------------------------------------------------------------------------
