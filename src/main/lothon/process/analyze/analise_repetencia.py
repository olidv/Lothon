"""
   Package lothon.process.analyze
   Module  analise_repetencia.py

"""

__all__ = [
    'AnaliseRepetencia'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.domain import Loteria, Concurso
from lothon.process.analyze.abstract_analyze import AbstractAnalyze
from lothon.process.compute.compute_repetencia import ComputeRepetencia


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
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Repetencia do Ultimo Concurso")

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- PROCESSAMENTO ------------------------------------------------------

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
        # qtd_items: int = payload.qtd_bolas_sorteio

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeRepetencia()
        cp.execute(payload)

        # efetua analise de repetencias de todos os sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de TODAS repetencias nos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # printa as repetencias de cada sorteio com todos o sorteio anterior:
        output: str = f"\n\t  ? REPETE    PERC%     #TOTAL\n"
        for key, value in enumerate(cp.repetencias_concursos):
            percent: float = cp.repetencias_percentos[key]
            output += f"\t {formatd(key,2)} repete: {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Repetencias Resultantes: {output}")

        # efetua analise de todas as repeticoes dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de FREQUENCIA de repetencias"
                     f"de dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # printa as medidas estatisticas para cada repetencia:
        output: str = f"\n\tREPETE:   #SORTEIOS   ULTIMO    #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA    MEDIA   H.MEDIA   G.MEDIA   MEDIANA    " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in cp.repetencias_series:
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
                      f"{formatf(serie.stdev_atraso,'8.1')}\n"
        logger.debug(f"{nmlot}: FREQUENCIA de Repetencias Resultantes: {output}")

        # efetua analise de todas as dezenas dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de frequencia das dezenas repetidas "
                     f"nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # printa as medidas estatisticas para cada dezena/bola:
        output: str = f"\n\t BOLA:   #SORTEIOS   ULTIMO     #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA   MEDIA   H.MEDIA   G.MEDIA      MEDIANA    " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in cp.frequencias_repetencias[1:]:
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
                      f"{formatf(serie.stdev_atraso,'8.1')}\n"
        logger.debug(f"{nmlot}: Frequencia de Dezenas Repetidas: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
