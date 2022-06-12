"""
   Package lothon.process.compute
   Module  compute_ciclo.py

"""

__all__ = [
    'ComputeCiclo'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging
from typing import Optional

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.stats import combinatoria as cb
from lothon.domain import Loteria, Concurso, SerieSorteio
from lothon.process.compute.abstract_compute import AbstractCompute


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class ComputeCiclo(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('frequencias_ciclos',)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Ciclo Fechado dos Concursos")

        # estrutura para a coleta de dados a partir do processamento de analise:
        self.frequencias_ciclos: Optional[SerieSorteio] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- PROCESSAMENTO DOS SORTEIOS -----------------------------------------

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = payload.nome_loteria
        concursos: list[Concurso] = payload.concursos
        # qtd_concursos: int = len(concursos)
        qtd_items: int = payload.qtd_bolas

        # inicializa a serie para os ciclos fechados:
        self.frequencias_ciclos = SerieSorteio(0)

        # contabiliza os ciclos fechados em todos os sorteios ja realizados:
        dezenas: list[int] = cb.new_list_int(qtd_items)
        dezenas[0] = -1

        # prepara a impressao evolutiva:
        for concurso in concursos:
            # identifica as bolas sorteadas para fechar o ciclo:
            cb.count_dezenas(concurso.bolas, dezenas)

            # se ainda tem algum zero, entao nao fechou o ciclo:
            if 0 in dezenas:
                continue

            # fechando o ciclo, contabiliza o ciclo fechado (onde fecha o ciclo eh inclusivo):
            self.frequencias_ciclos.add_sorteio(concurso.id_concurso, True)

            # zera contadores para proximo ciclo:
            dezenas = cb.new_list_int(qtd_items)
            dezenas[0] = -1  # p/ nao conflitar com o teste de fechamento do ciclo: 0 in dezena

        # ja calcula as medidas estatisticas para impressao ao final:
        self.frequencias_ciclos.update_stats()

        # indica o tempo do processamento:
        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, jogo: tuple) -> float:
        return 1.0

# ----------------------------------------------------------------------------
