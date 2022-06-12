"""
   Package lothon.process.analyze
   Module  analise_recorrencia.py

"""

__all__ = [
    'AnaliseRecorrencia'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.stats import combinatoria as cb
from lothon.domain import Loteria, Concurso
from lothon.process.analyze.abstract_analyze import AbstractAnalyze
from lothon.process.compute.compute_recorrencia import ComputeRecorrencia


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
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Recorrencia nos Concursos")

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
        cp = ComputeRecorrencia()
        cp.execute(payload)

        # efetua analise das recorrencias nos concursos da loteria:
        logger.debug(f"{nmlot}: Executando analise TOTAL de recorrencias dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # printa o maximo de repeticoes das dezenas de cada sorteio dos concursos:
        output: str = f"\n\t  ? RECORRE     PERC%     #TOTAL\n"
        for key, value in enumerate(cp.recorrencias_concursos):
            percent: float = cp.recorrencias_percentos[key]
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
            dezenas_repetidas: list[int] = cb.new_list_int(payload.qtd_bolas_sorteio)

            # calcula a paridade dos concursos passados ate o concurso anterior:
            for concurso_anterior in concursos_anteriores:
                vl_repetidas = cb.count_recorrencias(concurso_atual.bolas,
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

# ----------------------------------------------------------------------------
