"""
   Package lothon.process
   Module  analise_somatoria.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
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

class AnaliseSomatoria(AbstractProcess):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_process', '_options'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Somatoria das Dezenas")

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

        # o numero de sorteios realizados pode dobrar se for instancia de ConcursoDuplo:
        concursos: list[Concurso | ConcursoDuplo] = payload.concursos
        qtd_concursos: int = len(concursos)
        eh_duplo: bool = (concursos[0] is ConcursoDuplo)
        if eh_duplo:
            fator_sorteios: int = 2
        else:
            fator_sorteios: int = 1
        qtd_sorteios: int = qtd_concursos * fator_sorteios

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug("%s: Executando analise de somatoria dos  %d  jogos combinados da loteria.",
                     payload.nome_loteria, qtd_jogos)

        # zera os contadores de cada somatoria:
        maior_soma = sum(range(payload.qtd_bolas - payload.qtd_bolas_sorteio + 1,
                               payload.qtd_bolas + 1)) + 1  # soma 1 para nao usar zero-index.
        somatoria_jogos: list[int] = self.new_list_int(maior_soma)

        # contabiliza a somatoria de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            soma_dezenas = self.soma_dezenas(jogo)
            somatoria_jogos[soma_dezenas] += 1

        # printa o resultado:
        output: str = f"\n\t   ? SOMADO     PERC%     #TOTAL\n"
        for key, value in enumerate(somatoria_jogos):
            percent: float = round((value / qtd_jogos) * 100000) / 1000
            output += f"\t {key:0>3} somado:  {percent:0>6.3f}% ... #{value:,}\n"
        logger.debug("Somatorias Resultantes: %s", output)

        #
        logger.debug("%s: Executando analise TOTAL de somatória dos  %d  concursos da loteria.",
                     payload.nome_loteria, qtd_concursos)

        # contabiliza a somatoria de cada sorteio dos concursos:
        somatoria_cocursos: list[int] = self.new_list_int(maior_soma)
        for concurso in concursos:
            soma_dezenas = self.soma_dezenas(concurso.bolas)
            somatoria_cocursos[soma_dezenas] += 1

            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                soma_dezenas = self.soma_dezenas(concurso.bolas2)
                somatoria_cocursos[soma_dezenas] += 1

        # printa o resultado:
        output: str = f"\n\t   ? SOMADO     PERC%     #TOTAL\n"
        for key, value in enumerate(somatoria_cocursos):
            percent: float = round((value / qtd_sorteios) * 100000) / 1000
            output += f"\t {key:0>3} somado:  {percent:0>6.3f}% ... #{value:,}\n"
        logger.debug("Somatorias Resultantes: %s", output)

        return 0

# ----------------------------------------------------------------------------
