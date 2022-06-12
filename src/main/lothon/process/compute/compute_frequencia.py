"""
   Package lothon.process.compute
   Module  compute_frequencia.py

"""

__all__ = [
    'ComputeFrequencia'
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

class ComputeFrequencia(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('frequencias_dezenas',)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Frequencia dos Concursos")

        # estrutura para a coleta de dados a partir do processamento de analise:
        self.frequencias_dezenas: Optional[list[SerieSorteio]] = None

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
        # qtd_concursos: int = len(concursos)
        qtd_items: int = payload.qtd_bolas

        # zera os contadores de frequencias e atrasos:
        self.frequencias_dezenas = cb.new_list_series(qtd_items)

        # contabiliza as frequencias e atrasos das dezenas em todos os sorteios ja realizados:
        for concurso in concursos:
            # registra o concurso para cada dezena sorteada:
            for bola in concurso.bolas:
                self.frequencias_dezenas[bola].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_dezenas[1:]:
            # vai aproveitar e contabilizar as medidas estatisticas para a bola:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, jogo: tuple) -> float:
        return 1.0

# ----------------------------------------------------------------------------
