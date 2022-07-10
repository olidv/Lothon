"""
   Package lothon.process.compute
   Module  bet_dia_de_sorte.py

"""

__all__ = [
    'BetDiaDeSorte'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional, Any
import math
import random
import itertools as itt
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.stats import combinatoria as cb
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
paridades: dict[int: int] = {11: 5, 10: 5, 9: 4, 8: 4, 7: 3}


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


# printa as paridades geradas quando se aposta boloes com jogos combinados.
def print_paridades_boloes(qtd_bolas: int, faixa: tuple[int, int]) -> bool:
    pares: list[int] = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40]
    impares: list[int] = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39]

    # para cada faixa do bolao, gera um jogo completo e verifica as paridades:
    print("\n")
    for qtd_dezenas in range(faixa[0], faixa[1] + 1):
        for qtd_pares in range(1, qtd_dezenas + 1):
            # primeiro gera o jogo de bolao considerando qtd_pares:
            bolao: tuple[int, ...] = tuple(pares[:qtd_pares])
            # em seguida, gera o restante das dezenas impares:
            if qtd_pares < qtd_dezenas:
                qtd: int = qtd_dezenas - qtd_pares
                bolao += tuple(impares[:qtd])

            # gerado o bolao, verifica quantos pares tem em cada jogo:
            qtd_jogos: int = math.comb(qtd_dezenas, qtd_bolas)
            result_pares: dict[int: int] = {}
            for jogo in itt.combinations(bolao, qtd_bolas):
                # print("\t Jogo Combinado: ", jogo)
                qt_pares: int = cb.count_pares(jogo)
                qtd: int = result_pares.get(qt_pares, 0)
                result_pares[qt_pares] = qtd + 1

            # printa os jogos gerados e o numero de pares (ordenado desc) em cada um:
            result_pares = {k: v for k, v in sorted(result_pares.items(),
                                                    key=lambda item: item[1], reverse=True)}
            print(f"Bolao gerado com {qtd_dezenas} dezenas tendo {qtd_pares} pares: ", bolao)
            print(f"\t Paridades dos {formatd(qtd_jogos)} jogos do bolao: ", result_pares)
        print("\n")

    return True


def print_sequencias_boloes(qtd_bolas: int, faixa: tuple[int, int]) -> bool:
    sequs: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
    aleat: list[int] = [23, 25, 38, 24, 27, 30, 22, 26, 39, 31, 28, 33, 36, 34, 40, 35, 32, 37, 29]

    # para cada faixa do bolao, gera um jogo completo e verifica as sequencias:
    print("\n")
    for qtd_dezenas in range(faixa[0], faixa[1] + 1):
        for qtd_sequs in range(1, qtd_dezenas):
            # primeiro gera o jogo de bolao considerando qtd_sequs:
            bolao: tuple[int, ...] = tuple(sequs[:qtd_sequs+1])
            # em seguida, gera o restante das dezenas aleatorias:
            if qtd_sequs+1 < qtd_dezenas:
                qtd: int = qtd_dezenas - (qtd_sequs+1)
                bolao += tuple(aleat[:qtd])

            # gerado o bolao, verifica quantas sequencias tem em cada jogo:
            qtd_jogos: int = math.comb(qtd_dezenas, qtd_bolas)
            result_sequs: dict[int: int] = {}
            for jogo in itt.combinations(bolao, qtd_bolas):
                # print("\t Jogo Combinado: ", jogo)
                qt_sequs: int = cb.count_sequencias(jogo)
                qtd: int = result_sequs.get(qt_sequs, 0)
                result_sequs[qt_sequs] = qtd + 1

            # printa os jogos gerados e o numero de sequencias (ordenado desc) em cada um:
            result_sequs = {k: v for k, v in sorted(result_sequs.items(),
                                                    key=lambda item: item[1], reverse=True)}
            print(f"Bolao gerado com {qtd_dezenas} dezenas tendo {qtd_sequs} sequencias: ", bolao)
            print(f"\t Sequencias dos {formatd(qtd_jogos)} jogos do bolao: ", result_sequs)
        print("\n")

    return True


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class BetDiaDeSorte(AbstractBetting):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, loteria: Loteria):
        super().__init__("Geracao de Jogos para 'Dia de Sorte'", loteria)

        # estruturas para a coleta de dados a partir do processamento de analise:

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- METODOS ------------------------------------------------------------

    @classmethod
    def get_jogo_concurso(cls, bolas: tuple[int, ...], jogos: list[Jogo]) -> Optional[Jogo]:
        # procura na lista de jogos para identificar o jogo correspondente ao concurso (bolas):
        for jogo in jogos:
            if bolas == jogo.dezenas:
                return jogo

        # se percorreu toda a lista de jogos e nao encontrou, retorna vazio:
        return None

    @classmethod
    def get_ordinal_concurso(cls, bolas: tuple[int, ...], jogos: list[Jogo]) -> int:
        # procura na lista de jogos para identificar o ordinal do jogo correspondente:
        for idx, jogo in enumerate(jogos):
            if bolas == jogo.dezenas:
                return idx

        # se percorreu toda a lista de jogos e nao encontrou, entao informa que ha algo errado:
        return -1

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

        # identifica informacoes da loteria:
        concursos_passados: list[Concurso] = self.concursos[:-1]
        ultimo_concurso: Concurso = self.concursos[-1]
        qtd_bolas: int = self.loteria.qtd_bolas
        qtd_bolas_sorteio: int = self.loteria.qtd_bolas_sorteio
        qtd_jogos: int = self.loteria.qtd_jogos

        # efetua teste demonstrativo da geracao de jogos considerando paridades e sequencias:
        if print_paridades_boloes(5, (6, 15)) and print_sequencias_boloes(5, (6, 15)):
            return []

        # inicializa a cadeia de processos para computacao de jogos:
        compute_chain: list[AbstractCompute] = get_process_chain()

        # define os parametros para configurar o processamento de 'evaluate()' dos processos:
        parms: dict[str: Any] = {  # aplica limites e/ou faixas de corte...
            'qtd_bolas': qtd_bolas,
            'qtd_bolas_sorteio': qtd_bolas_sorteio,
            'qtd_jogos': qtd_jogos
        }
        # configura cada um dos processos de calculo-evaluate, para computarem os sorteios:
        logger.debug("Configurando a cadeia de processos para computacao de jogos.")
        for cproc in compute_chain:
            # configuracao de parametros para os processamentos em cada classe de analise:
            logger.debug(f"Processo '{cproc.id_process}': configurando parametros de SETUP...")
            cproc.setup(parms)

        # Efetua a execucao de cada processo de analise em sequencia (chain) para coleta de dados:
        logger.debug("Executando o processamento das loterias para computacao de jogos.")
        for cproc in compute_chain:
            # executa a analise para cada loteria:
            logger.debug(f"Processo '{cproc.id_process}': executando computacao dos sorteios...")
            cproc.execute(concursos_passados)

        # efetua analise geral (evaluate) de todas as combinacoes de jogos da loteria:
        jogos_computados: list[Jogo] = []
        qtd_zerados: int = 0

        # gera as combinacoes de jogos da loteria:
        range_jogos: range = range(1, qtd_bolas + 1)
        vl_ordinal: int = 0
        for jogo in itt.combinations(range_jogos, qtd_bolas_sorteio):
            vl_ordinal += 1  # primeiro jogo ira comecar do #1

            # executa a avaliacao do jogo, para verificar se sera considerado ou descartado:
            vl_fator: float = 0
            for cproc in compute_chain:
                vl_eval: float = cproc.eval(vl_ordinal, jogo)

                # ignora o resto das analises se a metrica zerou:
                if vl_eval > 0:
                    vl_fator += vl_eval  # probabilidade da uniao de dois eventos
                else:
                    vl_fator = 0  # zera o fator para que o jogo nao seja considerado
                    break  # ignora e pula para o proximo jogo, acelerando o processamento

            # se a metrica atingir o ponto de corte, entao mantem o jogo para apostar:
            if vl_fator > 0:
                jogos_computados.append(Jogo(vl_ordinal, vl_fator, jogo))
            else:
                qtd_zerados += 1

        qtd_inclusos: int = len(jogos_computados)
        logger.info(f"Finalizado o processamento das  {formatd(qtd_jogos)}  combinacoes de jogos. "
                    f" Eliminados (zerados)  {formatd(qtd_zerados)}  jogos entre os  "
                    f"{formatd(qtd_inclusos)}  jogos considerados.")

        # contabiliza as frequencias das dezenas em todos os jogos considerados:
        frequencias_bolas: list[int] = cb.new_list_int(qtd_bolas)
        for jogo in jogos_computados:
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

        # ordena os jogos processados pelo fator, do maior (maiores chances) para o menor:
        jogos_computados.sort(key=lambda n: n.fator, reverse=True)

        # procura na lista de jogos computados o jogo correspondente ao ultimo sorteio:
        ordinal_concurso: int = self.get_ordinal_concurso(ultimo_concurso.bolas, jogos_computados)
        jogo_concurso: Jogo = self.get_jogo_concurso(ultimo_concurso.bolas, jogos_computados)

        logger.debug(f"Para o ultimo concurso #{formatd(ultimo_concurso.id_concurso)} foi "
                     f"encontrado o jogo[{formatd(ordinal_concurso)}]:\n\t {jogo_concurso}")

        # printa os jogos computados, para verificar a ordem final dos jogos com o fator resultante:
        output: str = f"\n\t   ORDINAL     FATOR     DEZENAS\n"
        for idx, jogo in enumerate(jogos_computados):
            output += f"\t{formatd(idx,10)}    {formatf(jogo.fator,'6.3')}     {jogo.dezenas}\n"
        logger.debug(f"Finalizou a impressao dos  {formatd(len(jogos_computados))}  jogos "
                     f"computados e considerados: {output}")

        # identifica os 100 primeiros jogos, para fins de teste:
        jogos_bolao: list[tuple[int, ...]] = []
        for i in range(0, 100):
            jogos_bolao.append(jogos_computados[i].dezenas)

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return jogos_bolao

# ----------------------------------------------------------------------------
