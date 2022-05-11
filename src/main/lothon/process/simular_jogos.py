"""
   Test Package
   Module  simular_jogos.py

   Modulo para executar a simulacao de varios jogos para validar estrategias.
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import itertools as itt
import math
import random
import logging
from typing import Optional, Any
from collections import namedtuple

# Libs/Frameworks modules
# from memory_profiler import profile

# Own/Project modules
# from lothon.conf import app_config
from lothon import domain
from lothon.infra import parser_resultados
from lothon.domain import Loteria, Jogo, Numeral, LoteriaStruct, Premio
from lothon.process import simulate
from lothon.process.abstract_process import AbstractProcess
from lothon.stats import combinatoria as comb


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# relacao de instancias das loterias da caixa:
loterias_caixa: dict[str: Loteria] = None

# relacao de processos de analise, a serem executados sequencialmente:
process_chain: Optional[list[AbstractProcess]] = None

# parametros para configuracao dos processos de analise:
options: dict[str: Any] = {}


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# configura e executa o processo de analise:
def invoke_process(proc: AbstractProcess):
    # configura o processo antes,
    proc.init(options)

    # e depois executa a analise:
    proc.execute(loterias_caixa)


#
def sortear_bolas(qtd_bolas: int, qtd_bolas_sorteadas: int) -> list[int]:
    list_sorteio: list[int] = []
    while len(list_sorteio) < qtd_bolas_sorteadas:
        bola = random.randint(1, qtd_bolas)
        if bola not in list_sorteio:
            list_sorteio.append(bola)

    return list_sorteio


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas diarias:
# @profile
def run():
    global loterias_caixa, process_chain
    logger.info("Iniciando a analise dos dados de sorteios das loterias...")

    logger.debug("Vai efetuar carga das definicoes das loterias do arquivo de configuracao .INI")
    loterias_caixa = {"diadesorte": domain.get_dia_de_sorte(),
                      "duplasena": domain.get_dupla_sena(),
                      "lotofacil": domain.get_lotofacil(),
                      "megasena": domain.get_mega_sena(),
                      "quina": domain.get_quina(),
                      "supersete": domain.get_super_sete(),
                      "lotomania": domain.get_lotomania(),
                      "timemania": domain.get_timemania(),
                      "mesdasorte": domain.get_mes_da_sorte(),
                      "timedocoracao": domain.get_time_do_coracao()}
    logger.debug("Criadas instancias das loterias para processamento.")

    # # Efetua leitura dos arquivos HTML com resultados dos sorteios de cada loteria:
    # for key, value in loterias_caixa.items():
    #     logger.debug("Vai efetuar carga dos resultados da loteria: '%s'.", key)
    #     parser_resultados.parse_concursos_loteria(value)
    # logger.debug("Ultimos sorteios das loterias carregados dos arquivos HTML de resultados.")
    #
    # logger.debug("Inicializando a cadeia de processos para simulacao de jogos...")
    # process_chain = simulate.get_process_chain()
    # # Efetua a execução de cada processo de análise:
    # for proc in process_chain:
    #     invoke_process(proc)

    # BolaoStruct = namedtuple('BolaoStruct', 'bolas jogos premios')

    lot_quina = loterias_caixa["quina"]
    parser_resultados.parse_concursos_loteria(lot_quina)

    boloes: dict[int, int] = {6: 80, 7: 24, 8: 8, 9: 4, 10: 2, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1}
    media5: float = 0.00
    mediax: float = 0.00

    for _ in range(0, 100):
        premios5: float = 0.00
        premiosx: float = 0.00

        for qtd_dezenas, qtd_apostas in boloes.items():
            # gera os jogos para a quantidade de dezenas em cada bolao:
            bolao5: list[list[int]] = []
            qtd_jogos5 = math.comb(qtd_dezenas, 5) * qtd_apostas
            for i in range(0, qtd_jogos5):
                bolao5.append(sortear_bolas(80, 5))

            bolaox: list[list[int]] = []
            for i in range(0, qtd_apostas):
                bolaox.append(sortear_bolas(80, qtd_dezenas))

            # confere os jogos com os concursos da quina:
            for concurso in lot_quina.concursos:
                # confere os boloes de 5 jogos
                for jogo5 in bolao5:
                    premio = concurso.check_premiacao(jogo5)
                    if premio is not None:
                        premios5 += premio.premio

                # confere os boloes de x jogos
                for jogox in bolaox:
                    # gera as combinacoes de 5 dezenas para cada jogo com x dezenas:
                    for jogo5 in itt.combinations(jogox, 5):
                        premio = concurso.check_premiacao(jogo5)
                        if premio is not None:
                            premiosx += premio.premio

        media5 += premios5
        mediax += premiosx

    media5 = media5 / 100
    mediax = mediax / 100

    print(f"\n\n Comparando apostas de 5 dezenas com boloes de X dezenas:")
    print(f"\t\t Premios para 5 dezenas = {media5:,.2f}")
    print(f"\t\t Premios para X dezenas = {mediax:,.2f}")

    # idx = 0
    # megasena_struct: LoteriaStruct = domain.new_loteria_struct()
    # for numeros in itt.combinations(range(1, 61), 6):
    #     megasena_struct.jogos.append(numeros)
    #     megasena_struct.fatores.append(1)
    #     idx += 1
    #     if idx % 1000 == 0:
    #         print("indice = ", idx)
    #     if idx > 1000000:
    #         break
    #
    # del megasena_struct.jogos[2]
    # del megasena_struct.jogos[20]
    # del megasena_struct.fatores[2]
    # del megasena_struct.fatores[20]
    # print(f"megasena_struct.jogos = {len(megasena_struct.jogos)}")
    # print(f"megasena_struct.fatores = {len(megasena_struct.fatores)}")

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    logger.info("Finalizada a analise dos dados de sorteios das loterias.")
    return 0

# ----------------------------------------------------------------------------
