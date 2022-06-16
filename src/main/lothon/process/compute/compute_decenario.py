"""
   Package lothon.process.compute
   Module  compute_decenario.py

"""

__all__ = [
    'ComputeDecenario'
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
from lothon.domain import Loteria, Concurso, SerieSorteio
from lothon.process.compute.abstract_compute import AbstractCompute


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class ComputeDecenario(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('decenarios_jogos', 'decenarios_percentos',
                 'decenarios_concursos', 'str_decenarios_concursos',
                 'ultimos_decenarios_repetidos', 'ultimos_decenarios_percentos',
                 'str_decenarios_ultimo_concurso', 'str_decenarios_penultimo_concurso',
                 'frequencias_decenarios')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Decenario nos Concursos")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.decenarios_jogos: Optional[list[int]] = None
        self.decenarios_percentos: Optional[list[float]] = None
        self.decenarios_concursos: Optional[list[int]] = None
        self.str_decenarios_concursos: Optional[list[str]] = None
        self.ultimos_decenarios_repetidos: int = 0
        self.ultimos_decenarios_percentos: float = 0.0
        self.str_decenarios_ultimo_concurso: str = ''
        self.str_decenarios_penultimo_concurso: str = ''
        self.frequencias_decenarios: Optional[list[SerieSorteio]] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, loteria: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if loteria is None or loteria.concursos is None or len(loteria.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = loteria.nome_loteria
        qtd_jogos: int = loteria.qtd_jogos
        concursos: list[Concurso] = loteria.concursos
        qtd_concursos: int = len(concursos)
        qtd_items: int = (loteria.qtd_bolas-1) // 10

        # efetua analise de todas as combinacoes de jogos da loteria:
        self.decenarios_jogos = cb.new_list_int(qtd_items)
        range_jogos: range = range(1, loteria.qtd_bolas + 1)
        for jogo in itt.combinations(range_jogos, loteria.qtd_bolas_sorteio):
            # contabiliza os decenarios de cada combinacao de jogo:
            cb.count_decenarios(jogo, self.decenarios_jogos)

        # contabiliza o percentual dos decenarios:
        self.decenarios_percentos = cb.new_list_float(qtd_items)
        total: int = loteria.qtd_bolas_sorteio * qtd_jogos
        for key, value in enumerate(self.decenarios_jogos):
            percent: float = round((value / total) * 10000) / 100
            self.decenarios_percentos[key] = percent

        # contabiliza decenarios de cada sorteio ja realizado:
        self.decenarios_concursos = cb.new_list_int(qtd_items)
        self.str_decenarios_concursos = [None]  # deixa o primeiro item, zero-index, ja preenchido
        self.ultimos_decenarios_repetidos = 0
        self.str_decenarios_ultimo_concurso = ''
        self.str_decenarios_penultimo_concurso = ''
        for concurso in concursos:
            cb.count_decenarios(concurso.bolas, self.decenarios_concursos)
            # gera a representacao string do decenario para registro e comparacao:
            decenarios: list[int] = cb.new_list_int(qtd_items)
            cb.count_decenarios(concurso.bolas, decenarios)
            str_decenarios: str = cb.to_string(decenarios)
            self.str_decenarios_concursos.append(str_decenarios)
            # verifica se repetiu os decenarios do ultimo concurso:
            if str_decenarios == self.str_decenarios_ultimo_concurso:
                self.ultimos_decenarios_repetidos += 1
            # atualiza ambos flags, para ultimo e penultimo concursos
            self.str_decenarios_penultimo_concurso = self.str_decenarios_ultimo_concurso
            self.str_decenarios_ultimo_concurso = str_decenarios

        # contabiliza o percentual dos decenarios repetidos:
        self.ultimos_decenarios_percentos = round((self.ultimos_decenarios_repetidos /
                                                   qtd_concursos) * 10000) / 100

        # contabiliza as frequencias e atrasos dos decenarios em todos os sorteios ja realizados:
        self.frequencias_decenarios = cb.new_list_series(qtd_items)
        for concurso in concursos:
            # contabiliza a frequencia dos decenarios do concurso:
            for num in concurso.bolas:
                dezena: int = cb.get_decenario(num)
                self.frequencias_decenarios[dezena].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso = concursos[-1]
        for serie in self.frequencias_decenarios:
            # vai aproveitar e contabilizar as medidas estatisticas para a dezena:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de cada decenario no jogo:
        decenarios: list[int] = cb.new_list_int(9)
        cb.count_decenarios(jogo, decenarios)
        fator_percent: float = 1.0
        for key, value in enumerate(decenarios):
            if value > 0:
                # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
                fator_percent *= to_fator(self.decenarios_percentos[key]) ** value

        # gera a representacao string do decenario para comparacao:
        str_decenarios: str = cb.to_string(decenarios)

        # verifica se esse jogo repetiu os decenarios do ultimo e penultimo concursos:
        if str_decenarios != self.str_decenarios_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif str_decenarios == self.str_decenarios_ultimo_concurso == \
                self.str_decenarios_penultimo_concurso:
            self.qtd_zerados += 1
            return 0  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao dos ultimos decenarios:
        if self.ultimos_decenarios_percentos < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir os decenarios:
            return fator_percent * to_redutor(self.ultimos_decenarios_percentos)

# ----------------------------------------------------------------------------
