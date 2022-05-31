"""
   Package lothon.process
   Module  analise_colunario.py

"""

__all__ = [
    'AnaliseColunario'
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
from lothon.domain import Loteria, Concurso, ConcursoDuplo
from lothon.process.analyze.abstract_analyze import AbstractAnalyze


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseColunario(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # estruturas para a coleta de dados a partir do processamento de analise:
    colunarios_jogos: Optional[list[int]] = None
    colunarios_percentos: Optional[list[float]] = None
    colunarios_concursos: Optional[list[int]] = None

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Colunario nos Concursos")

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def count_colunarios(cls, bolas: tuple[int, ...], colunario: list[int]):
        # valida os parametros:
        if bolas is None or len(bolas) == 0 or colunario is None or len(colunario) == 0:
            return

        for num in bolas:
            colunario[num % 10] += 1

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.colunarios_jogos = None
        self.colunarios_percentos = None
        self.colunarios_concursos = None

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # o numero de sorteios realizados pode dobrar se for instancia de ConcursoDuplo:
        nmlot: str = payload.nome_loteria
        concursos: list[Concurso | ConcursoDuplo] = payload.concursos
        qtd_concursos: int = len(concursos)
        eh_duplo: bool = ([0] is ConcursoDuplo)
        if eh_duplo:
            fator_sorteios: int = 2
        else:
            fator_sorteios: int = 1
        qtd_sorteios: int = qtd_concursos * fator_sorteios
        qtd_items: int = 9

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug(f"{nmlot}: Executando analise de colunario dos  "
                     f"{qtd_jogos:,}  jogos combinados da loteria.")

        # zera os contadores de cada paridade:
        self.colunarios_jogos = self.new_list_int(qtd_items)
        self.colunarios_percentos = self.new_list_float(qtd_items)

        # contabiliza pares (e impares) de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            self.count_colunarios(jogo, self.colunarios_jogos)

        # printa o resultado:
        output: str = f"\n\t ? COLUNA     PERC%     #TOTAL\n"
        total: int = payload.qtd_bolas_sorteio * qtd_jogos
        for key, value in enumerate(self.colunarios_jogos):
            percent: float = round((value / total) * 1000) / 10
            self.colunarios_percentos[key] = percent
            output += f"\t {key} coluna:  {formatf(percent,'6.2')}% ... #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Colunarios Resultantes: {output}")

        # efetua analise de colunarios de todos os sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise TOTAL de colunarios dos  "
                     f"{qtd_concursos:,}  concursos da loteria.")

        # zera os contadores de cada sequencia:
        self.colunarios_concursos = self.new_list_int(qtd_items)

        # contabiliza colunarios de cada sorteio ja realizado:
        for concurso in concursos:
            self.count_colunarios(concurso.bolas, self.colunarios_concursos)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                self.count_colunarios(concurso.bolas2, self.colunarios_concursos)

        # printa o resultado:
        output: str = f"\n\t ? COLUNA     PERC%       %DIF%     #TOTAL\n"
        total: int = payload.qtd_bolas_sorteio * qtd_sorteios
        for key, value in enumerate(self.colunarios_concursos):
            percent: float = round((value / total) * 10000) / 100
            dif: float = percent - self.colunarios_percentos[key]
            output += f"\t {key} coluna:  {formatf(percent,'6.2')}% ... {formatf(dif,'6.2')}%  " \
                      f"   #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Colunarios Resultantes: {output}")

        #
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de colunario dos  "
                     f"{qtd_concursos:,}  concursos da loteria.")

        # contabiliza colunarios de cada evolucao de concurso:
        concursos_passados: list[Concurso | ConcursoDuplo] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        concurso_atual: Concurso | ConcursoDuplo
        for concurso_atual in payload.concursos:
            # zera os contadores de cada colunario:
            colunarios_passados: list[int] = self.new_list_int(qtd_items)

            # calcula a colunario dos concursos passados ate o concurso anterior:
            for concurso_passado in concursos_passados:
                self.count_colunarios(concurso_passado.bolas, colunarios_passados)
                # verifica se o concurso eh duplo (dois sorteios):
                if eh_duplo:
                    self.count_colunarios(concurso_passado.bolas2, colunarios_passados)

            # calcula a colunario do concurso atual para comparar a evolucao:
            colunario_atual: list[int] = self.new_list_int(qtd_items)
            self.count_colunarios(concurso_atual.bolas, colunario_atual)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                self.count_colunarios(concurso_atual.bolas2, colunario_atual)

            # printa o resultado:
            output: str = f"\n\t ? COLUNA     PERC%       %DIF%  " \
                          f"----->  CONCURSO Nr {concurso_atual.id_concurso} :  " \
                          f"Ultimo Colunario == {colunario_atual}\n"
            total: int = payload.qtd_bolas_sorteio * (qtd_concursos_passados * fator_sorteios)
            for key, value in enumerate(colunarios_passados):
                percent: float = round((value / total) * 10000) / 100
                dif: float = percent - self.colunarios_percentos[key]
                output += f"\t {key} coluna:  {formatf(percent,'6.2')}% ... {formatf(dif,'6.2')}%\n"
            logger.debug(f"{nmlot}: Colunarios Resultantes da EVOLUTIVA: {output}")

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        pass

    def evaluate(self, payload) -> float:
        pass

# ----------------------------------------------------------------------------
