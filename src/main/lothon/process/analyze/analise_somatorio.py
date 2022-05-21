"""
   Package lothon.process
   Module  analise_somatorio.py

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

class AnaliseSomatorio(AbstractProcess):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_process', '_options'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Análise de Somatório das Dezenas")

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def soma_dezenas(bolas: tuple[int, ...]) -> int:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return 0

        soma: int = sum(bolas)
        return soma

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
        qtd_sorteios: int = qtd_concursos * fator_sorteios
        qtd_items: int = sum(range(payload.qtd_bolas - payload.qtd_bolas_sorteio + 1,
                                   payload.qtd_bolas + 1)) + 1  # soma 1 para nao usar zero-index.

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug(f"{payload.nome_loteria}: Executando análise de somatório dos  "
                     f"{qtd_jogos:,}  jogos combinados da loteria.")

        # zera os contadores de cada somatorio:
        somatorio_jogos: list[int] = self.new_list_int(qtd_items)

        # contabiliza a somatorio de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            soma_dezenas = self.soma_dezenas(jogo)
            somatorio_jogos[soma_dezenas] += 1

        # printa o resultado:
        output: str = f"\n\t   ? SOMADO      PERC%     #TOTAL\n"
        for key, value in enumerate(somatorio_jogos):
            percent: float = round((value / qtd_jogos) * 100000) / 1000
            output += f"\t {key:0>3} somado:  {percent:0>7.3f}% ... #{value:,}\n"
        logger.debug(f"Somatorios Resultantes: {output}")

        #
        logger.debug(f"{payload.nome_loteria}: Executando análise TOTAL de somatório dos  "
                     f"{qtd_concursos:,}  concursos da loteria.")

        # contabiliza a somatorio de cada sorteio dos concursos:
        somatorio_cocursos: list[int] = self.new_list_int(qtd_items)
        for concurso in concursos:
            soma_dezenas = self.soma_dezenas(concurso.bolas)
            somatorio_cocursos[soma_dezenas] += 1

            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                soma_dezenas = self.soma_dezenas(concurso.bolas2)
                somatorio_cocursos[soma_dezenas] += 1

        # printa o resultado:
        output: str = f"\n\t   ? SOMADO      PERC%     #TOTAL\n"
        for key, value in enumerate(somatorio_cocursos):
            percent: float = round((value / qtd_sorteios) * 100000) / 1000
            output += f"\t {key:0>3} somado:  {percent:0>7.3f}% ... #{value:,}\n"
        logger.debug(f"Somatórios Resultantes: {output}")

        _totalTime: int = round(time.time() - _startTime)
        tempo_total: str = str(datetime.timedelta(seconds=_totalTime))
        logger.info(f"Tempo para executar {self.id_process.upper()}: {tempo_total} segundos.")
        return 0

# ----------------------------------------------------------------------------
