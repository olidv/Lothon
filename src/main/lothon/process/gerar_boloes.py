"""
   Test Package
   Module  gerar_boloes.py

   Modulo para executar a geracao de boloes de apostas para as loterias.
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
from lothon.process.betting.abstract_betting import AbstractBetting
from lothon.process.betting.bet_dia_de_sorte import BetDiaDeSorte


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# combinacoes de boloes para todas as faixas vendidas pela caixa, para as loterias consideradas:
boloes_diadesorte: dict[str: dict[int: int]] = {
    "B01": {7: 90, 8: 60, 9: 15, 10: 5, 11: 2, 12: 1, 13: 1, 14: 1, 15: 1},
    # "B02": {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
    # "B03": {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
}
boloes_lotofacil: dict[str: dict[int: int]] = {
    "B01": {15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0},
    # "B02": {15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0},
    # "B03": {15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0}
}
boloes_duplasena: dict[str: dict[int: int]] = {
    "B01": {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
    # "B02": {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
    # "B03": {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
}
boloes_quina: dict[str: dict[int: int]] = {
    "B01": {5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
    # "B02": {5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
    # "B03": {5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
}
boloes_megasena: dict[str: dict[int: int]] = {
    "B01": {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
    # "B02": {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
    # "B03": {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
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
    logger.info("Iniciando a geracao de boloes de apostas para as loterias...")

    # relacao de instancias das loterias da caixa e boloes para processamento
    logger.debug("Vai efetuar carga das definicoes das loterias do arquivo de configuracao .INI")
    # aproveita p/ efetuar leitura dos arquivos HTML com resultados dos sorteios de cada loteria:
    loterias_caixa: dict[str: AbstractBetting] = {
        "diadesorte": BetDiaDeSorte(domain.get_dia_de_sorte()),  #
        # "lotofacil": BetLotofacil(domain.get_lotofacil()),       #
        # "duplasena": BetDuplaSena(domain.get_dupla_sena()),      #
        # "quina": BetQuina(domain.get_quina()),                   #
        # "megasena": BetMegaSena(domain.get_mega_sena())          #
    }
    loterias_boloes: dict[str: dict] = {
        "diadesorte": boloes_diadesorte,
        "lotofacil": boloes_lotofacil,
        "duplasena": boloes_duplasena,
        "quina": boloes_quina,
        "megasena": boloes_megasena
    }
    logger.info("Criadas instancias das loterias para processamento, "
                "com ultimos sorteios carregados dos arquivos HTML de resultados.")

    logger.debug("Vai executar o processo de geracao de boloes para todas as loterias...")
    for lot, bet in loterias_caixa.items():
        # efetua a execucao do processo de geracao de boloes para cada loteria:
        logger.debug(f"Processo '{bet.id_process}': gerando boloes para a loteria '{lot}'.")
        for id_bolao, bolao in loterias_boloes[lot].items():
            # utiliza a lista de concursos carregada do arquivo HTML (default):
            jogos: list[tuple[int, ...]] = bet.execute(bolao)

            # efetua a gravacao do arquivo CSV contendo os jogos gerados (boloes):
            domain.export_boloes(bet.loteria.nome_loteria, id_bolao, jogos)

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    _stopWatch = stopwatch(_startWatch)
    logger.info(f"Finalizada a geracao de boloes de apostas para as loterias. "
                f"Tempo de Processamento: {_stopWatch}")

    return 0

# ----------------------------------------------------------------------------
