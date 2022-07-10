"""
   Package lothon.process.compute
   Module  compute_numerologia.py

"""

__all__ = [
    'ComputeNumerologia'
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

class ComputeNumerologia(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('numerologias_jogos', 'numerologias_percentos', 'numerologias_concursos',
                 'ultimas_numerologias_repetidas', 'ultimas_numerologias_percentos',
                 'vl_numerologia_ultimo_concurso', 'vl_numerologia_penultimo_concurso',
                 'frequencias_numerologias')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, threshold: int = 5):  # threshold minimo de 5% para filtro mais eficaz...
        super().__init__("Computacao de Numerologia das Dezenas", threshold)

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.numerologias_jogos: Optional[list[int]] = None
        self.numerologias_percentos: Optional[list[float]] = None
        self.numerologias_concursos: Optional[list[int]] = None
        self.ultimas_numerologias_repetidas: Optional[list[int]] = None
        self.ultimas_numerologias_percentos: Optional[list[float]] = None
        self.vl_numerologia_ultimo_concurso: int = 0
        self.vl_numerologia_penultimo_concurso: int = 0
        self.frequencias_numerologias: Optional[list[SerieSorteio]] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_items: int = 9  # numero de zero a nove
        self.numerologias_jogos = cb.new_list_int(qtd_items)
        range_jogos: range = range(1, self.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, self.qtd_bolas_sorteio):
            # calcula a numerologia de cada combinacao de jogo:
            numero: int = cb.calc_numerology(jogo)
            self.numerologias_jogos[numero] += 1

        # contabiliza o percentual das numerologias:
        self.numerologias_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.numerologias_jogos):
            if key == 0:  # ignora o zero-index, pois nenhuma numerologia darah zero.
                continue

            percent: float = round((value / self.qtd_jogos) * 10000) / 100
            self.numerologias_percentos[key] = percent

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, concursos: list[Concurso]) -> int:
        # valida se possui concursos a serem analisados:
        if concursos is None or len(concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        qtd_concursos: int = len(concursos)
        qtd_items: int = 9  # numero de zero a nove

        # calcula a numerologia de cada sorteio dos concursos:
        self.numerologias_concursos = cb.new_list_int(qtd_items)
        self.ultimas_numerologias_repetidas = cb.new_list_int(qtd_items)
        self.vl_numerologia_ultimo_concurso = -1
        self.vl_numerologia_penultimo_concurso = -1
        for concurso in concursos:
            vl_numerologia: int = cb.calc_numerology(concurso.bolas)
            self.numerologias_concursos[vl_numerologia] += 1
            # verifica se repetiu a numerologia do ultimo concurso:
            if vl_numerologia == self.vl_numerologia_ultimo_concurso:
                self.ultimas_numerologias_repetidas[vl_numerologia] += 1
            # atualiza ambos flags, para ultimo e penultimo concursos
            self.vl_numerologia_penultimo_concurso = self.vl_numerologia_ultimo_concurso
            self.vl_numerologia_ultimo_concurso = vl_numerologia

        # contabiliza o percentual das ultimas numerologias:
        self.ultimas_numerologias_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.ultimas_numerologias_repetidas):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.ultimas_numerologias_percentos[key] = percent

        # contabiliza as frequencias e atrasos das numerologias em todos os sorteios ja realizados:
        self.frequencias_numerologias = cb.new_list_series(qtd_items)
        for concurso in concursos:
            # contabiliza a numerologia do concurso:
            vl_numerologia = cb.calc_numerology(concurso.bolas)
            self.frequencias_numerologias[vl_numerologia].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_numerologias[1:]:  # nao ha numerologia com zero
            # vai aproveitar e contabilizar as medidas estatisticas para a numerologia:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def set_concursos_passados(self, concursos: list[Concurso]):
        return  # nada a fazer aqui...

    def rate(self, ordinal: int, jogo: tuple) -> int:
        vl_numerologia: int = cb.calc_numerology(jogo)
        return vl_numerologia

    def eval(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende da numerologia do jogo:
        vl_numerologia: int = cb.calc_numerology(jogo)
        percent: float = self.numerologias_percentos[vl_numerologia]

        # ignora valores muito baixos de probabilidade:
        if percent < self.min_threshold:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_redutor(percent)

        # verifica se esse jogo repetiu a numerologia do ultimo e penultimo concursos:
        if vl_numerologia != self.vl_numerologia_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif vl_numerologia == self.vl_numerologia_ultimo_concurso == \
                self.vl_numerologia_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao da ultima numerologia:
        percent_repetida: float = self.ultimas_numerologias_percentos[vl_numerologia]
        if percent_repetida == 0:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir a numerologia:
            return fator_percent * to_redutor(percent_repetida)

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende da numerologia do jogo:
        vl_numerologia: int = cb.calc_numerology(jogo)
        percent: float = self.numerologias_percentos[vl_numerologia]

        # ignora valores muito baixos de probabilidade:
        if percent == 0:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_fator(percent)

        # verifica se esse jogo repetiu a numerologia do ultimo e penultimo concursos:
        if vl_numerologia != self.vl_numerologia_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif vl_numerologia == self.vl_numerologia_ultimo_concurso == \
                self.vl_numerologia_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao da ultima numerologia:
        percent_repetida: float = self.ultimas_numerologias_percentos[vl_numerologia]
        if percent_repetida == 0:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir a numerologia:
            return fator_percent * to_redutor(percent_repetida)

# ----------------------------------------------------------------------------
