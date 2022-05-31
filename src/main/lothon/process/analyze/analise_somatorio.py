"""
   Package lothon.process
   Module  analise_somatorio.py

"""

__all__ = [
    'AnaliseSomatorio'
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

class AnaliseSomatorio(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('somatorios_jogos', 'somatorios_percentos', 'somatorios_concursos')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Somatorio das Dezenas")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.somatorios_jogos: Optional[list[int]] = None
        self.somatorios_percentos: Optional[list[float]] = None
        self.somatorios_concursos: Optional[list[int]] = None

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def soma_dezenas(cls, bolas: tuple[int, ...]) -> int:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return 0

        soma: int = sum(bolas)
        return soma

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.somatorios_jogos = None
        self.somatorios_percentos = None
        self.somatorios_concursos = None

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
        qtd_items: int = sum(range(payload.qtd_bolas - payload.qtd_bolas_sorteio + 1,
                                   payload.qtd_bolas + 1)) + 1  # soma 1 para nao usar zero-index.

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug(f"{nmlot}: Executando analise de somatorio dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # zera os contadores de cada somatorio:
        self.somatorios_jogos = self.new_list_int(qtd_items)
        self.somatorios_percentos = self.new_list_float(qtd_items)

        # contabiliza a somatorio de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            soma_dezenas = self.soma_dezenas(jogo)
            self.somatorios_jogos[soma_dezenas] += 1

        # printa o resultado:
        output: str = f"\n\t   ? SOMADO      PERC%     #TOTAL\n"
        for key, value in enumerate(self.somatorios_jogos):
            percent: float = round((value / qtd_jogos) * 100000) / 1000
            self.somatorios_percentos[key] = percent
            output += f"\t {formatd(key,3)} somado:  {formatf(percent,'7.3')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Somatorios Resultantes: {output}")

        #
        logger.debug(f"{nmlot}: Executando analise TOTAL de somatorio dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # contabiliza a somatorio de cada sorteio dos concursos:
        self.somatorios_concursos = self.new_list_int(qtd_items)
        for concurso in concursos:
            soma_dezenas = self.soma_dezenas(concurso.bolas)
            self.somatorios_concursos[soma_dezenas] += 1

            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                soma_dezenas = self.soma_dezenas(concurso.bolas2)
                self.somatorios_concursos[soma_dezenas] += 1

        # printa o resultado:
        output: str = f"\n\t   ? SOMADO      PERC%     #TOTAL\n"
        for key, value in enumerate(self.somatorios_concursos):
            percent: float = round((value / qtd_sorteios) * 100000) / 1000
            output += f"\t {formatd(key,3)} somado:  {formatf(percent,'7.3')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Somatorios Resultantes: {output}")

        #
        logger.debug(f"{nmlot}: Executando analise COMPARATIVA de somatorio dos  "
                     f"{qtd_concursos:,}  concursos da loteria.")

        # contabiliza a somatorio de cada sorteio dos concursos para exibicao em lista sequencial:
        output: str = f"\n\t #CONCURSO   SOMA          PERC%    #TOTAL\n"
        for concurso in concursos:
            soma_dezenas = self.soma_dezenas(concurso.bolas)
            percent = self.somatorios_percentos[soma_dezenas]
            total = self.somatorios_concursos[soma_dezenas]
            output += f"\t     {formatd(concurso.id_concurso,5)}    {formatd(soma_dezenas,3)}  " \
                      f"...  {formatf(percent,'7.3')}%    #{formatd(total)}\n"

            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                soma_dezenas = self.soma_dezenas(concurso.bolas2)
                percent = self.somatorios_percentos[soma_dezenas]
                total = self.somatorios_concursos[soma_dezenas]
                output += f"\t                          {formatd(soma_dezenas,3)}  ...  " \
                          f"{formatf(percent,'7.3')}%   #{formatd(total)}\n"
        # printa o resultado:
        logger.debug(f"{nmlot}: COMPARATIVA dos Somatorios Resultantes: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        pass

    def evaluate(self, payload) -> float:
        pass

# ----------------------------------------------------------------------------
