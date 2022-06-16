"""
   Package lothon.process.analyze
   Module  analise_finalista.py

"""

__all__ = [
    'AnaliseFinalista'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Any
import math
import itertools as itt
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.stats import combinatoria as cb
from lothon.domain import Loteria, Concurso
from lothon.process import compute
from lothon.process.compute.abstract_compute import AbstractCompute
from lothon.process.analyze.abstract_analyze import AbstractAnalyze


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseFinalista(AbstractAnalyze):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise Finalista das Estratégias")

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
        concursos: list[Concurso] = loteria.concursos
        ultimo_concurso: Concurso = concursos[-1]
        qtd_concursos: int = len(loteria.concursos)
        qtd_jogos: int = loteria.qtd_jogos
        qtd_items: int = loteria.qtd_bolas_sorteio

        # organiza dicionario com todos os concursos, para pesquisar jogos:
        sorteios_literal: dict[str: int] = {}
        for concurso in concursos:
            bolas_str: str = cb.to_string(concurso.bolas)
            sorteios_literal[bolas_str] = concurso.id_concurso

        # inicializa a cadeia de processos para computacao de jogos:
        compute_chain: list[AbstractCompute] = compute.get_process_chain()

        # define os parametros para configurar o processamento de 'evaluate()' dos processos:
        parms: dict[str: Any] = {  # aplica limites e/ou faixas de corte...
        }
        # configura cada um dos processos de calculo-evaluate, apos computarem os sorteios:
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
            cproc.execute(loteria)

        # efetua analise geral (evaluate) de todas as combinacoes de jogos da loteria:
        logger.debug(f"{nmlot}: Executando analise EVALUATE dos  "
                     f"{formatd(qtd_jogos)}  jogos combinados da loteria.")

        # processa cada combinacao de jogo da loteria:
        compute_jogos: list[tuple[int, ...]] = []
        range_jogos: range = range(1, loteria.qtd_bolas + 1)
        # para cada concurso, vai atribuir o respectivo ordinal das combinacoes de jogos da loteria:
        vl_ordinal: int = 0
        for jogo in itt.combinations(range_jogos, loteria.qtd_bolas_sorteio):
            vl_ordinal += 1  # primeiro jogo ira comecar do #1
            vl_metrica: float = 1.0
            for cproc in compute_chain:
                # executa o processamento de avaliacao do jogo, para verificar se sera descartado:
                vl_metrica *= cproc.evaluate(vl_ordinal, jogo)
                # ignora o resto das analises se a metrica zerou:
                if vl_metrica == 0:
                    break  # pula para o proximo jogo, acelerando o processamento

            # se a metrica atingir o ponto de corte, entao mantem o jogo para apostar:
            if vl_metrica > 0:
                compute_jogos.append(jogo)
        logger.debug("Finalizou o EVALUATE de todas as combinacoes de jogos...")

        # verifica quantos jogos foram descartados e quantos serao considerados:
        qtd_considerados: int = len(compute_jogos)
        qtd_zerados: int = 0
        for cproc in compute_chain:
            qtd_zerados += cproc.qtd_zerados
            logger.debug(f"{cproc.id_process}: Jogos Zerados = {formatd(cproc.qtd_zerados)}")

        logger.debug(f"Resultado da avaliacao dos  {formatd(qtd_jogos)}  jogos combinados:\n"
                     f"\tNumero de jogos descartados (zerado) = {formatd(qtd_zerados)}\n"
                     f"\tNumero de jogos a serem considerados = {formatd(qtd_considerados)}\n")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
