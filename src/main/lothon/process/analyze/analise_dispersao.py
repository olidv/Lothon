"""
   Package lothon.process
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

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def list_espacos(cls, bolas: tuple[int, ...]) -> list[int]:
        # valida os parametros:
        if bolas is None or len(bolas) <= 1:  # eh preciso ao menos 2 itens para calcular espacos
            return []

        # obtem os espacamentos entre as bolas:
        espacos: list[int] = []
        aux: int = bolas[0]  # nao precisa iterar no primeiro, p/ agilizar o calculo da diferenca
        for dezena in sorted(bolas[1:]):  # tem q estar ordenada
            dif: int = dezena - aux
            espacos.append(dif)
            aux = dezena

        return espacos

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.frequencias_dezenas = None
        self.atrasos_dezenas = None

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
        qtd_items: int = payload.qtd_bolas

        # efetua analise de todas as dezenas dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de frequencias e atrasos de TODAS as "
                     f"dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de frequencias e atrasos - usa -1 para nao conflitar com teste == 0:
        self.frequencias_dezenas = self.new_list_int(qtd_items, -1)
        self.atrasos_dezenas = self.new_list_int(qtd_items, -1)  #

        # contabiliza as frequencias e atrasos das dezenas em todos os sorteios ja realizados:
        for concurso in reversed(concursos):
            # cada ocorrencia de dezena incrementa sua respectiva frequencia:
            for dezena in concurso.bolas:
                self.frequencias_dezenas[dezena] += 1
                # contabiliza tambem os atrasos, aproveitando a ordem reversa dos concursos:
                if self.atrasos_dezenas[dezena] == -1:
                    self.atrasos_dezenas[dezena] = qtd_concursos - concurso.id_concurso

        # printa o resultado:
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
            list_espacos: list[int] = self.list_espacos(concurso.bolas)

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

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        self.set_options(parms)

    def evaluate(self, pick) -> float:
        return 1.1  # valor temporario

# ----------------------------------------------------------------------------
