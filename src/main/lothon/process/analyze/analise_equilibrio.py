"""
   Package lothon.process
   Module  analise_equilibrio.py

"""

__all__ = [
    'AnaliseEquilibrio'
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
from lothon import domain
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

class AnaliseEquilibrio(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('paridades_jogos', 'paridades_percentos', 'conjuntos_paridades',
                 'paridades_concursos')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Equilibrio das Dezenas")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.paridades_jogos: Optional[list[int]] = None
        self.paridades_percentos: Optional[list[float]] = None
        self.conjuntos_paridades: Optional[list[tuple[int, ...]]] = None
        self.paridades_concursos: Optional[list[int]] = None

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def count_pares(cls, bolas: tuple[int, ...]) -> int:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return 0

        qtd_pares: int = 0
        for bola in bolas:
            if (bola % 2) == 0:
                qtd_pares += 1

        return qtd_pares

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.paridades_jogos = None
        self.paridades_percentos = None
        self.conjuntos_paridades = None
        self.paridades_concursos = None

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1
        # elif payload.qtd_bolas > 26:  # maximo de 26 dezenas, com 10 milhoes de combinacoes:
        #     nmlot: str = payload.nome_loteria
        #     logger.info(f"{nmlot}: O processo '{self.id_process.upper()}' nao pode ser executado "
        #                 f"com loterias que possuem mais de 26 dezenas. PROCESSO ABORTADO!")
        #     return 0
        else:
            _startWatch = startwatch()

        # o numero de sorteios realizados pode dobrar se for instancia de ConcursoDuplo:
        nmlot: str = payload.nome_loteria
        concursos: list[Concurso | ConcursoDuplo] = payload.concursos
        qtd_concursos: int = len(concursos)
        eh_duplo: bool = isinstance(concursos[0], ConcursoDuplo)
        qtd_items: int = payload.qtd_bolas

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug(f"{nmlot}: Executando analise de paridade basica dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # zera os contadores de cada paridade:
        self.paridades_jogos = self.new_list_int(qtd_items)
        self.paridades_percentos = self.new_list_float(qtd_items)

        # contabiliza pares (e impares) de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            qtd_pares: int = self.count_pares(jogo)
            self.paridades_jogos[qtd_pares] += 1

        # printa o resultado:
        output: str = f"\n\t  ? PARES     PERC%     #TOTAL\n"
        for key, value in enumerate(self.paridades_jogos):
            percent: float = round((value / qtd_jogos) * 1000) / 10
            self.paridades_percentos[key] = percent
            output += f"\t {formatd(key,2)} pares:  {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Paridades Resultantes: {output}")

        # efetua analise diferencial dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise TOTAL de paridade dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # contabiliza pares (e impares) de cada sorteio dos concursos:
        self.paridades_concursos = self.new_list_int(qtd_items)
        for concurso in concursos:
            qtd_pares: int = self.count_pares(concurso.bolas)
            self.paridades_concursos[qtd_pares] += 1
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                qtd_pares = self.count_pares(concurso.bolas2)
                self.paridades_concursos[qtd_pares] += 1

        # printa o resultado:
        output: str = f"\n\t  ? PARES     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(self.paridades_concursos):
            percent: float = round((value / qtd_concursos) * 100000) / 1000
            dif: float = percent - self.paridades_percentos[key]
            output += f"\t {formatd(key,2)} pares:  {formatf(percent,'6.2')}% ... " \
                      f"{formatf(dif,'6.2')}%     #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Paridades Resultantes: {output}")

        # carrega os conjuntos de pares da loteria:
        self.conjuntos_paridades = domain.load_pares(payload.id_loteria)
        if self.conjuntos_paridades is None or len(self.conjuntos_paridades) == 0:
            logger.warning(f"{nmlot}: Nao foi possivel carregar o arquivo com conjuntos de pares. "
                           f"Processo abortado!")
            return -1
        else:
            tot_sets: int = len(self.conjuntos_paridades)
            logger.info(f"{nmlot}: Foram carregados  #{formatd(tot_sets)}  conjuntos de pares.")

        # transversa os conjuntos de pares com os concursos da loteria:
        logger.debug(f"{nmlot}: Executando analise transversal dos  #{formatd(tot_sets)}  "
                     f"conjuntos de pares com os  {formatd(qtd_concursos)}  concursos da loteria.")

        # contabiliza os pares de cada combinacao de jogo:
        cont: int = 0
        for set_pares in self.conjuntos_paridades:
            # a cada mil conjuntos processados, informa "sinal de vida" do processamento:
            cont += 1
            if cont % 1000 == 0:
                logger.warning(f"{nmlot}: Processando conjunto #{formatd(cont)} do "
                               f"total #{formatd(tot_sets)} de conjuntos de pares.")

            # contabiliza pares (e impares) de cada sorteio dos concursos:
            self.paridades_concursos = self.new_list_int(qtd_items)
            for concurso in concursos:
                # uma dezena "par" eh aquela presente no conjunto set_pares:
                qtd_pares: int = 0
                for bola in concurso.bolas:
                    if bola in set_pares:
                        qtd_pares += 1
                self.paridades_concursos[qtd_pares] += 1
                # verifica se o concurso eh duplo (dois sorteios):
                if eh_duplo:
                    qtd_pares = 0
                    for bola in concurso.bolas2:
                        if bola in set_pares:
                            qtd_pares += 1
                    self.paridades_concursos[qtd_pares] += 1

            # calcula as estatisticas para o conjunto de pares:
            ordenada: list[int] = sorted(self.paridades_concursos)
            total: int = sum(ordenada)
            topo1: int = ordenada[-1]
            topo3: int = sum(ordenada[-3:])

            percent1: int = round(topo1 / total * 100)
            percent3: int = round(topo3 / total * 100)
            if percent3 >= 80:
                logger.error(f"{nmlot}: Atingiu {percent3}% no conjunto de pares {set_pares}.")
            elif percent1 >= 35:
                logger.warning(f"{nmlot}: Topo Max {percent1}% no conjunto de pares {set_pares}.")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        pass

    def evaluate(self, payload) -> float:
        pass

# ----------------------------------------------------------------------------
