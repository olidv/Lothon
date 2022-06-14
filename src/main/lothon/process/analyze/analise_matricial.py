"""
   Package lothon.process.analyze
   Module  analise_matricial.py

"""

__all__ = [
    'AnaliseMatricial'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.domain import Loteria, Concurso
from lothon.process.analyze.abstract_analyze import AbstractAnalyze
from lothon.process.compute.compute_matricial import ComputeMatricial


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
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise Matricial dos Concursos")

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
        # qtd_items: int = loteria.qtd_bolas_sorteio

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeMatricial()
        cp.execute(loteria)

        # efetua analise de todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise matricial dos  "
                     f"{qtd_jogos:,}  jogos combinados da loteria.")

        # printa o numero maximo de colunas de cada combinacao de jogo:
        outputc: str = f"\n\t COLUNAS     PERC%     #TOTAL\n"
        for key, value in enumerate(cp.colunas_jogos):
            percent: float = cp.colunas_percentos[key]
            outputc += f"\t      {key:0>2}   {formatf(percent,'6.2')}% ... #{formatd(value)}\n"

        # printa o numero maximo de linhas de cada combinacao de jogo:
        outputl: str = f"\n\t  LINHAS     PERC%     #TOTAL\n"
        for key, value in enumerate(cp.linhas_jogos):
            percent: float = cp.linhas_percentos[key]
            outputl += f"\t      {key:0>2}   {formatf(percent,'6.2')}% ... #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Maximo de Colunas e Linhas dos jogos: {outputc}{outputl}")

        # efetua analise diferencial dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise matricial TOTAL dos  "
                     f"{qtd_concursos:,}  concursos da loteria.")

        # printa o numero maximo de colunas de cada sorteio ja realizado:
        outputc: str = f"\n\t COLUNAS     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(cp.colunas_concursos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            dif: float = percent - cp.colunas_percentos[key]
            outputc += f"\t      {key:0>2}   {formatf(percent,'6.2')}% ... {formatf(dif,'6.2')}% " \
                       f"    #{formatd(value)}\n"

        # printa o numero maximo de linhas de cada sorteio ja realizado:
        outputl: str = f"\n\t  LINHAS     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(cp.linhas_concursos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            dif: float = percent - cp.linhas_percentos[key]
            outputl += f"\t      {key:0>2}   {formatf(percent,'6.2')}% ... {formatf(dif,'6.2')}% " \
                       f"    #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Maximo de Colunas e Linhas dos concursos: {outputc}{outputl}")

        # printa quais matrizes de colunas e linhas repetiram no ultimo sorteio dos concursos:
        output: str = f"\n\t  MATRIZ     PERC%       #REPETIDAS\n"
        for key, value in cp.ultimas_matrizes_repetidas.items():
            percent: float = cp.ultimas_matrizes_percentos[key]
            output += f"\t    {key}   {formatf(percent,'6.2')}%  ...  " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Concursos que repetiram a matriz da maxima coluna e linha: "
                     f"{output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
