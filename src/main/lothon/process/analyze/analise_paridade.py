"""
   Package lothon.process
   Module  analise_paridade.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import datetime
import time
import math
import itertools as itt
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain import Loteria, Concurso, ConcursoDuplo
from lothon.process.abstract_process import AbstractProcess


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseParidade(AbstractProcess):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_process', '_options'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Análise de Paridade das Dezenas")

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def count_pares(bolas: tuple[int, ...]) -> int:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return 0

        qtd_pares: int = 0
        for bola in bolas:
            if (bola % 2) == 0:
                qtd_pares += 1

        return qtd_pares

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1
        else:
            _startTime: float = time.time()

        # o numero de sorteios realizados pode dobrar se for instancia de ConcursoDuplo:
        concursos: list[Concurso | ConcursoDuplo] = payload.concursos
        qtd_concursos: int = len(concursos)
        eh_duplo: bool = (concursos[0] is ConcursoDuplo)
        if eh_duplo:
            fator_sorteios: int = 2
        else:
            fator_sorteios: int = 1
        # qtd_sorteios: int = qtd_concursos * fator_sorteios
        qtd_items: int = payload.qtd_bolas_sorteio

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug(f"{payload.nome_loteria}: Executando análise de paridade dos  "
                     f"{qtd_jogos:,}  jogos combinados da loteria.")

        # zera os contadores de cada paridade:
        paridades_jogos: list[int] = self.new_list_int(qtd_items)
        percentos_jogos: list[float] = self.new_list_float(qtd_items)

        # contabiliza pares (e impares) de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            qtd_pares = self.count_pares(jogo)
            paridades_jogos[qtd_pares] += 1

        # printa o resultado:
        output: str = f"\n\t  ? PARES    PERC%     #TOTAL\n"
        for key, value in enumerate(paridades_jogos):
            percent: float = round((value / qtd_jogos) * 1000) / 10
            percentos_jogos[key] = percent
            output += f"\t {key:0>2} pares:  {percent:0>5.1f}% ... #{value:,}\n"
        logger.debug(f"Paridades Resultantes: {output}")

        #
        logger.debug(f"{payload.nome_loteria}: Executando análise EVOLUTIVA de paridade dos  "
                     f"{qtd_concursos:,}  concursos da loteria.")

        # contabiliza pares (e impares) de cada evolucao de concurso:
        concursos_passados: list[Concurso | ConcursoDuplo] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        list6_paridades: list[int] = []
        concurso_atual: Concurso | ConcursoDuplo
        for concurso_atual in payload.concursos:
            # zera os contadores de cada paridade:
            paridades_passados: list[int] = self.new_list_int(qtd_items)

            # calcula a paridade dos concursos passados até o concurso anterior:
            for concurso_passado in concursos_passados:
                qtd_pares_passado = self.count_pares(concurso_passado.bolas)
                paridades_passados[qtd_pares_passado] += 1
                # verifica se o concurso eh duplo (dois sorteios):
                if eh_duplo:
                    qtd_pares_passado = self.count_pares(concurso_passado.bolas2)
                    paridades_passados[qtd_pares_passado] += 1

            # calcula a paridade do concurso atual para comparar a evolucao:
            qtd_pares_atual = self.count_pares(concurso_atual.bolas)
            str_pares_atual = str(qtd_pares_atual)
            list6_paridades.append(qtd_pares_atual)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                qtd_pares2_atual = self.count_pares(concurso_atual.bolas2)
                str_pares_atual += '/' + str(qtd_pares2_atual)
                list6_paridades.append(qtd_pares2_atual)
            # soh mantem os ultimos 6 pares:
            while len(list6_paridades) > 6:
                del list6_paridades[0]

            # printa o resultado:
            output: str = f"\n\t  ? PARES    PERC%      %DIF%  " \
                          f"----->  CONCURSO Nº {concurso_atual.id_concurso} :  " \
                          f"Últimos Pares == { list(reversed(list6_paridades))}\n"
            for key, value in enumerate(paridades_passados):
                percent: float = round((value / (qtd_concursos_passados*fator_sorteios)) * 1000) \
                                 / 10
                dif: float = percent - percentos_jogos[key]
                output += f"\t {key:0>2} pares:  {percent:0>5.1f}% ... {dif:5.1f}%\n"
            logger.debug(f"Paridades Resultantes da EVOLUTIVA: {output}")

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        _totalTime: int = round(time.time() - _startTime)
        tempo_total: str = str(datetime.timedelta(seconds=_totalTime))
        logger.info(f"Tempo para executar {self.id_process.upper()}: {tempo_total} segundos.")
        return 0

# ----------------------------------------------------------------------------
