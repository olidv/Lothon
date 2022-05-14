"""
   Package lothon.process
   Module  analise_sequencia.py

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
def count_sequencias(bolas: tuple[int, ...]) -> int:
    # valida os parametros:
    if bolas is None or len(bolas) == 0:
        return 0

    # eh preciso ordenar a tupla para verificar se ha sequencia:
    bolas: tuple[int, ...] = tuple(sorted(bolas))

    qtd_sequencias: int = 0
    seq_anterior: int = -1
    for num in bolas:
        if num == seq_anterior:
            qtd_sequencias += 1
        seq_anterior = num + 1

    return qtd_sequencias


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseSequencia(AbstractProcess):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_process', '_options'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Sequência nos Concursos")

    # --- METODOS ------------------------------------------------------------

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1

        # o numero de sorteios realizados pode dobrar se for instancia de ConcursoDuplo:
        concursos: list[Concurso | ConcursoDuplo] = payload.concursos
        eh_duplo: bool = ([0] is ConcursoDuplo)
        print("eh duplo? ", eh_duplo)
        if eh_duplo:
            qtd_sorteios: int = 2 * len(concursos)
        else:
            qtd_sorteios: int = len(concursos)
        logger.debug("%s: Executando analise de sequencia nos  %d  sorteios da loteria.",
                     payload.nome_loteria, qtd_sorteios)

        # zera os contadores de cada repetencia:
        sequencias_sorteios: dict[int, int] = self.new_dict_int(payload.qtd_bolas_sorteio - 1)
        percentos_sequencia: dict[int, float] = self.new_dict_float(payload.qtd_bolas_sorteio - 1)

        # efetua varredura nos concursos para comparar as dezenas entre si e ver se ha sequencia:
        for concurso_atual in concursos:
            qt_sequencias = count_sequencias(concurso_atual.bolas)
            sequencias_sorteios[qt_sequencias] += 1

            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                # se for concurso duplo, precisa comparar as bolas do segundo sorteio:
                qt_sequencias = count_sequencias(concurso_atual.bolas2)
                sequencias_sorteios[qt_sequencias] += 1

        # printa o resultado:
        output: str = f"\n\t ? SEGUIDO   PERC%     #TOTAL\n"
        for key, value in sequencias_sorteios.items():
            percent: float = round((value / qtd_sorteios) * 1000) / 10
            percentos_sequencia[key] = percent
            output += f"\t {key} seguido:  {percent:0>4.1f}% ... #{value:,}\n"
        logger.debug("Sequencias em todos os sorteios: %s \n", output)
        return 0


        logger.debug("%s: Executando analise EVOLUTIVA de repetencia dos  %d  sorteios da loteria.",
                     payload.nome_loteria, qtd_sorteios)

        # contabiliza pares (e impares) de cada evolucao de concurso:
        concursos_passados: list[Concurso | ConcursoDuplo] = []
        qtd_sorteios = 1  # evita divisao por zero
        list6_paridades: list[int] = []
        for concurso_atual in payload.concursos:
            # zera os contadores de cada paridade:
            paridades_passados = new_dict_paridade(payload.qtd_bolas_sorteio)

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
                percent: float = round((value / qtd_sorteios) * 1000) / 10
                dif: float = percent - percentos_jogos[key]
                output += f"\t {key} pares: {percent:0>4.1f}% ... {dif:5.1f}%\n"
            logger.debug("Paridade Resultante: %s", output)

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_sorteios = len(concursos_passados)
            while len(list6_paridades) > 6:
                del list6_paridades[0]

        return 0

# ----------------------------------------------------------------------------
