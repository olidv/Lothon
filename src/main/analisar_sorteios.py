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
from memory_profiler import profile

# Own/Project modules
# from lothon.conf import app_config
from lothon.domain import Loteria
from lothon.domain import dia_de_sorte, dupla_sena, lotofacil, lotomania, mega_sena, quina, \
                          super_sete, timemania, mes_da_sorte, time_do_coracao
from lothon.infra import parser_resultados


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
@profile
def run():
    logger.info("Iniciando a analise dos dados de sorteios das loterias...")

    _dia_de_sorte: Loteria = dia_de_sorte()
    _dupla_sena: Loteria = dupla_sena()
    _lotofacil: Loteria = lotofacil()
    _lotomania: Loteria = lotomania()
    _mega_sena: Loteria = mega_sena()
    _quina: Loteria = quina()
    _super_sete: Loteria = super_sete()
    _timemania: Loteria = timemania()
    _mes_da_sorte: Loteria = mes_da_sorte()
    _time_do_coracao: Loteria = time_do_coracao()

    print('Instancias OK!')

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

    print('Carga OK!')

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    logger.info("Finalizada a analise dos dados de sorteios das loterias.")
    return 0

# ----------------------------------------------------------------------------
