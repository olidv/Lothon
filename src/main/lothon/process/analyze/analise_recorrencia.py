"""
   Package lothon.process
   Module  analise_recorrencia.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging
import itertools as itt

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

class AnaliseRecorrencia(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_process', '_options'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Recorrencia nos Concursos")

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def format_tuple(bolas: tuple[int, ...]) -> str:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return ''

        text: str = f"{bolas[0]:0>2}"
        if len(bolas) > 1:
            for bola in bolas[1:]:
                text += f".{bola:0>2}"

        return text

    @staticmethod
    def has_recorrencias(bolas1: tuple[int, ...], bolas2: tuple[int, ...]) -> bool:
        # valida os parametros:
        if bolas1 is None or len(bolas1) == 0 or bolas2 is None or len(bolas2) == 0:
            return False

        qtd_recorre: int = 0
        for num1 in bolas1:
            if num1 in bolas2:
                qtd_recorre += 1

        return qtd_recorre == len(bolas1)

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
        eh_duplo: bool = ([0] is ConcursoDuplo)
        # if eh_duplo:
        #     fator_sorteios: int = 2
        # else:
        #     fator_sorteios: int = 1
        # qtd_sorteios: int = qtd_concursos * fator_sorteios
        qtd_items: int = 1000  # maximo de 1000 recorrencias de cada tupla nos sorteios
        max_size_tuplas: int = min(8, payload.qtd_bolas_sorteio)  # maximo de 7 dezenas na tupla:

        # efetua analise de recorrencias de todos os sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de TODAS recorrencias nos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de cada recorrencia:
        recorrencias_tuplas: dict[str: int] = {}
        count_recorrencias: list[int] = self.new_list_int(qtd_items)
        tamanhos_tuplas: list[int] = self.new_list_int(max_size_tuplas - 1)

        # contabiliza recorrencias de cada sorteio com todos os sorteios ja realizados:
        variacoes_tuplas: range = range(2, max_size_tuplas)  # tuplas com range maximo de 2..7 bolas
        logger.debug(f"{nmlot}: Vai gerar combinacoes de tuplas de tamanho maximo de "
                     f"{max_size_tuplas} bolas, para pesquisar recorrencias.")
        for concurso in concursos:
            # pode haver combinacoes de 2 bolas ate qtd_bolas_sorteio - 1:
            for qt_parcial in variacoes_tuplas:
                # gera todas as combinacoes de bolas do sorteio, para tamanhos de qt_parcial:
                for bolas in itt.combinations(concurso.bolas, qt_parcial):
                    tupla: tuple[int, ...] = tuple(sorted(bolas))  # tupla ordenada de bolas
                    # contabiliza quantas tuplas possuem esse tamanho (numero de dezenas):
                    tamanhos_tuplas[qt_parcial] += 1

                    # se a tupla ja foi pesquisada, entao ignora e pula pra proxima:
                    tpstr: str = self.format_tuple(tupla)
                    if tpstr in recorrencias_tuplas:
                        # logger.debug(f"Tupla {tpstr} ja foi processada e sera ignorada.")
                        continue
                    # logger.debug(f"Vai processar a Tupla {tpstr}...")

                    # agora verifica em quantos concursos essa tupla de bolas apareceu:
                    qt_repeticoes: int = 0
                    for outro_concurso in concursos:
                        # somente compara com concursos distintos:
                        if outro_concurso.id_concurso == concurso.id_concurso:
                            continue

                        # contabiliza a tupla em cada sorteio, mas apenas uma vez em cada um:
                        if self.has_recorrencias(tupla, outro_concurso.bolas):
                            qt_repeticoes += 1
                        # verifica se o concurso eh duplo (dois sorteios):
                        if eh_duplo:
                            # se for concurso duplo, precisa comparar as bolas do segundo sorteio:
                            if self.has_recorrencias(tupla, outro_concurso.bolas2):
                                qt_repeticoes += 1

                    # somente registra tuplas que repetem mais de uma vez:
                    if qt_repeticoes > 1:
                        # logger.debug(f"Tupla {tpstr} possui #{qt_repeticoes} repeticoes nos "
                        #              f"concursos.")
                        recorrencias_tuplas[tpstr] = qt_repeticoes
                        count_recorrencias[qt_repeticoes] += 1

        # ordena as recorrencias em ordem decrescente do valor (quantidade de recorrencias):
        recorrencias_tuplas = {k: v for k, v in sorted(recorrencias_tuplas.items(),
                                                       key=lambda item: item[1], reverse=True)}
        # logger.debug('-' * 60)
        # for k, v in recorrencias_tuplas.items():
        #     logger.debug(f"{nmlot}: Tupla {k} ocorreu em #{v} sorteios.")
        # logger.debug('-' * 60)

        # identifica o numero de repeticoes de cada recorrencia
        recorrencias_total: dict[int: int] = {}
        total_tuplas: int = 0
        for qtd_repete, qtd_tuplas in enumerate(count_recorrencias):
            if qtd_repete == 0 or qtd_tuplas == 0:
                continue
            # logger.debug(f"{nmlot}: #{qtd_tuplas} Tuplas ocorreram em #{qtd_repete} sorteios.")
            recorrencias_total[qtd_repete] = qtd_tuplas
            total_tuplas += qtd_tuplas

        # printa a quantidade de tuplas pelo tamanho (len):
        output: str = f"\n\t  ? TUPLA     PERC%     #TOTAL\n"
        total: int = sum(tamanhos_tuplas)
        for i, value in enumerate(tamanhos_tuplas):
            if i < 2:  # os valores estao a partir da posicao #2 (tamanho minimo das tuplas)
                continue

            percent: float = round((value / total) * 10000) / 100
            output += f"\t  {i} tupla:  {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Numero de Dezenas das Tuplas: {output}")

        # printa o numero de tuplas para cada quantidade de recorrencias:
        output: str = f"\n\t  ? RECORRE     PERC%     #TUPLAS\n"
        for i, value in recorrencias_total.items():
            percent: float = round((value / total_tuplas) * 10000) / 100
            output += f"\t{formatd(i,3)} recorre:  {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Recorrencias Resultantes: {output}")

        # salva os dados resultantes da analise para utilizacao em simulacoes e geracoes de boloes:
        payload.statis["recorrencias_tuplas"] = recorrencias_tuplas
        payload.statis["recorrencias_total"] = recorrencias_total
        payload.statis["tamanhos_tuplas"] = tamanhos_tuplas

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def init(self, options: dict):
        self.options = options

    def evaluate(self, payload) -> float:
        pass

# ----------------------------------------------------------------------------
