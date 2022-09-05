"""
   Package lothon.process.quickpick
   Module  pick_mega_sena.py

"""

__all__ = [
    'PickMegaSena'
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

# limite de recorrencias especificas para esta loteria:
FAIXA_RECORRENCIAS: int = 2


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class PickMegaSena(AbstractQuickPick):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, loteria: Loteria):
        super().__init__("Geracao de Palpites para Mega-Sena", loteria)

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

        # identifica informacoes da loteria:
        nmlot: str = self.loteria.nome_loteria

        # verifica se os concursos ja foram computados e gerou arquivo com jogos computados:
        if self.existe_jogos_computados():
            logger.debug(f"{nmlot}: Arquivo com jogos computados ja existe. "
                         f"Processo externo ignorado.")
        # se ainda nao existe o arquivo com os jogos computados, entao inicia o processo externo:
        else:
            logger.debug(f"{nmlot}: Arquivo com jogos computados nao encontrado. "
                         f"Iniciando processo externo.")
            # Vai exportar os arquivos CSV com dezenas sorteadas das loterias...
            qtd_export: int = self.exportar_sorteios()
            logger.debug(f"{nmlot}: Foram exportados #{formatd(qtd_export)} sorteios da "
                         f"loteria em arquivo CSV.")

            # executa rotina Java para processamento e geracao dos jogos computados:
            run_ok: bool = self.executar_jlothon()
            if run_ok:
                logger.debug(f"{nmlot}: Programa jLothon foi executado com sucesso.")
            else:
                logger.error(f"{nmlot}: Erro na execucao do programa jLothon. "
                             f"Geracao de boloes abortada.")
                return []

        # importa os jogos computados em jLothon para prosseguir com o processamento:
        self.jogos = self.importar_jogos()
        qtd_jogos: int = len(self.jogos)
        logger.debug(f"{nmlot}: Foram importados  #{formatd(qtd_jogos)}  jogos computados da "
                     f"loteria de arquivo CSV.")

        # antes de gerar os palpites, calcula o maximo de recorrencias para cada jogo sorteado:
        # com o numero real de apostas, verifica qual a faixa de recorrencias ira utilizar:
        max_recorrencias: int = FAIXA_RECORRENCIAS
        logger.info(f"{nmlot}: Vai utilizar como maximo de recorrencias a faixa  "
                    f"{max_recorrencias}.")

        # inicia a geracao dos palpites, sorteando jogos para as apostas:
        logger.debug(f"{nmlot}: Iniciando a geracao dos palpites para a loteria...")
        jogos_sorteados: list[tuple[int, ...]] = []  # aqui estao todos os palpites

        # efetua o sorteio do(s) jogo(s) com o numero de dezenas requerido:
        for _ in range(0, qtd_palpites):
            jogo_sorteado: tuple[int, ...] = self.sortear_jogo(max_recorrencias, jogos_sorteados)
            # adiciona o jogo sorteado a lista de palpites:
            jogos_sorteados.append(jogo_sorteado)

        # com os jogos gerados, converte as dezenas das tuplas em strings de 2 digitos:
        palpites: list[tuple[str, ...]] = [tuple(f"{i:02}" for i in t) for t in jogos_sorteados]
        logger.debug(f"{nmlot}: Finalizada a geracao de  {qtd_palpites}  palpites para a loteria.")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return palpites

# ----------------------------------------------------------------------------
