"""
   Package lothon.process.compute
   Module  compute_espacamento.py

"""

__all__ = [
    'ComputeEspacamento'
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

class ComputeEspacamento(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('espacamentos_jogos', 'espacamentos_percentos', 'espacamentos_concursos',
                 'frequencias_espacamentos', 'qtd_zerados')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Espacamentos nos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.espacamentos_jogos: Optional[list[int]] = None
        self.espacamentos_percentos: Optional[list[float]] = None
        self.espacamentos_concursos: Optional[list[int]] = None
        self.frequencias_espacamentos: Optional[list[SerieSorteio]] = None
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
        qtd_items: int = payload.qtd_bolas // (payload.qtd_bolas_sorteio - 1)

        # efetua analise de todas as combinacoes de jogos da loteria:

        # zera os contadores de cada espacada:
        self.espacamentos_jogos = cb.new_list_int(qtd_items)

        # calcula o espacamento medio de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            vl_espacamento = cb.calc_espacada(jogo)
            self.espacamentos_jogos[vl_espacamento] += 1

        # contabiliza o percentual dos espacamentos:
        self.espacamentos_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.espacamentos_jogos):
            percent: float = round((value / qtd_jogos) * 10000) / 100
            self.espacamentos_percentos[key] = percent

        # calcula o espacamento de cada sorteio dos concursos:
        self.espacamentos_concursos = cb.new_list_int(qtd_items)
        for concurso in concursos:
            vl_espacamento: int = cb.calc_espacada(concurso.bolas)
            self.espacamentos_concursos[vl_espacamento] += 1

        # zera os contadores de frequencias e atrasos dos espacamentos:
        self.frequencias_espacamentos = cb.new_list_series(qtd_items)

        # contabiliza as frequencias e atrasos dos espacamentos em todos os sorteios ja realizados:
        for concurso in concursos:
            # contabiliza a frequencia dos espacamentos do concurso:
            vl_espacamento: int = cb.calc_espacada(concurso.bolas)
            self.frequencias_espacamentos[vl_espacamento].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_espacamentos:
            # vai aproveitar e contabilizar as medidas estatisticas para o espacamento:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de pares no jogo:
        vl_espacamento = cb.calc_espacada(jogo)
        percent: float = self.espacamentos_percentos[vl_espacamento]

        # ignora valores muito baixos de probabilidade:
        if percent < 5:
            self.qtd_zerados += 1
            return 0
        else:
            return to_fator(percent)

# ----------------------------------------------------------------------------
