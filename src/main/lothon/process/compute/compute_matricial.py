"""
   Package lothon.process.compute
   Module  compute_matricial.py

"""

__all__ = [
    'ComputeMatricial'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
import itertools as itt
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.stats import combinatoria as cb
from lothon.domain import Loteria, Concurso
from lothon.process.compute.abstract_compute import AbstractCompute


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class ComputeMatricial(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('colunas_jogos', 'colunas_percentos', 'colunas_concursos',
                 'linhas_jogos', 'linhas_percentos', 'linhas_concursos')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise Matricial dos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.colunas_jogos: Optional[list[int]] = None
        self.colunas_percentos: Optional[list[float]] = None
        self.colunas_concursos: Optional[list[int]] = None
        self.linhas_jogos: Optional[list[int]] = None
        self.linhas_percentos: Optional[list[float]] = None
        self.linhas_concursos: Optional[list[int]] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = payload.nome_loteria
        qtd_jogos: int = payload.qtd_jogos
        concursos: list[Concurso] = payload.concursos
        # qtd_concursos: int = len(concursos)
        qtd_items: int = payload.qtd_bolas_sorteio

        # efetua analise de todas as combinacoes de jogos da loteria:

        # zera os contadores de cada maximo de coluna e linha:
        self.colunas_jogos = cb.new_list_int(qtd_items)
        self.linhas_jogos = cb.new_list_int(qtd_items)

        # identifica o numero maximo de colunas e linhas de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            # maximo de colunas
            vl_max_col: int = cb.max_colunas(jogo)
            self.colunas_jogos[vl_max_col] += 1

            # maximo de linhas
            vl_max_lin: int = cb.max_linhas(jogo)
            self.linhas_jogos[vl_max_lin] += 1

        # contabiliza o percentual das colunas:
        self.colunas_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.colunas_jogos):
            percent: float = round((value / qtd_jogos) * 10000) / 100
            self.colunas_percentos[key] = percent

        # contabiliza o percentual das linhas:
        self.linhas_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.linhas_jogos):
            percent: float = round((value / qtd_jogos) * 10000) / 100
            self.linhas_percentos[key] = percent

        # zera os contadores de cada sequencia:
        self.colunas_concursos = cb.new_list_int(qtd_items)
        self.linhas_concursos = cb.new_list_int(qtd_items)

        # identifica o numero maximo de colunas e linhas de cada sorteio ja realizado:
        for concurso in concursos:
            # maximo de colunas
            vl_max_col: int = cb.max_colunas(concurso.bolas)
            self.colunas_concursos[vl_max_col] += 1

            # maximo de linhas
            vl_max_lin: int = cb.max_linhas(concurso.bolas)
            self.linhas_concursos[vl_max_lin] += 1

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero maximo de colunas e linhas do jogo:
        vl_max_col: int = cb.max_colunas(jogo)
        percent_col: float = self.colunas_percentos[vl_max_col]

        vl_max_lin: int = cb.max_linhas(jogo)
        percent_lin: float = self.linhas_percentos[vl_max_lin]

        # ignora valores muito baixos de probabilidade:
        if percent_col < 9 or percent_lin < 5:
            return 0
        else:
            return to_fator(percent_col) * to_fator(percent_lin)

# ----------------------------------------------------------------------------
