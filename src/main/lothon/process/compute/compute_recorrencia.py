"""
   Package lothon.process.compute
   Module  compute_recorrencia.py

"""

__all__ = [
    'ComputeRecorrencia'
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

class ComputeRecorrencia(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('recorrencias_concursos', 'recorrencias_percentos',
                 'concursos_passados')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Recorrencia nos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.recorrencias_concursos: Optional[list[int]] = None
        self.recorrencias_percentos: Optional[list[float]] = None

        # estruturas para avaliacao de jogo combinado da loteria:
        self.concursos_passados: Optional[list[Concurso]] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, loteria: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if loteria is None or loteria.concursos is None or len(loteria.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = loteria.nome_loteria
        concursos: list[Concurso] = loteria.concursos
        qtd_concursos: int = len(concursos)
        qtd_items: int = loteria.qtd_bolas_sorteio

        # salva os concursos analisados ate o momento para o EVALUATE posterior:
        self.concursos_passados = concursos

        # contabiliza o maximo de repeticoes das dezenas de cada sorteio dos concursos:
        self.recorrencias_concursos = cb.new_list_int(qtd_items)
        for concurso in concursos:
            qt_max_repeticoes: int = cb.max_recorrencias(concurso.bolas, concursos,
                                                         concurso.id_concurso)  # ignora o atual
            self.recorrencias_concursos[qt_max_repeticoes] += 1

        # contabiliza o percentual das recorrencias:
        self.recorrencias_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.recorrencias_concursos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.recorrencias_percentos[key] = percent

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero maximo de repeticoes nos concursos anteriores:
        qt_max_repeticoes: int = cb.max_recorrencias(jogo, self.concursos_passados)
        percent: float = self.recorrencias_percentos[qt_max_repeticoes]

        # ignora valores muito baixos de probabilidade:
        if percent < 10:
            self.qtd_zerados += 1
            return 0
        else:
            return to_fator(percent)

# ----------------------------------------------------------------------------
