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
        qtd_concursos: int = len(concursos)
        eh_duplo: bool = (concursos[0] is ConcursoDuplo)
        if eh_duplo:
            fator_sorteios: int = 2
        else:
            fator_sorteios: int = 1

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug("%s: Executando analise de sequencia dos  %d  jogos combinados da loteria.",
                     payload.nome_loteria, qtd_jogos)

        # zera os contadores de cada sequencia:
        sequencias_jogos: dict[int, int] = self.new_dict_int(payload.qtd_bolas_sorteio)
        percentos_jogos: dict[int, float] = self.new_dict_float(payload.qtd_bolas_sorteio)

        # contabiliza sequencias de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            qt_sequencias = count_sequencias(jogo)
            sequencias_jogos[qt_sequencias] += 1

        # printa o resultado:
        output: str = f"\n\t ? SEGUIDO  PERC%     #TOTAL\n"
        for key, value in sequencias_jogos.items():
            percent: float = round((value / qtd_jogos) * 1000) / 10
            percentos_jogos[key] = percent
            output += f"\t {key} seguido: {percent:0>4.1f}% ... #{value:,}\n"
        logger.debug("Sequencias Resultantes: %s \n", output)

        #
        logger.debug("%s: Executando analise EVOLUTIVA de sequencia dos  %d  concursos da loteria.",
                     payload.nome_loteria, qtd_concursos)

        # contabiliza dezenas sequenciais de cada evolucao de concurso:
        concursos_passados: list[Concurso | ConcursoDuplo] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        list6_sequencias: list[int] = []
        concurso_atual: Concurso | ConcursoDuplo
        for concurso_atual in payload.concursos:
            # zera os contadores de cada sequencia:
            sequencias_passadas: dict[int, int] = self.new_dict_int(payload.qtd_bolas_sorteio - 1)

            # calcula a sequencia dos concursos passados até o concurso anterior:
            for concurso_passado in concursos_passados:
                qt_sequencias_passadas = count_sequencias(concurso_passado.bolas)
                sequencias_passadas[qt_sequencias_passadas] += 1
                # verifica se o concurso eh duplo (dois sorteios):
                if eh_duplo:
                    qt_sequencias_passadas = count_sequencias(concurso_passado.bolas2)
                    sequencias_passadas[qt_sequencias_passadas] += 1

            # calcula a sequencia do concurso atual para comparar a evolucao:
            qtd_sequencias_atual = count_sequencias(concurso_atual.bolas)
            str_sequencias_atual = str(qtd_sequencias_atual)
            list6_sequencias.append(qtd_sequencias_atual)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                qtd_sequencias2_atual = count_sequencias(concurso_atual.bolas2)
                str_sequencias_atual += '/' + str(qtd_sequencias2_atual)
                list6_sequencias.append(qtd_sequencias2_atual)
            # soh mantem as ultimas 6 sequencias:
            while len(list6_sequencias) > 6:
                del list6_sequencias[0]

            # printa o resultado:
            output: str = f"\n\t ? SEGUIDO  PERC%      %DIF%  " \
                          f"----->  CONCURSO Nº {concurso_atual.id_concurso} :  " \
                          f"Ultimas Sequencias == { list(reversed(list6_sequencias))}\n"
            for key, value in sequencias_passadas.items():
                percent: float = round((value / (qtd_concursos_passados*fator_sorteios)) * 1000) \
                                 / 10
                dif: float = percent - percentos_jogos[key]
                output += f"\t {key} seguido: {percent:0>4.1f}% ... {dif:5.1f}%\n"
            logger.debug("Sequencias Resultantes EVOLUTIVA: %s", output)

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        return 0

# ----------------------------------------------------------------------------
