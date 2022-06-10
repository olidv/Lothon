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
    __slots__ = ('recorrencias_concursos', 'recorrencias_percentos',
                 'concursos_passados')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Recorrencia nos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.recorrencias_concursos: Optional[list[int]] = None
        self.recorrencias_percentos: Optional[list[float]] = None
        # estruturas para avaliacao de jogo combinado da loteria:
        self.concursos_passados: Optional[list[Concurso]] = None

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def count_recorrencias(cls, bolas1: tuple[int, ...], bolas2: tuple[int, ...]) -> int:
        # valida os parametros:
        if bolas1 is None or len(bolas1) == 0 or bolas2 is None or len(bolas2) == 0:
            return False

        qtd_recorre: int = 0
        for num1 in bolas1:
            if num1 in bolas2:
                qtd_recorre += 1

        return qtd_recorre

    @classmethod
    def max_recorrencias(cls, bolas: tuple[int, ...], concursos: list[Concurso],
                         id_concurso_ignore: int = 0) -> int:
        # valida os parametros:
        if bolas is None or len(bolas) == 0 or concursos is None or len(concursos) == 0:
            return False

        # ja percorre todos os concursos e retorna o numero maximo de recorrencias de [bolas]:
        qt_max_recorrencias: int = 0
        for concurso in concursos:
            # nao deixa comparar com o mesmo concurso:
            if concurso.id_concurso == id_concurso_ignore:
                continue

            qt_recorrencias: int = cls.count_recorrencias(bolas, concurso.bolas)
            if qt_recorrencias > qt_max_recorrencias:
                qt_max_recorrencias = qt_recorrencias

        return qt_max_recorrencias

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.recorrencias_concursos = None
        self.recorrencias_percentos = None
        self.concursos_passados = None

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
        qtd_items: int = payload.qtd_bolas_sorteio

        # efetua analise das recorrencias nos concursos da loteria:
        logger.debug(f"{nmlot}: Executando analise TOTAL de recorrencias dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # contabiliza o maximo de repeticoes das dezenas de cada sorteio dos concursos:
        self.recorrencias_concursos = self.new_list_int(qtd_items)
        self.recorrencias_percentos = self.new_list_float(qtd_items)
        for concurso in concursos:
            qt_max_repeticoes: int = self.max_recorrencias(concurso.bolas, concursos,
                                                           concurso.id_concurso)  # ignora o atual
            self.recorrencias_concursos[qt_max_repeticoes] += 1

        # printa o resultado:
        output: str = f"\n\t  ? RECORRE     PERC%     #TOTAL\n"
        for key, value in enumerate(self.recorrencias_concursos):
            percent: float = round((value / qtd_concursos) * 100000) / 1000
            self.recorrencias_percentos[key] = percent
            output += f"\t {formatd(key,2)} recorre:  {formatf(percent,'6.2')}% ... " \
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
                vl_repetidas = self.count_recorrencias(concurso_atual.bolas,
                                                       concurso_anterior.bolas)
                dezenas_repetidas[vl_repetidas] += 1

            # printa o resultado do concurso atual:
            output += f"\t   {formatd(concurso_atual.id_concurso,6)}"
            for key, value in enumerate(dezenas_repetidas):
                output += f"  {formatd(value,5)}"
            output += f"\n"

            # inclui o concurso atual como anterior para a proxima iteracao:
            concursos_anteriores.append(concurso_atual)
        logger.debug(f"{nmlot}: Recorrencia dos ultimos  100  Concursos da EVOLUTIVA: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        self.set_options(parms)

        # identifica os concursos passados:
        self.concursos_passados = parms["concursos_passados"]

    def evaluate(self, pick) -> float:
        # probabilidade de acerto depende do numero maximo de repeticoes nos concursos anteriores:
        qt_max_repeticoes: int = self.max_recorrencias(pick, self.concursos_passados)
        percent: float = self.recorrencias_percentos[qt_max_repeticoes]

        # ignora valores muito baixos de probabilidade:
        if percent < 10:
            return 0
        else:
            return to_fator(percent)

# ----------------------------------------------------------------------------
