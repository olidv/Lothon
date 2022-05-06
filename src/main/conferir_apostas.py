"""
   Test Package
   Module  conferir_apostas.py

   Modulo para executar a conferencia das apostas com os resultados das loterias.
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

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas diarias:
def run():
    logger.info("Iniciando a conferencia das apostas com os resultados das loterias...")

    print('Resultados OK!')

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    logger.info("Finalizada a conferencia das apostas com os resultados das loterias.")
    return 0

# ----------------------------------------------------------------------------
