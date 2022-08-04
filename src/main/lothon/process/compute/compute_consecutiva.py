"""
   Package lothon.process.compute
   Module  compute_consecutiva.py

"""

__all__ = [
    'ComputeConsecutiva'
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

class ComputeConsecutiva(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('consecutivas_jogos', 'consecutivas_percentos', 'consecutivas_concursos',
                 'ultimas_consecutivas_repetidas', 'ultimas_consecutivas_percentos',
                 'qtd_consecutivas_ultimo_concurso', 'qtd_consecutivas_penultimo_concurso',
                 'frequencias_consecutivas')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, threshold: int = 5):  # threshold minimo de 5% para filtro mais eficaz...
        super().__init__("Computacao de Dezenas Consecutivas nos Concursos", threshold)

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.consecutivas_jogos: Optional[list[int]] = None
        self.consecutivas_percentos: Optional[list[float]] = None
        self.consecutivas_concursos: Optional[list[int]] = None
        self.ultimas_consecutivas_repetidas: Optional[list[int]] = None
        self.ultimas_consecutivas_percentos: Optional[list[float]] = None
        self.qtd_consecutivas_ultimo_concurso: int = 0
        self.qtd_consecutivas_penultimo_concurso: int = 0
        self.frequencias_consecutivas: Optional[list[SerieSorteio]] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_items: int = self.qtd_bolas_sorteio - 1
        self.consecutivas_jogos = cb.new_list_int(qtd_items)
        range_jogos: range = range(1, self.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, self.qtd_bolas_sorteio):
            # contabiliza as dezenas consecutivas de cada combinacao de jogo:
            qtd_consecutivas = cb.count_consecutivas(jogo)
            self.consecutivas_jogos[qtd_consecutivas] += 1

        # contabiliza o percentual das dezenas consecutivas:
        self.consecutivas_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.consecutivas_jogos):
            percent: float = round((value / self.qtd_jogos) * 10000) / 100
            self.consecutivas_percentos[key] = percent

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

        # contabiliza as dezenas consecutivas de cada sorteio dos concursos:
        self.consecutivas_concursos = cb.new_list_int(qtd_items)
        self.ultimas_consecutivas_repetidas = cb.new_list_int(qtd_items)
        self.qtd_consecutivas_ultimo_concurso = -1
        self.qtd_consecutivas_penultimo_concurso = -1
        for concurso in concursos:
            qtd_consecutivas: int = cb.count_consecutivas(concurso.bolas)
            print("concurso: ", concurso.bolas, " tem consecutivas: ", qtd_consecutivas)
            self.consecutivas_concursos[qtd_consecutivas] += 1
            # verifica se repetiu o numero de dezenas consecutivas do ultimo concurso:
            if qtd_consecutivas == self.qtd_consecutivas_ultimo_concurso:
                self.ultimas_consecutivas_repetidas[qtd_consecutivas] += 1
            # atualiza ambos flags, para ultimo e penultimo concursos
            self.qtd_consecutivas_penultimo_concurso = self.qtd_consecutivas_ultimo_concurso
            self.qtd_consecutivas_ultimo_concurso = qtd_consecutivas

        # contabiliza o percentual das ultimas dezenas consecutivas:
        self.ultimas_consecutivas_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.ultimas_consecutivas_repetidas):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.ultimas_consecutivas_percentos[key] = percent

        # contabiliza frequencias e atrasos das dezenas consecutivas em todos os sorteios realizados
        self.frequencias_consecutivas = cb.new_list_series(qtd_items)
        for concurso in concursos:
            # contabiliza o numero de dezenas consecutivas do concurso:
            qtd_consecutivas = cb.count_consecutivas(concurso.bolas)
            self.frequencias_consecutivas[qtd_consecutivas].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_consecutivas:
            # vai aproveitar e contabilizar as medidas estatisticas para a dezena consecutiva:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def set_concursos_passados(self, concursos: list[Concurso]):
        return  # nada a fazer aqui...

    def rate(self, ordinal: int, jogo: tuple) -> int:
        qtd_consecutivas: int = cb.count_consecutivas(jogo)
        return qtd_consecutivas

    def eval(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de dezenas consecutivas no jogo:
        qtd_consecutivas: int = cb.count_consecutivas(jogo)
        percent: float = self.consecutivas_percentos[qtd_consecutivas]

        # ignora valores muito baixos de probabilidade:
        if percent < self.min_threshold:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_redutor(percent)

        # verifica se esse jogo repetiu o numero de consecutivas do ultimo e penultimo concursos:
        if qtd_consecutivas != self.qtd_consecutivas_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif qtd_consecutivas == self.qtd_consecutivas_ultimo_concurso == \
                self.qtd_consecutivas_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao do ultimo numero de dezenas consecutivas:
        percent_repetida: float = self.ultimas_consecutivas_percentos[qtd_consecutivas]
        if percent_repetida < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir o numero de consecutivas:
            return fator_percent * to_redutor(percent_repetida)

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de dezenas consecutivas no jogo:
        qtd_consecutivas: int = cb.count_consecutivas(jogo)
        percent: float = self.consecutivas_percentos[qtd_consecutivas]

        # ignora valores muito baixos de probabilidade:
        if percent < 1:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_fator(percent)

        # verifica se esse jogo repetiu o numero de consecutivas do ultimo e penultimo concursos:
        if qtd_consecutivas != self.qtd_consecutivas_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif qtd_consecutivas == self.qtd_consecutivas_ultimo_concurso == \
                self.qtd_consecutivas_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao do ultimo numero de dezenas consecutivas:
        percent_repetida: float = self.ultimas_consecutivas_percentos[qtd_consecutivas]
        if percent_repetida < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir o numero de consecutivas:
            return fator_percent * to_redutor(percent_repetida)

# ----------------------------------------------------------------------------
