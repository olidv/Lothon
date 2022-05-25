"""
   Test Package
   Module  simular_jogos.py

   Modulo para executar a simulacao de varios jogos para validar estrategias.
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import math
import random
import logging
import itertools as itt
from typing import Any

# Libs/Frameworks modules
# from memory_profiler import profile

# Own/Project modules
# from lothon.conf import app_config
from lothon import domain
from lothon.domain import Loteria, Concurso, ConcursoDuplo, Faixa, Premio
from lothon.process.abstract_process import AbstractProcess
# from lothon.process import simulate
# from lothon.stats import combinatoria as comb
from lothon.util.eve import *

# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# relacao de instancias das loterias da caixa:
loterias_caixa: Optional[dict[str: Loteria]] = None

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
def sortear_bolas(set_bolas: int, qtd_bolas_sorteadas: int) -> tuple[int, ...]:
    bolas: tuple[int, ...] = ()
    count: int = 0
    while count < qtd_bolas_sorteadas:
        bola = random.randint(1, set_bolas)
        if bola not in bolas:
            bolas = bolas + (bola,)
            count += 1

    return bolas


#
def gerar_bolao(qtd_bolas: int, qtd_dezenas: int, qtd_jogos: int,
                concursos_passados: list[Concurso] = None) -> list[tuple[int, ...]]:
    bolao: list[tuple[int, ...]] = []

    # se nao ha concursos passados para analisar, entao gera jogos com dezenas aleatorias:
    if concursos_passados is None:
        for i in range(0, qtd_jogos):
            bolao.append(sortear_bolas(qtd_bolas, qtd_dezenas))

    return bolao


# confere relacao de jogos de um bolao com o(s) sorteio(s) de determinado concurso:
def check_premiacao_jogos(concurso: Concurso | ConcursoDuplo,
                          bolao: list[tuple[int, ...]], qt_base: int = None) -> float:
    premiof: float = 0.00

    # confere cada jogo do bolao e soma o valor das premiacoes:
    for jogo in bolao:
        # se o numero de bolas de cada jogo corresponde ao numero basico de dezenas da loteria:
        qt_bolas_jogo: int = len(jogo)
        if qt_base is None or qt_base == qt_bolas_jogo:
            # basta conferir cada jogo com o concurso:
            premio: Optional[Premio] = concurso.check_premiacao(jogo)
            if premio is not None:
                premiof += premio.premio

        # se o numero de bolas for inferior ao tamanho de cada jogo,
        elif qt_base < qt_bolas_jogo:  # # entao o bolao esta com jogos combinados,
            # deve-se gerar as combinacoes de BASE dezenas para cada jogo com x dezenas:
            for jogob in itt.combinations(jogo, qt_base):
                premio: Optional[Premio] = concurso.check_premiacao(jogob)
                if premio is not None:
                    premiof += premio.premio

    return premiof


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas diarias:
# @profile
def run():
    global loterias_caixa, process_chain
    logger.info("Iniciando a analise dos dados de sorteios das loterias...")

    logger.debug("Vai efetuar carga das definicoes das loterias do arquivo de configuracao .INI")
    loterias_caixa = {
        "quina": domain.get_quina(),
        # "megasena": domain.get_mega_sena(),
        # "duplasena": domain.get_dupla_sena(),
        # "diadesorte": domain.get_dia_de_sorte(),
        # "lotofacil": domain.get_lotofacil()
    }
    boloes_caixa = {
        "quina": {6: 80, 7: 25, 8: 8, 9: 4, 10: 2, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1},
        "megasena": {7: 50, 8: 12, 9: 4, 10: 2, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1},
        "duplasena": {7: 60, 8: 15, 9: 5, 10: 2, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1},
        "diadesorte": {8: 60, 9: 15, 10: 5, 11: 2, 12: 1, 13: 1, 14: 1, 15: 1},
        "lotofacil": {16: 40, 17: 5, 18: 1, 19: 1, 20: 1}
    }
    logger.debug("Criadas instancias das loterias e boloes para processamento.")

    # Efetua leitura dos arquivos HTML com resultados dos sorteios de cada loteria:
    for key, loteria in loterias_caixa.items():
        logger.debug(f"Vai efetuar carga dos resultados da loteria: '{key}'.")
        domain.load_concursos(loteria)
    logger.debug("Ultimos sorteios das loterias carregados dos arquivos HTML de resultados.")

    # logger.debug("Inicializando a cadeia de processos para simulacao de jogos...")
    # process_chain = simulate.get_process_chain()
    # # Efetua a execucao de cada processo de analise:
    # for proc in process_chain:
    #     invoke_process(proc)

    for key, loteria in loterias_caixa.items():
        logger.debug(f"{loteria.nome_loteria}: Iniciando processamento de simulacao de apostas...")

        boloes: dict[int, int] = boloes_caixa[key]
        qtd_concursos: int = len(loteria.concursos)
        bolas: int = loteria.qtd_bolas
        base: int = loteria.qtd_bolas_sorteio
        faixas: dict[int, Faixa] = loteria.faixas
        precob: float = faixas[base].preco

        total_gastosb: float = 0.00
        total_premiosb: float = 0.00
        total_premiosx: float = 0.00

        # concursos passados sao usados para gerar novos jogos:
        concursos_passados: list[Concurso] = []

        # efetua apostas em todos os concursos, de forma acumulativa:
        for concurso in loteria.concursos:
            output: str = f"\t#DEZENAS      #APOSTAS        GASTO R$          PREMIOS R$\n"

            # para cada concurso, faz a comparacao entre jogos simples e com boloes:
            for qtd_dezenas, qtd_apostas in boloes.items():
                # *** APOSTAS BASE: MENOR PRECO ***
                qtd_jogosb: int = math.comb(qtd_dezenas, base) * qtd_apostas
                gastosb: float = precob * qtd_jogosb

                # gera os jogos simples, sem bolao:
                bolaob: list[tuple[int, ...]] = gerar_bolao(bolas, base, qtd_jogosb)

                # confere os boloes de BASE jogos
                premiosb: float = check_premiacao_jogos(concurso, bolaob)

                output += f"\t      {base:0>2}         {formatn(qtd_jogosb,6)}       " \
                          f"{formatf(gastosb,'9.2')}      {formatf(premiosb)}\n"

                # *** APOSTAS COM XX DEZENAS ***
                gastosx: float = faixas[qtd_dezenas].preco * qtd_apostas

                # gera os jogos para os boloes, usando analise estatistica:
                bolaox: list[tuple[int, ...]] = gerar_bolao(bolas, qtd_dezenas, qtd_apostas)

                # confere os boloes de x jogos
                premiosx: float = check_premiacao_jogos(concurso, bolaox, base)

                output += f"\t      {qtd_dezenas:0>2}        {formatn(qtd_apostas,6)}    " \
                          f"   {formatf(gastosx,'9.2')}      {formatf(premiosx)}\n\n"
                total_gastosb += gastosb
                total_premiosb += premiosb
                total_premiosx += premiosx

            logger.debug(f"{loteria.nome_loteria}: CONCURSO #{concurso.id_concurso}  .:.  "
                         f"Data: {concurso.data_sorteio}\n"
                         f"{output}")

            # este concurso sera usado como base para o proximo concurso:
            concursos_passados.append(concurso)

        media_gastosb: float = total_gastosb / qtd_concursos
        media_premiosb: float = total_premiosb / qtd_concursos
        media_premiosx: float = total_premiosx / qtd_concursos

        logger.info(f"{loteria.nome_loteria}: Comparando apostas de {base} dezenas com boloes de "
                    f"X dezenas:\n"
                    
                    f"\t\t MEDIA: Gasto medio com apostas = {formatf(media_gastosb)}\n"
                    f"\t\t MEDIA: Premios para {base:0>2} dezenas = {formatf(media_premiosb)}\n"
                    f"\t\t MEDIA: Premios para XX dezenas = {formatf(media_premiosx)}\n\n"
                    
                    f"\t\t TOTAL: Gasto total com apostas = {formatf(total_gastosb)}\n"
                    f"\t\t TOTAL: Premios para {base:0>2} dezenas = {formatf(total_premiosb)}\n"
                    f"\t\t TOTAL: Premios para XX dezenas = {formatf(total_premiosx)}\n")

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    logger.info("Finalizada a simulacao de apostas para todos os concursos das loterias.")
    return 0

# ----------------------------------------------------------------------------
