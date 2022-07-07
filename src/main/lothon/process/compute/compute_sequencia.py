"""
   Package lothon.process.compute
   Module  compute_sequencia.py

"""

__all__ = [
    'ComputeSequencia'
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

class ComputeSequencia(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('sequencias_jogos', 'sequencias_percentos', 'sequencias_concursos',
                 'ultimas_sequencias_repetidas', 'ultimas_sequencias_percentos',
                 'qtd_sequencias_ultimo_concurso', 'qtd_sequencias_penultimo_concurso',
                 'frequencias_sequencias')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, threshold: int = 5):  # threshold minimo de 5% para filtro mais eficaz...
        super().__init__("Computacao de Sequencia nos Concursos", threshold)

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.sequencias_jogos: Optional[list[int]] = None
        self.sequencias_percentos: Optional[list[float]] = None
        self.sequencias_concursos: Optional[list[int]] = None
        self.ultimas_sequencias_repetidas: Optional[list[int]] = None
        self.ultimas_sequencias_percentos: Optional[list[float]] = None
        self.qtd_sequencias_ultimo_concurso: int = 0
        self.qtd_sequencias_penultimo_concurso: int = 0
        self.frequencias_sequencias: Optional[list[SerieSorteio]] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_items: int = self.qtd_bolas_sorteio - 1
        self.sequencias_jogos = cb.new_list_int(qtd_items)
        range_jogos: range = range(1, self.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, self.qtd_bolas_sorteio):
            # contabiliza sequencias de cada combinacao de jogo:
            qt_sequencias = cb.count_sequencias(jogo)
            self.sequencias_jogos[qt_sequencias] += 1

        # contabiliza o percentual das sequencias:
        self.sequencias_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.sequencias_jogos):
            percent: float = round((value / self.qtd_jogos) * 10000) / 100
            self.sequencias_percentos[key] = percent

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, concursos: list[Concurso]) -> int:
        # valida se possui concursos a serem analisados:
        if concursos is None or len(concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        qtd_concursos: int = len(concursos)
        qtd_items: int = self.qtd_bolas_sorteio - 1

        # contabiliza sequencias de cada sorteio dos concursos:
        self.sequencias_concursos = cb.new_list_int(qtd_items)
        self.ultimas_sequencias_repetidas = cb.new_list_int(qtd_items)
        self.qtd_sequencias_ultimo_concurso = -1
        self.qtd_sequencias_penultimo_concurso = -1
        for concurso in concursos:
            qt_sequencias: int = cb.count_sequencias(concurso.bolas)
            self.sequencias_concursos[qt_sequencias] += 1
            # verifica se repetiu o numero de sequencias do ultimo concurso:
            if qt_sequencias == self.qtd_sequencias_ultimo_concurso:
                self.ultimas_sequencias_repetidas[qt_sequencias] += 1
            # atualiza ambos flags, para ultimo e penultimo concursos
            self.qtd_sequencias_penultimo_concurso = self.qtd_sequencias_ultimo_concurso
            self.qtd_sequencias_ultimo_concurso = qt_sequencias

        # contabiliza o percentual das ultimas sequencias:
        self.ultimas_sequencias_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.ultimas_sequencias_repetidas):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.ultimas_sequencias_percentos[key] = percent

        # contabiliza as frequencias e atrasos das sequencias em todos os sorteios ja realizados:
        self.frequencias_sequencias = cb.new_list_series(qtd_items)
        for concurso in concursos:
            # contabiliza o numero de sequencias do concurso:
            qt_sequencias = cb.count_sequencias(concurso.bolas)
            self.frequencias_sequencias[qt_sequencias].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_sequencias:
            # vai aproveitar e contabilizar as medidas estatisticas para a sequencia:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def rate(self, ordinal: int, jogo: tuple) -> int:
        qt_sequencias: int = cb.count_sequencias(jogo)
        return qt_sequencias

    def eval(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de sequencias no jogo:
        qt_sequencias: int = cb.count_sequencias(jogo)
        percent: float = self.sequencias_percentos[qt_sequencias]

        # ignora valores muito baixos de probabilidade:
        if percent < self.min_threshold:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_redutor(percent)

        # verifica se esse jogo repetiu o numero de sequencias do ultimo e penultimo concursos:
        if qt_sequencias != self.qtd_sequencias_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif qt_sequencias == self.qtd_sequencias_ultimo_concurso == \
                self.qtd_sequencias_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao do ultimo numero de sequencias:
        percent_repetida: float = self.ultimas_sequencias_percentos[qt_sequencias]
        if percent_repetida < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir o numero de sequencias:
            return fator_percent * to_redutor(percent_repetida)

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de sequencias no jogo:
        qt_sequencias: int = cb.count_sequencias(jogo)
        percent: float = self.sequencias_percentos[qt_sequencias]

        # ignora valores muito baixos de probabilidade:
        if percent < 1:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_fator(percent)

        # verifica se esse jogo repetiu o numero de sequencias do ultimo e penultimo concursos:
        if qt_sequencias != self.qtd_sequencias_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif qt_sequencias == self.qtd_sequencias_ultimo_concurso == \
                self.qtd_sequencias_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao do ultimo numero de sequencias:
        percent_repetida: float = self.ultimas_sequencias_percentos[qt_sequencias]
        if percent_repetida < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir o numero de sequencias:
            return fator_percent * to_redutor(percent_repetida)

# ----------------------------------------------------------------------------
