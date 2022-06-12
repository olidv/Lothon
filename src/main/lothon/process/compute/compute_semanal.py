"""
   Package lothon.process.compute
   Module  compute_semanal.py

"""

__all__ = [
    'ComputeSemanal'
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
from lothon.domain import Loteria
from lothon.process.compute.abstract_compute import AbstractCompute


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# dias da semana para facilitar a impressao dos resultados - acesso = [0] [1] ... [6]
DIAS: tuple[str, ...] = ('Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom')


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class ComputeSemanal(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('semanal_premiacoes', 'semanal_ganhadores')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao Semanal de Premiacoes")

        # estrutura para a coleta de dados a partir do processamento de analise:
        self.semanal_premiacoes: Optional[list[int]] = None
        self.semanal_ganhadores: Optional[list[int]] = None

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
        # qtd_concursos: int = len(payload.concursos)
        qt_acertos_premio_maximo: int = min(payload.faixas)  # a menor faixa eh o premio principal
        qtd_items: int = 6  # dias da semana onde ocorrem sorteios - vai de 0=Seg, ..., 6=Dom

        # contabiliza as premiacoes e identifica o dia da semana para cada faixa de premiacao:
        self.semanal_premiacoes = cb.new_list_int(qtd_items)  # vai de 0=Seg, ..., 6=Dom
        self.semanal_ganhadores = cb.new_list_int(qtd_items)
        for concurso in payload.concursos:
            # identifica o numero de ganhadores do premio maximo:
            qt_ganhadores: int = concurso.get_ganhadores_premio(qt_acertos_premio_maximo)
            if qt_ganhadores > 0:
                dia: int = concurso.data_sorteio.weekday()
                self.semanal_premiacoes[dia] += 1
                self.semanal_ganhadores[dia] += qt_ganhadores

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, jogo: tuple) -> float:
        return 1.0

# ----------------------------------------------------------------------------
