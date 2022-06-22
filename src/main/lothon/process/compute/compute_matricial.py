"""
   Package lothon.process.compute
   Module  compute_matricial.py

"""

__all__ = [
    'ComputeMatricial'
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

class ComputeMatricial(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('colunas_jogos', 'colunas_percentos', 'colunas_concursos',
                 'linhas_jogos', 'linhas_percentos', 'linhas_concursos',
                 'ultimas_matrizes_repetidas', 'ultimas_matrizes_percentos',
                 'str_matriz_ultimo_concurso', 'str_matriz_penultimo_concurso')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao Matricial dos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.colunas_jogos: Optional[list[int]] = None
        self.colunas_percentos: Optional[list[float]] = None
        self.colunas_concursos: Optional[list[int]] = None
        self.linhas_jogos: Optional[list[int]] = None
        self.linhas_percentos: Optional[list[float]] = None
        self.linhas_concursos: Optional[list[int]] = None
        self.ultimas_matrizes_repetidas: dict[str: int] = None
        self.ultimas_matrizes_percentos: dict[str: float] = None
        self.str_matriz_ultimo_concurso: str = ''
        self.str_matriz_penultimo_concurso: str = ''

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_items: int = self.qtd_bolas_sorteio
        self.colunas_jogos = cb.new_list_int(qtd_items)
        self.linhas_jogos = cb.new_list_int(qtd_items)

        # identifica o numero maximo de colunas e linhas de cada combinacao de jogo:
        range_jogos: range = range(1, self.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, self.qtd_bolas_sorteio):
            # maximo de colunas
            vl_max_col: int = cb.max_colunas(jogo)
            self.colunas_jogos[vl_max_col] += 1

            # maximo de linhas
            vl_max_lin: int = cb.max_linhas(jogo)
            self.linhas_jogos[vl_max_lin] += 1

        # contabiliza o percentual das colunas:
        self.colunas_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.colunas_jogos):
            percent: float = round((value / self.qtd_jogos) * 10000) / 100
            self.colunas_percentos[key] = percent

        # contabiliza o percentual das linhas:
        self.linhas_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.linhas_jogos):
            percent: float = round((value / self.qtd_jogos) * 10000) / 100
            self.linhas_percentos[key] = percent

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

        # identifica o numero maximo de colunas e linhas de cada sorteio ja realizado:
        self.colunas_concursos = cb.new_list_int(qtd_items)
        self.linhas_concursos = cb.new_list_int(qtd_items)
        self.ultimas_matrizes_repetidas = {}
        self.str_matriz_ultimo_concurso = ''
        self.str_matriz_penultimo_concurso = ''
        for concurso in concursos:
            # maximo de colunas
            vl_max_col: int = cb.max_colunas(concurso.bolas)
            self.colunas_concursos[vl_max_col] += 1

            # maximo de linhas
            vl_max_lin: int = cb.max_linhas(concurso.bolas)
            self.linhas_concursos[vl_max_lin] += 1

            # verifica se repetiu a matriz com maxima coluna e linha do ultimo concurso:
            tupla_matriz: tuple[int, ...] = (vl_max_col, vl_max_lin)
            str_matriz: str = cb.to_string(tupla_matriz)
            if str_matriz == self.str_matriz_ultimo_concurso:
                self.ultimas_matrizes_repetidas[str_matriz] = \
                    self.ultimas_matrizes_repetidas.get(str_matriz, 0) + 1
            # atualiza ambos flags, para ultimo e penultimo concursos
            self.str_matriz_penultimo_concurso = self.str_matriz_ultimo_concurso
            self.str_matriz_ultimo_concurso = str_matriz

        # contabiliza o percentual das ultimas matrizes de maxima coluna e linha:
        self.ultimas_matrizes_percentos = {}
        for key, value in self.ultimas_matrizes_repetidas.items():
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.ultimas_matrizes_percentos[key] = percent

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero maximo de colunas e linhas do jogo:
        vl_max_col: int = cb.max_colunas(jogo)
        percent_col: float = self.colunas_percentos[vl_max_col]

        vl_max_lin: int = cb.max_linhas(jogo)
        percent_lin: float = self.linhas_percentos[vl_max_lin]

        # ignora valores muito baixos de probabilidade:
        if percent_col == 0 or percent_lin == 0:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_fator(percent_col) * to_fator(percent_lin)
        tupla_matriz: tuple[int, ...] = (vl_max_col, vl_max_lin)
        str_matriz: str = cb.to_string(tupla_matriz)

        # verifica se esse jogo repetiu a matriz da maxima coluna e/ou linha dos ultimos concursos:
        if str_matriz != self.str_matriz_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif str_matriz == self.str_matriz_ultimo_concurso == self.str_matriz_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao da ultima matriz de coluna e linha:
        percent_repetida: float = self.ultimas_matrizes_percentos.get(str_matriz, 0.0)
        if percent_repetida < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir a matriz de coluna e linha:
            return fator_percent * to_redutor(percent_repetida)

# ----------------------------------------------------------------------------
