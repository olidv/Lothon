"""
   Test Package
   Module  analisar_sorteios.py

   Modulo para executar a analise dos dados de sorteios das loterias.
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
# from memory_profiler import profile

# Own/Project modules
# from lothon.conf import app_config
from lothon.util.eve import *
from lothon import domain
from lothon.domain import Loteria
from lothon.process import analyze
from lothon.process.analyze.abstract_analyze import AbstractAnalyze


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

# entry-point de execucao para tarefas de analise:
# @profile
def run():
    _startWatch = startwatch()
    logger.info("Iniciando a analise dos dados de sorteios das loterias...")

    logger.debug("Vai efetuar carga das definicoes das loterias do arquivo de configuracao .INI")
    # Ja aproveita e efetua leitura dos arquivos HTML com resultados dos sorteios de cada loteria:
    loterias_caixa: dict[str: Loteria] = {
        "diadesorte": domain.get_dia_de_sorte(),  #
        # "mesdasorte": domain.get_mes_da_sorte(),  #
        # "lotofacil": domain.get_lotofacil(),      #
        # "duplasena": domain.get_dupla_sena(),     #
        # "quina": domain.get_quina(),              #
        # "megasena": domain.get_mega_sena()        #
    }
    logger.info("Criadas instancias das loterias para processamento, "
                "com ultimos sorteios carregados dos arquivos HTML de resultados.")

    logger.debug("Inicializando a cadeia de processos para analise dos sorteios...")
    analise_chain: list[AbstractAnalyze] = analyze.get_process_chain()

    # configura cada um dos processos antes, mas apenas uma unica vez:
    options: dict[str: Any] = {}
    for aproc in analise_chain:
        # configuracao de parametros para os processamentos:
        logger.debug(f"processo '{aproc.id_process}': inicializando configuracao.")
        aproc.setup(options)

    logger.debug("Vai executar todos os processos de analise para as loterias...")
    for key, loteria in loterias_caixa.items():
        # efetua a execucao de cada processo de analise em sequencia (chain):
        for proc in analise_chain:
            #  executa a analise para cada loteria:
            logger.debug(f"Processo '{proc.id_process}': executando analise da loteria '{key}'.")
            proc.execute(loteria)

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    _stopWatch = stopwatch(_startWatch)
    logger.info(f"Finalizada a analise de sorteios para todos os concursos das loterias. "
                f"Tempo de Processamento: {_stopWatch}")

    return 0

# ----------------------------------------------------------------------------
