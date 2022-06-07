"""
   Test Package
   Module  simular_jogos.py

   Modulo para executar a simulacao de varios jogos para validar estrategias.
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
from lothon.process import simulate
from lothon.process.simulate.abstract_simulate import AbstractSimulate


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# relacao de instancias das loterias da caixa e boloes para processamento:
loterias_caixa: dict[str: Loteria] = None

# combinacoes de boloes para todas as faixas vendidas pela caixa.
boloes_caixa: dict[str: dict[int: int]] = {
    "megasena": {7: 50, 8: 12, 9: 4, 10: 2, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1},
    "quina": {6: 80, 7: 25, 8: 8, 9: 4, 10: 2, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1},
    "lotofacil": {16: 40, 17: 5, 18: 1, 19: 1, 20: 1},
    "diadesorte": {8: 60, 9: 15, 10: 5, 11: 2, 12: 1, 13: 1, 14: 1, 15: 1}
}

# combinacoes de boloes para gasto diario maximo de R$ 945,00.
boloes_945: dict[str: dict[int: int]] = {
    "megasena": {7: 30, 8: 7, 9: 2, 10: 1},
    "quina": {6: 78, 7: 22, 8: 8, 9: 3, 10: 1, 11: 1},
    "lotofacil": {16: 23, 17: 2},
    "diadesorte": {8: 59, 9: 13, 10: 3, 11: 1}
}

# relacao de processos de simulacao, a serem executados sequencialmente:
simulacao_chain: Optional[list[AbstractSimulate]] = None

# parametros para configuracao dos processos de simulacao:
options: dict[str: Any] = {}


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas de simulacao:
# @profile
def run():
    global loterias_caixa, boloes_caixa, simulacao_chain
    _startWatch = startwatch()
    logger.info("Iniciando a simulacao de jogos nos sorteios das loterias...")

    logger.debug("Vai efetuar carga das definicoes das loterias do arquivo de configuracao .INI")
    # Ja aproveita e efetua leitura dos arquivos HTML com resultados dos sorteios de cada loteria:
    loterias_caixa = {
        # "megasena": domain.get_mega_sena(),
        # "quina": domain.get_quina(),
        # "lotofacil": domain.get_lotofacil(),
        "diadesorte": domain.get_dia_de_sorte()
    }
    logger.info("Criadas instancias das loterias para processamento, "
                "com ultimos sorteios carregados dos arquivos HTML de resultados.")

    logger.debug("Inicializando a cadeia de processos para simulacao de jogos...")
    simulacao_chain = simulate.get_process_chain()

    # configura cada um dos processos antes, mas apenas uma unica vez:
    options["qtd_proc"] = 500  # vai simular jogos apenas nos ultimos 500 concursos
    options["boloes_caixa"] = boloes_945
    for sproc in simulacao_chain:
        # configuracao de parametros para os processamentos:
        logger.debug(f"processo '{sproc.id_process}': inicializando configuracao.")
        sproc.init(options)

    logger.debug("Vai executar todos os processos de simulacao para as loterias...")
    for key, loteria in loterias_caixa.items():
        # efetua a execucao de cada processo de simulacao em sequencia (chain):
        for sproc in simulacao_chain:
            # executa a simulacao para cada loteria:
            logger.debug(f"Processo '{sproc.id_process}': executando simulacao da loteria '{key}'.")
            sproc.execute(loteria)

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    _stopWatch = stopwatch(_startWatch)
    logger.info(f"Finalizada a simulacao de jogos para todos os concursos das loterias. "
                f"Tempo de Processamento: {_stopWatch}")

    return 0

# ----------------------------------------------------------------------------
