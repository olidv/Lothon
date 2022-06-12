"""
   Package lothon.process.analyze
   Module  analise_frequencia.py

"""

__all__ = [
    'AnaliseFrequencia'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging
import statistics as stts

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.stats import combinatoria as cb
from lothon.domain import Loteria, Concurso, SerieSorteio
from lothon.process.analyze.abstract_analyze import AbstractAnalyze
from lothon.process.compute.compute_frequencia import ComputeFrequencia


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseFrequencia(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Frequencia dos Concursos")

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
        # qtd_items: int = payload.qtd_bolas

        # inicializa componente para computacao dos sorteios da loteria:
        cp = ComputeFrequencia()
        cp.execute(payload)

        # efetua analise de todas as dezenas dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de frequencia de TODAS as "
                     f"dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # printa as frequencias e atrasos das dezenas em todos os sorteios ja realizados:
        output: str = f"\n\t BOLA:   #SORTEIOS   ULTIMO      #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA   MEDIA   H.MEDIA   G.MEDIA      MEDIANA   " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in cp.frequencias_dezenas[1:]:
            output += f"\t  {formatd(serie.id,3)}:       " \
                      f"{formatd(serie.len_sorteios,5)}    " \
                      f"{formatd(serie.ultimo_sorteio,5)}           " \
                      f"{formatd(serie.len_atrasos,3)}      " \
                      f"{formatd(serie.ultimo_atraso,3)}     " \
                      f"{formatd(serie.min_atraso,3)}    " \
                      f"{formatd(serie.max_atraso,3)}     " \
                      f"{formatd(serie.mode_atraso,3)}   " \
                      f"{formatf(serie.mean_atraso,'5.1')}     " \
                      f"{formatf(serie.hmean_atraso,'5.1')}     " \
                      f"{formatf(serie.gmean_atraso,'5.1')}        " \
                      f"{formatf(serie.median_atraso,'5.1')}       " \
                      f"{formatf(serie.varia_atraso,'5.1')}           " \
                      f"{formatf(serie.stdev_atraso,'5.1')}\n"
        logger.debug(f"{nmlot}: Frequencia de Dezenas Resultantes: {output}")

        # efetua analise de frequencias medias das dezenas em todos os concursos:
        logger.debug(f"{nmlot}: Executando analise media de frequencia das dezenas sorteadas "
                     f"em TODOS os  {formatd(qtd_concursos)}  concursos da loteria.")

        # inicializa o print de resultado dos contadores de frequencias:
        output: str = f"\n\tCONCURSO  FREQUENCIAS:   MENOR   MAIOR   MODA   MEDIA   MEDIANA\n"

        # contabiliza as frequencias das dezenas em todos os sorteios ja realizados:
        concursos_anteriores: list[Concurso] = [concursos[0]]
        for concurso in concursos[1:]:
            bolas_concurso: tuple[int, ...] = concurso.bolas
            # registra a frequencia de cada dezena sorteada no concurso corrente:
            frequencias: list[int] = [0] * len(bolas_concurso)  # uma frequencia para cada bola
            for concurso_anterior in concursos_anteriores:
                id_dezena: int = -1
                for dezena in bolas_concurso:
                    id_dezena += 1  # na primeira iteracao, vai incrementar para zero
                    if dezena in concurso_anterior.bolas:
                        frequencias[id_dezena] += 1

            # formata os valores para o concurso atual:
            frequencias = sorted(frequencias)  # ja ordena para o calculo da mediana
            output += f"\t   {formatd(concurso.id_concurso,5)}  ............   " \
                      f"{formatd(min(frequencias),5)}   " \
                      f"{formatd(max(frequencias),5)}  " \
                      f"{formatd(round(stts.mode(frequencias)),5)}   " \
                      f"{formatd(round(stts.fmean(frequencias)),5)}     " \
                      f"{formatd(round(stts.median(frequencias)),5)}\n"

            # adiciona o concurso atual para a proxima iteracao (ai ele sera um concurso anterior):
            concursos_anteriores.append(concurso)
        # apos percorrer todos os concursos, printa as frequencias medias:
        logger.debug(f"{nmlot}: Frequencias Medias das Dezenas Sorteadas: {output}")

        # efetua analise de atrasos medios das dezenas em todos os concursos:
        logger.debug(f"{nmlot}: Executando analise media de atrasos das dezenas sorteadas "
                     f"em TODOS os  {formatd(qtd_concursos)}  concursos da loteria.")

        # inicializa o print de resultado dos contadores de frequencias:
        output1: str = f"\n\tCONCURSO  ULTIMOS ATRASOS:   MENOR   MAIOR   MODA   MEDIA   MEDIANA\n"
        output2: str = f"\n\tCONCURSO   MEDIAS ATRASOS:   MENOR   MAIOR   MODA   MEDIA   MEDIANA\n"

        # contabiliza os atrasos das dezenas em todos os sorteios ja realizados:
        concursos_anteriores: list[Concurso] = [concursos[0]]
        for concurso in concursos[1:]:
            bolas_concurso: tuple[int, ...] = concurso.bolas
            # registra o atraso de cada dezena sorteada no concurso corrente:
            atrasos: list[SerieSorteio] = cb.new_list_series(len(bolas_concurso)-1)
            for concurso_anterior in concursos_anteriores:
                id_dezena: int = -1
                for dezena in bolas_concurso:
                    id_dezena += 1  # na primeira iteracao, vai incrementar para zero
                    if dezena in concurso_anterior.bolas:
                        atrasos[id_dezena].add_sorteio(concurso_anterior.id_concurso)

            # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
            ultimo_concurso: Concurso = concursos_anteriores[-1]
            for serie in atrasos:
                # vai aproveitar e contabilizar as medidas estatisticas para o atraso:
                serie.last_sorteio(ultimo_concurso.id_concurso)

            # formata os valores para o concurso atual:
            ultimos_atrasos: list[int] = sorted([o.ultimo_atraso for o in atrasos])
            output1 += f"\t   {formatd(concurso.id_concurso,5)}  ................   " \
                       f"{formatd(min(ultimos_atrasos),5)}   " \
                       f"{formatd(max(ultimos_atrasos),5)}  " \
                       f"{formatd(round(stts.mode(ultimos_atrasos)),5)}   " \
                       f"{formatd(round(stts.fmean(ultimos_atrasos)),5)}     " \
                       f"{formatd(round(stts.median(ultimos_atrasos)),5)}\n"
            medias_atrasos: list[int] = sorted([round(o.mean_atraso) for o in atrasos])
            output2 += f"\t   {formatd(concurso.id_concurso,5)}  ................   " \
                       f"{formatd(min(medias_atrasos),5)}   " \
                       f"{formatd(max(medias_atrasos),5)}  " \
                       f"{formatd(round(stts.mode(medias_atrasos)),5)}   " \
                       f"{formatd(round(stts.fmean(medias_atrasos)),5)}     " \
                       f"{formatd(round(stts.median(medias_atrasos)),5)}\n"

            # adiciona o concurso atual para a proxima iteracao (ai ele sera um concurso anterior):
            concursos_anteriores.append(concurso)
        # apos percorrer todos os concursos, printa os atrasos medias:
        logger.debug(f"{nmlot}: Atrasos Medios das Dezenas Sorteadas: {output1}\n\n{output2}")

        # efetua analise evolutiva de todos os concursos de maneira progressiva:
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de frequencias dos ultimos  100  "
                     f"concursos da loteria.")

        # formata o cabecalho da impressao do resultado:
        output: str = f"\n\t CONCURSO"
        for val in range(1, payload.qtd_bolas_sorteio + 1):
            output += f"     {val:0>2}"
        output += f"     VARIANCIA     DESVIO-PADRAO\n"

        # acumula os concursos passados para cada concurso atual:
        qtd_concursos_anteriores: int = qtd_concursos - 100
        concursos_anteriores: list[Concurso] = concursos[:qtd_concursos_anteriores]
        for concurso_atual in concursos[qtd_concursos_anteriores:]:
            # zera os contadores de cada concurso:
            dezenas_sorteios: list[int] = cb.new_list_int(payload.qtd_bolas)

            # quantas vezes cada uma das bolas sorteadas do concurso atual repetiu nos anteriores:
            for concurso_anterior in concursos_anteriores:
                cb.count_ocorrencias(concurso_anterior.bolas, dezenas_sorteios)

            # transforma a lista em dicionario para sortear pela frequencia nos sorteios:
            dezenas_frequencias: dict[int: int] = {}
            for key, val in enumerate(dezenas_sorteios):
                dezenas_frequencias[key] = val

            # ordena o dicionario para identificar o ranking de cada dezena:
            dezenas_frequencias = {k: v for k, v in sorted(dezenas_frequencias.items(),
                                                           key=lambda item: item[1], reverse=True)}
            dezenas_ranking: list[int] = cb.new_list_int(payload.qtd_bolas)
            idx: int = 0
            for k, v in dezenas_frequencias.items():
                idx += 1  # comeca do ranking #1
                dezenas_ranking[k] = idx

            # prepara para calcular variancia e desvio padrao dos rankings:
            ranking_bolas: list[int] = []

            # printa o resultado do concurso atual:
            output += f"\t   {formatd(concurso_atual.id_concurso,6)}"
            for bola in concurso_atual.bolas:
                ranking: int = dezenas_ranking[bola]
                ranking_bolas.append(ranking)
                output += f"  {formatd(ranking,5)}"

            # calcula a variancia e desvio padrao dos rankings antes do fim da linha:
            varia_rank: float = stts.pvariance(ranking_bolas)
            stdev_rank: float = stts.pstdev(ranking_bolas)
            output += f"     {formatf(varia_rank,'9.3')}         {formatf(stdev_rank,'9.3')}\n"

            # inclui o concurso atual como anterior para a proxima iteracao:
            concursos_anteriores.append(concurso_atual)
        logger.debug(f"{nmlot}: Ranking de Frequencias da EVOLUTIVA: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
