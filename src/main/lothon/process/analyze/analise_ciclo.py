"""
   Package lothon.process
   Module  analise_ciclo.py

"""

__all__ = [
    'AnaliseCiclo'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging
from typing import Optional

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.domain import Loteria, Concurso, SerieSorteio
from lothon.process.analyze.abstract_analyze import AbstractAnalyze


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseCiclo(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('frequencias_ciclos',)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Ciclo Fechado dos Concursos")

        # estrutura para a coleta de dados a partir do processamento de analise:
        self.frequencias_ciclos: Optional[SerieSorteio] = None

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def count_dezenas(cls, bolas: tuple[int, ...], dezenas: list[int]):
        # valida os parametros:
        if bolas is None or len(bolas) == 0 or dezenas is None or len(dezenas) == 0:
            return

        for num in bolas:
            dezenas[num] += 1

        return

    # --- PROCESSAMENTO DOS SORTEIOS -----------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.frequencias_ciclos = None

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
        qtd_items: int = payload.qtd_bolas

        # efetua analise de todas os ciclos fechados ao longo dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de TODOS os ciclos fechados nos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # inicializa a serie para os ciclos fechados:
        self.frequencias_ciclos = SerieSorteio(0)

        # contabiliza os ciclos fechados em todos os sorteios ja realizados:
        dezenas: list[int | None] = self.new_list_int(qtd_items)
        dezenas[0] = None

        # prepara a impressao evolutiva:
        output: str = f"\n\n\tCONCURSO   DEZENAS PARA FECHAR CICLO...\n"
        for concurso in concursos:
            output += f"\t  {formatd(concurso.id_concurso,6)}  "

            # identifica as bolas sorteadas para fechar o ciclo:
            self.count_dezenas(concurso.bolas, dezenas)

            # se ainda tem algum zero, entao nao fechou o ciclo:
            if 0 in dezenas:
                # printa as dezenas que ainda faltam para zerar:
                for idx, value in enumerate(dezenas[1:]):
                    if value == 0:
                        output += f" {idx+1:0>2}"
                output += "\n"
                continue
            else:
                # no inicio do ciclo, as dezenas sorteadas sao eliminadas do conjunto total:
                output += ' ' + ('---' * (payload.qtd_bolas - payload.qtd_bolas_sorteio)) + '\n'

            # fechando o ciclo, contabiliza o ciclo fechado (onde fecha o ciclo eh inclusivo):
            self.frequencias_ciclos.add_sorteio(concurso.id_concurso, True)

            # zera contadores para proximo ciclo:
            dezenas = self.new_list_int(qtd_items)
            dezenas[0] = None  # para nao conflitar com o teste de fechamento do ciclo

        logger.debug(f"{nmlot}: Evolucao dos ciclos fechados ao longo dos concursos: {output}")

        # ja calcula as medidas estatisticas para impressao ao final:
        self.frequencias_ciclos.update_stats()

        # printa o primeiro resultado:

        # printa o segundo resultado:
        output: str = f"\n\n\t  INICIO     FINAL   ATRASO \n"
        inicio: int = 1
        for i in range(0, len(self.frequencias_ciclos.sorteios)):
            final: int = self.frequencias_ciclos.sorteios[i]
            intervalo: int = self.frequencias_ciclos.atrasos[i]
            output += f"\t   {formatd(inicio,5)} ... {formatd(final,5)}      " \
                      f"{formatd(intervalo,3)}\n"
            inicio = final + 1

        output += f"\n\t #SORTEIOS   ULTIMO      #ATRASOS   ULTIMO   MENOR   MAIOR   MODA   " \
                  f"MEDIA   H.MEDIA   G.MEDIA   MEDIANA   VARIANCIA   DESVIO-PADRAO\n"
        output += f"\t     {formatd(self.frequencias_ciclos.len_sorteios,5)}    " \
                  f"{formatd(self.frequencias_ciclos.ultimo_sorteio,5)}         " \
                  f"{formatd(self.frequencias_ciclos.len_atrasos,5)}    " \
                  f"{formatd(self.frequencias_ciclos.ultimo_atraso,5)}   " \
                  f"{formatd(self.frequencias_ciclos.min_atraso,5)}   " \
                  f"{formatd(self.frequencias_ciclos.max_atraso,5)}  " \
                  f"{formatd(self.frequencias_ciclos.mode_atraso,5)} " \
                  f"{formatf(self.frequencias_ciclos.mean_atraso,'7.1')}   " \
                  f"{formatf(self.frequencias_ciclos.hmean_atraso,'7.1')}   " \
                  f"{formatf(self.frequencias_ciclos.gmean_atraso,'7.1')}   " \
                  f"{formatf(self.frequencias_ciclos.median_atraso,'7.1')}   " \
                  f"{formatf(self.frequencias_ciclos.varia_atraso,'9.1')}         " \
                  f"{formatf(self.frequencias_ciclos.stdev_atraso,'7.1')} \n"
        logger.debug(f"{nmlot}: Ciclos Fechados Resultantes: {output}")

        # indica o tempo do processamento:
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
