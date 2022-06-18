"""
   Package lothon.process.analyze
   Module  analise_sequencia.py

"""

__all__ = [
    'AnaliseSequencia'
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
from lothon.process.compute.compute_sequencia import ComputeSequencia


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseSequencia(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Sequencia nos Concursos")

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, loteria: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if loteria is None or loteria.concursos is None or len(loteria.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = loteria.nome_loteria
        qtd_jogos: int = loteria.qtd_jogos
        concursos: list[Concurso] = loteria.concursos
        qtd_concursos: int = len(concursos)
        qtd_items: int = loteria.qtd_bolas_sorteio - 1

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeSequencia()
        cp.setup({
            'qtd_bolas': loteria.qtd_bolas,
            'qtd_bolas_sorteio': loteria.qtd_bolas_sorteio,
            'qtd_jogos': loteria.qtd_jogos
        })
        cp.execute(loteria.concursos)

        # efetua analise de todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise de sequencia dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # printa as sequencias de cada combinacao de jogo:
        output: str = f"\n\t  ? SEGUIDO     PERC%     #TOTAL\n"
        for key, value in enumerate(cp.sequencias_jogos):
            percent: float = cp.sequencias_percentos[key]
            output += f"\t {formatd(key,2)} seguido:  {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Sequencias Resultantes: {output}")

        # efetua analise diferencial dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise TOTAL de sequencia dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # printa as sequencias de cada sorteio dos concursos:
        output: str = f"\n\t  ? SEGUIDO     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(cp.sequencias_concursos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            dif: float = percent - cp.sequencias_percentos[key]
            output += f"\t {formatd(key,2)} seguido:  {formatf(percent,'6.2')}% ... " \
                      f"{formatf(dif,'6.2')}%     #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Sequencias Resultantes: {output}")

        # printa quais as sequencias que repetiram no ultimo sorteio dos concursos:
        output: str = f"\n\t  ? SEGUIDO     PERC%       #REPETIDAS\n"
        for key, value in enumerate(cp.ultimas_sequencias_repetidas):
            percent: float = cp.ultimas_sequencias_percentos[key]
            output += f"\t {formatd(key,2)} seguido:  {formatf(percent,'6.2')}%  ...  " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Concursos que repetiram a ultima sequencia: {output}")

        # efetua analise de todas as sequencias dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de FREQUENCIA de sequencias"
                     f"de dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # printa as frequencias e atrasos das sequencias em todos os sorteios ja realizados:
        output: str = f"\n\tSEGUIDO:   #SORTEIOS   ULTIMO     #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA    MEDIA   H.MEDIA   G.MEDIA   MEDIANA     " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in cp.frequencias_sequencias:
            output += f"\t     {formatd(serie.id,2)}:       " \
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
                      f"{formatf(serie.varia_atraso,'11.1')}         " \
                      f"{formatf(serie.stdev_atraso,'7.1')}\n"
        logger.debug(f"{nmlot}: FREQUENCIA de Sequencias Resultantes: {output}")

        # efetua analise evolutiva de todos os concursos de maneira progressiva:
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de sequencia dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # contabiliza dezenas sequenciais de cada evolucao de concurso:
        concursos_passados: list[Concurso] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        list6_sequencias: list[int] = []
        for concurso_atual in loteria.concursos:
            # zera os contadores de cada sequencia:
            sequencias_passadas: list[int] = cb.new_list_int(qtd_items)

            # calcula a sequencia dos concursos passados ate o concurso anterior:
            for concurso_passado in concursos_passados:
                qt_sequencias_passadas = cb.count_sequencias(concurso_passado.bolas)
                sequencias_passadas[qt_sequencias_passadas] += 1

            # calcula a sequencia do concurso atual para comparar a evolucao:
            qtd_sequencias_atual = cb.count_sequencias(concurso_atual.bolas)
            list6_sequencias.append(qtd_sequencias_atual)
            # soh mantem as ultimas 6 sequencias:
            while len(list6_sequencias) > 6:
                del list6_sequencias[0]

            # printa o resultado:
            output: str = f"\n\t  ? SEGUIDO     PERC%       %DIF%  " \
                          f"----->  CONCURSO Nr {concurso_atual.id_concurso} :  " \
                          f"Ultimas Sequencias == { list(reversed(list6_sequencias))}\n"
            for key, value in enumerate(sequencias_passadas):
                percent: float = round((value / qtd_concursos_passados) * 10000) / 100
                dif: float = percent - cp.sequencias_percentos[key]
                output += f"\t {formatd(key,2)} seguido:  {formatf(percent,'6.2')}% ... " \
                          f"{formatf(dif,'6.2')}%\n"
            logger.debug(f"{nmlot}: Sequencias Resultantes da EVOLUTIVA: {output}")

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
