"""
   Package lothon.process.compute
   Module  compute_repetencia.py

"""

__all__ = [
    'ComputeRepetencia'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
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

class ComputeRepetencia(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('repetencias_concursos', 'repetencias_percentos', 'repetencias_series',
                 'frequencias_repetencias', 'ultimo_concurso')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Repetencia do Ultimo Concurso")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.repetencias_concursos: Optional[list[int]] = None
        self.repetencias_percentos: Optional[list[float]] = None
        self.repetencias_series: Optional[list[SerieSorteio]] = None
        self.frequencias_repetencias: Optional[list[SerieSorteio]] = None

        # estruturas para avaliacao de jogo combinado da loteria:
        self.ultimo_concurso: Optional[Concurso] = None

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = payload.nome_loteria
        concursos: list[Concurso] = payload.concursos
        qtd_concursos: int = len(concursos)
        qtd_items: int = payload.qtd_bolas_sorteio

        # zera os contadores de cada repetencia:
        self.repetencias_concursos = cb.new_list_int(qtd_items)
        self.repetencias_series = cb.new_list_series(qtd_items)
        self.frequencias_repetencias = cb.new_list_series(payload.qtd_bolas)

        # contabiliza repetencias de cada sorteio com todos o sorteio anterior:
        concurso_anterior: Concurso = concursos[0]
        for concurso in concursos[1:]:
            qt_repeticoes: int = cb.count_repeticoes(concurso.bolas,
                                                     concurso_anterior.bolas,
                                                     self.frequencias_repetencias,
                                                     concurso.id_concurso)
            self.repetencias_concursos[qt_repeticoes] += 1
            self.repetencias_series[qt_repeticoes].add_sorteio(concurso.id_concurso)
            concurso_anterior = concurso

        # contabiliza o percentual das repetencias:
        self.repetencias_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.repetencias_concursos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.repetencias_percentos[key] = percent

        # contabiliza as medidas estatisticas para cada repetencia:
        for serie in self.repetencias_series:
            serie.update_stats()

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_repetencias[1:]:
            # vai aproveitar e contabilizar as medidas estatisticas para a bola:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

        # identifica os concursos passados:
        if "concursos_passados" in parms:
            concursos_passados: list[Concurso] = parms["concursos_passados"]
            # identifica o ultimo concurso, que sera considerado o concurso anterior:
            self.ultimo_concurso = concursos_passados[-1]

    def evaluate(self, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de repeticoes no jogo:
        qt_dezenas_repetidas: int = cb.count_dezenas_repetidas(jogo, self.ultimo_concurso.bolas)
        percent: float = self.repetencias_percentos[qt_dezenas_repetidas]

        # ignora valores muito baixos de probabilidade:
        if percent < 10:
            return 0
        else:
            return to_fator(percent)

# ----------------------------------------------------------------------------
