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
from lothon import domain
from lothon import infra
from lothon.domain import Loteria
from lothon.process import analyze
from lothon.process.abstract_process import AbstractProcess


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
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

# entry-point de execucao para tarefas diarias:
# @profile
def run():
    global loterias_caixa, process_chain
    logger.info("Iniciando a analise dos dados de sorteios das loterias...")

    logger.debug("Vai efetuar carga das definicoes das loterias do arquivo de configuracao .INI")
    loterias_caixa = {"diadesorte": domain.get_dia_de_sorte(),
                      "duplasena": domain.get_dupla_sena(),
                      "lotofacil": domain.get_lotofacil(),
                      "lotomania": domain.get_lotomania(),
                      "megasena": domain.get_mega_sena(),
                      "quina": domain.get_quina(),
                      "supersete": domain.get_super_sete(),
                      "timemania": domain.get_timemania(),
                      "mesdasorte": domain.get_mes_da_sorte(),
                      "timedocoracao": domain.get_time_do_coracao()}
    logger.debug("Criadas instancias das loterias para processamento.")

    # Efetua leitura dos arquivos HTML com resultados dos sorteios de cada loteria:
    for key, value in loterias_caixa.items():
        logger.debug("Vai efetuar carga dos resultados da loteria: '%s'.", key)
        infra.parser_resultados.parse_concursos_loteria(value)
    logger.debug("Ultimos sorteios das loterias carregados dos arquivos HTML de resultados.")

    logger.debug("Inicializando a cadeia de processos para analise dos resultados...")
    process_chain = analyze.get_process_chain()

    # Efetua a execução de cada processo de análise:
    for proc in process_chain:
        invoke_process(proc)

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    logger.info("Finalizada a analise dos dados de sorteios das loterias.")
    return 0

# ----------------------------------------------------------------------------
