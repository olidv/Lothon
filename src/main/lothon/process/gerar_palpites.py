"""
   Test Package
   Module  gerar_palpites.py

   Modulo para executar a geracao de palpites de apostas para as loterias.
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
from lothon.process.quickpick import AbstractQuickPick, \
                                     PickDiaDeSorte, PickDuplaSena, PickLotofacil, \
                                     PickLotomania, PickMaisMilionaria, PickMegaSena, \
                                     PickQuina, PickSuperSete, PickTimemania


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# numero de palpites a serem gerados para as loterias consideradas:
PALPITES_DIADESORTE: int = 112
PALPITES_DUPLASENA: int = 114
PALPITES_LOTOFACIL: int = 114
PALPITES_LOTOMANIA: int = 100
PALPITES_MAISMILIONARIA: int = 120
PALPITES_MEGASENA: int = 114
PALPITES_QUINA: int = 102
PALPITES_SUPERSETE: int = 108
PALPITES_TIMEMANIA: int = 115


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas diarias:
def run():
    _startWatch = startwatch()
    logger.info("Iniciando a geracao de palpites de apostas para as loterias...")

    # relacao de instancias das loterias da caixa e quantidades de palpites para processamento:
    logger.debug("Vai efetutar carga das definicoes das loterias do arquivo de configuracao .INI")
    # aproveita p/ efetuar leitura dos arquivos HTML com resultados dos sorteios de cada loteria:
    loterias_caixa: dict[str: AbstractQuickPick] = {
        "diadesorte": PickDiaDeSorte(domain.get_dia_de_sorte(),
                                     domain.get_mes_da_sorte()),
        "duplasena": PickDuplaSena(domain.get_dupla_sena()),
        "lotofacil": PickLotofacil(domain.get_lotofacil()),
        "lotomania": PickLotomania(domain.get_lotomania()),
        "maismilionaria": PickMaisMilionaria(domain.get_mais_milionaria(),
                                             domain.get_trevo_duplo()),
        "megasena": PickMegaSena(domain.get_mega_sena()),
        "quina": PickQuina(domain.get_quina()),
        "supersete": PickSuperSete(domain.get_super_sete()),
        "timemania": PickTimemania(domain.get_timemania())
    }
    loterias_palpites: dict[str: int] = {
        "diadesorte": PALPITES_DIADESORTE,
        "duplasena": PALPITES_DUPLASENA,
        "lotofacil": PALPITES_LOTOFACIL,
        "lotomania": PALPITES_LOTOMANIA,
        "maismilionaria": PALPITES_MAISMILIONARIA,
        "megasena": PALPITES_MEGASENA,
        "quina": PALPITES_QUINA,
        "supersete": PALPITES_SUPERSETE,
        "timemania": PALPITES_TIMEMANIA
    }
    logger.info("Criadas instancias das loterias para processamento, "
                "com ultimos sorteios carregados dos arquivos HTML de resultados.")

    logger.debug("Vai executar o processo de geracao de palpites para todas as loterias...")
    for id_loteria, pick_loteria in loterias_caixa.items():
        # efetua a execucao do processo de geracao de palpites para cada loteria:
        logger.debug(f"Processo '{pick_loteria.id_process}': gerando palpites para a loteria "
                     f"'{id_loteria}'.")
        # utiliza a lista de concursos carregada do arquivo HTML (default):
        palpites: list[tuple] = pick_loteria.execute(loterias_palpites[id_loteria])

        # efetua a gravacao do arquivo CSV contendo os palpites gerados (dezenas):
        domain.export_palpites(pick_loteria.loteria.nome_loteria, palpites)

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    _stopWatch = stopwatch(_startWatch)
    logger.info(f"Finalizada a geracao de palpites de apostas para as loterias. "
                f"Tempo de Processamento: {_stopWatch}")

    return 0

# ----------------------------------------------------------------------------
