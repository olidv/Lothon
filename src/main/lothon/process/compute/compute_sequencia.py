"""
   Package lothon.process.compute
   Module  compute_sequencia.py

"""

__all__ = [
    'ComputeSequencia'
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

class ComputeSequencia(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('sequencias_jogos', 'sequencias_percentos', 'sequencias_concursos',
                 'frequencias_sequencias', 'qtd_zerados')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Sequencia nos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.sequencias_jogos: Optional[list[int]] = None
        self.sequencias_percentos: Optional[list[float]] = None
        self.sequencias_concursos: Optional[list[int]] = None
        self.frequencias_sequencias: Optional[list[SerieSorteio]] = None
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
        qtd_items: int = payload.qtd_bolas_sorteio - 1

        # efetua analise de todas as combinacoes de jogos da loteria:

        # contabiliza sequencias de cada combinacao de jogo:
        self.sequencias_jogos = cb.new_list_int(qtd_items)
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            qt_sequencias = cb.count_sequencias(jogo)
            self.sequencias_jogos[qt_sequencias] += 1

        # contabiliza o percentual das sequencias:
        self.sequencias_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.sequencias_jogos):
            percent: float = round((value / qtd_jogos) * 10000) / 100
            self.sequencias_percentos[key] = percent

        # contabiliza sequencias de cada sorteio dos concursos:
        self.sequencias_concursos = cb.new_list_int(qtd_items)
        for concurso in concursos:
            qt_sequencias: int = cb.count_sequencias(concurso.bolas)
            self.sequencias_concursos[qt_sequencias] += 1

        # contabiliza as frequencias e atrasos das sequencias em todos os sorteios ja realizados:
        self.frequencias_sequencias = cb.new_list_series(qtd_items)
        for concurso in concursos:
            # contabiliza o numero de sequencias do concurso:
            qt_sequencias = cb.count_sequencias(concurso.bolas)
            self.frequencias_sequencias[qt_sequencias].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_sequencias:
            # vai aproveitar e contabilizar as medidas estatisticas para a sequencia:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de sequencias no jogo:
        qt_sequencias: int = cb.count_sequencias(jogo)
        percent: float = self.sequencias_percentos[qt_sequencias]

        # ignora valores muito baixos de probabilidade:
        if percent < 9:
            self.qtd_zerados += 1
            return 0
        else:
            return to_fator(percent)

# ----------------------------------------------------------------------------
