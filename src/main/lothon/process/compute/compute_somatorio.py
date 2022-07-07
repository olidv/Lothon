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

class ComputeSomatorio(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('somatorios_jogos', 'somatorios_percentos', 'somatorios_concursos', 
                 'ultimos_somatorios_repetidos', 'ultimos_somatorios_percentos',
                 'vl_somatorio_ultimo_concurso', 'vl_somatorio_penultimo_concurso')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, threshold: int = 5):  # threshold minimo de 5% para filtro mais eficaz...
        super().__init__("Computacao de Somatorio das Dezenas", threshold)

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.somatorios_jogos: Optional[list[int]] = None
        self.somatorios_percentos: Optional[list[float]] = None
        self.somatorios_concursos: Optional[list[int]] = None
        self.ultimos_somatorios_repetidos: Optional[list[int]] = None
        self.ultimos_somatorios_percentos: Optional[list[float]] = None
        self.vl_somatorio_ultimo_concurso: int = 0
        self.vl_somatorio_penultimo_concurso: int = 0

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_items: int = sum(range(self.qtd_bolas - self.qtd_bolas_sorteio + 1,
                                   self.qtd_bolas + 1)) + 1  # soma 1 para nao usar zero-index.
        self.somatorios_jogos = cb.new_list_int(qtd_items)
        range_jogos: range = range(1, self.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, self.qtd_bolas_sorteio):
            # contabiliza a somatorio de cada combinacao de jogo:
            soma_dezenas = cb.soma_dezenas(jogo)
            self.somatorios_jogos[soma_dezenas] += 1

        # contabiliza o percentual dos somatorios:
        self.somatorios_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.somatorios_jogos):
            percent: float = round((value / self.qtd_jogos) * 100000) / 1000
            self.somatorios_percentos[key] = percent

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, concursos: list[Concurso]) -> int:
        # valida se possui concursos a serem analisados:
        if concursos is None or len(concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        qtd_concursos: int = len(concursos)
        qtd_items: int = sum(range(self.qtd_bolas - self.qtd_bolas_sorteio + 1,
                                   self.qtd_bolas + 1)) + 1  # soma 1 para nao usar zero-index.

        # contabiliza a somatorio de cada sorteio dos concursos:
        self.somatorios_concursos = cb.new_list_int(qtd_items)
        self.ultimos_somatorios_repetidos = cb.new_list_int(qtd_items)
        self.vl_somatorio_ultimo_concurso = -1
        self.vl_somatorio_penultimo_concurso = -1
        for concurso in concursos:
            vl_somatorio = cb.soma_dezenas(concurso.bolas)
            self.somatorios_concursos[vl_somatorio] += 1
            # verifica se repetiu o somatorio do ultimo concurso:
            if vl_somatorio == self.vl_somatorio_ultimo_concurso:
                self.ultimos_somatorios_repetidos[vl_somatorio] += 1
            # atualiza ambos flags, para ultimo e penultimo concursos
            self.vl_somatorio_penultimo_concurso = self.vl_somatorio_ultimo_concurso
            self.vl_somatorio_ultimo_concurso = vl_somatorio

        # contabiliza o percentual dos ultimos somatorios:
        self.ultimos_somatorios_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.ultimos_somatorios_repetidos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.ultimos_somatorios_percentos[key] = percent

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def rate(self, ordinal: int, jogo: tuple) -> int:
        vl_somatorio: int = cb.soma_dezenas(jogo)
        return vl_somatorio

    def eval(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do somatorio das dezenas do jogo:
        vl_somatorio: int = cb.soma_dezenas(jogo)
        percent: float = self.somatorios_percentos[vl_somatorio]

        # ignora valores muito baixos de probabilidade:
        if percent < self.min_threshold:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_redutor(percent)

        # verifica se esse jogo repetiu o somatorio do ultimo e penultimo concursos:
        if vl_somatorio != self.vl_somatorio_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif vl_somatorio == self.vl_somatorio_ultimo_concurso == \
                self.vl_somatorio_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao do ultimo somatorio:
        percent_repetido: float = self.ultimos_somatorios_percentos[vl_somatorio]
        if percent_repetido == 0:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir o somatorio:
            return fator_percent * to_redutor(percent_repetido)

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do somatorio das dezenas do jogo:
        vl_somatorio: int = cb.soma_dezenas(jogo)
        percent: float = self.somatorios_percentos[vl_somatorio]

        # ignora valores muito baixos de probabilidade:
        if percent == 0:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_fator(percent)

        # verifica se esse jogo repetiu o somatorio do ultimo e penultimo concursos:
        if vl_somatorio != self.vl_somatorio_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif vl_somatorio == self.vl_somatorio_ultimo_concurso == \
                self.vl_somatorio_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao do ultimo somatorio:
        percent_repetido: float = self.ultimos_somatorios_percentos[vl_somatorio]
        if percent_repetido == 0:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir o somatorio:
            return fator_percent * to_redutor(percent_repetido)

# ----------------------------------------------------------------------------
