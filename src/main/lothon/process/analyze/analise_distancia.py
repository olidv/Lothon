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

class AnaliseDistancia(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Distancia nos Concursos")

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def calc_distancia(bolas: tuple[int, ...]) -> int:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return 0

        # calcula a distancia entre a menor e a maior bola:
        return max(bolas) - min(bolas)

    # --- PROCESSAMENTO ------------------------------------------------------

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
        eh_duplo: bool = (concursos[0] is ConcursoDuplo)
        if eh_duplo:
            fator_sorteios: int = 2
        else:
            fator_sorteios: int = 1
        qtd_sorteios: int = qtd_concursos * fator_sorteios
        qtd_items: int = payload.qtd_bolas

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug(f"{nmlot}: Executando analise de distancia dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # zera os contadores de cada distancia:
        distancias_jogos: list[int] = self.new_list_int(qtd_items)
        percentos_jogos: list[float] = self.new_list_float(qtd_items)

        # calcula a distancia de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            vl_distancia = self.calc_distancia(jogo)
            distancias_jogos[vl_distancia] += 1

        # printa o resultado:
        output: str = f"\n\t  ? DISTANTE     PERC%     #TOTAL\n"
        for key, value in enumerate(distancias_jogos):
            percent: float = round((value / qtd_jogos) * 1000) / 10
            percentos_jogos[key] = percent
            output += f"\t {formatd(key,2)} distante:  {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Distancias Resultantes: {output}")

        #
        logger.debug(f"{nmlot}: Executando analise TOTAL de distancia dos  "
                     f"{formatf(qtd_concursos)}  concursos da loteria.")

        # calcula a distancia de cada sorteio dos concursos:
        distancias_concursos: list[int] = self.new_list_int(qtd_items)
        for concurso in concursos:
            vl_distancia: int = self.calc_distancia(concurso.bolas)
            distancias_concursos[vl_distancia] += 1
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                vl_distancia: int = self.calc_distancia(concurso.bolas2)
                distancias_concursos[vl_distancia] += 1

        # printa o resultado:
        output: str = f"\n\t  ? DISTANTE     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(distancias_concursos):
            percent: float = round((value / qtd_sorteios) * 100000) / 1000
            dif: float = percent - percentos_jogos[key]
            output += f"\t {formatd(key,2)} distante:  {formatf(percent,'6.2')}% ... " \
                      f"{formatf(dif,'6.2')}%     #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Distancias Resultantes: {output}")

        #
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de distancia dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # calcula distancias dos extremos de cada evolucao de concurso:
        concursos_passados: list[Concurso | ConcursoDuplo] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        list6_distancias: list[int] = []
        concurso_atual: Concurso | ConcursoDuplo
        for concurso_atual in payload.concursos:
            # zera os contadores de cada distancia:
            distancias_passadas: list[int] = self.new_list_int(qtd_items)

            # calcula a distancia nos concursos passados ate o concurso anterior:
            for concurso_passado in concursos_passados:
                vl_distancia_passada = self.calc_distancia(concurso_passado.bolas)
                distancias_passadas[vl_distancia_passada] += 1
                # verifica se o concurso eh duplo (dois sorteios):
                if eh_duplo:
                    vl_distancia_passada = self.calc_distancia(concurso_passado.bolas2)
                    distancias_passadas[vl_distancia_passada] += 1

            # calcula a distancia do concurso atual para comparar a evolucao:
            vl_distancia_atual = self.calc_distancia(concurso_atual.bolas)
            list6_distancias.append(vl_distancia_atual)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                vl_distancia_atual = self.calc_distancia(concurso_atual.bolas2)
                list6_distancias.append(vl_distancia_atual)
            # soh mantem as ultimas 6 distancias:
            while len(list6_distancias) > 6:
                del list6_distancias[0]

            # printa o resultado:
            output: str = f"\n\t  ? DISTANTE     PERC%       %DIF%  " \
                          f"----->  CONCURSO Nr {concurso_atual.id_concurso} :  " \
                          f"Ultimas Distancias == { list(reversed(list6_distancias))}\n"
            for key, value in enumerate(distancias_passadas):
                percent: float = round((value / (qtd_concursos_passados*fator_sorteios)) * 1000) \
                                 / 10
                dif: float = percent - percentos_jogos[key]
                output += f"\t {formatd(key,2)} distante:  {formatf(percent,'6.2')}% ... " \
                          f"{formatf(dif,'6.2')}%\n"
            logger.debug(f"{nmlot}: Distancias Resultantes da EVOLUTIVA: {output}")

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        # salva os dados resultantes da analise para utilizacao em simulacoes e geracoes de boloes:
        payload.statis["distancias_jogos"] = distancias_jogos
        payload.statis["distancias_percentos"] = percentos_jogos
        payload.statis["distancias_concursos"] = distancias_concursos

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        pass

    def evaluate(self, payload) -> float:
        pass

# ----------------------------------------------------------------------------
