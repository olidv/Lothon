"""
   Package lothon.process
   Module  analise_numerologia.py

"""

__all__ = [
    'AnaliseNumerologia'
]

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

class AnaliseNumerologia(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('numerologias_jogos', 'numerologias_percentos', 'numerologias_concursos',
                 'frequencias_numelogias')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Numerologia das Dezenas")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.numerologias_jogos: Optional[list[int]] = None
        self.numerologias_percentos: Optional[list[float]] = None
        self.numerologias_concursos: Optional[list[int]] = None
        self.frequencias_numelogias: Optional[list[SerieSorteio | None]] = None

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def calc_numerology(cls, bolas: tuple[int, ...]) -> int:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return 0

        return numerology(bolas)

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.numerologias_jogos = None
        self.numerologias_percentos = None
        self.numerologias_concursos = None
        self.frequencias_numelogias = None

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
        qtd_items: int = 9  # numero de zero a nove

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug(f"{nmlot}: Executando analise de numerologia dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # zera os contadores de cada somatorio:
        self.numerologias_jogos = self.new_list_int(qtd_items)
        self.numerologias_percentos = self.new_list_float(qtd_items)

        # calcula a numerologia de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            numero: int = self.calc_numerology(jogo)
            self.numerologias_jogos[numero] += 1

        # printa o resultado:
        output: str = f"\n\t ? NUMERO     PERC%     #TOTAL\n"
        for key, value in enumerate(self.numerologias_jogos):
            if key == 0:  # ignora o zero-index, pois nenhuma numerologia darah zero.
                continue

            percent: float = round((value / qtd_jogos) * 10000) / 100
            self.numerologias_percentos[key] = percent
            output += f"\t {key} numero:  {formatf(percent,'6.2')}% ... #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Numerologias Resultantes: {output}")

        #
        logger.debug(f"{nmlot}: Executando analise TOTAL de numerologia dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # calcula a numerologia de cada sorteio dos concursos:
        self.numerologias_concursos = self.new_list_int(qtd_items)
        for concurso in concursos:
            numero: int = self.calc_numerology(concurso.bolas)
            self.numerologias_concursos[numero] += 1
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                numero: int = self.calc_numerology(concurso.bolas2)
                self.numerologias_concursos[numero] += 1

        # printa o resultado:
        output: str = f"\n\t ? NUMERO     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(self.numerologias_concursos):
            if key == 0:  # ignora o zero-index, pois nenhuma numerologia darah zero.
                continue

            percent: float = round((value / qtd_sorteios) * 100000) / 1000
            dif: float = percent - self.numerologias_percentos[key]
            output += f"\t {key} numero:  {formatf(percent,'6.2')}% ... " \
                      f"{formatf(dif,'6.2')}%     #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Numerologias Resultantes: {output}")

        #
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de numerologia dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # calcula a numerologia de cada evolucao de concurso:
        concursos_passados: list[Concurso | ConcursoDuplo] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        list6_numerologias: list[int] = []
        concurso_atual: Concurso | ConcursoDuplo
        for concurso_atual in payload.concursos:
            # zera os contadores de cada numerologia:
            numerologias_passados: list[int] = self.new_list_int(qtd_items)

            # calcula a numerologia dos concursos passados ate o concurso anterior:
            for concurso_passado in concursos_passados:
                numero_passado = self.calc_numerology(concurso_passado.bolas)
                numerologias_passados[numero_passado] += 1
                # verifica se o concurso eh duplo (dois sorteios):
                if eh_duplo:
                    numero_passado = self.calc_numerology(concurso_passado.bolas2)
                    numerologias_passados[numero_passado] += 1

            # calcula a numerologia do concurso atual para comparar a evolucao:
            numero_atual = self.calc_numerology(concurso_atual.bolas)
            str_numero_atual = str(numero_atual)
            list6_numerologias.append(numero_atual)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                qtd_numero2_atual = self.calc_numerology(concurso_atual.bolas2)
                str_numero_atual += '/' + str(qtd_numero2_atual)
                list6_numerologias.append(qtd_numero2_atual)
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

                percent: float = round((value / (qtd_concursos_passados*fator_sorteios))
                                       * 1000) / 10
                dif: float = percent - self.numerologias_percentos[key]
                output += f"\t {key} numero:  {formatf(percent,'6.2')}% ... " \
                          f"{formatf(dif,'6.2')}%\n"
            logger.debug(f"{nmlot}: Numerologias Resultantes da EVOLUTIVA: {output}")

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        # efetua analise de todas as numerologias dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de FREQUENCIA de numerologias"
                     f"de dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de frequencias e atrasos das numerologias:
        self.frequencias_numelogias = self.new_list_series(qtd_items)
        self.frequencias_numelogias[0] = None  # nao ha numerologia com zero

        # contabiliza as frequencias e atrasos das numerologias em todos os sorteios ja realizados:
        concurso_anterior: Optional[Concurso | ConcursoDuplo] = None
        for concurso in concursos:
            # o primeiro concurso soh eh registrado para teste no proximo:
            if concurso_anterior is None:
                concurso_anterior = concurso
                continue

            # contabiliza a numerologia do concurso:
            numero = self.calc_numerology(concurso.bolas)
            self.frequencias_numelogias[numero].add_sorteio(concurso.id_concurso)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                numero = self.calc_numerology(concurso.bolas2)
                self.frequencias_numelogias[numero].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso | ConcursoDuplo = concursos[-1]
        for serie in self.frequencias_numelogias[1:]:
            # vai aproveitar e contabilizar as medidas estatisticas para a numerologia:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        # printa o resultado:
        output: str = f"\n\tNUMERO:   #SORTEIOS   ULTIMO     #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA    MEDIA   H.MEDIA   G.MEDIA   MEDIANA   " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in self.frequencias_numelogias[1:]:
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
                      f"{formatf(serie.stdev_atraso,'6.1')} \n"
        logger.debug(f"{nmlot}: FREQUENCIA de Numerologias Resultantes: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        pass

    def evaluate(self, payload) -> float:
        pass

# ----------------------------------------------------------------------------
