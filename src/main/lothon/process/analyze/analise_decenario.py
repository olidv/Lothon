"""
   Package lothon.process
   Module  analise_decenario.py

"""

__all__ = [
    'AnaliseDecenario'
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

class AnaliseDecenario(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('decenarios_jogos', 'decenarios_percentos', 'decenarios_concursos',
                 'frequencias_decenarios')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Decenario nos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.decenarios_jogos: Optional[list[int]] = None
        self.decenarios_percentos: Optional[list[float]] = None
        self.decenarios_concursos: Optional[list[int]] = None
        self.frequencias_decenarios: Optional[list[SerieSorteio | None]] = None

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def get_decenario(cls, dezena: int) -> int:
        if dezena is not None and dezena > 0:
            return (dezena - 1) // 10
        else:
            return 0

    @classmethod
    def count_decenarios(cls, bolas: tuple[int, ...], decenario: list[int]) -> None:
        # valida os parametros:
        if bolas is None or len(bolas) == 0 or decenario is None or len(decenario) == 0:
            return

        for num in bolas:
            decenario[cls.get_decenario(num)] += 1

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.decenarios_jogos = None
        self.decenarios_percentos = None
        self.decenarios_concursos = None
        self.frequencias_decenarios = None

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
        qtd_items: int = (payload.qtd_bolas-1) // 10

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_jogos: int = math.comb(payload.qtd_bolas, payload.qtd_bolas_sorteio)
        logger.debug(f"{nmlot}: Executando analise de decenario dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # zera os contadores de cada decenario:
        self.decenarios_jogos = self.new_list_int(qtd_items)
        self.decenarios_percentos = self.new_list_float(qtd_items)

        # contabiliza os decenarios de cada combinacao de jogo:
        range_jogos: range = range(1, payload.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, payload.qtd_bolas_sorteio):
            self.count_decenarios(jogo, self.decenarios_jogos)

        # printa o resultado:
        output: str = f"\n\t ? DEZENA     PERC%     #TOTAL\n"
        total: int = payload.qtd_bolas_sorteio * qtd_jogos
        for key, value in enumerate(self.decenarios_jogos):
            percent: float = round((value / total) * 1000) / 10
            self.decenarios_percentos[key] = percent
            output += f"\t {key} dezena:  {formatf(percent,'6.2')}% ... #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Decenarios Resultantes: {output}")

        # efetua analise diferencial dos concursos com todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise TOTAL de decenarios dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de cada sequencia:
        self.decenarios_concursos = self.new_list_int(qtd_items)

        # contabiliza decenarios de cada sorteio ja realizado:
        for concurso in concursos:
            self.count_decenarios(concurso.bolas, self.decenarios_concursos)

        # printa o resultado:
        output: str = f"\n\t ? DEZENA     PERC%       %DIF%     #TOTAL\n"
        total: int = payload.qtd_bolas_sorteio * qtd_concursos
        for key, value in enumerate(self.decenarios_concursos):
            percent: float = round((value / total) * 10000) / 100
            dif: float = percent - self.decenarios_percentos[key]
            output += f"\t {key} dezena:  {formatf(percent,'6.2')}% ... {formatf(dif,'6.2')}%  " \
                      f"   #{formatd(value)}\n"
        logger.debug(f"{nmlot}: Decenarios Resultantes: {output}")

        # efetua analise de frequencia de todos os decenarios dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de FREQUENCIA de decenarios "
                     f"nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de frequencias e atrasos dos decenarios:
        self.frequencias_decenarios = self.new_list_series(qtd_items)
        self.frequencias_decenarios[0] = SerieSorteio(0)  # neste caso especifico tem a dezena zero

        # contabiliza as frequencias e atrasos dos decenarios em todos os sorteios ja realizados:
        for concurso in concursos:
            # contabiliza a frequencia dos decenarios do concurso:
            for num in concurso.bolas:
                dezena: int = self.get_decenario(num)
                self.frequencias_decenarios[dezena].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_decenarios:
            # vai aproveitar e contabilizar as medidas estatisticas para a dezena:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        # printa o resultado:
        output: str = f"\n\tDEZENA:   #SORTEIOS   ULTIMO     #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA    MEDIA   H.MEDIA   G.MEDIA   MEDIANA   " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in self.frequencias_decenarios:
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
        logger.debug(f"{nmlot}: FREQUENCIA de Decenarios Resultantes: {output}")

        # efetua analise evolutiva de todos os concursos de maneira progressiva:
        logger.debug(f"{nmlot}: Executando analise EVOLUTIVA de decenario dos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # contabiliza decenarios de cada evolucao de concurso:
        concursos_passados: list[Concurso] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        for concurso_atual in payload.concursos:
            # zera os contadores de cada decenario:
            decenarios_passados: list[int] = self.new_list_int(qtd_items)

            # calcula a decenario dos concursos passados ate o concurso anterior:
            for concurso_passado in concursos_passados:
                self.count_decenarios(concurso_passado.bolas, decenarios_passados)

            # calcula a decenario do concurso atual para comparar a evolucao:
            decenario_atual: list[int] = self.new_list_int(qtd_items)
            self.count_decenarios(concurso_atual.bolas, decenario_atual)

            # printa o resultado:
            output: str = f"\n\t ? DEZENA     PERC%       %DIF%  " \
                          f"----->  CONCURSO Nr {concurso_atual.id_concurso} :  " \
                          f"Ultimo Decenario == {decenario_atual}\n"
            total: int = payload.qtd_bolas_sorteio * qtd_concursos_passados
            for key, value in enumerate(decenarios_passados):
                percent: float = round((value / total) * 10000) / 100
                dif: float = percent - self.decenarios_percentos[key]
                output += f"\t {key} dezena:  {formatf(percent,'6.2')}% ... {formatf(dif,'6.2')}%\n"
            logger.debug(f"{nmlot}: Decenarios Resultantes da EVOLUTIVA: {output}")

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

    def evaluate(self, payload) -> float:
        return 1.1  # valor temporario

# ----------------------------------------------------------------------------
