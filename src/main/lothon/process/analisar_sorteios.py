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
from typing import Optional, Any

# Libs/Frameworks modules
# from memory_profiler import profile

# Own/Project modules
# from lothon.conf import app_config
from lothon.util.eve import *
from lothon import domain
from lothon.domain import Loteria
from lothon.process import analyze
from lothon.process.abstract_process import AbstractProcess


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# relacao de instancias das loterias da caixa:
loterias_caixa: dict[str: Loteria] = None

# relacao de processos de analise, a serem executados sequencialmente:
process_chain: Optional[list[AbstractProcess]] = None

# parametros para configuracao dos processos de analise:
options: dict[str: Any] = {}


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# configura e executa o processo de analise:
def invoke_process(proc: AbstractProcess):
    # configura o processo antes,
    proc.init(options)
    # e depois executa a analise:
    proc.execute(loterias_caixa)


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas de analise:
# @profile
def run():
    global loterias_caixa, process_chain
    _startWatch = startwatch()
    logger.info("Iniciando a analise dos dados de sorteios das loterias...")

    logger.debug("Vai efetuar carga das definicoes das loterias do arquivo de configuracao .INI")
    # Ja aproveita e efetua leitura dos arquivos HTML com resultados dos sorteios de cada loteria:
    loterias_caixa = {
        # "megasena": domain.get_mega_sena(),
        # "quina": domain.get_quina(),
        # "duplasena": domain.get_dupla_sena(),
        # "lotofacil": domain.get_lotofacil(),
        "diadesorte": domain.get_dia_de_sorte()
    }
    logger.info("Criadas instancias das loterias para processamento, "
                "com ultimos sorteios carregados dos arquivos HTML de resultados.")

    logger.debug("Inicializando a cadeia de processos para analise dos sorteios...")
    process_chain = analyze.get_process_chain()

    # configuracao de parametros para os processamentos:
    # options["qtd_proc"] = 500  # vai analisar sorteios apenas dos ultimos 500 concursos

    logger.debug("Vai executar todos os processos de analise...")
    # Efetua a execucao de cada processo de analise em sequencia (chain):
    for proc in process_chain:
        logger.debug(f"processo '{proc.id_process}': inicializando configuracao.")
        # configura o processo antes,
        proc.init(options)

        # e depois executa a analise para cada loteria:
        for key, loteria in loterias_caixa.items():
            logger.debug(f"Processo '{proc.id_process}': executando analise da loteria '{key}'.")
            proc.execute(loteria)

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    _stopWatch = stopwatch(_startWatch)
    logger.info(f"Finalizada a analise de sorteios para todos os concursos das loterias. "
                f"Tempo de Processamento: {_stopWatch}")

    return 0

# ----------------------------------------------------------------------------
