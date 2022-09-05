"""
   Package lothon.process.quickpick
   Module  pick_quina.py

"""

__all__ = [
    'PickQuina'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.domain import Loteria, Concurso
from lothon.process.quickpick.abstract_quickpick import AbstractQuickPick


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# faixas de limites de recorrencias especificas para esta loteria:
FAIXAS_RECORRENCIAS: dict[int: int] = {0: 8, 1: 211, 2: 4208}


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class PickQuina(AbstractQuickPick):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, loteria: Loteria):
        super().__init__("Geracao de Palpites para Quina", loteria)

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, qtd_palpites: int, concursos: list[Concurso] = None) -> list[tuple]:
        # valida se possui concursos a serem analisados:
        if qtd_palpites is None or qtd_palpites == 0:
            return []
        elif concursos is not None:
            if len(concursos) > 0:
                self.concursos = concursos
            else:
                return []
        _startWatch = startwatch()

        # verifica se os concursos ja foram computados e gerou arquivo com jogos computados:
        if self.existe_jogos_computados():
            logger.debug("Arquivo com jogos computados ja existe. Processo externo ignorado.")
        # se ainda nao existe o arquivo com os jogos computados, entao inicia o processo externo:
        else:
            logger.debug(
                "Arquivo com jogos computados nao encontrado. Iniciando processo externo.")
            # Vai exportar os arquivos CSV com dezenas sorteadas das loterias...
            qtd_export: int = self.exportar_sorteios()
            logger.debug(f"Foram exportados #{formatd(qtd_export)} sorteios da loteria "
                         f"'{self.loteria.nome_loteria}' em arquivo CSV.")

            # executa rotina Java para processamento e geracao dos jogos computados:
            run_ok: bool = self.executar_jlothon()
            if run_ok:
                logger.debug(f"Programa jLothon foi executado com sucesso.")
            else:
                logger.error(
                    f"Erro na execucao do programa jLothon. Geracao de boloes abortada.")
                return []

        # importa os jogos computados em jLothon para prosseguir com o processamento:
        self.jogos = self.importar_jogos()
        qtd_jogos: int = len(self.jogos)
        logger.debug(f"Foram importados  #{formatd(qtd_jogos)}  jogos computados da loteria "
                     f"{self.loteria.nome_loteria}' de arquivo CSV.")

        # antes de gerar os palpites, calcula o maximo de recorrencias para cada jogo sorteado:
        # com o numero real de apostas, verifica qual a faixa de recorrencias ira utilizar:
        max_recorrencias: int = self.get_max_recorrencias(qtd_palpites, FAIXAS_RECORRENCIAS)
        logger.info(f"Vai utilizar como maximo de recorrencias a faixa  {max_recorrencias}.")

        # inicia a geracao dos palpites, sorteando jogos para as apostas:
        logger.debug(f"Iniciando a geracao dos palpites para loteria DIA-DE-SORTE...")
        jogos_sorteados: list[tuple[int, ...]] = []  # aqui estao todos os palpites

        # efetua o sorteio do(s) jogo(s) com o numero de dezenas requerido:
        for _ in range(0, qtd_palpites):
            jogo_sorteado: tuple[int, ...] = self.sortear_jogo(max_recorrencias, jogos_sorteados)
            # adiciona o jogo sorteado a lista de palpites:
            jogos_sorteados.append(jogo_sorteado)

        # com os jogos gerados, converte as dezenas das tuplas em strings de 2 digitos:
        palpites: list[tuple[str, ...]] = [tuple(f"{i:02}" for i in t) for t in jogos_sorteados]

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return palpites

# ----------------------------------------------------------------------------
