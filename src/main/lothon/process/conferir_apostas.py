"""
   Test Package
   Module  conferir_apostas.py

   Modulo para executar a conferencia das apostas com os resultados das loterias.
"""

__all__ = [
    'run'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Any
import logging

# Libs/Frameworks modules
# Own/Project modules
# from lothon.conf import app_config
from lothon.util.eve import *
from lothon import domain
from lothon.domain import Loteria
from lothon.process import checkup
from lothon.process.checkup.abstract_checkup import AbstractCheckup


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
    _startWatch = startwatch()
    logger.info("Iniciando a conferencia das apostas com os resultados das loterias...")

    # relacao de instancias das loterias da caixa para processamento
    logger.debug("Vai efetuar carga das definicoes das loterias do arquivo de configuracao .INI")
    # aproveita p/ efetuar leitura dos arquivos HTML com resultados dos sorteios de cada loteria:
    loterias_caixa: dict[str: Loteria] = {
        "diadesorte": domain.get_dia_de_sorte(),         #
        "duplasena": domain.get_dupla_sena(),            #
        "lotofacil": domain.get_lotofacil(),             #
        "lotomania": domain.get_lotomania(),             #
        "quina": domain.get_quina(),                     #
        "maismilionaria": domain.get_mais_milionaria(),  #
        "megasena": domain.get_mega_sena(),              #
        "supersete": domain.get_super_sete(),            #
        "timemania": domain.get_timemania(),             #
    }

    logger.debug("Inicializando a cadeia de processos para analise dos sorteios...")
    check_chain: list[AbstractCheckup] = checkup.get_process_chain()

    # configura cada um dos processos antes, mas apenas uma unica vez:
    options: dict[str: Any] = {}
    for chkproc in check_chain:
        # configuracao de parametros para os processamentos:
        logger.debug(f"processo '{chkproc.id_process}': inicializando configuracao.")
        chkproc.setup(options)

    logger.debug("Vai executar todos os processos para conferencia dos resultados das loterias...")
    for key, loteria in loterias_caixa.items():
        # efetua a execucao de cada processo de analise em sequencia (chain):
        for chkproc in check_chain:
            #  executa a conferencia dos resultados da loteria:
            logger.debug(f"Processo '{chkproc.id_process}': executando conferencia de apostas "
                         f"da loteria '{key}'.")
            chkproc.execute(loteria)

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    _stopWatch = stopwatch(_startWatch)
    logger.info(f"Finalizada a conferencia das apostas com os resultados das loterias. "
                f"Tempo de Processamento: {_stopWatch}")

    return 0

# ----------------------------------------------------------------------------
