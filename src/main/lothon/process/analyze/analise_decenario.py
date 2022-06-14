"""
   Package lothon.process.analyze
   Module  analise_decenario.py

"""

__all__ = [
    'AnaliseDecenario'
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
from lothon.process.compute.compute_decenario import ComputeDecenario


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseDecenario(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Decenario nos Concursos")

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
        qtd_items: int = (loteria.qtd_bolas-1) // 10

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeDecenario()
        cp.execute(loteria)

        # efetua analise de todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise de decenario dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # printa os decenarios de cada combinacao de jogo:
        output: str = f"\n\t ? DEZENA     PERC%     #TOTAL\n"
        for key, value in enumerate(cp.decenarios_jogos):
            percent: float = cp.decenarios_percentos[key]
            output += f"\t {key} dezena:  {formatf(percent,'6.2')}% ... #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Decenarios Resultantes: {output}")

        # efetua analise diferencial dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise TOTAL de decenarios dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # printa os decenarios de cada sorteio ja realizado:
        output: str = f"\n\t ? DEZENA     PERC%       %DIF%     #TOTAL\n"
        total: int = loteria.qtd_bolas_sorteio * qtd_concursos
        for key, value in enumerate(cp.decenarios_concursos):
            percent: float = round((value / total) * 10000) / 100
            dif: float = percent - cp.decenarios_percentos[key]
            output += f"\t {key} dezena:  {formatf(percent,'6.2')}% ... {formatf(dif,'6.2')}%  " \
                      f"   #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Decenarios Resultantes: {output}")

        # printa a representacao string de cada decenario dos sorteios realizados:
        output: str = f"\n\t CONCURSO       DECENARIO\n"
        for concurso in concursos:
            id_concurso: int = concurso.id_concurso
            str_decenario: str = cp.str_decenarios_concursos[id_concurso]
            output += f"\t   {formatd(id_concurso,6)}  ...  {str_decenario}\n"
        logger.debug(f"{nmlot}: Representacao STR dos Decenarios: {output}")

        # printa quais o percentual de decenarios que repetiram no ultimo sorteio dos concursos:
        logger.debug(f"{nmlot}: Percentual de concursos que repetiram o ultimo decenario: "
                     f"{formatf(cp.ultimos_decenarios_percentos,'6.2')}%")

        # efetua analise de frequencia de todos os decenarios dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de FREQUENCIA de decenarios "
                     f"nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # printa as frequencias e atrasos dos decenarios em todos os sorteios ja realizados:
        output: str = f"\n\tDEZENA:   #SORTEIOS   ULTIMO     #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA    MEDIA   H.MEDIA   G.MEDIA   MEDIANA   " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in cp.frequencias_decenarios:
            output += f"\t    {formatd(serie.id,2)}:       " \
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
        logger.debug(f"{nmlot}: FREQUENCIA de Decenarios Resultantes: {output}")

        # efetua analise evolutiva de todos os concursos de maneira progressiva:
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de decenario dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # contabiliza decenarios de cada evolucao de concurso:
        concursos_passados: list[Concurso] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        for concurso_atual in loteria.concursos:
            # zera os contadores de cada decenario:
            decenarios_passados: list[int] = cb.new_list_int(qtd_items)

            # calcula a decenario dos concursos passados ate o concurso anterior:
            for concurso_passado in concursos_passados:
                cb.count_decenarios(concurso_passado.bolas, decenarios_passados)

            # calcula a decenario do concurso atual para comparar a evolucao:
            decenario_atual: list[int] = cb.new_list_int(qtd_items)
            cb.count_decenarios(concurso_atual.bolas, decenario_atual)

            # printa o resultado:
            output: str = f"\n\t ? DEZENA     PERC%       %DIF%  " \
                          f"----->  CONCURSO Nr {concurso_atual.id_concurso} :  " \
                          f"Ultimo Decenario == {decenario_atual}\n"
            total: int = loteria.qtd_bolas_sorteio * qtd_concursos_passados
            for key, value in enumerate(decenarios_passados):
                percent: float = round((value / total) * 10000) / 100
                dif: float = percent - cp.decenarios_percentos[key]
                output += f"\t {key} dezena:  {formatf(percent,'6.2')}% ... {formatf(dif,'6.2')}%\n"
            logger.debug(f"{nmlot}: Decenarios Resultantes da EVOLUTIVA: {output}")

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
