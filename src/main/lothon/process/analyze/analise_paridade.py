"""
   Package lothon.process
   Module  analise_paridade.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
import math
import itertools as itt
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.domain import Loteria, Concurso, ConcursoDuplo, SerieSorteio
from lothon.process.analyze.abstract_analyze import AbstractAnalyze


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
    __slots__ = '_id_process', '_options'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Paridade das Dezenas")

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def count_pares(bolas: tuple[int, ...]) -> int:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return 0

        qtd_pares: int = 0
        for bola in bolas:
            if (bola % 2) == 0:
                qtd_pares += 1

        return qtd_pares

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # o numero de sorteios realizados pode dobrar se for instancia de ConcursoDuplo:
        nmlot: str = payload.nome_loteria
        concursos: list[Concurso | ConcursoDuplo] = payload.concursos
        qtd_concursos: int = len(concursos)
        eh_duplo: bool = (concursos[0] is ConcursoDuplo)
        if eh_duplo:
            fator_sorteios: int = 2
        else:
            fator_sorteios: int = 1
        qtd_sorteios: int = qtd_concursos * fator_sorteios
        qtd_items: int = payload.qtd_bolas_sorteio

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug(f"{nmlot}: Executando analise de paridade dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # zera os contadores de cada paridade:
        paridades_jogos: list[int] = self.new_list_int(qtd_items)
        percentos_jogos: list[float] = self.new_list_float(qtd_items)

        # contabiliza pares (e impares) de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            qtd_pares: int = self.count_pares(jogo)
            paridades_jogos[qtd_pares] += 1

        # printa o resultado:
        output: str = f"\n\t  ? PARES     PERC%     #TOTAL\n"
        for key, value in enumerate(paridades_jogos):
            percent: float = round((value / qtd_jogos) * 1000) / 10
            percentos_jogos[key] = percent
            output += f"\t {formatd(key,2)} pares:  {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Paridades Resultantes: {output}")

        #
        logger.debug(f"{nmlot}: Executando analise TOTAL de paridade dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # contabiliza pares (e impares) de cada sorteio dos concursos:
        paridades_concursos: list[int] = self.new_list_int(qtd_items)
        for concurso in concursos:
            qtd_pares: int = self.count_pares(concurso.bolas)
            paridades_concursos[qtd_pares] += 1
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                qtd_pares: int = self.count_pares(concurso.bolas2)
                paridades_concursos[qtd_pares] += 1

        # printa o resultado:
        output: str = f"\n\t  ? PARES     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(paridades_concursos):
            percent: float = round((value / qtd_sorteios) * 100000) / 1000
            dif: float = percent - percentos_jogos[key]
            output += f"\t {formatd(key,2)} pares:  {formatf(percent,'6.2')}% ... " \
                      f"{formatf(dif,'6.2')}%     #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Paridades Resultantes: {output}")

        #
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de paridade dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # contabiliza pares (e impares) de cada evolucao de concurso:
        concursos_passados: list[Concurso | ConcursoDuplo] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        list6_paridades: list[int] = []
        concurso_atual: Concurso | ConcursoDuplo
        for concurso_atual in payload.concursos:
            # zera os contadores de cada paridade:
            paridades_passados: list[int] = self.new_list_int(qtd_items)

            # calcula a paridade dos concursos passados ate o concurso anterior:
            for concurso_passado in concursos_passados:
                qtd_pares_passado = self.count_pares(concurso_passado.bolas)
                paridades_passados[qtd_pares_passado] += 1
                # verifica se o concurso eh duplo (dois sorteios):
                if eh_duplo:
                    qtd_pares_passado = self.count_pares(concurso_passado.bolas2)
                    paridades_passados[qtd_pares_passado] += 1

            # calcula a paridade do concurso atual para comparar a evolucao:
            qtd_pares_atual = self.count_pares(concurso_atual.bolas)
            str_pares_atual = str(qtd_pares_atual)
            list6_paridades.append(qtd_pares_atual)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                qtd_pares2_atual = self.count_pares(concurso_atual.bolas2)
                str_pares_atual += '/' + str(qtd_pares2_atual)
                list6_paridades.append(qtd_pares2_atual)
            # soh mantem os ultimos 6 pares:
            while len(list6_paridades) > 6:
                del list6_paridades[0]

            # printa o resultado:
            output: str = f"\n\t  ? PARES     PERC%       %DIF%  " \
                          f"----->  CONCURSO Nr {concurso_atual.id_concurso} :  " \
                          f"Ultimos Pares == { list(reversed(list6_paridades))}\n"
            for key, value in enumerate(paridades_passados):
                percent: float = round((value / (qtd_concursos_passados*fator_sorteios)) * 1000) \
                                 / 10
                dif: float = percent - percentos_jogos[key]
                output += f"\t {formatd(key,2)} pares:  {formatf(percent,'6.2')}% ... " \
                          f"{formatf(dif,'6.2')}%\n"
            logger.debug(f"{nmlot}: Paridades Resultantes da EVOLUTIVA: {output}")

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        # efetua analise de todas as paridades dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de FREQUENCIA de paridades"
                     f"de dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de frequencias e atrasos das paridades:
        frequencias_paridades: list[Optional[SerieSorteio]] = self.new_list_series(qtd_items)
        frequencias_paridades[0] = SerieSorteio(0)  # neste caso especifico tem a paridade zero!

        # contabiliza as frequencias e atrasos das paridades em todos os sorteios ja realizados:
        concurso_anterior: Optional[Concurso | ConcursoDuplo] = None
        for concurso in concursos:
            # o primeiro concurso soh eh registrado para teste no proximo:
            if concurso_anterior is None:
                concurso_anterior = concurso
                continue

            # contabiliza o numero de paridades do concurso:
            qtd_pares = self.count_pares(concurso.bolas)
            frequencias_paridades[qtd_pares].add_sorteio(concurso.id_concurso)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                qtd_pares = self.count_pares(concurso.bolas2)
                frequencias_paridades[qtd_pares].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso | ConcursoDuplo = concursos[-1]
        for serie in frequencias_paridades:
            # vai aproveitar e contabilizar as medidas estatisticas para a paridade:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        # printa o resultado:
        output: str = f"\n\tPARES:   #SORTEIOS   ULTIMO     #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA    MEDIA   H.MEDIA   G.MEDIA   MEDIANA   " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in frequencias_paridades:
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
                      f"{formatf(serie.stdev_atraso,'7.1')} \n"
        logger.debug(f"{nmlot}: FREQUENCIA de Paridades Resultantes: {output}")

        # salva os dados resultantes da analise para utilizacao em simulacoes e geracoes de boloes:
        payload.statis["paridades_jogos"] = paridades_jogos
        payload.statis["paridades_percentos"] = percentos_jogos
        payload.statis["paridades_concursos"] = paridades_concursos
        payload.statis["frequencias_paridades"] = frequencias_paridades

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def init(self, options: dict):
        self.options = options

    def evaluate(self, payload) -> float:
        pass

# ----------------------------------------------------------------------------
