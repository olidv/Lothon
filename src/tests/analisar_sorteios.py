"""
   Test Package
   Module  analisar_sorteios.py

   Modulo para executar a analise dos dados de sorteios das loterias.
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.conf import app_config


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
    logger.info("Iniciando a analise dos dados de sorteios das loterias...")

    print('Analise OK!')

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    logger.info("Finalizada a analise dos dados de sorteios das loterias.")
    return 0

# ----------------------------------------------------------------------------
