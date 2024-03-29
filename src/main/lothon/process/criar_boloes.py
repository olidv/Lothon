"""
   Test Package
   Module  criar_boloes.py

   Modulo para executar a criacao de boloes de apostas para as loterias.
"""

__all__ = [
    'run'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
import logging

# Libs/Frameworks modules
# Own/Project modules
# from lothon.conf import app_config
from lothon.util.eve import *
from lothon import domain
from lothon.process.betting import AbstractBetting, \
                                   BetDiaDeSorte, BetDuplaSena, BetLotofacil, BetLotomania, \
                                   BetMaisMilionaria, BetMegaSena, BetQuina, BetSuperSete, \
                                   BetTimemania, BetMesDaSorte, BetTimeDoCoracao, BetTrevoDuplo

# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# combinacoes de boloes para todas as faixas vendidas pela caixa, para as loterias consideradas:
loterias_boloes: dict[str: dict[str: dict[int: int]]] = {
    "diadesorte": {
        "B01": {7: 25, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
        # "B02": {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
        # "B03": {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
    },
    "duplasena": {
        "B01": {6: 5, 7: 2, 8: 1, 9: 2, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
        # "B02": {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
        # "B03": {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
    },
    "lotofacil": {
        "B01": {15: 10, 16: 8, 17: 6, 18: 4, 19: 2, 20: 1},
        # "B02": {15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0},
        # "B03": {15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0}
    },
    "lotomania": {
        "B01": {50: 10},
        # "B02": {50: 0},
        # "B03": {50: 0}
    },
    "maismilionaria": {
        "1": {6: 5, 7: 2, 8: 1, 9: 2, 10: 0, 11: 0, 12: 0},
        "B02": {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0},
        "B03": {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
    },
    "megasena": {
        "B01": {6: 2, 7: 1, 8: 3, 9: 1, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
        # "B02": {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
        # "B03": {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
    },
    "quina": {
        "B01": {5: 4, 6: 3, 7: 2, 8: 1, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
        # "B02": {5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0},
        # "B03": {5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
    },
    "supersete": {
        "B01": {7: 10, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0,
                17: 0, 18: 0, 19: 0, 20: 0, 21: 0},
        # "B02": {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0,
        #         17: 0, 18: 0, 19: 0, 20: 0, 21: 0},
        # "B03": {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0,
        #         17: 0, 18: 0, 19: 0, 20: 0, 21: 0}
    },
    "timemania": {
        "B01": {10: 10},
        # "B02": {10: 0},
        # "B03": {10: 0}
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
    logger.info("Iniciando a criacao de boloes de apostas para as loterias...")

    # relacao de instancias das loterias da caixa e boloes para processamento
    logger.debug("Vai efetuar carga das definicoes das loterias do arquivo de configuracao .INI")
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

    logger.debug("Vai executar o processo de criacao de boloes para todas as loterias...")
    for id_loteria, bet_loteria in loterias_caixa.items():
        # algumas loterias precisam processar tambem o sorteio secundario:
        bet_secundario: Optional[AbstractBetting] = None
        if id_loteria == "diadesorte":
            bet_secundario = BetMesDaSorte(domain.get_mes_da_sorte())
        elif id_loteria == "timemania":
            bet_secundario = BetTimeDoCoracao(domain.get_time_do_coracao())
        if id_loteria == "maismilionaria":
            bet_secundario = BetTrevoDuplo(domain.get_trevo_duplo())

        # efetua a execucao do processo de criacao de boloes para cada loteria:
        logger.debug(f"Processo '{bet_loteria.id_process}': criando boloes para a loteria "
                     f"'{id_loteria}'.")
        for id_bolao, bolao in loterias_boloes[id_loteria].items():
            # utiliza a lista de concursos carregada do arquivo HTML (default):
            apostas_bolao: list[tuple] = bet_loteria.execute(bolao)

            # em seguida, processa o sorteio secundario e adiciona o(s) valor(es) complementar(es):
            if bet_secundario is not None:   # mes da sorte, time do coracao, trevo duplo/numerado
                apostas_bolao = bet_secundario.execute(apostas_bolao)

            # efetua a gravacao do arquivo CSV contendo os jogos criados (boloes):
            domain.export_boloes(bet_loteria.loteria.nome_loteria, id_bolao, apostas_bolao)

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    _stopWatch = stopwatch(_startWatch)
    logger.info(f"Finalizada a criacao de boloes de apostas para as loterias. "
                f"Tempo de Processamento: {_stopWatch}")

    return 0

# ----------------------------------------------------------------------------
