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
        self.ordinais_concursos = None
        self.ordinais_percentos = None
        self.parciais_concursos = None
        self.qtd_jogos = None
        self.vl_ultimo_ordinal = None

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

        # zera os contadores de cada ordinal:
        self.ordinais_concursos = self.new_list_int(qtd_items)
        self.parciais_concursos = self.new_list_int(qtd_jogos // 100000)

        # para cada concurso, vai atribuir o respectivo ordinal das combinacoes de jogos da loteria:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        ordinal_jogo: int = 0
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            ordinal_jogo += 1  # primeiro jogo ira comecar do #1

            # procura no dicionario de literais o jogo corrente:
            bolas_str: str = self.to_string(jogo)
            id_concurso: int = sorteios_literal.get(bolas_str, -1)
            if id_concurso > 0:
                self.ordinais_concursos[id_concurso] = ordinal_jogo
                self.parciais_concursos[ordinal_jogo // 100000] += 1

        # printa o resultado:
        output: str = f"\n\t ORDEM     PERC%     #CONCURSOS\n"
        for key, value in enumerate(self.parciais_concursos):
            percent: float = round((value / qtd_concursos) * 1000) / 10
            output += f"\t    {key:0>2}    {formatf(percent,'5.1')}% ... {value:,}\n"
        logger.debug(f"{nmlot}: Concursos para cada Ordem de 100mil jogos: {output}")

        # zera os contadores de cada faixa percentual de ordinal abaixo:
        self.ordinais_percentos = self.new_list_int(9)

        # calcula o diferencial em percentual entre o concurso e os demais abaixo e acima:
        vl_ordinal_anterior: int = self.ordinais_concursos[1]  # ordinal do primeiro concurso
        # formata o cabecalho da impressao do resultado:
        output: str = f"\n\t CONCURSO         #ORDINAL      ANTERIOR   ABAIXO%       " \
                      f"PROXIMO   ACIMA%\n"
        for concurso in concursos:
            idx: int = concurso.id_concurso
            # verifica o ordinal do concurso atual e diferenca com ordinal do anterior:
            vl_ordinal_atual: int = self.ordinais_concursos[idx]  # esta sincronizado com concursos
            dif_ordinal_anterior: int = abs(vl_ordinal_atual - vl_ordinal_anterior)
            dif_percent_abaixo: int = round((dif_ordinal_anterior / qtd_jogos) * 100)
            self.ordinais_percentos[dif_percent_abaixo // 10] += 1
            # calcula a diferenca com o ordinal do proximo concurso:
            idx_next: int = idx + 1
            dif_ordinal_proximo: int = abs(self.ordinais_concursos[idx_next] -
                                           vl_ordinal_atual) if idx_next <= qtd_concursos else 0
            dif_percent_acima: int = round((dif_ordinal_proximo / qtd_jogos) * 100)

            # printa os valores do concurso atual:
            output += f"\t    {formatd(concurso.id_concurso,5)}  ...  " \
                      f"{formatd(vl_ordinal_atual,10)}    " \
                      f"{formatd(dif_ordinal_anterior,10)}      " \
                      f"{formatd(dif_percent_abaixo,3)}%    " \
                      f"{formatd(dif_ordinal_proximo,10)}     " \
                      f"{formatd(dif_percent_acima,3)}%\n"

            # atualiza o anterior (atual) para a proxima iteracao:
            vl_ordinal_anterior = vl_ordinal_atual
        logger.debug(f"{nmlot}: Relacao de Ordinais dos Concursos: {output}")

        # printa o resultado das faixas de percentuais:
        output: str = f"\n\t ABAIXO%     PERC%     #CONCURSOS\n"
        for key, value in enumerate(self.ordinais_percentos):
            percent: float = round((value / qtd_concursos) * 1000) / 10
            output += f"\t     {key*10:0>2}%    {formatf(percent,'5.1')}% ... {value:,}\n"
        logger.debug(f"{nmlot}: Concursos para cada faixa de ordinais: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        self.set_options(parms)

        # identifica os concursos passados:
        id_ultimo_concurso: int = parms["id_ultimo_concurso"]
        self.vl_ultimo_ordinal = self.ordinais_percentos[id_ultimo_concurso]

    def evaluate(self, ordinal) -> float:
        dif_ordinal_anterior: int = abs(ordinal - self.vl_ultimo_ordinal)
        faixa_percent_abaixo: int = round((dif_ordinal_anterior / self.qtd_jogos) * 100)
        percent: float = self.ordinais_percentos[faixa_percent_abaixo // 10]

        # ignora valores muito baixos de probabilidade:
        if percent < 5:
            return 0
        else:
            return to_fator(percent)

# ----------------------------------------------------------------------------
