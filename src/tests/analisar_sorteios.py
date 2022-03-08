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
# Own/Project modules
from lothon.conf import app_config
from lothon.domain import DIA_DE_SORTE, DUPLA_SENA, LOTOFACIL, LOTOMANIA, MEGA_SENA, QUINA, \
                          SUPER_SETE, TIMEMANIA, MES_DA_SORTE, TIME_DO_CORACAO
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
def run():
    logger.info("Iniciando a analise dos dados de sorteios das loterias...")

    print(DIA_DE_SORTE())
    print(DUPLA_SENA())
    print(LOTOFACIL())
    print(LOTOMANIA())
    print(MEGA_SENA())
    print(QUINA())
    print(SUPER_SETE())
    print(TIMEMANIA())
    print(MES_DA_SORTE())
    print(TIME_DO_CORACAO())

    print('Instancias OK!')

    parser_resultados.parse_concursos_loteria(DIA_DE_SORTE())
    parser_resultados.parse_concursos_loteria(DUPLA_SENA())
    parser_resultados.parse_concursos_loteria(LOTOFACIL())
    parser_resultados.parse_concursos_loteria(LOTOMANIA())
    parser_resultados.parse_concursos_loteria(MEGA_SENA())
    parser_resultados.parse_concursos_loteria(QUINA())
    parser_resultados.parse_concursos_loteria(SUPER_SETE())
    parser_resultados.parse_concursos_loteria(TIMEMANIA())
    parser_resultados.parse_concursos_loteria(TIME_DO_CORACAO())
    parser_resultados.parse_concursos_loteria(MES_DA_SORTE())

    print('Carga OK!')

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    logger.info("Finalizada a analise dos dados de sorteios das loterias.")
    return 0

# ----------------------------------------------------------------------------
