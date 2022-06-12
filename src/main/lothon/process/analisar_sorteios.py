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
import logging
from typing import Optional, Any

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

# relacao de instancias das loterias da caixa:
loterias_caixa: dict[str: Loteria] = None

# relacao de processos de analise, a serem executados sequencialmente:
analise_chain: Optional[list[AbstractAnalyze]] = None

# parametros para configuracao dos processos de analise:
options: dict[str: Any] = {}


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas de analise:
# @profile
def run():
    global loterias_caixa, analise_chain
    _startWatch = startwatch()
    logger.info("Iniciando a analise dos dados de sorteios das loterias...")

    logger.debug("Vai efetuar carga das definicoes das loterias do arquivo de configuracao .INI")
    # Ja aproveita e efetua leitura dos arquivos HTML com resultados dos sorteios de cada loteria:
    loterias_caixa = {
        "diadesorte": domain.get_dia_de_sorte(),  # 1 min, 17 seg, 826 ms
        "lotofacil": domain.get_lotofacil(),      # 1 hor, 7 min, 41 seg, 548 ms
        "megasena": domain.get_mega_sena()        # 20 min, 33 seg, 370 ms
    }
    logger.info("Criadas instancias das loterias para processamento, "
                "com ultimos sorteios carregados dos arquivos HTML de resultados.")

    logger.debug("Inicializando a cadeia de processos para analise dos sorteios...")
    analise_chain = analyze.get_process_chain()

    # configura cada um dos processos antes, mas apenas uma unica vez:
    # options[""] = 0  # ...
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
