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
from lothon.domain import Concurso
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

    def __init__(self, threshold: int = 5):  # threshold minimo de 5% para filtro mais eficaz...
        super().__init__("Computacao de Recorrencia nos Concursos", threshold)

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.recorrencias_concursos: Optional[list[int]] = None
        self.recorrencias_percentos: Optional[list[float]] = None

        # estruturas para avaliacao de jogo combinado da loteria:
        self.concursos_passados: Optional[list[Concurso]] = None

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
        qtd_concursos: int = len(concursos)
        qtd_items: int = self.qtd_bolas_sorteio

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
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def set_concursos_passados(self, concursos: list[Concurso]):
        self.concursos_passados = concursos

    def rate(self, ordinal: int, jogo: tuple) -> int:
        qt_max_repeticoes: int = cb.max_recorrencias(jogo, self.concursos_passados)
        return qt_max_repeticoes

    def eval(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero maximo de repeticoes nos concursos anteriores:
        qt_max_repeticoes: int = cb.max_recorrencias(jogo, self.concursos_passados)
        percent: float = self.recorrencias_percentos[qt_max_repeticoes]

        # ignora valores muito baixos de probabilidade:
        if percent < self.min_threshold:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica):
        fator_percent: float = to_redutor(percent)
        return fator_percent

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero maximo de repeticoes nos concursos anteriores:
        qt_max_repeticoes: int = cb.max_recorrencias(jogo, self.concursos_passados)
        percent: float = self.recorrencias_percentos[qt_max_repeticoes]

        # ignora valores muito baixos de probabilidade:
        if percent < 10:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica):
        fator_percent: float = to_fator(percent)
        return fator_percent

# ----------------------------------------------------------------------------
