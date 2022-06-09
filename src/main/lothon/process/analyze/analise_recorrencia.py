"""
   Package lothon.process
   Module  analise_recorrencia.py

"""

__all__ = [
    'AnaliseRecorrencia'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
import logging
import itertools as itt

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.domain import Loteria, Concurso
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
    __slots__ = ('recorrencias_tuplas', 'recorrencias_total', 'tamanhos_tuplas',
                 'concursos_passados', 'max_repeticoes')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Recorrencia nos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.recorrencias_tuplas: dict[str: int] = None
        self.recorrencias_total: dict[int: int] = None
        self.tamanhos_tuplas: Optional[list[int]] = None
        self.concursos_passados: Optional[list[Concurso]] = None
        self.max_repeticoes: int = 0

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def count_dezenas_repetidas(cls, bolas1: tuple[int, ...], bolas2: tuple[int, ...]) -> int:
        # aqui nao precisa validar os parametros:
        qtd_repete: int = 0
        for num1 in bolas1:
            if num1 in bolas2:
                qtd_repete += 1

        return qtd_repete

    @classmethod
    def format_tuple(cls, bolas: tuple[int, ...]) -> str:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return ''

        text: str = f"{bolas[0]:0>2}"
        if len(bolas) > 1:
            for bola in bolas[1:]:
                text += f".{bola:0>2}"

        return text

    @classmethod
    def has_recorrencias(cls, bolas1: tuple[int, ...], bolas2: tuple[int, ...]) -> bool:
        # valida os parametros:
        if bolas1 is None or len(bolas1) == 0 or bolas2 is None or len(bolas2) == 0:
            return False

        qtd_recorre: int = 0
        for num1 in bolas1:
            if num1 in bolas2:
                qtd_recorre += 1

        return qtd_recorre == len(bolas1)

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.recorrencias_tuplas = None
        self.recorrencias_total = None
        self.tamanhos_tuplas = None
        self.concursos_passados = None
        self.max_repeticoes = 0

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = payload.nome_loteria
        concursos: list[Concurso] = payload.concursos
        qtd_concursos: int = len(concursos)
        qtd_items: int = 1000  # maximo de 1000 recorrencias de cada tupla nos sorteios
        max_size_tuplas: int = min(8, payload.qtd_bolas_sorteio)  # maximo de 7 dezenas na tupla:

        # efetua analise de recorrencias de todos os sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de TODAS recorrencias nos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de cada recorrencia:
        self.recorrencias_tuplas = {}
        self.tamanhos_tuplas = self.new_list_int(max_size_tuplas - 1)
        count_recorrencias: list[int] = self.new_list_int(qtd_items)

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
                    self.tamanhos_tuplas[qt_parcial] += 1

                    # se a tupla ja foi pesquisada, entao ignora e pula pra proxima:
                    tpstr: str = self.format_tuple(tupla)
                    if tpstr in self.recorrencias_tuplas:
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

                    # somente registra tuplas que repetem mais de uma vez:
                    if qt_repeticoes > 1:
                        # logger.debug(f"Tupla {tpstr} possui #{qt_repeticoes} repeticoes nos "
                        #              f"concursos.")
                        self.recorrencias_tuplas[tpstr] = qt_repeticoes
                        count_recorrencias[qt_repeticoes] += 1

        # ordena as recorrencias em ordem decrescente do valor (quantidade de recorrencias):
        self.recorrencias_tuplas = {k: v for k, v in sorted(self.recorrencias_tuplas.items(),
                                    key=lambda item: item[1], reverse=True)}
        # logger.debug('-' * 60)
        # for k, v in self.recorrencias_tuplas.items():
        #     logger.debug(f"{nmlot}: Tupla {k} ocorreu em #{v} sorteios.")
        # logger.debug('-' * 60)

        # identifica o numero de repeticoes de cada recorrencia
        self.recorrencias_total = {}
        total_tuplas: int = 0
        for qtd_repete, qtd_tuplas in enumerate(count_recorrencias):
            if qtd_repete == 0 or qtd_tuplas == 0:
                continue
            # logger.debug(f"{nmlot}: #{qtd_tuplas} Tuplas ocorreram em #{qtd_repete} sorteios.")
            self.recorrencias_total[qtd_repete] = qtd_tuplas
            total_tuplas += qtd_tuplas

        # printa a quantidade de tuplas pelo tamanho (len):
        output: str = f"\n\t  ? TUPLA     PERC%     #TOTAL\n"
        total: int = sum(self.tamanhos_tuplas)
        for i, value in enumerate(self.tamanhos_tuplas):
            if i < 2:  # os valores estao a partir da posicao #2 (tamanho minimo das tuplas)
                continue

            percent: float = round((value / total) * 10000) / 100
            output += f"\t  {i} tupla:  {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Numero de Dezenas das Tuplas: {output}")

        # printa o numero de tuplas para cada quantidade de recorrencias:
        output: str = f"\n\t  ? RECORRE     PERC%     #TUPLAS\n"
        for i, value in self.recorrencias_total.items():
            percent: float = round((value / total_tuplas) * 10000) / 100
            output += f"\t{formatd(i,3)} recorre:  {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Recorrencias Resultantes: {output}")

        # efetua analise evolutiva de todos os concursos de maneira progressiva:
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de recorrencia dos ultimos  100  "
                     f"concursos da loteria.")

        # formata o cabecalho da impressao do resultado:
        output: str = f"\n\t CONCURSO"
        for val in range(0, payload.qtd_bolas_sorteio + 1):
            output += f"     {val:0>2}"
        output += f"\n"

        # acumula os concursos passados para cada concurso atual:
        qtd_concursos_anteriores: int = qtd_concursos - 100
        concursos_anteriores: list[Concurso] = concursos[:qtd_concursos_anteriores]
        for concurso_atual in concursos[qtd_concursos_anteriores:]:
            # zera os contadores de cada recorrencia:
            dezenas_repetidas: list[int] = self.new_list_int(payload.qtd_bolas_sorteio)

            # calcula a paridade dos concursos passados ate o concurso anterior:
            for concurso_anterior in concursos_anteriores:
                vl_repetidas = self.count_dezenas_repetidas(concurso_atual.bolas,
                                                            concurso_anterior.bolas)
                dezenas_repetidas[vl_repetidas] += 1

            # printa o resultado do concurso atual:
            output += f"\t   {formatd(concurso_atual.id_concurso,6)}"
            for key, value in enumerate(dezenas_repetidas):
                output += f"  {formatd(value,5)}"
            output += f"\n"

            # inclui o concurso atual como anterior para a proxima iteracao:
            concursos_anteriores.append(concurso_atual)
        logger.debug(f"{nmlot}: Recorrencia de Sorteios da EVOLUTIVA: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        self.set_options(parms)

        # identifica os concursos passados:
        self.concursos_passados = parms["concursos_passados"]
        self.max_repeticoes = parms["max_repeticoes"]

    def evaluate(self, pick) -> float:
        # probabilidade de acerto depende do numero maximo de repeticoes nos concursos anteriores:
        qt_max_repeticoes: int = 0
        for concurso in self.concursos_passados:
            qt_repeticoes: int = self.count_dezenas_repetidas(pick, concurso.bolas)
            if qt_repeticoes > qt_max_repeticoes:
                qt_max_repeticoes = qt_repeticoes

        # ignora jogos com muitas repeticoes nos concursos anteriores:
        if qt_max_repeticoes > self.max_repeticoes:
            return 0
        else:
            return 1.5

# ----------------------------------------------------------------------------
