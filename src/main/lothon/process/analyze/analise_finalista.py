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
# import sys
from typing import Any
# import math
import statistics as stts
import itertools as itt
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.stats import combinatoria as cb
from lothon.domain import Loteria, Concurso, Jogo
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
    __slots__ = ('sorteios_literal', 'qtd_concursos')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise Finalista das Estrategias")

        # estruturas para a coleta de dados a partir do processamento de analise:
        self.sorteios_literal: dict[str: int] = None
        self.qtd_concursos: int = 0

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- METODOS ------------------------------------------------------------

    @classmethod
    def get_ordinal_concurso(cls, bolas: tuple[int, ...], jogos: list[Jogo]) -> int:
        # procura na lista de jogos para identificar o ordinal do jogo correspondente:
        for idx, jogo in enumerate(jogos):
            if bolas == jogo.dezenas:
                return idx

        # se percorreu toda a lista de jogos e nao encontrou, entao informa que ha algo errado:
        return -1

    def get_ordinais_concursos(self, jogos: list[Jogo]) -> list[int]:
        ordinais_concursos: list[int] = cb.new_list_int(self.qtd_concursos)
        ordinais_concursos[0] = -1  # para nao cair no teste == 0

        for idx, jogo in enumerate(jogos):
            # procura no dicionario de literais as dezenas do jogo corrente:
            id_concurso: int = self.sorteios_literal.get(jogo.to_string(), -1)
            if id_concurso > 0:
                ordinais_concursos[id_concurso] = idx

        return ordinais_concursos

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, loteria: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if loteria is None or loteria.concursos is None or len(loteria.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = loteria.nome_loteria
        concursos: list[Concurso] = loteria.concursos[:-1]  # nao processa o ultimo por enquanto
        self.qtd_concursos: int = len(concursos)
        ultimo_concurso: Concurso = loteria.concursos[-1]
        range_jogos: range = range(1, loteria.qtd_bolas + 1)

        # organiza dicionario com todos os concursos, para pesquisar jogos:
        self.sorteios_literal: dict[str: int] = {}
        for concurso in concursos:
            bolas_str: str = cb.to_string(concurso.bolas)
            self.sorteios_literal[bolas_str] = concurso.id_concurso

        # inicializa a cadeia de processos para computacao de jogos:
        compute_chain: list[AbstractCompute | None] = compute.get_process_chain()

        # define os parametros para configurar o processamento de 'evaluate()' dos processos:
        parms: dict[str: Any] = {  # aplica limites e/ou faixas de corte...
            'qtd_bolas': loteria.qtd_bolas,
            'qtd_bolas_sorteio': loteria.qtd_bolas_sorteio,
            'qtd_jogos': loteria.qtd_jogos
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
            cproc.execute(concursos)

        # o primeiro item corresponde a buscar ordinais de jogos combinados, sem EVALUATE:
        # compute_chain.insert(0, None)
        output: str = f"\n\n COMPUTE                INCLUIDOS      ZERADOS    EXCLUIDOS" \
                      f"       MENOR        MAIOR        FAIXA        MEDIA      DESVIO" \
                      f"      #ULTIMO    FATOR\n"
        for cproc in compute_chain:
            nmproc: str = "Nenhum" if cproc is None else type(cproc).__name__
            logger.debug(f"{nmproc}: Executando analise EVALUATE dos  "
                         f"{formatd(loteria.qtd_jogos)}  jogos da loteria...")

            # efetua analise geral (evaluate) de todas as combinacoes de jogos da loteria:
            jogos_computados: list[Jogo] = []
            qtd_zerados: int = 0

            # gera todas as combinacoes de jogos com ordinal igual a numeracao sequencial:
            vl_ordinal: int = 0
            for jogo in itt.combinations(range_jogos, loteria.qtd_bolas_sorteio):
                vl_ordinal += 1  # primeiro jogo ira comecar do #1

                # executa o processamento de avaliacao do jogo, para verificar se sera descartado:
                vl_fator: float = 1.0 if cproc is None else cproc.evaluate(vl_ordinal, jogo)
                # se a metrica atingir o ponto de corte, entao mantem o jogo para apostar:
                if vl_fator > 0:
                    jogos_computados.append(Jogo(vl_ordinal, vl_fator, jogo))
                else:
                    qtd_zerados += 1

            # ordena os jogos processados pelo fator, do maior (maiores chances) para o menor:
            jogos_computados.sort(key=lambda n: n.fator, reverse=True)

            # para cada concurso, vai atribuir o respectivo ordinal do jogo processado:
            ordinais_concursos: list[int] = self.get_ordinais_concursos(jogos_computados)

            # verifica se algum sorteio nao foi localizado / considerado nos jogos:
            qtd_excluidos: int = ordinais_concursos.count(0)
            qtd_incluidos: int = len(jogos_computados) - qtd_excluidos

            # elimina os zerados para nao afetar os calculos estatisticos de media e desvio:
            min_ordinal: float = 0
            max_ordinal: float = 0
            faixa_ordinal: float = 0
            mean_ordinal: float = 0
            stdev_ordinal: float = 0
            ordinais_concursos = sorted([n for n in ordinais_concursos if n > 0])
            if len(ordinais_concursos) > 0:
                min_ordinal = min(ordinais_concursos)
                max_ordinal = max(ordinais_concursos)
                faixa_ordinal = abs(max_ordinal - min_ordinal)
                mean_ordinal = stts.fmean(ordinais_concursos)
                stdev_ordinal = stts.pstdev(ordinais_concursos)

            # procura na lista de jogos computados o ordinal correspondente do ultimo sorteio:
            ultimo_ordinal: int = self.get_ordinal_concurso(ultimo_concurso.bolas, jogos_computados)

            # tambem processa o ultimo sorteio para saber seu fator (metrica):
            ultimo_fator: float = 0 if cproc is None \
                else cproc.evaluate(ultimo_ordinal, ultimo_concurso.bolas)
            print("***** ULTIMO CONCURSO:", ultimo_concurso)

            # printa quantos jogos foram descartado, quantos serao considerados, etc...
            output += f" {nmproc:<20}  " \
                      f"{formatd(qtd_incluidos,10)}    " \
                      f"{formatd(qtd_zerados,9)}       " \
                      f"{formatd(qtd_excluidos,6)}  " \
                      f"{formatd(min_ordinal,10)}   " \
                      f"{formatd(max_ordinal,10)}   " \
                      f"{formatd(faixa_ordinal,10)}   " \
                      f"{formatd(mean_ordinal,10)}     " \
                      f"{formatd(stdev_ordinal,7)}   " \
                      f"{formatd(ultimo_ordinal,10)}   " \
                      f"{formatf(ultimo_fator,'6.3')}" \
                      f"\n"

        logger.debug(f"{nmlot}: Finalizou o EVALUATE dos jogos: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
