"""
   Package lothon.process.compute
   Module  compute_ausencia.py

"""

__all__ = [
    'ComputeAusencia'
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
from lothon.domain import Loteria, Concurso
from lothon.process.compute.abstract_compute import AbstractCompute


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# constante com numero de topos a serem extraidos para criar ranking de top-dezenas:
QTD_TOPOS_RANKING: int = 10


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class ComputeAusencia(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('topos_concursos', 'topos_dezenas', 'topos_ausentes', 'topos_percentos',
                 'ultimos_topos_repetidos', 'ultimos_topos_percentos',
                 'qtd_topos_ultimo_concurso', 'qtd_topos_penultimo_concurso',
                 'qtd_zerados')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao da Ausencia das Dezenas")

        # estrutura para a coleta de dados a partir do processamento de analise:
        self.topos_concursos: Optional[list[int]] = None
        self.topos_dezenas: Optional[list[int]] = None
        self.topos_ausentes: Optional[list[int]] = None
        self.topos_percentos: Optional[list[float]] = None
        self.ultimos_topos_repetidos: Optional[list[int]] = None
        self.ultimos_topos_percentos: Optional[list[float]] = None
        self.qtd_topos_ultimo_concurso: int = 0
        self.qtd_topos_penultimo_concurso: int = 0
        self.qtd_zerados: int = 0

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- METODOS ------------------------------------------------------------

    def count_topos_ausencia(self, bolas: tuple[int, ...]) -> int:
        qtd_topos: int = cb.count_recorrencias(bolas, self.topos_dezenas)
        return qtd_topos

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, loteria: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if loteria is None or loteria.concursos is None or len(loteria.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = loteria.nome_loteria
        concursos: list[Concurso] = loteria.concursos
        qtd_concursos: int = len(concursos)
        # qtd_items: int = loteria.qtd_bolas

        # contabiliza os atrasos evolutivos das dezenas para extrair os topos mais frequentes:
        self.topos_concursos = cb.new_list_int(qtd_concursos)  # registro o topo de cada concurso
        self.topos_ausentes = cb.new_list_int(QTD_TOPOS_RANKING)
        self.ultimos_topos_repetidos = cb.new_list_int(QTD_TOPOS_RANKING)
        self.qtd_topos_ultimo_concurso = -1
        self.qtd_topos_penultimo_concurso = -1

        concursos_anteriores: list[Concurso] = concursos[:1]
        for concurso in concursos[1:]:
            # extrai o topo do ranking com as dezenas com maior ausencia:
            topos_concurso: list[int] = cb.calc_topos_ausencia(concursos_anteriores,
                                                               loteria.qtd_bolas, QTD_TOPOS_RANKING)

            # identifica o numero de dezenas do concurso que estao entre o topo de ausencia:
            qtd_topos: int = cb.count_recorrencias(concurso.bolas, topos_concurso)
            self.topos_concursos[concurso.id_concurso] = qtd_topos
            self.topos_ausentes[qtd_topos] += 1

            # verifica se repetiu o numero de topos do ultimo concurso:
            if qtd_topos == self.qtd_topos_ultimo_concurso:
                self.ultimos_topos_repetidos[qtd_topos] += 1
            # atualiza ambos flags, para ultimo e penultimo concursos
            self.qtd_topos_penultimo_concurso = self.qtd_topos_ultimo_concurso
            self.qtd_topos_ultimo_concurso = qtd_topos

            # adiciona o concurso atual para a proxima iteracao (ai ele sera um concurso anterior):
            concursos_anteriores.append(concurso)

        # extrai os topos do ranking com as dezenas com maior ausencia em todos os concursos:
        self.topos_dezenas = cb.calc_topos_ausencia(concursos, loteria.qtd_bolas, QTD_TOPOS_RANKING)

        # contabiliza o percentual dos topos dos concursos:
        self.topos_percentos = cb.new_list_float(QTD_TOPOS_RANKING)
        for key, value in enumerate(self.topos_ausentes):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.topos_percentos[key] = percent

        # contabiliza o percentual dos ultimos topos:
        self.ultimos_topos_percentos = cb.new_list_float(QTD_TOPOS_RANKING)
        for key, value in enumerate(self.ultimos_topos_repetidos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.ultimos_topos_percentos[key] = percent

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de topos no jogo:
        qtd_topos: int = self.count_topos_ausencia(jogo)
        percent: float = self.topos_percentos[qtd_topos]

        # ignora valores muito baixos de probabilidade:
        if percent < 2:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_fator(percent)

        # verifica se esse jogo repetiu o numero de topos do ultimo e penultimo concursos:
        if qtd_topos != self.qtd_topos_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif qtd_topos == self.qtd_topos_ultimo_concurso == self.qtd_topos_penultimo_concurso:
            self.qtd_zerados += 1
            return 0  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao do ultimo numero de topos:
        percent_repetido: float = self.ultimos_topos_percentos[qtd_topos]
        if percent_repetido < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir o numero de topos:
            return fator_percent * to_redutor(percent_repetido)

# ----------------------------------------------------------------------------
