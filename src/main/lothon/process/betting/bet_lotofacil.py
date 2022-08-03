"""
   Package lothon.process.compute
   Module  bet_lotofacil.py

"""

__all__ = [
    'BetLotofacil'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional
import random
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.infra import console, parser_resultados
from lothon.stats import combinatoria as cb
from lothon import domain
from lothon.domain import Loteria, Concurso, Jogo
from lothon.process.betting.abstract_betting import AbstractBetting
from lothon.process.compute.abstract_compute import AbstractCompute
from lothon.process.compute.compute_ausencia import ComputeAusencia
from lothon.process.compute.compute_espacamento import ComputeEspacamento
from lothon.process.compute.compute_frequencia import ComputeFrequencia
from lothon.process.compute.compute_matricial import ComputeMatricial
from lothon.process.compute.compute_mediana import ComputeMediana
from lothon.process.compute.compute_paridade import ComputeParidade
from lothon.process.compute.compute_recorrencia import ComputeRecorrencia
from lothon.process.compute.compute_repetencia import ComputeRepetencia
from lothon.process.compute.compute_sequencia import ComputeSequencia


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# medidas otimas de equilibrio de paridades para boloes:
PARIDADES_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
SEQUENCIAS_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
AUSENCIAS_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
FREQUENCIAS_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
REPETENCIAS_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# apenas as computacoes com valores mais significativos, apos analises e simulados:
def get_process_chain() -> list[AbstractCompute]:
    return [  # define o percentual de corte, ignorando jogos com rates abaixo de 10%...
        ComputeParidade(10),
        ComputeSequencia(10),
        ComputeEspacamento(10),
        ComputeMediana(10),
        ComputeMatricial(10),
        ComputeAusencia(10),
        ComputeFrequencia(10),
        ComputeRepetencia(10),
        ComputeRecorrencia(10)
    ]


def sortear_bolas(set_bolas: int, qtd_bolas_sorteadas: int) -> tuple[int, ...]:
    bolas: tuple[int, ...] = ()
    count: int = 0
    while count < qtd_bolas_sorteadas:
        bola = random.randint(1, set_bolas)
        if bola not in bolas:
            bolas = bolas + (bola,)
            count += 1

    return bolas


def gerar_bolao_aleatorio(qtd_bolas: int, qtd_dezenas: int,
                          qtd_jogos: int) -> list[tuple[int, ...]]:
    bolao: list[tuple[int, ...]] = []

    # gera jogos com dezenas aleatorias:
    for i in range(0, qtd_jogos):
        bolao.append(sortear_bolas(qtd_bolas, qtd_dezenas))

    return bolao


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class BetLotofacil(AbstractBetting):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, loteria: Loteria):
        super().__init__("Geracao de Jogos para 'Lotofacil'", loteria)

        # estruturas para a coleta de dados a partir do processamento de analise:

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- METODOS ------------------------------------------------------------

    def exportar_sorteios(self):
        # o local de gravacao dos arquivos ja foi padronizado na configuracao INI
        qtd_export: int = domain.export_sorteios(self.loteria)
        return qtd_export

    def get_jogo_concurso(self, bolas: tuple[int, ...]) -> Optional[Jogo]:
        # procura na lista de jogos para identificar o jogo correspondente ao concurso (bolas):
        for jogo in self.jogos:
            if bolas == jogo.dezenas:
                return jogo

        # se percorreu toda a lista de jogos e nao encontrou, retorna vazio:
        return None

    def get_ordinal_concurso(self, bolas: tuple[int, ...]) -> int:
        # procura na lista de jogos para identificar o ordinal do jogo correspondente:
        for idx, jogo in enumerate(self.jogos):
            if bolas == jogo.dezenas:
                return idx

        # se percorreu toda a lista de jogos e nao encontrou, entao informa que ha algo errado:
        return -1

    def sortear_jogos(self, qtd_sorteadas: int, qtd_recorrencia: int) -> list[tuple[int, ...]]:
        jogos_sorteados: list[tuple[int, ...]] = []

        qtd_jogos: int = len(self.jogos)
        for _ in range(0, qtd_sorteadas):
            idx: int = -1
            while idx < 0:
                idx = random.randint(0, qtd_jogos-1)
                # print("idx = ", idx)
                jogo: Jogo = self.jogos[idx]
                qt_max_recorrencias: int = 0
                for sorteado in jogos_sorteados:
                    qt_recorrencias: int = cb.count_recorrencias(jogo.dezenas, sorteado)
                    if qt_recorrencias > qt_max_recorrencias:
                        qt_max_recorrencias = qt_recorrencias

                if qt_max_recorrencias > qtd_recorrencia:
                    idx = -1

            jogos_sorteados.append(self.jogos[idx].dezenas)

        return jogos_sorteados

    def relacionar_jogos(self, qtd_max_recorrencias: int) -> list[tuple[int, ...]]:
        jogos_sorteados: list[tuple[int, ...]] = [self.jogos[0].dezenas]
        for jogo in self.jogos[1:]:
            max_count: int = -1
            for sorteado in jogos_sorteados:
                count: int = cb.count_recorrencias(jogo.dezenas, sorteado)
                if count > max_count:
                    max_count = count

            if max_count <= qtd_max_recorrencias:
                jogos_sorteados.append(jogo.dezenas)

        return jogos_sorteados

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, bolao: dict[int: int],
                concursos: list[Concurso] = None) -> list[tuple[int, ...]]:
        # valida se possui concursos a serem analisados:
        if bolao is None or len(bolao) == 0:
            return []
        elif concursos is not None:
            if len(concursos) > 0:
                self.concursos = concursos
            else:
                return []
        _startWatch = startwatch()

        # Vai exportar os arquivos CSV com dezenas sorteadas das loterias...
        qtd_export: int = self.exportar_sorteios()
        logger.debug(f"Foram exportados #{formatd(qtd_export)} sorteios da loteria "
                     f"{self.loteria.nome_loteria}' em arquivo CSV.")

        # executa rotina Java para processamento e geracao dos jogos computados:
        exit_code: int = console.execute_jlothon('l')
        logger.debug(f"Retornou do programa jLothon o exit-code: {exit_code}")

        # importa os jogos computados para prosseguir com o processamento:
        self.jogos = parser_resultados.read_jogos_loteria(self.loteria.nome_loteria)

        # contabiliza as frequencias das dezenas em todos os jogos considerados:
        frequencias_bolas: list[int] = cb.new_list_int(self.loteria.qtd_bolas)
        for jogo in self.jogos:
            # registra a frequencia para cada dezena dos jogos:
            for dezena in jogo.dezenas:
                frequencias_bolas[dezena] += 1

        # identifica a frequencia das dezenas em ordem reversa do numero de ocorrencias nos jogos:
        frequencias_dezenas: dict = cb.to_dict(frequencias_bolas, reverse_value=True)
        output: str = f"\n\t DEZENA    #JOGOS\n"
        for key, val in frequencias_dezenas.items():
            if key == 0:
                continue
            output += f"\t     {formatd(key,2)}    {formatd(val)}\n"
        logger.debug(f"Frequencia das Dezenas Computadas: {output}")

        # TODO efetuar geracao dos jogos...
        jogos_bolao: list[tuple[int, ...]] = self.sortear_jogos(16, 10)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return jogos_bolao

# ----------------------------------------------------------------------------
