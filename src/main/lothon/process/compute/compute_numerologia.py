"""
   Package lothon.process.compute
   Module  compute_numerologia.py

"""

__all__ = [
    'ComputeNumerologia'
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

class ComputeNumerologia(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('numerologias_jogos', 'numerologias_percentos', 'numerologias_concursos',
                 'frequencias_numerologias')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Numerologia das Dezenas")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.numerologias_jogos: Optional[list[int]] = None
        self.numerologias_percentos: Optional[list[float]] = None
        self.numerologias_concursos: Optional[list[int]] = None
        self.frequencias_numerologias: Optional[list[SerieSorteio]] = None

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
        qtd_items: int = 9  # numero de zero a nove

        # efetua analise de todas as combinacoes de jogos da loteria:

        # zera os contadores de cada somatorio:
        self.numerologias_jogos = cb.new_list_int(qtd_items)

        # calcula a numerologia de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            numero: int = cb.calc_numerology(jogo)
            self.numerologias_jogos[numero] += 1

        # contabiliza o percentual das numerologias:
        self.numerologias_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.numerologias_jogos):
            if key == 0:  # ignora o zero-index, pois nenhuma numerologia darah zero.
                continue

            percent: float = round((value / qtd_jogos) * 10000) / 100
            self.numerologias_percentos[key] = percent

        # calcula a numerologia de cada sorteio dos concursos:
        self.numerologias_concursos = cb.new_list_int(qtd_items)
        for concurso in concursos:
            numero: int = cb.calc_numerology(concurso.bolas)
            self.numerologias_concursos[numero] += 1

        # zera os contadores de frequencias e atrasos das numerologias:
        self.frequencias_numerologias = cb.new_list_series(qtd_items)

        # contabiliza as frequencias e atrasos das numerologias em todos os sorteios ja realizados:
        for concurso in concursos:
            # contabiliza a numerologia do concurso:
            numero = cb.calc_numerology(concurso.bolas)
            self.frequencias_numerologias[numero].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_numerologias[1:]:  # nao ha numerologia com zero
            # vai aproveitar e contabilizar as medidas estatisticas para a numerologia:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, jogo: tuple) -> float:
        return 1.0

# ----------------------------------------------------------------------------
