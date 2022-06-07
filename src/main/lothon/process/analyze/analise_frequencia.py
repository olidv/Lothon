"""
   Package lothon.process
   Module  analise_frequencia.py

"""

__all__ = [
    'AnaliseFrequencia'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
import logging
import statistics as stts

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

class AnaliseFrequencia(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('frequencias_dezenas',)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Frequencia dos Concursos")

        # estrutura para a coleta de dados a partir do processamento de analise:
        self.frequencias_dezenas: Optional[list[SerieSorteio]] = None

    # --- METODOS STATIC -----------------------------------------------------

    # --- PROCESSAMENTO ------------------------------------------------------

    def init(self, parms: dict):
        # absorve os parametros fornecidos:
        super().init(parms)

        # inicializa as estruturas de coleta de dados:
        self.frequencias_dezenas = None

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
        eh_duplo: bool = isinstance(concursos[0], ConcursoDuplo)
        # if eh_duplo:
        #     fator_sorteios: int = 2
        # else:
        #     fator_sorteios: int = 1
        # qtd_sorteios: int = qtd_concursos * fator_sorteios
        qtd_items: int = payload.qtd_bolas

        # efetua analise de todas as dezenas dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de frequencia de TODAS as "
                     f"dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de frequencias e atrasos:
        self.frequencias_dezenas = self.new_list_series(qtd_items)

        # contabiliza as frequencias e atrasos das dezenas em todos os sorteios ja realizados:
        for concurso in concursos:
            # registra o concurso para cada dezena sorteada:
            for bola in concurso.bolas:
                self.frequencias_dezenas[bola].add_sorteio(concurso.id_concurso)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                # se for concurso duplo, precisa comparar as bolas do segundo sorteio:
                for bola in concurso.bolas2:
                    self.frequencias_dezenas[bola].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso | ConcursoDuplo = concursos[-1]
        for serie in self.frequencias_dezenas[1:]:
            # vai aproveitar e contabilizar as medidas estatisticas para a bola:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        # printa o resultado:
        output: str = f"\n\t BOLA:   #SORTEIOS   ULTIMO      #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA   MEDIA   H.MEDIA   G.MEDIA      MEDIANA   " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in self.frequencias_dezenas[1:]:
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
                      f"{formatf(serie.stdev_atraso,'5.1')} \n"
        logger.debug(f"{nmlot}: Frequencia de Dezenas Resultantes: {output}")

        # efetua analise de frequencias medias das dezenas em todos os concursos:
        logger.debug(f"{nmlot}: Executando analise media de frequencia das dezenas sorteadas "
                     f"em TODOS os  {formatd(qtd_concursos)}  concursos da loteria.")

        # inicializa o print de resultado dos contadores de frequencias:
        output: str = f"\n\tCONCURSO  FREQUENCIAS:   MENOR   MAIOR   MODA   MEDIA   MEDIANA\n"

        # contabiliza as frequencias das dezenas em todos os sorteios ja realizados:
        concursos_anteriores: list[Concurso | ConcursoDuplo] = [concursos[0]]
        for concurso in concursos[1:]:
            bolas_concurso: tuple[int, ...] = concurso.bolas + concurso.bolas2 if eh_duplo \
                                              else concurso.bolas
            # registra a frequencia de cada dezena sorteada no concurso corrente:
            frequencias: list[int] = [0] * len(bolas_concurso)  # uma frequencia para cada bola
            for concurso_anterior in concursos_anteriores:
                id_dezena: int = -1
                for dezena in bolas_concurso:
                    id_dezena += 1  # na primeira iteracao, vai incrementar para zero
                    if dezena in concurso_anterior.bolas:
                        frequencias[id_dezena] += 1
                    # verifica se o concurso eh duplo (dois sorteios):
                    if eh_duplo and dezena in concurso_anterior.bolas2:
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
        concursos_anteriores: list[Concurso | ConcursoDuplo] = [concursos[0]]
        for concurso in concursos[1:]:
            bolas_concurso: tuple[int, ...] = concurso.bolas + concurso.bolas2 if eh_duplo \
                                              else concurso.bolas
            # registra o atraso de cada dezena sorteada no concurso corrente:
            atrasos: list[SerieSorteio] = self.new_list_series(len(bolas_concurso)-1)
            for concurso_anterior in concursos_anteriores:
                id_dezena: int = -1
                for dezena in bolas_concurso:
                    id_dezena += 1  # na primeira iteracao, vai incrementar para zero
                    if dezena in concurso_anterior.bolas:
                        atrasos[id_dezena].add_sorteio(concurso_anterior.id_concurso)
                    # verifica se o concurso eh duplo (dois sorteios):
                    if eh_duplo and dezena in concurso_anterior.bolas2:
                        atrasos[id_dezena].add_sorteio(concurso_anterior.id_concurso)

            # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
            ultimo_concurso: Concurso | ConcursoDuplo = concursos_anteriores[-1]
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
