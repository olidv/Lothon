"""
   Package lothon.process.compute
   Module  compute_ordinal.py

"""

__all__ = [
    'ComputeOrdinal'
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

class ComputeOrdinal(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('ordinais_concursos', 'ordinais_percentos', 'parciais_concursos',
                 'qtd_jogos', 'vl_ultimo_ordinal')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise Ordinal dos Sorteios")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.ordinais_concursos: Optional[list[int]] = None
        self.ordinais_percentos: Optional[list[float]] = None
        self.parciais_concursos: Optional[list[int]] = None

        # estruturas para avaliacao de jogo combinado da loteria:
        self.qtd_jogos: Optional[int] = None
        self.vl_ultimo_ordinal: Optional[int] = None

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = payload.nome_loteria
        self.qtd_jogos = payload.qtd_jogos
        concursos: list[Concurso] = payload.concursos
        qtd_concursos: int = len(concursos)
        qtd_items: int = qtd_concursos

        # primeiro organiza dicionario com todos os concursos:
        sorteios_literal: dict[str: int] = {}
        for concurso in concursos:
            bolas_str: str = cb.to_string(concurso.bolas)
            sorteios_literal[bolas_str] = concurso.id_concurso

        # efetua analise de todas as combinacoes de jogos da loteria:

        # zera os contadores de cada ordinal:
        self.ordinais_concursos = cb.new_list_int(qtd_items)
        self.parciais_concursos = cb.new_list_int(self.qtd_jogos // 100000)

        # para cada concurso, vai atribuir o respectivo ordinal das combinacoes de jogos da loteria:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        ordinal_jogo: int = 0
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            ordinal_jogo += 1  # primeiro jogo ira comecar do #1

            # procura no dicionario de literais o jogo corrente:
            bolas_str: str = cb.to_string(jogo)
            id_concurso: int = sorteios_literal.get(bolas_str, -1)
            if id_concurso > 0:
                self.ordinais_concursos[id_concurso] = ordinal_jogo
                self.parciais_concursos[ordinal_jogo // 100000] += 1

        # zera os contadores de cada faixa percentual de ordinal abaixo:
        self.ordinais_percentos = cb.new_list_int(9)

        # calcula o diferencial em percentual entre o concurso e os demais abaixo e acima:
        vl_ordinal_anterior: int = self.ordinais_concursos[1]  # ordinal do primeiro concurso
        for concurso in concursos:
            idx: int = concurso.id_concurso
            # verifica o ordinal do concurso atual e diferenca com ordinal do anterior:
            vl_ordinal_atual: int = self.ordinais_concursos[idx]  # esta sincronizado com concursos
            dif_ordinal_anterior: int = abs(vl_ordinal_atual - vl_ordinal_anterior)
            dif_percent_abaixo: int = round((dif_ordinal_anterior / self.qtd_jogos) * 100)
            self.ordinais_percentos[dif_percent_abaixo // 10] += 1

            # atualiza o anterior (atual) para a proxima iteracao:
            vl_ordinal_anterior = vl_ordinal_atual

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

        # identifica os concursos passados:
        if "concursos_passados" in parms:
            concursos_passados: list[Concurso] = parms["concursos_passados"]
            id_ultimo_concurso: int = concursos_passados[-1].id_concurso
            self.vl_ultimo_ordinal = self.ordinais_concursos[id_ultimo_concurso]

    def evaluate(self, jogo: tuple) -> float:
        ordinal: int = jogo[0]  # apenas foi passado o ordinal do jogo, ainda que como tupla[int]
        dif_ordinal_anterior: int = abs(ordinal - self.vl_ultimo_ordinal)

        # print("ordinal =", ordinal)
        # print("self.vl_ultimo_ordinal =", self.vl_ultimo_ordinal)
        # print("dif_ordinal_anterior =", dif_ordinal_anterior)
        # print("self.qtd_jogos =", self.qtd_jogos)

        faixa_percent_abaixo: int = round((dif_ordinal_anterior / self.qtd_jogos) * 100)
        percent: float = self.ordinais_percentos[faixa_percent_abaixo // 10]

        # ignora valores muito baixos de probabilidade:
        if percent < 5:
            return 0
        else:
            return to_fator(percent)

# ----------------------------------------------------------------------------
