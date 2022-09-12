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
from lothon.process.betting import AbstractBetting, \
                                   BetDiaDeSorte, BetDuplaSena, BetLotofacil, \
                                   BetLotomania, BetMaisMilionaria, BetMegaSena, \
                                   BetQuina, BetSuperSete, BetTimemania


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# numero de palpites a serem gerados para as loterias consideradas eh sempre 100, por enquanto:
loterias_palpites: dict[str: dict[str: dict[int: int]]] = {
    "diadesorte": {
        "P100": {7: 100}
    },
    "duplasena": {
        "P100": {6: 100}
    },
    "lotofacil": {
        "P100": {15: 100}
    },
    "lotomania": {
        "P100": {50: 100}
    },
    "maismilionaria": {
        "P100": {6: 100}
    },
    "megasena": {
        "P100": {6: 100}
    },
    "quina": {
        "P100": {5: 100}
    },
    "supersete": {
        "P100": {7: 100}
    },
    "timemania": {
        "P100": {10: 100}
    }
}

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
    loterias_caixa: dict[str: AbstractBetting] = {
        "diadesorte": BetDiaDeSorte(domain.get_dia_de_sorte()),
        "duplasena": BetDuplaSena(domain.get_dupla_sena()),
        "lotofacil": BetLotofacil(domain.get_lotofacil()),
        "lotomania": BetLotomania(domain.get_lotomania()),
        "maismilionaria": BetMaisMilionaria(domain.get_mais_milionaria()),
        "megasena": BetMegaSena(domain.get_mega_sena()),
        "quina": BetQuina(domain.get_quina()),
        "supersete": BetSuperSete(domain.get_super_sete()),
        "timemania": BetTimemania(domain.get_timemania())
    }
    logger.info("Criadas instancias das loterias para processamento, "
                "com ultimos sorteios carregados dos arquivos HTML de resultados.")

    logger.debug("Vai executar o processo de geracao de palpites para todas as loterias...")
    for id_loteria, bet_loteria in loterias_caixa.items():
        # efetua a execucao do processo de geracao de palpites para cada loteria:
        logger.debug(f"Processo '{bet_loteria.id_process}': gerando palpites para a loteria "
                     f"'{id_loteria}'.")
        for id_bolao, bolao in loterias_palpites[id_loteria].items():
            # utiliza a lista de concursos carregada do arquivo HTML (default):
            palpites: list[tuple] = bet_loteria.execute(bolao)

            # com os jogos gerados, converte as dezenas das tuplas em strings de 2 digitos:
            if id_loteria != 'supersete':  # a super sete apenas possui 1 digito...
                palpites = [tuple(f"{i:02}" for i in t) for t in palpites]

            # efetua a gravacao do arquivo CSV contendo os jogos gerados (palpites):
            domain.export_palpites(bet_loteria.loteria.nome_loteria.lower(), palpites)

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    _stopWatch = stopwatch(_startWatch)
    logger.info(f"Finalizada a geracao de palpites de apostas para as loterias. "
                f"Tempo de Processamento: {_stopWatch}")

    return 0

# ----------------------------------------------------------------------------
