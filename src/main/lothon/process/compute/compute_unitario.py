"""
   Package lothon.process.compute
   Module  compute_unitario.py

"""

__all__ = [
    'ComputeUnitario'
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
from lothon.domain import Concurso, SerieSorteio
from lothon.process.compute.abstract_compute import AbstractCompute


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class ComputeUnitario(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('frequencias_meses', 'topos_frequentes', 'topos_ausentes')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, threshold: int = 5):  # threshold minimo de 5% para filtro mais eficaz...
        super().__init__("Computacao dos Concursos com Sorteio Unitario", threshold)

        # estrutura para a coleta de dados a partir do processamento de analise:
        self.frequencias_meses: Optional[list[SerieSorteio]] = None
        self.topos_frequentes: Optional[list[int]] = None
        self.topos_ausentes: Optional[list[int]] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, concursos: list[Concurso]) -> int:
        # valida se possui concursos a serem analisados:
        if concursos is None or len(concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        # qtd_concursos: int = len(concursos)
        qtd_items: int = self.qtd_bolas

        # contabiliza as frequencias e atrasos dos meses em todos os sorteios ja realizados:
        self.frequencias_meses = cb.new_list_series(qtd_items)
        for concurso in concursos:
            # registra o concurso para cada dezena sorteada:
            mes_da_sorte: int = concurso.bolas[0]
            self.frequencias_meses[mes_da_sorte].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_meses[1:]:
            # vai aproveitar e contabilizar as medidas estatisticas para cada mes:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        # extrai os topos do ranking com as dezenas com maior frequencia em todos os concursos:
        self.topos_frequentes = cb.calc_topos_frequencia(concursos, self.qtd_bolas)
        self.topos_ausentes = cb.calc_topos_ausencia(concursos, self.qtd_bolas)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def set_concursos_passados(self, concursos: list[Concurso]):
        return  # nada a fazer aqui...

    def rate(self, ordinal: int, jogo: tuple) -> int:
        return 0  # nada a fazer aqui...

    def eval(self, ordinal: int, jogo: tuple) -> float:
        return 0.0  # nada a fazer aqui...

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        return 0.0  # nada a fazer aqui...

# ----------------------------------------------------------------------------
