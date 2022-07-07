"""
   Package lothon.process.compute
   Module  compute_colunario.py

"""

__all__ = [
    'ComputeColunario'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
import itertools as itt
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

class ComputeColunario(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('colunarios_jogos', 'colunarios_percentos', 
                 'colunarios_concursos', 'str_colunarios_concursos',
                 'ultimos_colunarios_repetidos', 'ultimos_colunarios_percentos',
                 'str_colunarios_ultimo_concurso', 'str_colunarios_penultimo_concurso',
                 'frequencias_colunarios')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, threshold: int = 5):  # threshold minimo de 5% para filtro mais eficaz...
        super().__init__("Computacao de Colunario nos Concursos", threshold)

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.colunarios_jogos: Optional[list[int]] = None
        self.colunarios_percentos: Optional[list[float]] = None
        self.colunarios_concursos: Optional[list[int]] = None
        self.str_colunarios_concursos: Optional[list[str]] = None
        self.ultimos_colunarios_repetidos: int = 0
        self.ultimos_colunarios_percentos: float = 0.0
        self.str_colunarios_ultimo_concurso: str = ''
        self.str_colunarios_penultimo_concurso: str = ''
        self.frequencias_colunarios: Optional[list[SerieSorteio]] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

        # efetua analise de todas as combinacoes de jogos da loteria:
        qtd_items: int = 9
        self.colunarios_jogos = cb.new_list_int(qtd_items)
        range_jogos: range = range(1, self.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, self.qtd_bolas_sorteio):
            # contabiliza os colunarios de cada combinacao de jogo:
            cb.count_colunarios(jogo, self.colunarios_jogos)

        # contabiliza o percentual dos colunarios:
        self.colunarios_percentos = cb.new_list_float(qtd_items)
        total: int = self.qtd_bolas_sorteio * self.qtd_jogos
        for key, value in enumerate(self.colunarios_jogos):
            percent: float = round((value / total) * 10000) / 100
            self.colunarios_percentos[key] = percent

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, concursos: list[Concurso]) -> int:
        # valida se possui concursos a serem analisados:
        if concursos is None or len(concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        qtd_concursos: int = len(concursos)
        qtd_items: int = 9

        # contabiliza colunarios de cada sorteio ja realizado:
        self.colunarios_concursos = cb.new_list_int(qtd_items)
        self.str_colunarios_concursos = [None]  # deixa o primeiro item, zero-index, ja preenchido
        self.ultimos_colunarios_repetidos = 0
        self.str_colunarios_ultimo_concurso = ''
        self.str_colunarios_penultimo_concurso = ''
        for concurso in concursos:
            cb.count_colunarios(concurso.bolas, self.colunarios_concursos)
            # gera a representacao string do colunario para registro e comparacao:
            colunarios: list[int] = cb.new_list_int(qtd_items)
            cb.count_colunarios(concurso.bolas, colunarios)
            str_colunarios: str = cb.to_string(colunarios)
            self.str_colunarios_concursos.append(str_colunarios)
            # verifica se repetiu os colunarios do ultimo concurso:
            if str_colunarios == self.str_colunarios_ultimo_concurso:
                self.ultimos_colunarios_repetidos += 1
            # atualiza ambos flags, para ultimo e penultimo concursos
            self.str_colunarios_penultimo_concurso = self.str_colunarios_ultimo_concurso
            self.str_colunarios_ultimo_concurso = str_colunarios

        # contabiliza o percentual dos colunarios repetidos:
        self.ultimos_colunarios_percentos = round((self.ultimos_colunarios_repetidos /
                                                   qtd_concursos) * 10000) / 100

        # contabiliza as frequencias e atrasos dos colunarios em todos os sorteios ja realizados:
        self.frequencias_colunarios = cb.new_list_series(qtd_items)
        for concurso in concursos:
            # contabiliza a frequencia dos colunarios do concurso:
            for num in concurso.bolas:
                coluna: int = cb.get_colunario(num)
                self.frequencias_colunarios[coluna].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_colunarios:
            # vai aproveitar e contabilizar as medidas estatisticas para a coluna:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f" para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def rate(self, ordinal: int, jogo: tuple) -> int:
        return 1

    def eval(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de cada colunario no jogo:
        colunarios: list[int] = cb.new_list_int(9)
        cb.count_colunarios(jogo, colunarios)
        fator_percent: float = 0
        for key, value in enumerate(colunarios):
            if value > 0:
                # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
                fator_percent += to_redutor(self.colunarios_percentos[key]) ** value

        # gera a representacao string do colunario para comparacao:
        str_colunarios: str = cb.to_string(colunarios)

        # verifica se esse jogo repetiu os colunarios do ultimo e penultimo concursos:
        if str_colunarios != self.str_colunarios_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif str_colunarios == self.str_colunarios_ultimo_concurso == \
                self.str_colunarios_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao dos ultimos colunarios:
        if self.ultimos_colunarios_percentos < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir os colunarios:
            return fator_percent * to_redutor(self.ultimos_colunarios_percentos)

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de cada colunario no jogo:
        colunarios: list[int] = cb.new_list_int(9)
        cb.count_colunarios(jogo, colunarios)
        fator_percent: float = 1.0
        for key, value in enumerate(colunarios):
            if value > 0:
                # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
                fator_percent *= to_fator(self.colunarios_percentos[key]) ** value

        # gera a representacao string do colunario para comparacao:
        str_colunarios: str = cb.to_string(colunarios)

        # verifica se esse jogo repetiu os colunarios do ultimo e penultimo concursos:
        if str_colunarios != self.str_colunarios_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif str_colunarios == self.str_colunarios_ultimo_concurso == \
                self.str_colunarios_penultimo_concurso:
            return fator_percent * .1  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao dos ultimos colunarios:
        if self.ultimos_colunarios_percentos < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir os colunarios:
            return fator_percent * to_redutor(self.ultimos_colunarios_percentos)

# ----------------------------------------------------------------------------
