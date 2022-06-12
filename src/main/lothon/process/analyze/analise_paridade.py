"""
   Package lothon.process.analyze
   Module  analise_paridade.py

"""

__all__ = [
    'AnaliseParidade'
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
from lothon.process.compute.compute_paridade import ComputeParidade


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseParidade(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Paridade das Dezenas")

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
        qtd_jogos: int = payload.qtd_jogos
        concursos: list[Concurso] = payload.concursos
        qtd_concursos: int = len(concursos)
        qtd_items: int = payload.qtd_bolas_sorteio

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeParidade()
        cp.execute(payload)

        # efetua analise de todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise de paridade dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # printa pares (e impares) de cada combinacao de jogo:
        output: str = f"\n\t  ? PARES     PERC%     #TOTAL\n"
        for key, value in enumerate(cp.paridades_jogos):
            percent: float = cp.paridades_percentos[key]
            output += f"\t {formatd(key,2)} pares:  {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Paridades Resultantes: {output}")

        # efetua analise diferencial dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise TOTAL de paridade dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # printa os pares (e impares) de cada sorteio dos concursos:
        output: str = f"\n\t  ? PARES     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(cp.paridades_concursos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            dif: float = percent - cp.paridades_percentos[key]
            output += f"\t {formatd(key,2)} pares:  {formatf(percent,'6.2')}% ... " \
                      f"{formatf(dif,'6.2')}%     #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Paridades Resultantes: {output}")

        # efetua analise de todas as paridades dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de FREQUENCIA de paridades"
                     f"de dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # printa as frequencias e atrasos das paridades em todos os sorteios ja realizados:
        output: str = f"\n\tPARES:   #SORTEIOS   ULTIMO     #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA    MEDIA   H.MEDIA   G.MEDIA   MEDIANA   " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in cp.frequencias_paridades:
            output += f"\t   {formatd(serie.id,2)}:       " \
                      f"{formatd(serie.len_sorteios,5)}    " \
                      f"{formatd(serie.ultimo_sorteio,5)}        " \
                      f"{formatd(serie.len_atrasos,5)}    " \
                      f"{formatd(serie.ultimo_atraso,5)}   " \
                      f"{formatd(serie.min_atraso,5)}  " \
                      f"{formatd(serie.max_atraso,5)}   " \
                      f"{formatd(serie.mode_atraso,5)}  " \
                      f"{formatf(serie.mean_atraso,'7.1')}   " \
                      f"{formatf(serie.hmean_atraso,'7.1')}   " \
                      f"{formatf(serie.gmean_atraso,'7.1')}   " \
                      f"{formatf(serie.median_atraso,'7.1')}   " \
                      f"{formatf(serie.varia_atraso,'9.1')}         " \
                      f"{formatf(serie.stdev_atraso,'7.1')}\n"
        logger.debug(f"{nmlot}: FREQUENCIA de Paridades Resultantes: {output}")

        # efetua analise evolutiva de todos os concursos de maneira progressiva:
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de paridade dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # contabiliza pares (e impares) de cada evolucao de concurso:
        concursos_passados: list[Concurso] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        list6_paridades: list[int] = []
        for concurso_atual in payload.concursos:
            # zera os contadores de cada paridade:
            paridades_passados: list[int] = cb.new_list_int(qtd_items)

            # calcula a paridade dos concursos passados ate o concurso anterior:
            for concurso_passado in concursos_passados:
                qtd_pares_passado = cb.count_pares(concurso_passado.bolas)
                paridades_passados[qtd_pares_passado] += 1

            # calcula a paridade do concurso atual para comparar a evolucao:
            qtd_pares_atual = cb.count_pares(concurso_atual.bolas)
            list6_paridades.append(qtd_pares_atual)
            # soh mantem os ultimos 6 pares:
            while len(list6_paridades) > 6:
                del list6_paridades[0]

            # printa o resultado:
            output: str = f"\n\t  ? PARES     PERC%       %DIF%  " \
                          f"----->  CONCURSO Nr {concurso_atual.id_concurso} :  " \
                          f"Ultimos Pares == { list(reversed(list6_paridades))}\n"
            for key, value in enumerate(paridades_passados):
                percent: float = round((value / qtd_concursos_passados) * 10000) / 100
                dif: float = percent - cp.paridades_percentos[key]
                output += f"\t {formatd(key,2)} pares:  {formatf(percent,'6.2')}% ... " \
                          f"{formatf(dif,'6.2')}%\n"
            logger.debug(f"{nmlot}: Paridades Resultantes da EVOLUTIVA: {output}")

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
