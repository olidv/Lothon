"""
   Package lothon.process.betting
   Module  bet_quina.py

"""

__all__ = [
    'BetQuina'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import itertools as itt
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.domain import Loteria, Concurso
from lothon.process.betting.abstract_betting import AbstractBetting


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# faixas de limites de recorrencias especificas para esta loteria:
FAIXAS_RECORRENCIAS: dict[int: int] = {0: 8, 1: 211, 2: 4208}

# medidas otimas de equilibrio de paridades para boloes:
PARIDADES_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
SEQUENCIAS_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
AUSENCIAS_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
FREQUENCIAS_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}
REPETENCIAS_BOLOES: dict[int: int] = {7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0}


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class BetQuina(AbstractBetting):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, loteria: Loteria):
        super().__init__("Criacao de Boloes para Quina", loteria)

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, bolao: dict[int: int], concursos: list[Concurso] = None) -> list[tuple]:
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
        nmlot: str = self.loteria.nome_loteria

        # se ainda nao existe o arquivo com os jogos computados, entao inicia o processo externo:
        if self.existe_jogos_computados():
            logger.debug(f"{nmlot}: Arquivo com jogos computados ja existe. "
                         f"Processo externo ignorado.")
        else:
            logger.debug(f"{nmlot}: Arquivo com jogos computados nao encontrado. "
                         f"Iniciando processo externo.")
            # Vai exportar os arquivos CSV com dezenas sorteadas das loterias...
            qtd_export: int = self.exportar_sorteios()
            logger.debug(f"{nmlot}: Foram exportados #{formatd(qtd_export)} sorteios da "
                         f"loteria em arquivo CSV.")

            # executa rotina Java para processamento e criacao dos jogos computados:
            run_ok: bool = self.executar_jlothon()
            if run_ok:
                logger.debug(f"{nmlot}: Programa jLothon foi executado com sucesso.")
            else:
                logger.error(f"{nmlot}: Erro na execucao do programa jLothon. "
                             f"Criacao de boloes abortada.")
                return []

        # importa os jogos computados em jLothon para prosseguir com o processamento:
        self.jogos = self.importar_jogos()
        qtd_jogos: int = len(self.jogos)
        logger.debug(f"{nmlot}: Foram importados  #{formatd(qtd_jogos)}  jogos computados da "
                     f"loteria de arquivo CSV.")

        # contabiliza as frequencias das dezenas em todos os jogos considerados:
        logger.debug(f"{nmlot}: Processando sorteios e jogos para computacao de "
                     f"frequencias e ausencias...")
        topos_dezenas: list[int] = self.get_topos_dezenas_jogos(10)

        # antes de criar os jogos, calcula o maximo de recorrencias para o bolao a ser criado:
        # com o numero real de apostas, verifica qual a faixa de recorrencias ira utilizar:
        max_recorrencias: int = self.get_max_recorrencias(bolao, FAIXAS_RECORRENCIAS)
        logger.info(f"{nmlot}: Vai utilizar como maximo de recorrencias a faixa  "
                    f"{max_recorrencias}.")

        # inicia a criacao do bolao, sorteando jogos para as apostas:
        logger.debug(f"{nmlot}: Iniciando a criacao do bolao para a loteria...")
        apostas_bolao: list[tuple[int, ...]] = []  # aqui estao as apostas
        jogos_bolao: list[tuple[int, ...]] = []  # aqui estao todas as combinacoes das apostas
        # utiliza os topos acumulados (merge) para complementar os jogos com mais dezenas:
        for qtd_dezenas, qtd_apostas in bolao.items():
            # se o numero de apostas estiver zerado, entao ignora esta faixa
            if qtd_apostas == 0:
                continue

            # efetua o sorteio do(s) jogo(s) com o numero de dezenas requerido:
            for _ in range(0, qtd_apostas):
                jogo_sorteado: tuple[int, ...] = self.sortear_jogo(max_recorrencias,
                                                                   jogos_bolao)
                # se for um numero maior de dezenas, eh preciso complementar o jogo:
                if qtd_dezenas > self.loteria.qtd_bolas_sorteio:
                    qtd_add: int = qtd_dezenas - self.loteria.qtd_bolas_sorteio
                    # obtem mais qtd-add dezenas a partir da lista topo-dezenas (do inicio):
                    for dezena in topos_dezenas:
                        # se ja pegou as dezenas necessarias, pula fora
                        if qtd_add == 0:
                            break
                        # eh preciso verificar se a dezena ja esta no jogo sorteado antes:
                        elif dezena not in jogo_sorteado:
                            qtd_add -= 1
                            jogo_sorteado += (dezena,)

                # se nao houver problema com as recorrencias, adiciona o jogo sorteado ao bolao:
                apostas_bolao.append(jogo_sorteado)
                # se for um numero maior de dezenas, tem q criar os jogos de base antes de incluir:
                if len(jogo_sorteado) == self.loteria.qtd_bolas_sorteio:
                    jogos_bolao.append(jogo_sorteado)
                else:
                    for jogo in itt.combinations(jogo_sorteado, self.loteria.qtd_bolas_sorteio):
                        jogos_bolao.append(jogo)

        logger.debug(f"{nmlot}: Finalizada a criacao de boloes para a loteria.")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return apostas_bolao

# ----------------------------------------------------------------------------
