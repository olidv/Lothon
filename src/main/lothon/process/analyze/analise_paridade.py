"""
   Package lothon.process
   Module  analise_paridade.py

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
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

#
def count_pares(bolas: tuple[int, ...]) -> int:
    qtd_pares: int = 0
    for bola in bolas:
        if (bola % 2) == 0:
            qtd_pares += 1

    return qtd_pares


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
        super().__init__("Analise de Paridade das Dezenas")

    # --- METODOS ------------------------------------------------------------

    def execute(self, payload: Loteria) -> int:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug("%s: Executando analise de paridade dos  %d  jogos combinados da loteria.",
                     payload.nome_loteria, qtd_jogos)

        # zera os contadores de cada paridade:
        paridades_jogos: dict[int, int] = self.new_dict_int(payload.qtd_bolas_sorteio)
        percentos_jogos: dict[int, float] = self.new_dict_float(payload.qtd_bolas_sorteio)

        # contabiliza pares (e impares) de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            qtd_pares = count_pares(jogo)
            paridades_jogos[qtd_pares] += 1

        # printa o resultado:
        output: str = f"\n\t ? PARES  PERC%     #TOTAL\n"
        for key, value in paridades_jogos.items():
            percent: float = round((value / qtd_jogos) * 1000) / 10
            percentos_jogos[key] = percent
            output += f"\t {key} pares: {percent:0>4.1f}% ... #{value:,}\n"
        logger.debug("Paridade Resultante: %s \n", output)

        qtd_concursos: int = len(payload.concursos)
        logger.debug("%s: Executando analise EVOLUTIVA de paridade dos  %d  concursos da loteria.",
                     payload.nome_loteria, qtd_concursos)

        # contabiliza pares (e impares) de cada evolucao de concurso:
        concursos_passados: list[Concurso | ConcursoDuplo] = []
        qtd_concursos = 1  # evita divisao por zero
        list6_paridades: list[int] = []
        for concurso_atual in payload.concursos:
            # zera os contadores de cada paridade:
            paridades_passados: dict[int, int] = self.new_dict_int(payload.qtd_bolas_sorteio)

            # calcula a paridade dos concursos passados até o concurso anterior:
            for concurso_passado in concursos_passados:
                qtd_pares = count_pares(concurso_passado.bolas)
                paridades_passados[qtd_pares] += 1
                # verifica se o concurso eh duplo (dois sorteios):
                if concurso_passado is ConcursoDuplo:
                    qtd_pares = count_pares(concurso_passado.bolas2)
                    paridades_passados[qtd_pares] += 1

            # calcula a paridade do concurso atual para comparar a evolucao:
            qtd_pares_atual = count_pares(concurso_atual.bolas)
            list6_paridades.append(qtd_pares_atual)
            str_pares_atual = str(qtd_pares_atual)
            # verifica se o concurso eh duplo (dois sorteios):
            if concurso_atual is ConcursoDuplo:
                qtd_pares2_atual = count_pares(concurso_atual.bolas2)
                list6_paridades.append(qtd_pares2_atual)
                str_pares_atual += '/' + str(qtd_pares2_atual)

            # printa o resultado:
            output: str = f"\n\t ? PARES  PERC%      %DIF%  " \
                          f"----->  CONCURSO Nº {concurso_atual.id_concurso} :  " \
                          f"Últimos pares == { list(reversed(list6_paridades))}\n"
            for key, value in paridades_passados.items():
                percent: float = round((value / qtd_concursos) * 1000) / 10
                dif: float = percent - percentos_jogos[key]
                output += f"\t {key} pares: {percent:0>4.1f}% ... {dif:5.1f}%\n"
            logger.debug("Paridade Resultante: %s", output)

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos = len(concursos_passados)
            while len(list6_paridades) > 6:
                del list6_paridades[0]

        return 0

# ----------------------------------------------------------------------------
