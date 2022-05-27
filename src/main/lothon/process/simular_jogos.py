"""
   Test Package
   Module  simular_jogos.py

   Modulo para executar a simulacao de varios jogos para validar estrategias.
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
from lothon.process.abstract_process import AbstractProcess
from lothon.process import simulate
# from lothon.stats import combinatoria as comb


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# relacao de instancias das loterias da caixa e boloes para processamento:
loterias_caixa: dict[str: Loteria] = None
boloes_caixa: dict[int: int] = {  # combinacoes de boloes para todas as faixas vendidas pela caixa.
    "megasena": {7: 50, 8: 12, 9: 4, 10: 2, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1},
    "quina": {6: 80, 7: 25, 8: 8, 9: 4, 10: 2, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1},
    "duplasena": {7: 60, 8: 15, 9: 5, 10: 2, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1},
    "lotofacil": {16: 40, 17: 5, 18: 1, 19: 1, 20: 1},
    "diadesorte": {8: 60, 9: 15, 10: 5, 11: 2, 12: 1, 13: 1, 14: 1, 15: 1}
}
boloes_945: dict[int: int] = {  # combinacoes de boloes para gasto diario maximo de R$ 945,00.
    "megasena": {7: 30, 8: 7, 9: 2, 10: 1},
    "quina": {6: 78, 7: 22, 8: 8, 9: 3, 10: 1, 11: 1},
    "duplasena": {7: 54, 8: 13, 9: 4, 10: 1},
    "lotofacil": {16: 23, 17: 2},
    "diadesorte": {8: 59, 9: 13, 10: 3, 11: 1}
}

# relacao de processos de simulacao, a serem executados sequencialmente:
process_chain: Optional[list[AbstractProcess]] = None

# parametros para configuracao dos processos de simulacao:
options: dict[str: Any] = {}


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# configura e executa o processo de simulacao:
def invoke_process(proc: AbstractProcess):
    # configura o processo antes,
    proc.init(options)

    # e depois executa a simulacao:
    proc.execute(loterias_caixa)


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas de simulacao:
# @profile
def run():
    global loterias_caixa, boloes_caixa, process_chain
    _startWatch = startwatch()
    logger.info("Iniciando a simulacao de jogos nos sorteios das loterias...")

    logger.debug("Vai efetuar carga das definicoes das loterias do arquivo de configuracao .INI")
    # Ja aproveita e efetua leitura dos arquivos HTML com resultados dos sorteios de cada loteria:
    loterias_caixa = {
        # "megasena": domain.get_mega_sena(boloes_945["megasena"]),
        # "quina": domain.get_quina(boloes_945["quina"]),
        # "duplasena": domain.get_dupla_sena(boloes_945["duplasena"]),
        # "lotofacil": domain.get_lotofacil(boloes_945["lotofacil"]),
        "diadesorte": domain.get_dia_de_sorte(boloes_945["diadesorte"])
    }
    logger.info("Criadas instancias das loterias para processamento, "
                "com ultimos sorteios carregados dos arquivos HTML de resultados.")

    logger.debug("Inicializando a cadeia de processos para simulacao de jogos...")
    process_chain = simulate.get_process_chain()

    # configuracao de parametros para os processamentos:
    options["qtd_proc"] = 500  # vai simular jogos apenas nos ultimos 500 concursos

    logger.debug("Vai executar todos os processos de simulacao...")
    # Efetua a execucao de cada processo de simulacao em sequencia (chain):
    for proc in process_chain:
        logger.debug(f"processo '{proc.id_process}': inicializando configuracao.")
        # configura o processo antes,
        proc.init(options)

        # e depois executa a simulacao para cada loteria:
        for key, loteria in loterias_caixa.items():
            logger.debug(f"Processo '{proc.id_process}': executando simulacao da loteria '{key}'.")
            proc.execute(loteria)

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    _stopWatch = stopwatch(_startWatch)
    logger.info(f"Finalizada a simulacao de jogos para todos os concursos das loterias. "
                f"Tempo de Processamento: {_stopWatch}")

    return 0

# ----------------------------------------------------------------------------
