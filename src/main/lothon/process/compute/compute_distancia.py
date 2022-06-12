"""
   Package lothon.process.compute
   Module  compute_distancia.py

"""

__all__ = [
    'ComputeDistancia'
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

class ComputeDistancia(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('distancias_jogos', 'distancias_percentos', 'distancias_concursos', 'qtd_zerados')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Distancia nos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.distancias_jogos: Optional[list[int]] = None
        self.distancias_percentos: Optional[list[float]] = None
        self.distancias_concursos: Optional[list[int]] = None
        self.qtd_zerados: int = 0

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
        qtd_items: int = payload.qtd_bolas

        # efetua analise de todas as combinacoes de jogos da loteria:

        # zera os contadores de cada distancia:
        self.distancias_jogos = cb.new_list_int(qtd_items)

        # calcula a distancia de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            vl_distancia = cb.calc_distancia(jogo)
            self.distancias_jogos[vl_distancia] += 1

        # contabiliza o percentual das distancias:
        self.distancias_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.distancias_jogos):
            percent: float = round((value / qtd_jogos) * 10000) / 100
            self.distancias_percentos[key] = percent

        # calcula a distancia de cada sorteio dos concursos:
        self.distancias_concursos = cb.new_list_int(qtd_items)
        for concurso in concursos:
            vl_distancia: int = cb.calc_distancia(concurso.bolas)
            self.distancias_concursos[vl_distancia] += 1

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, jogo: tuple) -> float:
        # probabilidade de acerto depende da distancia entre as dezenas:
        vl_distancia: int = cb.calc_distancia(jogo)
        percent: float = self.distancias_percentos[vl_distancia]

        # ignora valores muito baixos de probabilidade:
        if percent < 2:
            self.qtd_zerados += 1
            return 0
        else:
            return to_fator(percent)

# ----------------------------------------------------------------------------
