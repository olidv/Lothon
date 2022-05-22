"""
   Test Package
   Module  gerar_boloes.py

   Modulo para executar a geracao de boloes de apostas para as loterias.
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
# from lothon.conf import app_config


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas diarias:
def run():
    logger.info("Iniciando a geracao de boloes de apostas para as loterias...")

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    logger.info("Finalizada a geracao de boloes de apostas para as loterias.")
    return 0

# ----------------------------------------------------------------------------
