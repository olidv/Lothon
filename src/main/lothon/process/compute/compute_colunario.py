"""
   Package lothon.process.compute
   Module  compute_colunario.py

"""

__all__ = [
    'ComputeColunario'
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

class ComputeColunario(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('colunarios_jogos', 'colunarios_percentos', 'colunarios_concursos',
                 'frequencias_colunarios')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Colunario nos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.colunarios_jogos: Optional[list[int]] = None
        self.colunarios_percentos: Optional[list[float]] = None
        self.colunarios_concursos: Optional[list[int]] = None
        self.frequencias_colunarios: Optional[list[SerieSorteio]] = None

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
        concursos: list[Concurso] = payload.concursos
        qtd_jogos: int = payload.qtd_jogos
        # qtd_concursos: int = len(concursos)
        qtd_items: int = 9

        # efetua analise de todas as combinacoes de jogos da loteria:

        # zera os contadores de cada colunario:
        self.colunarios_jogos = cb.new_list_int(qtd_items)

        # contabiliza pares (e impares) de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            cb.count_colunarios(jogo, self.colunarios_jogos)

        # contabiliza o percentual dos colunarios:
        self.colunarios_percentos = cb.new_list_float(qtd_items)
        total: int = payload.qtd_bolas_sorteio * qtd_jogos
        for key, value in enumerate(self.colunarios_jogos):
            percent: float = round((value / total) * 10000) / 100
            self.colunarios_percentos[key] = percent

        # zera os contadores de cada sequencia:
        self.colunarios_concursos = cb.new_list_int(qtd_items)

        # contabiliza colunarios de cada sorteio ja realizado:
        for concurso in concursos:
            cb.count_colunarios(concurso.bolas, self.colunarios_concursos)

        # zera os contadores de frequencias e atrasos dos colunarios:
        self.frequencias_colunarios = cb.new_list_series(qtd_items)

        # contabiliza as frequencias e atrasos dos colunarios em todos os sorteios ja realizados:
        for concurso in concursos:
            # contabiliza a frequencia dos colunarios do concurso:
            for num in concurso.bolas:
                coluna: int = cb.get_colunario(num)
                self.frequencias_colunarios[coluna].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_colunarios:
            # vai aproveitar e contabilizar as medidas estatisticas para a coluna:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, jogo: tuple) -> float:
        return 1.0

# ----------------------------------------------------------------------------
