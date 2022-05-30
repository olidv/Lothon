"""
   Package lothon.process
   Module  analise_sequencia.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
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

class AnaliseSequencia(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_process', '_options'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Sequencia nos Concursos")

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def count_sequencias(bolas: tuple[int, ...]) -> int:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return 0

        # eh preciso ordenar a tupla para verificar se ha sequencia:
        bolas: tuple[int, ...] = tuple(sorted(bolas))

        qtd_sequencias: int = 0
        seq_anterior: int = -1
        for num in bolas:
            if num == seq_anterior:
                qtd_sequencias += 1
            seq_anterior = num + 1

        return qtd_sequencias

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
        qtd_items: int = payload.qtd_bolas_sorteio - 1

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug(f"{nmlot}: Executando analise de sequencia dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # zera os contadores de cada sequencia:
        sequencias_jogos: list[int] = self.new_list_int(qtd_items)
        percentos_jogos: list[float] = self.new_list_float(qtd_items)

        # contabiliza sequencias de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            qt_sequencias = self.count_sequencias(jogo)
            sequencias_jogos[qt_sequencias] += 1

        # printa o resultado:
        output: str = f"\n\t  ? SEGUIDO     PERC%     #TOTAL\n"
        for key, value in enumerate(sequencias_jogos):
            percent: float = round((value / qtd_jogos) * 1000) / 10
            percentos_jogos[key] = percent
            output += f"\t {formatd(key,2)} seguido:  {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Sequencias Resultantes: {output}")

        #
        logger.debug(f"{nmlot}: Executando analise TOTAL de sequencia dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # contabiliza sequencias de cada sorteio dos concursos:
        sequencias_concursos: list[int] = self.new_list_int(qtd_items)
        for concurso in concursos:
            qt_sequencias: int = self.count_sequencias(concurso.bolas)
            sequencias_concursos[qt_sequencias] += 1
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                qt_sequencias: int = self.count_sequencias(concurso.bolas2)
                sequencias_concursos[qt_sequencias] += 1

        # printa o resultado:
        output: str = f"\n\t  ? SEGUIDO     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(sequencias_concursos):
            percent: float = round((value / qtd_sorteios) * 100000) / 1000
            dif: float = percent - percentos_jogos[key]
            output += f"\t {formatd(key,2)} seguido:  {formatf(percent,'6.2')}% ... " \
                      f"{formatf(dif,'6.2')}%     #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Sequencias Resultantes: {output}")

        #
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de sequencia dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # contabiliza dezenas sequenciais de cada evolucao de concurso:
        concursos_passados: list[Concurso | ConcursoDuplo] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        list6_sequencias: list[int] = []
        concurso_atual: Concurso | ConcursoDuplo
        for concurso_atual in payload.concursos:
            # zera os contadores de cada sequencia:
            sequencias_passadas: list[int] = self.new_list_int(qtd_items)

            # calcula a sequencia dos concursos passados ate o concurso anterior:
            for concurso_passado in concursos_passados:
                qt_sequencias_passadas = self.count_sequencias(concurso_passado.bolas)
                sequencias_passadas[qt_sequencias_passadas] += 1
                # verifica se o concurso eh duplo (dois sorteios):
                if eh_duplo:
                    qt_sequencias_passadas = self.count_sequencias(concurso_passado.bolas2)
                    sequencias_passadas[qt_sequencias_passadas] += 1

            # calcula a sequencia do concurso atual para comparar a evolucao:
            qtd_sequencias_atual = self.count_sequencias(concurso_atual.bolas)
            str_sequencias_atual = str(qtd_sequencias_atual)
            list6_sequencias.append(qtd_sequencias_atual)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                qtd_sequencias2_atual = self.count_sequencias(concurso_atual.bolas2)
                str_sequencias_atual += '/' + str(qtd_sequencias2_atual)
                list6_sequencias.append(qtd_sequencias2_atual)
            # soh mantem as ultimas 6 sequencias:
            while len(list6_sequencias) > 6:
                del list6_sequencias[0]

            # printa o resultado:
            output: str = f"\n\t  ? SEGUIDO     PERC%       %DIF%  " \
                          f"----->  CONCURSO Nr {concurso_atual.id_concurso} :  " \
                          f"Ultimas Sequencias == { list(reversed(list6_sequencias))}\n"
            for key, value in enumerate(sequencias_passadas):
                percent: float = round((value / (qtd_concursos_passados*fator_sorteios)) * 1000) \
                                 / 10
                dif: float = percent - percentos_jogos[key]
                output += f"\t {formatd(key,2)} seguido:  {formatf(percent,'6.2')}% ... " \
                          f"{formatf(dif,'6.2')}%\n"
            logger.debug(f"{nmlot}: Sequencias Resultantes da EVOLUTIVA: {output}")

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        # efetua analise de todas as sequencias dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de FREQUENCIA de sequencias"
                     f"de dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de frequencias e atrasos das sequencias:
        frequencias_sequencias: list[SerieSorteio | None] = self.new_list_series(qtd_items)
        frequencias_sequencias[0] = SerieSorteio(0)  # neste caso especifico tem a sequencia zero!

        # contabiliza as frequencias e atrasos das sequencias em todos os sorteios ja realizados:
        concurso_anterior: Concurso | ConcursoDuplo | None = None
        for concurso in concursos:
            # o primeiro concurso soh eh registrado para teste no proximo:
            if concurso_anterior is None:
                concurso_anterior = concurso
                continue

            # contabiliza o numero de sequencias do concurso:
            qt_sequencias = self.count_sequencias(concurso.bolas)
            frequencias_sequencias[qt_sequencias].add_sorteio(concurso.id_concurso)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                qt_sequencias = self.count_sequencias(concurso.bolas2)
                frequencias_sequencias[qt_sequencias].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso | ConcursoDuplo = concursos[-1]
        for serie in frequencias_sequencias:
            # vai aproveitar e contabilizar as medidas estatisticas para a sequencia:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        # printa o resultado:
        output: str = f"\n\tSEGUIDO:   #SORTEIOS   ULTIMO     #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA    MEDIA   H.MEDIA   G.MEDIA   MEDIANA     " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in frequencias_sequencias:
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
                      f"{formatf(serie.stdev_atraso,'7.1')} \n"
        logger.debug(f"{nmlot}: FREQUENCIA de Sequencias Resultantes: {output}")

        # salva os dados resultantes da analise para utilizacao em simulacoes e geracoes de boloes:
        payload.statis["sequencias_jogos"] = sequencias_jogos
        payload.statis["sequencias_percentos"] = percentos_jogos
        payload.statis["sequencias_concursos"] = sequencias_concursos
        payload.statis["frequencias_sequencias"] = frequencias_sequencias

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
