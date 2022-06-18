"""
   Package lothon.process.compute
   Module  compute_ciclo.py

"""

__all__ = [
    'ComputeCiclo'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging
from typing import Optional

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

# constante com numero maximo de concursos que formam um ciclo:
MAX_CICLOS: int = 100

# constante com percentual de dezenas que devem ser sorteadas para compor um ciclo:
LIMIT_BOLAS: int = 90  # se 90% das bolas forem sorteadas, entao considera um ciclo fechado.


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class ComputeCiclo(AbstractCompute):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('frequencias_ciclos', 'ciclos_concursos', 'ciclos_percentos',
                 'ultimos_ciclos_repetidos', 'ultimos_ciclos_percentos',
                 'vl_ciclo_ultimo_concurso', 'vl_ciclo_penultimo_concurso',
                 'concursos_passados', 'limit_bolas_ciclo')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Computacao de Ciclo Fechado dos Concursos")

        # estrutura para a coleta de dados a partir do processamento de analise:
        self.frequencias_ciclos: Optional[SerieSorteio] = None
        self.ciclos_concursos: Optional[list[int]] = None
        self.ciclos_percentos: Optional[list[float]] = None
        self.ultimos_ciclos_repetidos: Optional[list[int]] = None
        self.ultimos_ciclos_percentos: Optional[list[float]] = None
        self.vl_ciclo_ultimo_concurso: int = 0
        self.vl_ciclo_penultimo_concurso: int = 0

        # estruturas para avaliacao de jogo combinado da loteria:
        self.concursos_passados: Optional[list[Concurso]] = None
        self.limit_bolas_ciclo: int = 0

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- METODOS ------------------------------------------------------------

    def count_concursos_ciclo(self, bolas: tuple[int, ...]) -> int:
        # contabiliza o ultimo ciclo fechado nos concursos fornecidos:
        dezenas: list[int] = cb.new_list_int(self.qtd_bolas)
        dezenas[0] = -1

        # inicia registrando as dezenas do jogo:
        cb.count_dezenas(bolas, dezenas)

        # percorre os concursos ate fechar o ciclo:
        qtd_concursos_ciclo: int = 0
        for concurso in self.concursos_passados:
            qtd_concursos_ciclo += 1

            # identifica as bolas sorteadas para fechar o ciclo:
            cb.count_dezenas(concurso.bolas, dezenas)

            # se ainda tem algum zero, entao nao fechou o ciclo:
            qtd_falta_ciclo: int = dezenas.count(0)  # quantas dezenas faltam para fechar o ciclo?
            if qtd_falta_ciclo > self.limit_bolas_ciclo:
                continue
            else:
                break

        return qtd_concursos_ciclo

    # --- PROCESSAMENTO DOS SORTEIOS -----------------------------------------

    def execute(self, concursos: list[Concurso]) -> int:
        # valida se possui concursos a serem analisados:
        if concursos is None or len(concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        qtd_concursos: int = len(concursos)
        # nao precisa de sortear 100% das bolas para fechar o ciclo:
        self.limit_bolas_ciclo = self.qtd_bolas - (self.qtd_bolas * LIMIT_BOLAS // 100)

        # inicializa as estruturas para registrar os ciclos fechados:
        self.frequencias_ciclos = SerieSorteio(0)
        self.ciclos_concursos = cb.new_list_int(MAX_CICLOS)
        self.ultimos_ciclos_repetidos = cb.new_list_int(MAX_CICLOS)
        self.vl_ciclo_ultimo_concurso = -1
        self.vl_ciclo_penultimo_concurso = -1

        # contabiliza os ciclos fechados em todos os sorteios ja realizados:
        dezenas: list[int] = cb.new_list_int(self.qtd_bolas)
        dezenas[0] = -1
        qtd_concursos_ciclo: int = 0
        for concurso in concursos:
            qtd_concursos_ciclo += 1

            # identifica as bolas sorteadas para fechar o ciclo:
            cb.count_dezenas(concurso.bolas, dezenas)

            # se ainda tem algum zero, entao nao fechou o ciclo:
            qtd_falta_ciclo: int = dezenas.count(0)  # quantas dezenas faltam para fechar o ciclo?
            if qtd_falta_ciclo > self.limit_bolas_ciclo:
                continue

            # fechando o ciclo, contabiliza o ciclo fechado (onde fecha o ciclo eh inclusivo):
            self.frequencias_ciclos.add_sorteio(concurso.id_concurso, True)

            # registra o numero de concursos necessario para fechar mais um ciclo:
            self.ciclos_concursos[qtd_concursos_ciclo] += 1
            # verifica se repetiu o ciclo do ultimo concurso:
            if qtd_concursos_ciclo == self.vl_ciclo_ultimo_concurso:
                self.ultimos_ciclos_repetidos[qtd_concursos_ciclo] += 1
            # atualiza ambos flags, para ultimo e penultimo concursos
            self.vl_ciclo_penultimo_concurso = self.vl_ciclo_ultimo_concurso
            self.vl_ciclo_ultimo_concurso = qtd_concursos_ciclo

            # zera contadores para proximo ciclo:
            dezenas = cb.new_list_int(self.qtd_bolas)
            dezenas[0] = -1  # p/ nao conflitar com o teste de fechamento do ciclo: 0 in dezena
            qtd_concursos_ciclo = 0

        # ja calcula as medidas estatisticas para impressao ao final:
        self.frequencias_ciclos.update_stats()

        # calcula o percentual dos ciclos:
        self.ciclos_percentos: list[float] = cb.new_list_float(MAX_CICLOS)
        for key, value in enumerate(self.ciclos_concursos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.ciclos_percentos[key] = percent

        # contabiliza o percentual dos ultimos ciclos:
        self.ultimos_ciclos_percentos = cb.new_list_float(MAX_CICLOS)
        for key, value in enumerate(self.ultimos_ciclos_repetidos):
            percent: float = round((value / qtd_concursos) * 10000) / 100
            self.ultimos_ciclos_percentos[key] = percent

        # salva os ultimos concursos processados ate o momento para o EVALUATE posterior:
        self.concursos_passados = list(reversed(concursos[-MAX_CICLOS:]))

        # indica o tempo do processamento:
        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

    # --- ANALISE E AVALIACAO DE JOGOS ---------------------------------------

    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        # probabilidade de acerto depende do numero de concursos para fechar um ciclo com o jogo:
        size_ciclo: int = self.count_concursos_ciclo(jogo)
        percent: float = self.ciclos_percentos[size_ciclo]

        # ignora valores muito baixos de probabilidade:
        if percent < 1:
            self.qtd_zerados += 1
            return 0

        # calcula o fator de percentual (metrica), para facilitar o calculo seguinte:
        fator_percent: float = to_fator(percent)

        # verifica se esse jogo repetiu ultimo e penultimo ciclos:
        if size_ciclo != self.vl_ciclo_ultimo_concurso:
            return fator_percent  # nao repetiu, ja pode pular fora
        elif size_ciclo == self.vl_ciclo_ultimo_concurso == self.vl_ciclo_penultimo_concurso:
            self.qtd_zerados += 1
            return 0  # pouco provavel de repetir mais de 2 ou 3 vezes

        # se repetiu, obtem a probabilidade de repeticao do ultimo ciclo:
        percent_repetido: float = self.ultimos_ciclos_percentos[size_ciclo]
        if percent_repetido < 1:  # baixa probabilidade pode ser descartada
            self.qtd_zerados += 1
            return 0
        else:  # reduz a probabilidade porque esse jogo vai repetir o ciclo:
            return fator_percent * to_redutor(percent_repetido)

# ----------------------------------------------------------------------------
