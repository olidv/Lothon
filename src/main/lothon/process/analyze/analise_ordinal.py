"""
   Package lothon.process
   Module  analise_ordinal.py

"""

__all__ = [
    'AnaliseOrdinal'
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

class AnaliseOrdinal(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('sorteios_ordinal', 'sorteios_parcial')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise Ordinal dos Sorteios")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.sorteios_ordinal: Optional[list[int]] = None
        self.sorteios_parcial: Optional[list[int]] = None

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def to_string(cls, bolas: tuple[int, ...]) -> str:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return ''

        tupla_str: str = ''
        for num in bolas:
            tupla_str += f"{num:0>2}"

        return tupla_str

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.sorteios_ordinal = None
        self.sorteios_parcial = None

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
        qtd_items: int = qtd_concursos

        # primeiro organiza dicionario com todos os concursos:
        sorteios_literal: dict[str: int] = {}
        for concurso in concursos:
            bolas_str: str = self.to_string(concurso.bolas)
            sorteios_literal[bolas_str] = concurso.id_concurso

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug(f"{nmlot}: Executando analise ordinal dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # zera os contadores de cada somatorio:
        self.sorteios_ordinal = self.new_list_int(qtd_items)
        self.sorteios_parcial = self.new_list_int(qtd_jogos // 100000)

        # para cada concurso, vai atribuir o respectivo ordinal das combinacoes de jogos da loteria:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        ordinal_jogo: int = 0
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            ordinal_jogo += 1  # primeiro jogo ira comecar do #1

            # procura no dicionario de literais o jogo corrente:
            bolas_str: str = self.to_string(jogo)
            id_concurso: int = sorteios_literal.get(bolas_str, -1)
            if id_concurso > 0:
                self.sorteios_ordinal[id_concurso] = ordinal_jogo
                self.sorteios_parcial[ordinal_jogo // 100000] += 1

        # printa o primeiro resultado:
        output: str = f"\n\t ORDEM     PERC%     #CONCURSOS\n"
        for key, value in enumerate(self.sorteios_parcial):
            percent: float = round((value / qtd_concursos) * 1000) / 10
            output += f"\t    {key:0>2}    {formatf(percent,'5.1')}% ... {formatd(value,5)}\n"
        logger.debug(f"{nmlot}: Concursos para cada Ordem de 100mil jogos: {output}")

        # printa o segundo resultado:
        output: str = f"\n\t CONCURSO        #ORDINAL\n"
        for concurso in concursos:
            ordinal_jogo: int = self.sorteios_ordinal[concurso.id_concurso]
            output += f"\t    {formatd(concurso.id_concurso,5)}  ...  {formatd(ordinal_jogo,9)}\n"
        logger.debug(f"{nmlot}: Relacao de Ordinais dos Concursos: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        self.set_options(parms)

    def evaluate(self, pick) -> float:
        # probabilidade de acerto depende da ordem sequencial (ordinal) do jogo:
        return 0

# ----------------------------------------------------------------------------
