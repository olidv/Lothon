"""
   Package lothon.process.compute
   Module  compute_somatorio.py

"""

__all__ = [
    'ComputeSomatorio'
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

class ComputeSomatorio(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('somatorios_jogos', 'somatorios_percentos', 'somatorios_concursos', 'qtd_zerados')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Somatorio das Dezenas")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.somatorios_jogos: Optional[list[int]] = None
        self.somatorios_percentos: Optional[list[float]] = None
        self.somatorios_concursos: Optional[list[int]] = None
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
        qtd_items: int = sum(range(payload.qtd_bolas - payload.qtd_bolas_sorteio + 1,
                                   payload.qtd_bolas + 1)) + 1  # soma 1 para nao usar zero-index.

        # efetua analise de todas as combinacoes de jogos da loteria:

        # contabiliza a somatorio de cada combinacao de jogo:
        self.somatorios_jogos = cb.new_list_int(qtd_items)
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            soma_dezenas = cb.soma_dezenas(jogo)
            self.somatorios_jogos[soma_dezenas] += 1

        # contabiliza o percentual dos somatorios:
        self.somatorios_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.somatorios_jogos):
            percent: float = round((value / qtd_jogos) * 100000) / 1000
            self.somatorios_percentos[key] = percent

        # contabiliza a somatorio de cada sorteio dos concursos:
        self.somatorios_concursos = cb.new_list_int(qtd_items)
        for concurso in concursos:
            soma_dezenas = cb.soma_dezenas(concurso.bolas)
            self.somatorios_concursos[soma_dezenas] += 1

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, jogo: tuple) -> float:
        # probabilidade de acerto depende do somatorio das dezenas do jogo:
        vl_somatorio: int = cb.soma_dezenas(jogo)
        percent: float = self.somatorios_percentos[vl_somatorio]

        # ignora valores muito baixos de probabilidade:
        if percent < 0.1:
            self.qtd_zerados += 1
            return 0
        else:
            return to_fator(percent)

# ----------------------------------------------------------------------------
