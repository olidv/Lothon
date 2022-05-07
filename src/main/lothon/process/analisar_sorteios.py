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
# from memory_profiler import profile

# Own/Project modules
# from lothon.conf import app_config
from lothon import domain
from lothon.domain import Loteria
from lothon.infra import parser_resultados
import analyze


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
# @profile
def run():
    logger.info("Iniciando a analise dos dados de sorteios das loterias...")

    _dia_de_sorte: Loteria = domain.get_dia_de_sorte()
    _dupla_sena: Loteria = domain.get_dupla_sena()
    _lotofacil: Loteria = domain.get_lotofacil()
    _lotomania: Loteria = domain.get_lotomania()
    _mega_sena: Loteria = domain.get_mega_sena()
    _quina: Loteria = domain.get_quina()
    _super_sete: Loteria = domain.get_super_sete()
    _timemania: Loteria = domain.get_timemania()
    _mes_da_sorte: Loteria = domain.get_mes_da_sorte()
    _time_do_coracao: Loteria = domain.get_time_do_coracao()
    logger.debug("Criadas instancias das loterias para processamento.")

    parser_resultados.parse_concursos_loteria(_dia_de_sorte)
    parser_resultados.parse_concursos_loteria(_dupla_sena)
    parser_resultados.parse_concursos_loteria(_lotofacil)
    parser_resultados.parse_concursos_loteria(_lotomania)
    parser_resultados.parse_concursos_loteria(_mega_sena)
    parser_resultados.parse_concursos_loteria(_quina)
    parser_resultados.parse_concursos_loteria(_super_sete)
    parser_resultados.parse_concursos_loteria(_timemania)
    parser_resultados.parse_concursos_loteria(_mes_da_sorte)
    parser_resultados.parse_concursos_loteria(_time_do_coracao)
    logger.debug("Ultimos sorteios das loterias carregados dos arquivos HTML de resultados.")

    _process_chain: list = analyze.get_process_chain()

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    logger.info("Finalizada a analise dos dados de sorteios das loterias.")
    return 0

# ----------------------------------------------------------------------------
