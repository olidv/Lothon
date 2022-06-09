"""
   Package lothon.process
   Module  analise_espacamento.py

"""

__all__ = [
    'AnaliseEspacamento'
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
from lothon.domain import Loteria, Concurso, SerieSorteio
from lothon.process.analyze.abstract_analyze import AbstractAnalyze


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseEspacamento(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('espacamentos_jogos', 'espacamentos_percentos', 'espacamentos_concursos',
                 'frequencias_espacamentos')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Espacamentos nos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.espacamentos_jogos: Optional[list[int]] = None
        self.espacamentos_percentos: Optional[list[float]] = None
        self.espacamentos_concursos: Optional[list[int]] = None
        self.frequencias_espacamentos: Optional[list[SerieSorteio | None]] = None

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def calc_espacada(cls, bolas: tuple[int, ...]) -> int:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return 0

        # calcula o espacamento medio entre cada bola:
        qtd: int = 0
        soma: int = 0
        aux: int = 0
        for num in sorted(bolas):  # tem q estar ordenada
            if aux == 0:
                aux = num
            else:
                dif: int = num - aux
                soma += dif
                qtd += 1
                aux = num

        return soma // qtd

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.espacamentos_jogos = None
        self.espacamentos_percentos = None
        self.espacamentos_concursos = None
        self.frequencias_espacamentos = None

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
        qtd_items: int = payload.qtd_bolas // (payload.qtd_bolas_sorteio - 1)

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug(f"{nmlot}: Executando analise de espacamento dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # zera os contadores de cada espacada:
        self.espacamentos_jogos = self.new_list_int(qtd_items)
        self.espacamentos_percentos = self.new_list_float(qtd_items)

        # calcula o espacamento medio de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            vl_espacamento = self.calc_espacada(jogo)
            self.espacamentos_jogos[vl_espacamento] += 1

        # printa o resultado:
        output: str = f"\n\t  ? ESPACO     PERC%     #TOTAL\n"
        for key, value in enumerate(self.espacamentos_jogos):
            percent: float = round((value / qtd_jogos) * 1000) / 10
            self.espacamentos_percentos[key] = percent
            output += f"\t {formatd(key,2)} espaco:  {formatf(percent,'6.2')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Espacamentos Resultantes: {output}")

        # efetua analise diferencial dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise TOTAL de espacamento dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # calcula o espacamento de cada sorteio dos concursos:
        self.espacamentos_concursos = self.new_list_int(qtd_items)
        for concurso in concursos:
            vl_espacamento: int = self.calc_espacada(concurso.bolas)
            self.espacamentos_concursos[vl_espacamento] += 1

        # printa o resultado:
        output: str = f"\n\t  ? ESPACO     PERC%       %DIF%     #TOTAL\n"
        for key, value in enumerate(self.espacamentos_concursos):
            percent: float = round((value / qtd_concursos) * 100000) / 1000
            dif: float = percent - self.espacamentos_percentos[key]
            output += f"\t {formatd(key,2)} espaco:  {formatf(percent,'6.2')}% ... " \
                      f"{formatf(dif,'6.2')}%     #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Espacamentos Resultantes: {output}")

        # efetua analise de frequencia de todos os espacamentos dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de FREQUENCIA de espacamentos "
                     f"nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de frequencias e atrasos dos espacamentos:
        self.frequencias_espacamentos = self.new_list_series(qtd_items)

        # contabiliza as frequencias e atrasos dos espacamentos em todos os sorteios ja realizados:
        for concurso in concursos:
            # contabiliza a frequencia dos espacamentos do concurso:
            vl_espacamento: int = self.calc_espacada(concurso.bolas)
            self.frequencias_espacamentos[vl_espacamento].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_espacamentos:
            # vai aproveitar e contabilizar as medidas estatisticas para o espacamento:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        # printa o resultado:
        output: str = f"\n\tESPACO:   #SORTEIOS   ULTIMO     #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA    MEDIA   H.MEDIA   G.MEDIA   MEDIANA   " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in self.frequencias_espacamentos:
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
                      f"{formatf(serie.stdev_atraso,'7.1')} \n"
        logger.debug(f"{nmlot}: FREQUENCIA de Espacamentos Resultantes: {output}")

        # efetua analise evolutiva de todos os concursos de maneira progressiva:
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de espacamento dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # calcula espacamentos de cada evolucao de concurso:
        concursos_passados: list[Concurso] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        list6_espacamentos: list[int] = []
        for concurso_atual in payload.concursos:
            # zera os contadores de cada sequencia:
            espacamentos_passados: list[int] = self.new_list_int(qtd_items)

            # calcula o espacamento nos concursos passados ate o concurso anterior:
            for concurso_passado in concursos_passados:
                vl_espacamento_passado = self.calc_espacada(concurso_passado.bolas)
                espacamentos_passados[vl_espacamento_passado] += 1

            # calcula a distancia do concurso atual para comparar a evolucao:
            vl_espacamento_atual = self.calc_espacada(concurso_atual.bolas)
            list6_espacamentos.append(vl_espacamento_atual)
            # soh mantem as ultimas 6 sequencias:
            while len(list6_espacamentos) > 6:
                del list6_espacamentos[0]

            # printa o resultado:
            output: str = f"\n\t  ? ESPACO     PERC%        %DIF%  " \
                          f"----->  CONCURSO Nr {concurso_atual.id_concurso} :  " \
                          f"Ultimos Espacamentos == { list(reversed(list6_espacamentos))}\n"
            for key, value in enumerate(espacamentos_passados):
                percent: float = round((value / qtd_concursos_passados) * 1000) \
                                 / 10
                dif: float = percent - self.espacamentos_percentos[key]
                output += f"\t {formatd(key,2)} espaco:  {formatf(percent,'6.2')}% ... " \
                          f"{formatf(dif,'7.2')}%\n"
            logger.debug(f"{nmlot}: Espacamentos Resultantes da EVOLUTIVA: {output}")

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE DE JOGOS ---------------------------------------------------

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        self.set_options(parms)

    def evaluate(self, pick) -> float:
        # probabilidade de acerto depende do numero de pares no jogo:
        vl_espacamento = self.calc_espacada(pick)
        percent: float = self.espacamentos_percentos[vl_espacamento]

        # ignora valores muito baixos de probabilidade:
        if percent < 5:
            return 0
        else:
            return 1 + (percent / 100)

# ----------------------------------------------------------------------------
