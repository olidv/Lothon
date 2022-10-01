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
from lothon.process.analyze.analise_unitario import AnaliseUnitario
from lothon.process.analyze.analise_premiacao import AnalisePremiacao


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# define quais os processamentos a serem realizados:
EXEC_ANALISE_SORTEIO_PRINCIPAL: bool = True
EXEC_ANALISE_SORTEIO_SECUNDARIO: bool = False
EXEC_ANALISE_TODAS_LOTERIAS: bool = False


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
        # "diadesorte": domain.get_dia_de_sorte(),         #
        # "duplasena": domain.get_dupla_sena(),            #
        # "lotofacil": domain.get_lotofacil(),             #
        # "quina": domain.get_quina(),                     #
        "megasena": domain.get_mega_sena(),              #
        # "lotomania": domain.get_lotomania(),           #
        # "maismilionaria": domain.get_mais_milionaria(),#
        # "supersete": domain.get_super_sete(),          #
        # "timemania": domain.get_timemania()            #
    }
    logger.info("Criadas instancias das loterias para processamento, "
                "com ultimos sorteios carregados dos arquivos HTML de resultados.")
    # estrutura comum para parametrizacao dos processamentos:
    options: dict[str: Any] = {}

    # --- ANALISE DO SORTEIO PRINCIPAL ---------------------------------------

    if EXEC_ANALISE_SORTEIO_PRINCIPAL:
        logger.debug("Inicializando a cadeia de processos para analise dos sorteios...")
        analise_chain: list[AbstractAnalyze] = analyze.get_process_chain()

        # configura cada um dos processos antes, mas apenas uma unica vez:
        for aproc in analise_chain:
            # configuracao de parametros para os processamentos:
            logger.debug(f"processo '{aproc.id_process}': inicializando configuracao.")
            aproc.setup(options)

        logger.debug("Vai executar todos os processos de analise para as loterias...")
        for key, loteria in loterias_caixa.items():
            # efetua a execucao de cada processo de analise em sequencia (chain):
            for proc in analise_chain:
                #  executa a analise para cada loteria:
                logger.debug(f"Processo '{proc.id_process}': "
                             f"executando analise da loteria '{key}'.")
                proc.execute(loteria)

    # --- ANALISE DO SORTEIO SECUNDARIO --------------------------------------

    if EXEC_ANALISE_SORTEIO_SECUNDARIO:
        # analise dos sorteios secundarios: Mes da Sorte, Time do Coracao, Trevo Duplo.
        sorteios_secundarios: dict[str: Loteria] = {
            # "mesdasorte": domain.get_mes_da_sorte(),        #
            # "timedocoracao": domain.get_time_do_coracao(),  #
            # "trevoduplo": domain.get_trevo_duplo()          #
        }

        # configura o processo de analise antes, mas apenas uma unica vez para todas as loterias:
        analise_unitaria: AnaliseUnitario = AnaliseUnitario()
        logger.debug(f"processo '{analise_unitaria.id_process}': inicializando configuracao.")
        analise_unitaria.setup(options)

        logger.debug("Vai executar o processo de analise unica para os sorteios secundarios...")
        for key, loteria in sorteios_secundarios.items():
            #  executa a analise para cada loteria:
            logger.debug(f"Processo '{analise_unitaria.id_process}': "
                         f"executando analise unica do sorteio secundario '{key}'.")
            analise_unitaria.execute(loteria)

    # --- ANALISE GERAL DAS LOTERIAS -----------------------------------------

    if EXEC_ANALISE_TODAS_LOTERIAS:
        # analise executada uma unica vez, mas para todas as loterias, para comparacao.
        analise_premiacao: AnalisePremiacao = AnalisePremiacao()
        # configuracao de parametros para os processamentos:
        logger.debug(f"processo '{analise_premiacao.id_process}': inicializando configuracao.")
        analise_premiacao.setup(options)
        logger.debug(f"Processo '{analise_premiacao.id_process}': executando analise da "
                     f"loteria 'mesdasorte'.")
        analise_premiacao.execute(loterias_caixa)

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    _stopWatch = stopwatch(_startWatch)
    logger.info(f"Finalizada a analise de sorteios para todos os concursos das loterias. "
                f"Tempo de Processamento: {_stopWatch}")

    return 0

# ----------------------------------------------------------------------------
