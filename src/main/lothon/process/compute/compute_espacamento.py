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

class ComputeEspacamento(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('espacamentos_jogos', 'espacamentos_percentos', 'espacamentos_concursos',
                 'ultimos_espacamentos_repetidos', 'ultimos_espacamentos_percentos',
                 'qtd_espacamentos_ultimo_concurso', 'qtd_espacamentos_penultimo_concurso',
                 'frequencias_espacamentos')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Espacamentos nos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.espacamentos_jogos: Optional[list[int]] = None
        self.espacamentos_percentos: Optional[list[float]] = None
        self.espacamentos_concursos: Optional[list[int]] = None
        self.ultimos_espacamentos_repetidos: Optional[list[int]] = None
        self.ultimos_espacamentos_percentos: Optional[list[float]] = None
        self.qtd_espacamentos_ultimo_concurso: int = 0
        self.qtd_espacamentos_penultimo_concurso: int = 0
        self.frequencias_espacamentos: Optional[list[SerieSorteio]] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_items: int = self.qtd_bolas // (self.qtd_bolas_sorteio - 1)
        self.espacamentos_jogos = cb.new_list_int(qtd_items)
        range_jogos: range = range(1, self.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, self.qtd_bolas_sorteio):
            # calcula o espacamento medio de cada combinacao de jogo:
            vl_espacamento = cb.calc_espacada(jogo)
            self.espacamentos_jogos[vl_espacamento] += 1

        # contabiliza o percentual dos espacamentos:
        self.espacamentos_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.espacamentos_jogos):
            percent: float = round((value / self.qtd_jogos) * 10000) / 100
            self.espacamentos_percentos[key] = percent

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, concursos: list[Concurso]) -> int:
        # valida se possui concursos a serem analisados:
        if concursos is None or len(concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        qtd_concursos: int = len(concursos)
        qtd_items: int = self.qtd_bolas // (self.qtd_bolas_sorteio - 1)

        # calcula o espacamento de cada sorteio dos concursos:
        self.espacamentos_concursos = cb.new_list_int(qtd_items)
        self.ultimos_espacamentos_repetidos = cb.new_list_int(qtd_items)
        self.qtd_espacamentos_ultimo_concurso = -1
        self.qtd_espacamentos_penultimo_concurso = -1
        for concurso in concursos:
            vl_espacamento: int = cb.calc_espacada(concurso.bolas)
            self.espacamentos_concursos[vl_espacamento] += 1
            # verifica se repetiu o espacamento do ultimo concurso:
            if vl_espacamento == self.qtd_espacamentos_ultimo_concurso:
                self.ultimos_espacamentos_repetidos[vl_espacamento] += 1
            # atualiza ambos flags, para ultimo e penultimo concursos
            self.qtd_espacamentos_penultimo_concurso = self.qtd_espacamentos_ultimo_concurso
            self.qtd_espacamentos_ultimo_concurso = vl_espacamento

        # contabiliza o percentual dos ultims espacamentos:
        self.ultimos_espacamentos_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.ultimos_espacamentos_repetidos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.ultimos_espacamentos_percentos[key] = percent

        # contabiliza as frequencias e atrasos dos espacamentos em todos os sorteios ja realizados:
        self.frequencias_espacamentos = cb.new_list_series(qtd_items)
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
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def rate(self, ordinal: int, jogo: tuple) -> int:
        vl_espacamento = cb.calc_espacada(jogo)
        return vl_espacamento

    def eval(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de espacamentos no jogo:
        vl_espacamento = cb.calc_espacada(jogo)
        percent: float = self.espacamentos_percentos[vl_espacamento]

        # ignora valores muito baixos de probabilidade:
        if percent < 5:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_redutor(percent)

        # verifica se esse jogo repetiu o espacamento do ultimo e penultimo concursos:
        if vl_espacamento != self.qtd_espacamentos_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif vl_espacamento == self.qtd_espacamentos_ultimo_concurso == \
                self.qtd_espacamentos_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao do ultimo espacamento:
        percent_repetido: float = self.ultimos_espacamentos_percentos[vl_espacamento]
        if percent_repetido < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir o espacamento:
            return fator_percent * to_redutor(percent_repetido)

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de espacamentos no jogo:
        vl_espacamento = cb.calc_espacada(jogo)
        percent: float = self.espacamentos_percentos[vl_espacamento]

        # ignora valores muito baixos de probabilidade:
        if percent < 1:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_fator(percent)

        # verifica se esse jogo repetiu o espacamento do ultimo e penultimo concursos:
        if vl_espacamento != self.qtd_espacamentos_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif vl_espacamento == self.qtd_espacamentos_ultimo_concurso == \
                self.qtd_espacamentos_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao do ultimo espacamento:
        percent_repetido: float = self.ultimos_espacamentos_percentos[vl_espacamento]
        if percent_repetido < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir o espacamento:
            return fator_percent * to_redutor(percent_repetido)

# ----------------------------------------------------------------------------
