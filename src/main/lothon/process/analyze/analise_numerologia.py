"""
   Package lothon.process.analyze
   Module  analise_numerologia.py

"""

__all__ = [
    'AnaliseNumerologia'
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
from lothon.process.compute.compute_numerologia import ComputeNumerologia


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseNumerologia(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Numerologia das Dezenas")

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
        qtd_items: int = 9  # numero de zero a nove

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeNumerologia()
        cp.execute(loteria)

        # efetua analise de todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise de numerologia dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # printa a numerologia de cada combinacao de jogo:
        output: str = f"\n\t ? NUMERO     PERC%     #TOTAL\n"
        for key, value in enumerate(cp.numerologias_jogos):
            if key == 0:  # ignora o zero-index, pois nenhuma numerologia darah zero.
                continue

            percent: float = cp.numerologias_percentos[key]
            output += f"\t {key} numero:  {formatf(percent,'6.2')}% ... #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Numerologias Resultantes: {output}")

        # efetua analise diferencial dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise TOTAL de numerologia dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # printa a numerologia de cada sorteio dos concursos:
        output: str = f"\n\t ? NUMERO     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(cp.numerologias_concursos):
            if key == 0:  # ignora o zero-index, pois nenhuma numerologia darah zero.
                continue

            percent: float = round((value / qtd_concursos) * 10000) / 100
            dif: float = percent - cp.numerologias_percentos[key]
            output += f"\t {key} numero:  {formatf(percent,'6.2')}% ... " \
                      f"{formatf(dif,'6.2')}%     #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Numerologias Resultantes: {output}")

        # printa quais as numerologias que repetiram no ultimo sorteio dos concursos:
        output: str = f"\n\t  ? NUMERO     PERC%       #REPETIDAS\n"
        for key, value in enumerate(cp.ultimas_numerologias_repetidas):
            percent: float = cp.ultimas_numerologias_percentos[key]
            output += f"\t {formatd(key,2)} numero:  {formatf(percent,'6.2')}%  ...  " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Concursos que repetiram a ultima numerologia: {output}")

        # efetua analise de todas as numerologias dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de FREQUENCIA de numerologias"
                     f"de dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # printa as frequencias e atrasos das numerologias em todos os sorteios ja realizados:
        output: str = f"\n\tNUMERO:   #SORTEIOS   ULTIMO     #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA    MEDIA   H.MEDIA   G.MEDIA   MEDIANA   " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in cp.frequencias_numerologias[1:]:
            output += f"\t     {serie.id}:       " \
                      f"{formatd(serie.len_sorteios,5)}    " \
                      f"{formatd(serie.ultimo_sorteio,5)}        " \
                      f"{formatd(serie.len_atrasos,5)}    " \
                      f"{formatd(serie.ultimo_atraso,5)}   " \
                      f"{formatd(serie.min_atraso,5)}  " \
                      f"{formatd(serie.max_atraso,5)}   " \
                      f"{formatd(serie.mode_atraso,5)}   " \
                      f"{formatf(serie.mean_atraso,'6.1')}    " \
                      f"{formatf(serie.hmean_atraso,'6.1')}    " \
                      f"{formatf(serie.gmean_atraso,'6.1')}    " \
                      f"{formatf(serie.median_atraso,'6.1')}   " \
                      f"{formatf(serie.varia_atraso,'9.1')}          " \
                      f"{formatf(serie.stdev_atraso,'6.1')}\n"
        logger.debug(f"{nmlot}: FREQUENCIA de Numerologias Resultantes: {output}")

        # efetua analise evolutiva de todos os concursos de maneira progressiva:
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de numerologia dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # calcula a numerologia de cada evolucao de concurso:
        concursos_passados: list[Concurso] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        list6_numerologias: list[int] = []
        for concurso_atual in loteria.concursos:
            # zera os contadores de cada numerologia:
            numerologias_passados: list[int] = cb.new_list_int(qtd_items)

            # calcula a numerologia dos concursos passados ate o concurso anterior:
            for concurso_passado in concursos_passados:
                numero_passado = cb.calc_numerology(concurso_passado.bolas)
                numerologias_passados[numero_passado] += 1

            # calcula a numerologia do concurso atual para comparar a evolucao:
            numero_atual = cb.calc_numerology(concurso_atual.bolas)
            list6_numerologias.append(numero_atual)
            # soh mantem as ultimas 6 numerologias:
            while len(list6_numerologias) > 6:
                del list6_numerologias[0]

            # printa o resultado:
            output: str = f"\n\t ? NUMERO     PERC%       %DIF%  " \
                          f"----->  CONCURSO Nr {concurso_atual.id_concurso} :  " \
                          f"Ultimos Numeros == { list(reversed(list6_numerologias))}\n"
            for key, value in enumerate(numerologias_passados):
                if key == 0:  # ignora o zero-index, pois nenhuma numerologia darah zero.
                    continue

                percent: float = round((value / qtd_concursos_passados) * 10000) / 100
                dif: float = percent - cp.numerologias_percentos[key]
                output += f"\t {key} numero:  {formatf(percent,'6.2')}% ... " \
                          f"{formatf(dif,'6.2')}%\n"
            logger.debug(f"{nmlot}: Numerologias Resultantes da EVOLUTIVA: {output}")

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
