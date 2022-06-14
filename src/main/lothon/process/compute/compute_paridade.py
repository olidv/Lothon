"""
   Package lothon.process.compute
   Module  compute_paridade.py

"""

__all__ = [
    'ComputeParidade'
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

class ComputeParidade(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('paridades_jogos', 'paridades_percentos', 'paridades_concursos',
                 'ultimas_paridades_repetidas', 'ultimas_paridades_percentos',
                 'qtd_pares_ultimo_concurso', 'qtd_pares_penultimo_concurso',
                 'frequencias_paridades', 'qtd_zerados')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Paridade das Dezenas")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.paridades_jogos: Optional[list[int]] = None
        self.paridades_percentos: Optional[list[float]] = None
        self.paridades_concursos: Optional[list[int]] = None
        self.ultimas_paridades_repetidas: Optional[list[int]] = None
        self.ultimas_paridades_percentos: Optional[list[float]] = None
        self.qtd_pares_ultimo_concurso: int = 0
        self.qtd_pares_penultimo_concurso: int = 0
        self.frequencias_paridades: Optional[list[SerieSorteio]] = None
        self.qtd_zerados: int = 0

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
        qtd_jogos: int = loteria.qtd_jogos
        concursos: list[Concurso] = loteria.concursos
        qtd_concursos: int = len(concursos)
        qtd_items: int = loteria.qtd_bolas_sorteio

        # efetua analise de todas as combinacoes de jogos da loteria:
        self.paridades_jogos = cb.new_list_int(qtd_items)

        # contabiliza pares (e impares) de cada combinacao de jogo:
        range_jogos: range = range(1, loteria.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, loteria.qtd_bolas_sorteio):
            qtd_pares: int = cb.count_pares(jogo)
            self.paridades_jogos[qtd_pares] += 1

        # contabiliza o percentual das paridades:
        self.paridades_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.paridades_jogos):
            percent: float = round((value / qtd_jogos) * 10000) / 100
            self.paridades_percentos[key] = percent

        # contabiliza os pares (e impares) de cada sorteio dos concursos:
        self.paridades_concursos = cb.new_list_int(qtd_items)
        self.ultimas_paridades_repetidas = cb.new_list_int(qtd_items)
        self.qtd_pares_ultimo_concurso = -1
        self.qtd_pares_penultimo_concurso = -1
        for concurso in concursos:
            qtd_pares: int = cb.count_pares(concurso.bolas)
            self.paridades_concursos[qtd_pares] += 1
            # verifica se repetiu a paridade do ultimo concurso:
            if qtd_pares == self.qtd_pares_ultimo_concurso:
                self.ultimas_paridades_repetidas[qtd_pares] += 1
            # atualiza ambos flags, para ultimo e penultimo concursos
            self.qtd_pares_penultimo_concurso = self.qtd_pares_ultimo_concurso
            self.qtd_pares_ultimo_concurso = qtd_pares

        # contabiliza o percentual das ultimas paridades:
        self.ultimas_paridades_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.ultimas_paridades_repetidas):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.ultimas_paridades_percentos[key] = percent

        # contabiliza as frequencias e atrasos das paridades em todos os sorteios ja realizados:
        self.frequencias_paridades = cb.new_list_series(qtd_items)
        for concurso in concursos:
            # contabiliza o numero de paridades do concurso:
            qtd_pares = cb.count_pares(concurso.bolas)
            self.frequencias_paridades[qtd_pares].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_paridades:
            # vai aproveitar e contabilizar as medidas estatisticas para a paridade:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de pares no jogo:
        qt_pares: int = cb.count_pares(jogo)
        percent: float = self.paridades_percentos[qt_pares]

        # ignora valores muito baixos de probabilidade:
        if percent < 10:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_fator(percent)

        # verifica se esse jogo repetiu a paridade do ultimo e penultimo concursos:
        if qt_pares != self.qtd_pares_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif qt_pares == self.qtd_pares_ultimo_concurso == self.qtd_pares_penultimo_concurso:
            self.qtd_zerados += 1
            return 0  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao da ultima paridade:
        percent_repetida: float = self.ultimas_paridades_percentos[qt_pares]
        if percent_repetida < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir a paridade:
            return fator_percent * to_redutor(percent_repetida)

# ----------------------------------------------------------------------------
