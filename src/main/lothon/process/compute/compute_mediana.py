"""
   Package lothon.process.compute
   Module  compute_mediana.py

"""

__all__ = [
    'ComputeMediana'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import math
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

class ComputeMediana(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('medias_jogos', 'medias_percentos', 'medias_concursos',
                 'ultimas_medias_repetidas', 'ultimas_medias_percentos',
                 'vl_media_ultimo_concurso', 'vl_media_penultimo_concurso',
                 'frequencias_medias')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, threshold: int = 5):  # threshold minimo de 5% para filtro mais eficaz...
        super().__init__("Computacao da Raiz-Media das Dezenas", threshold)

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.medias_jogos: Optional[list[int]] = None
        self.medias_percentos: Optional[list[float]] = None
        self.medias_concursos: Optional[list[int]] = None
        self.ultimas_medias_repetidas: Optional[list[int]] = None
        self.ultimas_medias_percentos: Optional[list[float]] = None
        self.vl_media_ultimo_concurso: int = 0
        self.vl_media_penultimo_concurso: int = 0
        self.frequencias_medias: Optional[list[SerieSorteio]] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_items: int = round(math.sqrt(self.qtd_bolas))  # vai depender do valor da ultima bola
        self.medias_jogos = cb.new_list_int(qtd_items)
        range_jogos: range = range(1, self.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, self.qtd_bolas_sorteio):
            # calcula a raiz-media de cada combinacao de jogo:
            numero: int = cb.root_mean(jogo)
            self.medias_jogos[numero] += 1

        # contabiliza o percentual das raiz-medias:
        self.medias_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.medias_jogos):
            # if key == 0:  # ignora o zero-index, pois nenhuma raiz-media darah zero.
            #     continue
            percent: float = round((value / self.qtd_jogos) * 10000) / 100
            self.medias_percentos[key] = percent

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, concursos: list[Concurso]) -> int:
        # valida se possui concursos a serem analisados:
        if concursos is None or len(concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        qtd_concursos: int = len(concursos)
        qtd_items: int = round(math.sqrt(self.qtd_bolas))  # vai depender do valor da ultima bola

        # calcula a raiz-media de cada sorteio dos concursos:
        self.medias_concursos = cb.new_list_int(qtd_items)
        self.ultimas_medias_repetidas = cb.new_list_int(qtd_items)
        self.vl_media_ultimo_concurso = -1
        self.vl_media_penultimo_concurso = -1
        for concurso in concursos:
            vl_media: int = cb.root_mean(concurso.bolas)
            self.medias_concursos[vl_media] += 1
            # verifica se repetiu a raiz-media do ultimo concurso:
            if vl_media == self.vl_media_ultimo_concurso:
                self.ultimas_medias_repetidas[vl_media] += 1
            # atualiza ambos flags, para ultimo e penultimo concursos
            self.vl_media_penultimo_concurso = self.vl_media_ultimo_concurso
            self.vl_media_ultimo_concurso = vl_media

        # contabiliza o percentual das ultimas raiz-medias:
        self.ultimas_medias_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.ultimas_medias_repetidas):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.ultimas_medias_percentos[key] = percent

        # contabiliza as frequencias e atrasos das raiz-medias em todos os sorteios ja realizados:
        self.frequencias_medias = cb.new_list_series(qtd_items)
        for concurso in concursos:
            # contabiliza a raiz-media do concurso:
            vl_media = cb.root_mean(concurso.bolas)
            self.frequencias_medias[vl_media].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_medias[1:]:  # nao ha raiz-media com zero
            # vai aproveitar e contabilizar as medidas estatisticas para a raiz-media:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def rate(self, ordinal: int, jogo: tuple) -> int:
        vl_media: int = cb.root_mean(jogo)
        return vl_media

    def eval(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende da raiz-media do jogo:
        vl_media: int = cb.root_mean(jogo)
        percent: float = self.medias_percentos[vl_media]

        # ignora valores muito baixos de probabilidade:
        if percent < self.min_threshold:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_redutor(percent)

        # verifica se esse jogo repetiu a raiz-media do ultimo e penultimo concursos:
        if vl_media != self.vl_media_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif vl_media == self.vl_media_ultimo_concurso == \
                self.vl_media_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao da ultima raiz-media:
        percent_repetida: float = self.ultimas_medias_percentos[vl_media]
        if percent_repetida < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir a raiz-media:
            return fator_percent * to_redutor(percent_repetida)

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende da raiz-media do jogo:
        vl_media: int = cb.root_mean(jogo)
        percent: float = self.medias_percentos[vl_media]

        # ignora valores muito baixos de probabilidade:
        if percent < 1:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_fator(percent)

        # verifica se esse jogo repetiu a raiz-media do ultimo e penultimo concursos:
        if vl_media != self.vl_media_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif vl_media == self.vl_media_ultimo_concurso == \
                self.vl_media_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao da ultima raiz-media:
        percent_repetida: float = self.ultimas_medias_percentos[vl_media]
        if percent_repetida < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir a raiz-media:
            return fator_percent * to_redutor(percent_repetida)

# ----------------------------------------------------------------------------
