"""
   Package lothon.process.analyze
   Module analise_dispersao.py

"""

__all__ = [
    'AnaliseDispersao'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging
import statistics as stts
import math

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.stats import combinatoria as cb
from lothon.domain import Loteria, Concurso
from lothon.process.analyze.abstract_analyze import AbstractAnalyze
from lothon.process.compute.compute_dispersao import ComputeDispersao


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseDispersao(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Dispersao das Dezenas")

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
        qtd_items: int = loteria.qtd_bolas

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeDispersao()
        cp.execute(loteria)

        # efetua analise de todas as dezenas dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de frequencias e atrasos de TODAS as "
                     f"dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # printa as frequencias e atrasos das dezenas em todos os sorteios ja realizados:
        output: str = f"\n\t BOLA:   #SORTEIOS   #ATRASOS\n"
        for idx, frequencia in enumerate(cp.frequencias_dezenas[1:]):
            dezena: int = idx + 1
            atrasos: int = cp.atrasos_dezenas[dezena]
            output += f"\t   {formatd(dezena,2)}:       " \
                      f"{formatd(frequencia,5)}      " \
                      f"{formatd(atrasos,5)}\n"
        logger.debug(f"{nmlot}: Frequencias e Atrasos de Dezenas Resultantes: {output}")

        # efetua analise de variancia e desvio-padrao das dezenas:
        logger.debug(f"{nmlot}: Executando analise de variancia e desvio-padrao das dezenas "
                     f"sorteadas em TODOS os  {formatd(qtd_concursos)}  concursos da loteria.")

        # inicializa o print de resultado dos contadores de frequencias:
        output: str = f"\n\t CONCURSO    VARIANCIAS    FREQUENCIAS    ATRASOS    ESPACOS  ...  " \
                      f"DISPERSAO\n"

        # contabiliza as variancias das dezenas em todos os sorteios ja realizados:
        dispersao: list[int] = cb.new_list_int(qtd_items)
        for concurso in concursos:
            list_frequencias: list[int] = cp.list_frequencias(concurso.bolas)
            list_atrasos: list[int] = cp.list_atrasos(concurso.bolas)
            list_espacos: list[int] = cb.list_espacos(concurso.bolas)

            # calcula as medidas estatisticas de dispersao:
            varia_dezenas: float = stts.pstdev(concurso.bolas)
            varia_frequencia: float = stts.pstdev(list_frequencias)
            varia_atrasos: float = stts.pstdev(list_atrasos)
            varia_espacos: float = stts.pstdev(list_espacos)

            # calcula a dispersao entre as frequencias e atrasos das dezenas:
            varia_fator: int = round(math.sqrt(varia_frequencia * varia_atrasos))
            dispersao[varia_fator] += 1

            # formata os valores para o concurso atual:
            output += f"\t    {formatd(concurso.id_concurso,5)}     " \
                      f"{formatf(varia_dezenas,'9.2')}      " \
                      f"{formatf(varia_frequencia,'9.2')}  " \
                      f"{formatf(varia_atrasos,'9.2')}  " \
                      f"{formatf(varia_espacos,'9.2')}  ...        " \
                      f"{formatd(varia_fator,3)}\n"
        # apos percorrer todos os concursos, printa as frequencias medias:
        logger.debug(f"{nmlot}: Variancias das Dezenas Sorteadas: {output}")

        # printa o percentual das faixas de dispersoes:
        output: str = f"\n\t DISPERSAO    PERC%       #TOTAL\n"
        for key, value in enumerate(cp.dispersoes_concursos):
            percent: float = cp.dispersoes_percentos[key]
            output += f"\t        {formatd(key,2)}  {formatf(percent,'6.2')}%  ...  " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Faixas de dispersao dos concursos: {output}")

        # printa quais as faixas de dispersao que repetiram no ultimo sorteio dos concursos:
        output: str = f"\n\t DISPERSAO    PERC%       #REPETIDAS\n"
        for key, value in enumerate(cp.ultimas_dispersoes_repetidas):
            percent: float = cp.ultimas_dispersoes_percentos[key]
            output += f"\t        {formatd(key,2)}  {formatf(percent,'6.2')}%  ...  " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Concursos que repetiram a ultima dispersao: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
