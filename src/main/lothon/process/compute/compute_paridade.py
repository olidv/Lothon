"""
   Package lothon.process.compute
   Module  compute_paridade.py

"""

__all__ = [
    'ComputeParidade'
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
from lothon.domain import Loteria, Concurso, SerieSorteio
from lothon.process.compute.abstract_compute import AbstractCompute


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class ComputeParidade(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('paridades_jogos', 'paridades_percentos', 'paridades_concursos',
                 'frequencias_paridades')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Paridade das Dezenas")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.paridades_jogos: Optional[list[int]] = None
        self.paridades_percentos: Optional[list[float]] = None
        self.paridades_concursos: Optional[list[int]] = None
        self.frequencias_paridades: Optional[list[SerieSorteio]] = None

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

        # zera os contadores de cada paridade:
        self.paridades_jogos = cb.new_list_int(qtd_items)

        # contabiliza pares (e impares) de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            qtd_pares: int = cb.count_pares(jogo)
            self.paridades_jogos[qtd_pares] += 1

        # contabiliza o percentual das paridades:
        self.paridades_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.paridades_jogos):
            percent: float = round((value / qtd_jogos) * 10000) / 100
            self.paridades_percentos[key] = percent

        # contabiliza pares (e impares) de cada sorteio dos concursos:
        self.paridades_concursos = cb.new_list_int(qtd_items)
        for concurso in concursos:
            qtd_pares: int = cb.count_pares(concurso.bolas)
            self.paridades_concursos[qtd_pares] += 1

        # zera os contadores de frequencias e atrasos das paridades:
        self.frequencias_paridades = cb.new_list_series(qtd_items)

        # contabiliza as frequencias e atrasos das paridades em todos os sorteios ja realizados:
        for concurso in concursos:
            # contabiliza o numero de paridades do concurso:
            qtd_pares = cb.count_pares(concurso.bolas)
            self.frequencias_paridades[qtd_pares].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_paridades:
            # vai aproveitar e contabilizar as medidas estatisticas para a paridade:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    def evaluate(self, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de pares no jogo:
        qt_pares: int = cb.count_pares(jogo)
        percent: float = self.paridades_percentos[qt_pares]

        # ignora valores muito baixos de probabilidade:
        if percent < 10:
            return 0
        else:
            return to_fator(percent)

# ----------------------------------------------------------------------------
