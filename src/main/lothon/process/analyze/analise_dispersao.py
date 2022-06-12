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
from typing import Optional
import logging
import statistics as stts

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
    __slots__ = ('frequencias_dezenas', 'atrasos_dezenas')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Dispersao das Dezenas")

        # estrutura para a coleta de dados a partir do processamento de analise:
        self.frequencias_dezenas: Optional[list[int]] = None
        self.atrasos_dezenas: Optional[list[int]] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- METODOS ------------------------------------------------------------

    def list_frequencias(self, bolas: tuple[int, ...]) -> list[int]:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return []

        # obtem as frequencias das bolas:
        frequencias: list[int] = []
        for dezena in bolas:
            frequencias.append(self.frequencias_dezenas[dezena])

        return frequencias

    def list_atrasos(self, bolas: tuple[int, ...]) -> list[int]:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return []

        # obtem os atrasos das bolas:
        atrasos: list[int] = []
        for dezena in bolas:
            atrasos.append(self.atrasos_dezenas[dezena])

        return atrasos

    # --- PROCESSAMENTO ------------------------------------------------------

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
        # qtd_items: int = payload.qtd_bolas

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeDispersao()
        cp.execute(payload)

        # efetua analise de todas as dezenas dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de frequencias e atrasos de TODAS as "
                     f"dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # inicializa os contadores de frequencias e atrasos:
        self.frequencias_dezenas = cp.frequencias_dezenas
        self.atrasos_dezenas = cp.atrasos_dezenas

        # printa as frequencias e atrasos das dezenas em todos os sorteios ja realizados:
        output: str = f"\n\t BOLA:   #SORTEIOS   #ATRASOS\n"
        for idx, frequencia in enumerate(self.frequencias_dezenas[1:]):
            dezena: int = idx + 1
            atrasos: int = self.atrasos_dezenas[dezena]
            output += f"\t   {formatd(dezena,2)}:       " \
                      f"{formatd(frequencia,5)}      " \
                      f"{formatd(atrasos,5)}\n"
        logger.debug(f"{nmlot}: Frequencias e Atrasos de Dezenas Resultantes: {output}")

        # efetua analise de variancia e desvio-padrao das dezenas:
        logger.debug(f"{nmlot}: Executando analise de variancia e desvio-padrao das dezenas "
                     f"sorteadas em TODOS os  {formatd(qtd_concursos)}  concursos da loteria.")

        # inicializa o print de resultado dos contadores de frequencias:
        output: str = f"\n\t CONCURSO    VARIANCIAS    FREQUENCIAS    ATRASOS    ESPACOS\n"

        # contabiliza as variancias das dezenas em todos os sorteios ja realizados:
        for concurso in concursos:
            list_frequencias: list[int] = self.list_frequencias(concurso.bolas)
            list_atrasos: list[int] = self.list_atrasos(concurso.bolas)
            list_espacos: list[int] = cb.list_espacos(concurso.bolas)

            # calcula as medidas estatisticas de dispersao:
            varia_dezenas: float = stts.pstdev(concurso.bolas)
            varia_frequencia: float = stts.pstdev(list_frequencias)
            varia_atrasos: float = stts.pstdev(list_atrasos)
            varia_espacos: float = stts.pstdev(list_espacos)

            # formata os valores para o concurso atual:
            output += f"\t    {formatd(concurso.id_concurso,5)}     " \
                      f"{formatf(varia_dezenas,'9.2')}      " \
                      f"{formatf(varia_frequencia,'9.2')}  " \
                      f"{formatf(varia_atrasos,'9.2')}  " \
                      f"{formatf(varia_espacos,'9.2')}\n"
        # apos percorrer todos os concursos, printa as frequencias medias:
        logger.debug(f"{nmlot}: Variancias das Dezenas Sorteadas: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
