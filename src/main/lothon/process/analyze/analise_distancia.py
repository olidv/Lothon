"""
   Package lothon.process
   Module  analise_distancia.py

"""

__all__ = [
    'AnaliseDistancia'
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

class AnaliseDistancia(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('distancias_jogos', 'distancias_percentos', 'distancias_concursos')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Distancia nos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.distancias_jogos: Optional[list[int]] = None
        self.distancias_percentos: Optional[list[float]] = None
        self.distancias_concursos: Optional[list[int]] = None

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def calc_distancia(cls, bolas: tuple[int, ...]) -> int:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return 0

        # calcula a distancia entre a menor e a maior bola:
        return max(bolas) - min(bolas)

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.distancias_jogos = None
        self.distancias_percentos = None
        self.distancias_concursos = None

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

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug(f"{nmlot}: Executando analise de distancia dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # zera os contadores de cada distancia:
        self.distancias_jogos = self.new_list_int(qtd_items)
        self.distancias_percentos = self.new_list_float(qtd_items)

        # calcula a distancia de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            vl_distancia = self.calc_distancia(jogo)
            self.distancias_jogos[vl_distancia] += 1

        # printa o resultado:
        output: str = f"\n\t  ? DISTANTE     PERC%     #TOTAL\n"
        for key, value in enumerate(self.distancias_jogos):
            percent: float = round((value / qtd_jogos) * 1000) / 10
            self.distancias_percentos[key] = percent
            output += f"\t {formatd(key,2)} distante:  {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Distancias Resultantes: {output}")

        # efetua analise diferencial dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise TOTAL de distancia dos  "
                     f"{formatf(qtd_concursos)}  concursos da loteria.")

        # calcula a distancia de cada sorteio dos concursos:
        self.distancias_concursos = self.new_list_int(qtd_items)
        for concurso in concursos:
            vl_distancia: int = self.calc_distancia(concurso.bolas)
            self.distancias_concursos[vl_distancia] += 1

        # printa o resultado:
        output: str = f"\n\t  ? DISTANTE     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(self.distancias_concursos):
            percent: float = round((value / qtd_concursos) * 100000) / 1000
            dif: float = percent - self.distancias_percentos[key]
            output += f"\t {formatd(key,2)} distante:  {formatf(percent,'6.2')}% ... " \
                      f"{formatf(dif,'6.2')}%     #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Distancias Resultantes: {output}")

        # efetua analise comparativa dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise COMPARATIVA de distancia dos  "
                     f"{qtd_concursos:,}  concursos da loteria.")

        # contabiliza a distancia de cada sorteio dos concursos para exibicao em lista sequencial:
        output: str = f"\n\t CONCURSO   DISTANCIA         JOGOS%    #TOTAL CONCURSOS\n"
        for concurso in concursos:
            vl_distancia = self.calc_distancia(concurso.bolas)
            percent = self.distancias_percentos[vl_distancia]
            total = self.distancias_concursos[vl_distancia]
            output += f"\t    {formatd(concurso.id_concurso,5)}         {formatd(vl_distancia,3)}"\
                      f"  ...  {formatf(percent,'7.3')}%    #{formatd(total)}\n"

        # printa o resultado:
        logger.debug(f"{nmlot}: COMPARATIVA das Distancias Resultantes: {output}")

        # efetua analise evolutiva de todos os concursos de maneira progressiva:
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de distancia dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # calcula distancias dos extremos de cada evolucao de concurso:
        concursos_passados: list[Concurso] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        list6_distancias: list[int] = []
        for concurso_atual in payload.concursos:
            # zera os contadores de cada distancia:
            distancias_passadas: list[int] = self.new_list_int(qtd_items)

            # calcula a distancia nos concursos passados ate o concurso anterior:
            for concurso_passado in concursos_passados:
                vl_distancia_passada = self.calc_distancia(concurso_passado.bolas)
                distancias_passadas[vl_distancia_passada] += 1

            # calcula a distancia do concurso atual para comparar a evolucao:
            vl_distancia_atual = self.calc_distancia(concurso_atual.bolas)
            list6_distancias.append(vl_distancia_atual)
            # soh mantem as ultimas 6 distancias:
            while len(list6_distancias) > 6:
                del list6_distancias[0]

            # printa o resultado:
            output: str = f"\n\t  ? DISTANTE     PERC%       %DIF%  " \
                          f"----->  CONCURSO Nr {concurso_atual.id_concurso} :  " \
                          f"Ultimas Distancias == { list(reversed(list6_distancias))}\n"
            for key, value in enumerate(distancias_passadas):
                percent: float = round((value / qtd_concursos_passados) * 1000) \
                                 / 10
                dif: float = percent - self.distancias_percentos[key]
                output += f"\t {formatd(key,2)} distante:  {formatf(percent,'6.2')}% ... " \
                          f"{formatf(dif,'6.2')}%\n"
            logger.debug(f"{nmlot}: Distancias Resultantes da EVOLUTIVA: {output}")

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        self.set_options(parms)

    def evaluate(self, pick) -> float:
        # probabilidade de acerto depende da distancia entre as dezenas:
        vl_distancia: int = self.calc_distancia(pick)
        percent: float = self.distancias_percentos[vl_distancia]

        # ignora valores muito baixos de probabilidade:
        if percent < 2:
            return 0
        else:
            return 1 + (percent / 100)

# ----------------------------------------------------------------------------
