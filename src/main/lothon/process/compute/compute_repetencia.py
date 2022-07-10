"""
   Package lothon.process.compute
   Module  compute_repetencia.py

"""

__all__ = [
    'ComputeRepetencia'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.stats import combinatoria as cb
from lothon.domain import Concurso, SerieSorteio
from lothon.process.compute.abstract_compute import AbstractCompute


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class ComputeRepetencia(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('repetencias_concursos', 'repetencias_percentos', 'repetencias_series',
                 'ultimas_repetencias_repetidas', 'ultimas_repetencias_percentos',
                 'qtd_repetencias_ultimo_concurso', 'qtd_repetencias_penultimo_concurso',
                 'frequencias_repetencias', 'ultimo_sorteio')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, threshold: int = 5):  # threshold minimo de 5% para filtro mais eficaz...
        super().__init__("Computacao de Repetencia do Ultimo Concurso", threshold)

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.repetencias_concursos: Optional[list[int]] = None
        self.repetencias_percentos: Optional[list[float]] = None
        self.repetencias_series: Optional[list[SerieSorteio]] = None
        self.ultimas_repetencias_repetidas: Optional[list[int]] = None
        self.ultimas_repetencias_percentos: Optional[list[float]] = None
        self.qtd_repetencias_ultimo_concurso: int = 0
        self.qtd_repetencias_penultimo_concurso: int = 0
        self.frequencias_repetencias: Optional[list[SerieSorteio]] = None

        # estruturas para avaliacao de jogo combinado da loteria:
        self.ultimo_sorteio: Optional[tuple[int, ...]] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, concursos: list[Concurso]) -> int:
        # valida se possui concursos a serem analisados:
        if concursos is None or len(concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        ultimo_concurso: Concurso = concursos[-1]
        qtd_concursos: int = len(concursos)
        qtd_items: int = self.qtd_bolas_sorteio

        # salva o sorteio do ultimo concurso para o EVALUATE posterior:
        self.ultimo_sorteio = ultimo_concurso.bolas

        # zera os contadores de cada repetencia:
        self.repetencias_concursos = cb.new_list_int(qtd_items)
        self.repetencias_series = cb.new_list_series(qtd_items)
        self.frequencias_repetencias = cb.new_list_series(self.qtd_bolas)
        self.ultimas_repetencias_repetidas = cb.new_list_int(qtd_items)

        # contabiliza repetencias de cada sorteio com todos o sorteio anterior:
        concurso_anterior: Concurso = concursos[0]
        self.qtd_repetencias_ultimo_concurso = -1
        self.qtd_repetencias_penultimo_concurso = -1
        for concurso in concursos[1:]:
            qt_repeticoes: int = cb.count_repeticoes(concurso.bolas,
                                                     concurso_anterior.bolas,
                                                     self.frequencias_repetencias,
                                                     concurso.id_concurso)
            self.repetencias_concursos[qt_repeticoes] += 1
            self.repetencias_series[qt_repeticoes].add_sorteio(concurso.id_concurso)
            concurso_anterior = concurso
            # verifica se repetiu a repetencia do ultimo concurso:
            if qt_repeticoes == self.qtd_repetencias_ultimo_concurso:
                self.ultimas_repetencias_repetidas[qt_repeticoes] += 1
            # atualiza ambos flags, para ultimo e penultimo concursos
            self.qtd_repetencias_penultimo_concurso = self.qtd_repetencias_ultimo_concurso
            self.qtd_repetencias_ultimo_concurso = qt_repeticoes

        # contabiliza o percentual das repetencias:
        self.repetencias_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.repetencias_concursos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.repetencias_percentos[key] = percent

        # contabiliza as medidas estatisticas para cada repetencia:
        for serie in self.repetencias_series:
            serie.update_stats()

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        for serie in self.frequencias_repetencias[1:]:
            # vai aproveitar e contabilizar as medidas estatisticas para a bola:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        # contabiliza o percentual das ultimas repetencias:
        self.ultimas_repetencias_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.ultimas_repetencias_repetidas):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.ultimas_repetencias_percentos[key] = percent

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def set_concursos_passados(self, concursos: list[Concurso]):
        self.ultimo_sorteio = concursos[-1].bolas

    def rate(self, ordinal: int, jogo: tuple) -> int:
        qt_repeticoes: int = cb.count_dezenas_repetidas(jogo, self.ultimo_sorteio)
        return qt_repeticoes

    def eval(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de repeticoes no jogo:
        qt_repeticoes: int = cb.count_dezenas_repetidas(jogo, self.ultimo_sorteio)
        percent: float = self.repetencias_percentos[qt_repeticoes]

        # ignora valores muito baixos de probabilidade:
        if percent < self.min_threshold:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_redutor(percent)

        # verifica se esse jogo repetiu a repetencia do ultimo e penultimo concursos:
        if qt_repeticoes != self.qtd_repetencias_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif qt_repeticoes == self.qtd_repetencias_ultimo_concurso == \
                self.qtd_repetencias_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao da ultima repetencia:
        percent_repetida: float = self.ultimas_repetencias_percentos[qt_repeticoes]
        if percent_repetida < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir a repetencia:
            return fator_percent * to_redutor(percent_repetida)

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de repeticoes no jogo:
        qt_repeticoes: int = cb.count_dezenas_repetidas(jogo, self.ultimo_sorteio)
        percent: float = self.repetencias_percentos[qt_repeticoes]

        # ignora valores muito baixos de probabilidade:
        if percent < 1:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_fator(percent)

        # verifica se esse jogo repetiu a repetencia do ultimo e penultimo concursos:
        if qt_repeticoes != self.qtd_repetencias_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif qt_repeticoes == self.qtd_repetencias_ultimo_concurso == \
                self.qtd_repetencias_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao da ultima repetencia:
        percent_repetida: float = self.ultimas_repetencias_percentos[qt_repeticoes]
        if percent_repetida < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir a repetencia:
            return fator_percent * to_redutor(percent_repetida)

# ----------------------------------------------------------------------------
