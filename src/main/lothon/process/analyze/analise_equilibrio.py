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
    __slots__ = ('paridades_jogos', 'paridades_percentos', 'paridades_concursos',
                 'conjuntos_paridades', 'paridades_conjuntos')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Equilibrio das Dezenas")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.paridades_jogos: Optional[list[int]] = None
        self.paridades_percentos: Optional[list[float]] = None
        self.paridades_concursos: Optional[list[int]] = None
        self.conjuntos_paridades: Optional[list[tuple[int, ...]]] = None
        self.paridades_conjuntos: Optional[list[int]] = None

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

    @classmethod
    def count_set_pares(cls, bolas: tuple[int, ...], set_pares: tuple[int, ...]) -> int:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return 0

        qtd_pares: int = 0
        for bola in bolas:
            if bola in set_pares:
                qtd_pares += 1

        return qtd_pares

    @classmethod
    def to_dict_sorted(cls, lista: list) -> dict:
        # valida os parametros:
        if lista is None or len(lista) == 0:
            return {}

        # primeiro transforma a lista em dicionario:
        dicio: dict = {}
        for k, v in enumerate(lista):
            dicio[k] = v

        # depois ordena o dicionario pelos valores, do maior (topo) decrescendo para o menor:
        return {k: v for k, v in sorted(dicio.items(), key=lambda item: item[1], reverse=True)}

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.paridades_jogos = None
        self.paridades_percentos = None
        self.paridades_concursos = None
        self.conjuntos_paridades = None
        self.paridades_conjuntos = None

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
        eh_duplo: bool = isinstance(concursos[0], ConcursoDuplo)
        qtd_items: int = payload.qtd_bolas_sorteio

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
        logger.debug(f"{nmlot}: Executando analise de paridade normal dos  "
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
        tot_sets: int = 0 if self.conjuntos_paridades is None else len(self.conjuntos_paridades)
        if tot_sets == 0:
            logger.warning(f"{nmlot}: Nao foi possivel carregar o arquivo com conjuntos de pares. "
                           f"Processo abortado!")
            return -1
        else:
            logger.info(f"{nmlot}: Foram carregados  #{formatd(tot_sets)}  conjuntos de pares.")

        # transversa os conjuntos de pares com os concursos da loteria:
        logger.debug(f"{nmlot}: Executando analises transversais dos  #{formatd(tot_sets)}  "
                     f"conjuntos de pares com os  {formatd(qtd_concursos)}  concursos da loteria.")

        # ANALISE CONCURSOS -> PARIDADES: formata matriz para apresentacao dos dados coletados:
        output: str = f"\n\t#CONCURSO  PARES:"
        for p in range(0, qtd_items + 1):
            output += f"     {p:0>2}"
        output += "\n"

        # contabiliza pares (e impares) de cada sorteio dos concursos:
        for concurso in concursos:
            # contabiliza os pares de cada combinacao de jogo no conjunto de pares:
            self.paridades_conjuntos = self.new_list_int(qtd_items)
            for set_pares in self.conjuntos_paridades:
                # uma dezena "par" eh aquela presente no conjunto set_pares:
                qtd_pares: int = self.count_set_pares(concurso.bolas, set_pares)
                self.paridades_conjuntos[qtd_pares] += 1
                # verifica se o concurso eh duplo (dois sorteios):
                if eh_duplo:
                    qtd_pares = self.count_set_pares(concurso.bolas2, set_pares)
                    self.paridades_conjuntos[qtd_pares] += 1

            # formata o resultado do conjunto corrente:
            output += f"\t    {formatd(concurso.id_concurso,5)}        "
            total: int = sum(self.paridades_conjuntos)
            for value in self.paridades_conjuntos:
                output += f"  {formatf(value / total * 100,'4.1')}%"
            output += "\n"
        logger.debug(f"{nmlot}: Paridades dos concursos para todos os conjuntos de pares: {output}")

        # ANALISE PARIDADES -> CONCURSOS: primeiro identifica topos de cada conjunto de paridades:
        paridades_topo2: list[tuple[int, ...]] = []
        paridades_topo3: list[tuple[int, ...]] = []
        paridades_topo4: list[tuple[int, ...]] = []

        # eh preciso analisar cada concurso com os conjuntos de pares, para identificar os topos:
        for set_pares in self.conjuntos_paridades:
            # contabiliza os pares de cada concurso no conjunto de pares:
            self.paridades_conjuntos = self.new_list_int(qtd_items)
            for concurso in concursos:
                # uma dezena "par" eh aquela presente no conjunto set_pares:
                qtd_pares: int = self.count_set_pares(concurso.bolas, set_pares)
                self.paridades_conjuntos[qtd_pares] += 1
                # verifica se o concurso eh duplo (dois sorteios):
                if eh_duplo:
                    qtd_pares = self.count_set_pares(concurso.bolas2, set_pares)
                    self.paridades_conjuntos[qtd_pares] += 1

            # ordena do maior (topo) numero de paridades para o menor:
            paridades_dict: dict = self.to_dict_sorted(self.paridades_conjuntos)
            # percorre os itens do dicionario e adiciona em cada lista de topos correspondente:
            cont: int = 0
            topo2: tuple[int, ...] = ()
            topo3: tuple[int, ...] = ()
            topo4: tuple[int, ...] = ()
            for k, v in paridades_dict.items():
                cont += 1
                if cont <= 2:
                    topo2 += (k,)
                if cont <= 3:
                    topo3 += (k,)
                if cont <= 4:
                    topo4 += (k,)

            # a adicao segue a mesma ordem dos conjuntos de pares em self.conjuntos_paridades
            paridades_topo2.append(topo2)
            paridades_topo3.append(topo3)
            paridades_topo4.append(topo4)

        # depois, contabiliza novamente os pares de cada concurso no conjunto de pares:
        output: str = f"\n\t#CONCURSO  TOPOS:    02        03        04\n"
        soma_topo2: float = 0
        soma_topo3: float = 0
        soma_topo4: float = 0
        for concurso in concursos:
            # contabiliza os conjuntos de pares onde o concurso fica nos topos (2, 3 ou 4):
            count_topo2: int = 0
            count_topo3: int = 0
            count_topo4: int = 0
            self.paridades_conjuntos = self.new_list_int(qtd_items)
            for i, set_pares in enumerate(self.conjuntos_paridades):
                # uma dezena "par" eh aquela presente no conjunto set_pares:
                qtd_pares: int = self.count_set_pares(concurso.bolas, set_pares)
                if qtd_pares in paridades_topo2[i]:
                    count_topo2 += 1
                if qtd_pares in paridades_topo3[i]:
                    count_topo3 += 1
                if qtd_pares in paridades_topo4[i]:
                    count_topo4 += 1
                # verifica se o concurso eh duplo (dois sorteios):
                if eh_duplo:
                    qtd_pares = self.count_set_pares(concurso.bolas2, set_pares)
                    if qtd_pares in paridades_topo2[i]:
                        count_topo2 += 1
                    if qtd_pares in paridades_topo3[i]:
                        count_topo3 += 1
                    if qtd_pares in paridades_topo4[i]:
                        count_topo4 += 1

            # formata o resultado do concurso corrente:
            percent_topo2: float = count_topo2 / tot_sets * 100
            percent_topo3: float = count_topo3 / tot_sets * 100
            percent_topo4: float = count_topo4 / tot_sets * 100
            output += f"\t    {formatd(concurso.id_concurso,5)}       " \
                      f" {formatf(percent_topo2,'5.2')}%   " \
                      f" {formatf(percent_topo3,'5.2')}%   " \
                      f" {formatf(percent_topo4,'5.2')}%\n"

            # acumula o percentual para calcular a media ao final:
            soma_topo2 += percent_topo2
            soma_topo3 += percent_topo3
            soma_topo4 += percent_topo4

        output += f"--------------------------------------------------\n" \
                  f"\t        MEDIA:  "  \
                  f" {formatf(soma_topo2 / qtd_concursos,'5.2')}%   " \
                  f" {formatf(soma_topo3 / qtd_concursos,'5.2')}%   " \
                  f" {formatf(soma_topo4 / qtd_concursos,'5.2')}%\n"
        logger.debug(f"{nmlot}: Incidencia em Topos de Paridades para todos os concursos: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        self.set_options(parms)

    def evaluate(self, payload) -> float:
        return 1.1  # valor temporario

# ----------------------------------------------------------------------------
