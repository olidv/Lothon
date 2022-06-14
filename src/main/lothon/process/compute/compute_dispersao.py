"""
   Package lothon.process.compute
   Module compute_dispersao.py

"""

__all__ = [
    'ComputeDispersao'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
import logging
import math
import statistics as stts

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


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class ComputeDispersao(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('frequencias_dezenas', 'atrasos_dezenas',
                 'dispersoes_concursos', 'dispersoes_percentos',
                 'ultimas_dispersoes_repetidas', 'ultimas_dispersoes_percentos',
                 'vl_dispersao_ultimo_concurso', 'vl_dispersao_penultimo_concurso',
                 'qtd_zerados')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Dispersao das Dezenas")

        # estrutura para a coleta de dados a partir do processamento de analise:
        self.frequencias_dezenas: Optional[list[int]] = None
        self.atrasos_dezenas: Optional[list[int]] = None
        self.dispersoes_concursos: Optional[list[int]] = None
        self.dispersoes_percentos: Optional[list[float]] = None
        self.ultimas_dispersoes_repetidas: Optional[list[int]] = None
        self.ultimas_dispersoes_percentos: Optional[list[float]] = None
        self.vl_dispersao_ultimo_concurso: int = 0
        self.vl_dispersao_penultimo_concurso: int = 0
        self.qtd_zerados: int = 0

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- METODOS ------------------------------------------------------------

    def list_frequencias(self, bolas: tuple[int, ...]) -> list[int]:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return []

        # obtem as frequencias das bolas:
        frequencias: list[int] = []
        for dezena in bolas:
            frequencias.append(self.frequencias_dezenas[dezena])

        return frequencias

    def list_atrasos(self, bolas: tuple[int, ...]) -> list[int]:
        # valida os parametros:
        if bolas is None or len(bolas) == 0:
            return []

        # obtem os atrasos das bolas:
        atrasos: list[int] = []
        for dezena in bolas:
            atrasos.append(self.atrasos_dezenas[dezena])

        return atrasos

    def calc_dispersao(self, bolas: tuple[int, ...]) -> int:
        list_frequencias: list[int] = self.list_frequencias(bolas)
        list_atrasos: list[int] = self.list_atrasos(bolas)

        # calcula as medidas estatisticas de dispersao:
        varia_frequencia: float = stts.pstdev(list_frequencias)
        varia_atrasos: float = stts.pstdev(list_atrasos)

        # calcula a dispersao entre as frequencias e atrasos das dezenas:
        return round(math.sqrt(varia_frequencia * varia_atrasos))

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
        qtd_items: int = loteria.qtd_bolas

        # zera os contadores de frequencias e atrasos - usa -1 para nao conflitar com teste == 0:
        self.frequencias_dezenas = cb.new_list_int(qtd_items, -1)
        self.atrasos_dezenas = cb.new_list_int(qtd_items, -1)

        # contabiliza as frequencias e atrasos das dezenas em todos os sorteios ja realizados:
        for concurso in reversed(concursos):
            # cada ocorrencia de dezena incrementa sua respectiva frequencia:
            for dezena in concurso.bolas:
                self.frequencias_dezenas[dezena] += 1
                # contabiliza tambem os atrasos, aproveitando a ordem reversa dos concursos:
                if self.atrasos_dezenas[dezena] == -1:
                    self.atrasos_dezenas[dezena] = qtd_concursos - concurso.id_concurso

        # contabiliza as dispersoes das variancias das dezenas em todos os sorteios ja realizados:
        self.dispersoes_concursos = cb.new_list_int(qtd_items)
        self.ultimas_dispersoes_repetidas = cb.new_list_int(qtd_items)
        self.vl_dispersao_ultimo_concurso = -1
        self.vl_dispersao_penultimo_concurso = -1
        for concurso in concursos:
            faixa_dispersao: int = self.calc_dispersao(concurso.bolas)
            self.dispersoes_concursos[faixa_dispersao] += 1
            # verifica se repetiu a dispersao do ultimo concurso:
            if faixa_dispersao == self.vl_dispersao_ultimo_concurso:
                self.ultimas_dispersoes_repetidas[faixa_dispersao] += 1
            # atualiza ambos flags, para ultimo e penultimo concursos
            self.vl_dispersao_penultimo_concurso = self.vl_dispersao_ultimo_concurso
            self.vl_dispersao_ultimo_concurso = faixa_dispersao

        # como a estrutura de dispersao tem muitos elementos (100), apaga aqueles zerados ao final:
        # while len(self.dispersoes_concursos) > 0:
        #     # apaga o ultimo elemento, ate encontrar alguma posicao nao-zerada:
        #     if self.dispersoes_concursos[-1] == 0:
        #         del self.dispersoes_concursos[-1]
        #     else:
        #         break

        # calcula o percentual das dispersoes:
        self.dispersoes_percentos: list[float] = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.dispersoes_concursos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.dispersoes_percentos[key] = percent

        # contabiliza o percentual das ultimas dispersoes:
        self.ultimas_dispersoes_percentos = cb.new_list_float(qtd_items)
        for key, value in enumerate(self.ultimas_dispersoes_repetidas):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.ultimas_dispersoes_percentos[key] = percent

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do fator de dispersao do jogo:
        faixa_dispersao: int = self.calc_dispersao(jogo)
        percent: float = self.dispersoes_percentos[faixa_dispersao]

        # ignora valores muito baixos de probabilidade:
        if percent < 2:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_fator(percent)

        # verifica se esse jogo repetiu a dispersao do ultimo e penultimo concursos:
        if faixa_dispersao != self.vl_dispersao_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif faixa_dispersao == self.vl_dispersao_ultimo_concurso == \
                self.vl_dispersao_penultimo_concurso:
            self.qtd_zerados += 1
            return 0  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao da ultima dispersao:
        percent_repetida: float = self.ultimas_dispersoes_percentos[faixa_dispersao]
        if percent_repetida < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir a dispersao:
            return fator_percent * to_redutor(percent_repetida)

# ----------------------------------------------------------------------------
