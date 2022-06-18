"""
   Package lothon.process.analyze
   Module  analise_ausencia.py

"""

__all__ = [
    'AnaliseAusencia'
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
from lothon.process.compute.compute_ausencia import ComputeAusencia


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseAusencia(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise da Ausencia das Dezenas")

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
        concursos: list[Concurso] = loteria.concursos
        qtd_concursos: int = len(concursos)

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeAusencia()
        cp.setup({
            'qtd_bolas': loteria.qtd_bolas,
            'qtd_bolas_sorteio': loteria.qtd_bolas_sorteio,
            'qtd_jogos': loteria.qtd_jogos
        })
        cp.execute(loteria.concursos)

        # efetua analise de todas as dezenas dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de ausencia de TODAS as "
                     f"dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # inicializa o print de resultado dos contadores de ausencias:
        output: str = f"\n\tCONCURSO  AUSENCIAS:   #TOPOS\n"
        for concurso in concursos[1:]:
            # formata os valores para o concurso atual:
            output += f"\t   {formatd(concurso.id_concurso,5)}  ..........  " \
                      f"{formatd(cp.topos_concursos[concurso.id_concurso], 2)}\n"
        logger.debug(f"{nmlot}: Topos de Ausencias das Dezenas Sorteadas: {output}")

        # printa os topos de cada sorteio dos concursos:
        output: str = f"\n\t  ? TOPOS     PERC%       #TOTAL\n"
        for key, value in enumerate(cp.topos_ausentes):
            percent: float = cp.topos_percentos[key]
            output += f"\t {formatd(key,2)} topos:  {formatf(percent,'6.2')}%  ...  " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Topos de Ausencia Resultantes: {output}")

        # printa quais os topos de ausencias que repetiram no ultimo sorteio dos concursos:
        output: str = f"\n\t  ? TOPOS     PERC%       #REPETIDOS\n"
        for key, value in enumerate(cp.ultimos_topos_repetidos):
            percent: float = cp.ultimos_topos_percentos[key]
            output += f"\t {formatd(key,2)} topos:  {formatf(percent,'6.2')}%  ...  " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Concursos que repetiram ultimo topo: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
