"""
   Package lothon.process.compute
   Module  compute_premiacao.py

"""

__all__ = [
    'ComputePremiacao'
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
from lothon.domain import Concurso, SerieSorteio
from lothon.process.compute.abstract_compute import AbstractCompute


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# constante com numero de topos a serem extraidos para criar ranking de top-dezenas:
QTD_TOPOS_RANKING: int = 10


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class ComputePremiacao(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('frequencia_premiacoes',)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, threshold: int = 0):  # threshold nao se aplica aqui.
        super().__init__("Computacao de Frequencia das Premiacoes Maximas", threshold)

        # estrutura para a coleta de dados a partir do processamento de analise:
        self.frequencia_premiacoes: Optional[SerieSorteio] = None

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

        # contabiliza as frequencias e atrasos das dezenas em todos os sorteios ja realizados:
        self.frequencia_premiacoes = SerieSorteio(0)
        for concurso in concursos:
            # verifica se houve ganhador na premiacao principal:
            if concurso.get_ganhadores_premio(self.qtd_bolas_sorteio) > 0:
                self.frequencia_premiacoes.add_sorteio(concurso.id_concurso, True)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        self.frequencia_premiacoes.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS (NAO SE APLICA AQUI) ------------------

    def set_concursos_passados(self, concursos: list[Concurso]):
        pass

    def rate(self, ordinal: int, jogo: tuple) -> int:
        pass

    def eval(self, ordinal: int, jogo: tuple) -> float:
        pass

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        pass

# ----------------------------------------------------------------------------
