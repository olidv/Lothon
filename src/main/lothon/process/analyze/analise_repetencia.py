"""
   Package lothon.process
   Module  analise_repetencia.py

"""

__all__ = [
    'AnaliseRepetencia'
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

class AnaliseRepetencia(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('repetencias_concursos', 'repetencias_series', 'frequencias_repetencias')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Repetencia do Ultimo Concurso")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.repetencias_concursos: Optional[list[int]] = None
        self.repetencias_series: Optional[list[SerieSorteio]] = None
        self.frequencias_repetencias: Optional[list[SerieSorteio | None]] = None

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def count_repeticoes(cls, bolas1: tuple[int, ...], bolas2: tuple[int, ...],
                         dezenas: list[SerieSorteio], id_concurso: int) -> int:
        # valida os parametros:
        if bolas1 is None or len(bolas1) == 0 or bolas2 is None or len(bolas2) == 0:
            return 0

        qtd_repete: int = 0
        for num1 in bolas1:
            if num1 in bolas2:
                qtd_repete += 1
                dezenas[num1].add_sorteio(id_concurso)

        return qtd_repete

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.repetencias_concursos = None
        self.repetencias_series = None
        self.frequencias_repetencias = None

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

        # efetua analise de repetencias de todos os sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de TODAS repetencias nos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de cada repetencia:
        self.repetencias_concursos = self.new_list_int(qtd_items)
        self.repetencias_series = self.new_list_series(qtd_items)
        self.repetencias_series[0] = SerieSorteio(0)  # neste caso especifico tem a repetencia zero
        self.frequencias_repetencias = self.new_list_series(payload.qtd_bolas)

        # contabiliza repetencias de cada sorteio com todos o sorteio anterior:
        concurso_anterior: Concurso = concursos[0]
        for concurso in concursos[1:]:
            qt_repeticoes: int = self.count_repeticoes(concurso.bolas,
                                                       concurso_anterior.bolas,
                                                       self.frequencias_repetencias,
                                                       concurso.id_concurso)
            self.repetencias_concursos[qt_repeticoes] += 1
            self.repetencias_series[qt_repeticoes].add_sorteio(concurso.id_concurso)
            concurso_anterior = concurso

        # printa o resultado:
        output: str = f"\n\t  ? REPETE    PERC%     #TOTAL\n"
        for key, value in enumerate(self.repetencias_concursos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            output += f"\t {formatd(key,2)} repete: {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Repetencias Resultantes: {output}")

        # efetua analise de todas as repeticoes dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de FREQUENCIA de repetencias"
                     f"de dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # contabiliza as medidas estatisticas para cada repetencia:
        for serie in self.repetencias_series:
            serie.update_stats()

        # printa o resultado:
        output: str = f"\n\tREPETE:   #SORTEIOS   ULTIMO    #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA    MEDIA   H.MEDIA   G.MEDIA   MEDIANA    " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in self.repetencias_series:
            output += f"\t    {formatd(serie.id,2)}:       " \
                      f"{formatd(serie.len_sorteios,5)}    " \
                      f"{formatd(serie.ultimo_sorteio,5)}       " \
                      f"{formatd(serie.len_atrasos,5)}    " \
                      f"{formatd(serie.ultimo_atraso,5)}   " \
                      f"{formatd(serie.min_atraso,5)}  " \
                      f"{formatd(serie.max_atraso,5)}   " \
                      f"{formatd(serie.mode_atraso,5)}  " \
                      f"{formatf(serie.mean_atraso,'7.1')}   " \
                      f"{formatf(serie.hmean_atraso,'7.1')}   " \
                      f"{formatf(serie.gmean_atraso,'7.1')}   " \
                      f"{formatf(serie.median_atraso,'7.1')}  " \
                      f"{formatf(serie.varia_atraso,'11.1')}        " \
                      f"{formatf(serie.stdev_atraso,'8.1')} \n"
        logger.debug(f"{nmlot}: FREQUENCIA de Repetencias Resultantes: {output}")

        # efetua analise de todas as dezenas dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de frequencia das dezenas repetidas "
                     f"nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_repetencias[1:]:
            # vai aproveitar e contabilizar as medidas estatisticas para a bola:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        # printa o resultado:
        output: str = f"\n\t BOLA:   #SORTEIOS   ULTIMO     #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA   MEDIA   H.MEDIA   G.MEDIA      MEDIANA    " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in self.frequencias_repetencias[1:]:
            output += f"\t  {formatd(serie.id,3)}:       " \
                      f"{formatd(serie.len_sorteios,5)}    " \
                      f"{formatd(serie.ultimo_sorteio,5)}        " \
                      f"{formatd(serie.len_atrasos,5)}    " \
                      f"{formatd(serie.ultimo_atraso,5)}   " \
                      f"{formatd(serie.min_atraso,5)}  " \
                      f"{formatd(serie.max_atraso,5)}   " \
                      f"{formatd(serie.mode_atraso,5)} " \
                      f"{formatf(serie.mean_atraso,'7.1')}   " \
                      f"{formatf(serie.hmean_atraso,'7.1')}   " \
                      f"{formatf(serie.gmean_atraso,'7.1')}      " \
                      f"{formatf(serie.median_atraso,'7.1')}  " \
                      f"{formatf(serie.varia_atraso,'11.1')}        " \
                      f"{formatf(serie.stdev_atraso,'8.1')} \n"
        logger.debug(f"{nmlot}: Frequencia de Dezenas Repetidas: {output}")

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
