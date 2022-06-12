"""
   Package lothon.process.compute
   Module compute_dispersao.py

"""

__all__ = [
    'ComputeDispersao'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.stats import combinatoria as cb
from lothon.domain import Loteria, Concurso
from lothon.process.compute.abstract_compute import AbstractCompute


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class ComputeDispersao(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('frequencias_dezenas', 'atrasos_dezenas')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Dispersao das Dezenas")

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
        qtd_items: int = payload.qtd_bolas

        # zera os contadores de frequencias e atrasos - usa -1 para nao conflitar com teste == 0:
        self.frequencias_dezenas = cb.new_list_int(qtd_items, -1)
        self.atrasos_dezenas = cb.new_list_int(qtd_items, -1)  #

        # contabiliza as frequencias e atrasos das dezenas em todos os sorteios ja realizados:
        for concurso in reversed(concursos):
            # cada ocorrencia de dezena incrementa sua respectiva frequencia:
            for dezena in concurso.bolas:
                self.frequencias_dezenas[dezena] += 1
                # contabiliza tambem os atrasos, aproveitando a ordem reversa dos concursos:
                if self.atrasos_dezenas[dezena] == -1:
                    self.atrasos_dezenas[dezena] = qtd_concursos - concurso.id_concurso

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, jogo: tuple) -> float:
        return 1.0

# ----------------------------------------------------------------------------
