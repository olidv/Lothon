"""
   Package lothon.process
   Module  analise_matricial.py

"""

__all__ = [
    'AnaliseMatricial'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
import math
import itertools as itt
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.domain import Loteria, Concurso
from lothon.process.analyze.abstract_analyze import AbstractAnalyze


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseMatricial(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('colunas_jogos', 'colunas_percentos', 'colunas_concursos',
                 'linhas_jogos', 'linhas_percentos', 'linhas_concursos')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise Matricial dos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.colunas_jogos: Optional[list[int]] = None
        self.colunas_percentos: Optional[list[float]] = None
        self.colunas_concursos: Optional[list[int]] = None
        self.linhas_jogos: Optional[list[int]] = None
        self.linhas_percentos: Optional[list[float]] = None
        self.linhas_concursos: Optional[list[int]] = None

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def get_coluna(cls, dezena: int) -> int:
        return dezena % 10

    @classmethod
    def max_colunas(cls, bolas: tuple[int, ...]) -> int:
        # prepara contador de dezenas por coluna
        colunas: list[int] = cls.new_list_int(9)

        # verifica quantas dezenas em cada coluna:
        for num in bolas:
            colunas[cls.get_coluna(num)] += 1

        # informa o maior numero de dezenas encontradas em determinada coluna:
        return max(colunas)

    @classmethod
    def get_linha(cls, dezena: int) -> int:
        return (dezena - 1) // 10

    @classmethod
    def max_linhas(cls, bolas: tuple[int, ...]):
        # prepara contador de dezenas por linha
        linhas: list[int] = cls.new_list_int(9)

        # verifica quantas dezenas em cada linha:
        for num in bolas:
            linhas[cls.get_linha(num)] += 1

        # informa o maior numero de dezenas encontradas em determinada linha:
        return max(linhas)

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.colunas_jogos = None
        self.colunas_percentos = None
        self.colunas_concursos = None
        self.linhas_jogos = None
        self.linhas_percentos = None
        self.linhas_concursos = None

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = payload.nome_loteria
        concursos: list[Concurso] = payload.concursos
        qtd_concursos: int = len(concursos)
        qtd_items: int = payload.qtd_bolas_sorteio

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug(f"{nmlot}: Executando analise matricial dos  "
                     f"{qtd_jogos:,}  jogos combinados da loteria.")

        # zera os contadores de cada maximo de coluna e linha:
        self.colunas_jogos = self.new_list_int(qtd_items)
        self.colunas_percentos = self.new_list_float(qtd_items)
        self.linhas_jogos = self.new_list_int(qtd_items)
        self.linhas_percentos = self.new_list_float(qtd_items)

        # identifica o numero maximo de colunas e linhas de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            # maximo de colunas
            vl_max_col: int = self.max_colunas(jogo)
            self.colunas_jogos[vl_max_col] += 1

            # maximo de linhas
            vl_max_lin: int = self.max_linhas(jogo)
            self.linhas_jogos[vl_max_lin] += 1

        # printa o resultado das colunas:
        outputc: str = f"\n\t COLUNAS     PERC%     #TOTAL\n"
        for key, value in enumerate(self.colunas_jogos):
            percent: float = round((value / qtd_jogos) * 10000) / 100
            self.colunas_percentos[key] = percent
            outputc += f"\t      {key:0>2}   {formatf(percent,'6.2')}% ... #{formatd(value)}\n"

        # printa o resultado das linhas:
        outputl: str = f"\n\t  LINHAS     PERC%     #TOTAL\n"
        for key, value in enumerate(self.linhas_jogos):
            percent: float = round((value / qtd_jogos) * 10000) / 100
            self.linhas_percentos[key] = percent
            outputl += f"\t      {key:0>2}   {formatf(percent,'6.2')}% ... #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Maximo de Colunas e Linhas dos jogos: {outputc}{outputl}")

        # efetua analise diferencial dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise matricial TOTAL dos  "
                     f"{qtd_concursos:,}  concursos da loteria.")

        # zera os contadores de cada sequencia:
        self.colunas_concursos = self.new_list_int(qtd_items)
        self.linhas_concursos = self.new_list_int(qtd_items)

        # identifica o numero maximo de colunas e linhas de cada sorteio ja realizado:
        for concurso in concursos:
            # maximo de colunas
            vl_max_col: int = self.max_colunas(concurso.bolas)
            self.colunas_concursos[vl_max_col] += 1

            # maximo de linhas
            vl_max_lin: int = self.max_linhas(concurso.bolas)
            self.linhas_concursos[vl_max_lin] += 1

        # printa o resultado das colunas:
        outputc: str = f"\n\t COLUNAS     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(self.colunas_concursos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            dif: float = percent - self.colunas_percentos[key]
            outputc += f"\t      {key:0>2}   {formatf(percent,'6.2')}% ... {formatf(dif,'6.2')}% " \
                       f"    #{formatd(value)}\n"

        # printa o resultado das linhas:
        outputl: str = f"\n\t  LINHAS     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(self.linhas_concursos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            dif: float = percent - self.linhas_percentos[key]
            outputl += f"\t      {key:0>2}   {formatf(percent,'6.2')}% ... {formatf(dif,'6.2')}% " \
                       f"    #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Maximo de Colunas e Linhas dos concursos: {outputc}{outputl}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        self.set_options(parms)

    def evaluate(self, pick) -> float:
        # probabilidade de acerto depende do numero maximo de colunas e linhas do jogo:
        vl_max_col: int = self.max_colunas(pick)
        percent_col: float = self.colunas_percentos[vl_max_col]

        vl_max_lin: int = self.max_linhas(pick)
        percent_lin: float = self.linhas_percentos[vl_max_lin]

        # ignora valores muito baixos de probabilidade:
        if percent_col < 9 or percent_lin < 5:
            return 0
        else:
            return (1 + (percent_col / 100)) * (1 + (percent_lin / 100))

# ----------------------------------------------------------------------------
