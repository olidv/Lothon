"""
   Test Package
   Module  exportar_arquivos.py

   Modulo para executar a exportacao de arquivos CSV com dezenas sorteadas dos concursos.
"""

__all__ = [
    'run'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
# from lothon.conf import app_config
from lothon.util.eve import *
from lothon import domain
from lothon.domain import Loteria


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# relacao de instancias das loterias da caixa:
loterias_caixa: dict[str: Loteria] = None


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas diarias:
def run():
    global loterias_caixa
    _startWatch = startwatch()
    logger.info("Iniciando a exportacao de arquivos CSV com dezenas sorteadas dos concursos...")

    # sorteios: list[tuple[int, ...]] = domain.load_pares("lotofacil")
    # print(f"sorteios = #{len(sorteios)}")
    # if True is not None:
    #     return

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

    logger.debug("Vai exportar os arquivos CSV com dezenas sorteadas das loterias...")
    for key, loteria in loterias_caixa.items():
        # o local de gravacao dos arquivos ja foi padronizado na configuracao INI
        qtd_export: int = domain.export_sorteios(loteria)
        logger.debug(f"Foram exportados #{formatd(qtd_export)} sorteios da loteria "
                     f"{loteria.nome_loteria}' em arquivo CSV.")

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    _stopWatch = stopwatch(_startWatch)
    logger.info(f"Finalizada a exportacao de arquivos CSV com dezenas sorteadas dos concursos. "
                f"Tempo de Processamento: {_stopWatch}")

    return 0

# ----------------------------------------------------------------------------
