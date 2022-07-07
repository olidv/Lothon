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
from lothon.domain import Concurso
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
                 'fracoes_concursos', 'vl_ordinal_ultimo_concurso')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, threshold: int = 5):  # threshold minimo de 5% para filtro mais eficaz...
        super().__init__("Computacao Ordinal dos Sorteios", threshold)

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.ordinais_concursos: Optional[list[int]] = None
        self.parciais_concursos: Optional[list[int]] = None
        self.fracoes_concursos: Optional[list[int]] = None
        self.ordinais_percentos: Optional[list[float]] = None

        # estruturas para avaliacao de jogo combinado da loteria:
        self.vl_ordinal_ultimo_concurso: Optional[int] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, concursos: list[Concurso]) -> int:
        # valida se possui concursos a serem analisados:
        if concursos is None or len(concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        ultimo_concurso: Concurso = concursos[-1]
        qtd_concursos: int = len(concursos)
        qtd_items: int = qtd_concursos

        # primeiro organiza dicionario com todos os concursos:
        sorteios_literal: dict[str: int] = {}
        for concurso in concursos:
            bolas_str: str = cb.to_string(concurso.bolas)
            sorteios_literal[bolas_str] = concurso.id_concurso

        # efetua analise de todas as combinacoes de jogos da loteria:
        self.ordinais_concursos = cb.new_list_int(qtd_items)
        self.parciais_concursos = cb.new_list_int(self.qtd_jogos // 100000)

        # para cada concurso, vai atribuir o respectivo ordinal das combinacoes de jogos da loteria:
        range_jogos: range = range(1, self.qtd_bolas + 1)
        ordinal_jogo: int = 0
        for jogo in itt.combinations(range_jogos, self.qtd_bolas_sorteio):
            ordinal_jogo += 1  # primeiro jogo ira comecar do #1

            # procura no dicionario de literais o jogo corrente:
            bolas_str: str = cb.to_string(jogo)
            id_concurso: int = sorteios_literal.get(bolas_str, -1)
            if id_concurso > 0:
                self.ordinais_concursos[id_concurso] = ordinal_jogo
                self.parciais_concursos[ordinal_jogo // 100000] += 1

        # salva o ordinal do ultimo concurso para o EVALUATE posterior:
        self.vl_ordinal_ultimo_concurso = self.ordinais_concursos[ultimo_concurso.id_concurso]

        # calcula o diferencial em percentual entre o concurso e os demais abaixo e acima:
        self.fracoes_concursos = cb.new_list_int(9)
        vl_ordinal_anterior: int = self.ordinais_concursos[1]  # ordinal do primeiro concurso
        for concurso in concursos:
            idx: int = concurso.id_concurso
            # verifica o ordinal do concurso atual e diferenca com ordinal do anterior:
            vl_ordinal_atual: int = self.ordinais_concursos[idx]  # esta sincronizado com concursos
            dif_ordinal_anterior: int = abs(vl_ordinal_atual - vl_ordinal_anterior)
            faixa_percent_abaixo: int = round((dif_ordinal_anterior / self.qtd_jogos) * 100) // 10
            self.fracoes_concursos[faixa_percent_abaixo] += 1

            # atualiza o anterior (atual) para a proxima iteracao:
            vl_ordinal_anterior = vl_ordinal_atual

        # calcula os percentuais de cada fracao diferencial:
        self.ordinais_percentos = cb.new_list_float(9)
        for key, value in enumerate(self.fracoes_concursos):
            self.ordinais_percentos[key] = round((value / qtd_concursos) * 10000) / 100

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def rate(self, ordinal: int, jogo: tuple) -> int:
        dif_ordinal_anterior: int = abs(ordinal - self.vl_ordinal_ultimo_concurso)
        faixa_percent_abaixo: int = round((dif_ordinal_anterior / self.qtd_jogos) * 100) // 10
        return faixa_percent_abaixo

    def eval(self, ordinal: int, jogo: tuple) -> float:
        dif_ordinal_anterior: int = abs(ordinal - self.vl_ordinal_ultimo_concurso)
        faixa_percent_abaixo: int = round((dif_ordinal_anterior / self.qtd_jogos) * 100) // 10
        percent: float = self.ordinais_percentos[faixa_percent_abaixo]

        # ignora valores muito baixos de probabilidade:
        if percent < self.min_threshold:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica):
        fator_percent: float = to_redutor(percent)
        return fator_percent

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        dif_ordinal_anterior: int = abs(ordinal - self.vl_ordinal_ultimo_concurso)
        faixa_percent_abaixo: int = round((dif_ordinal_anterior / self.qtd_jogos) * 100) // 10
        percent: float = self.ordinais_percentos[faixa_percent_abaixo]

        # ignora valores muito baixos de probabilidade:
        if percent < 1:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica):
        fator_percent: float = to_fator(percent)
        return fator_percent

# ----------------------------------------------------------------------------
