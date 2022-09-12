"""
   Package lothon.process.betting
   Module  bet_time_do_coracao.py

"""

__all__ = [
    'BetTimeDoCoracao'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.stats import combinatoria as cb
from lothon.domain import Loteria, Concurso
from lothon.process.betting.abstract_betting import AbstractBetting

# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class BetTimeDoCoracao(AbstractBetting):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('clubes',)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, loteria: Loteria):
        super().__init__("Complemento de Boloes para Timemania", loteria)

        # mantem as informacoes dos clubes computados:
        self.clubes: list[int] = []

    # --- METODOS HELPERS ----------------------------------------------------

    def compute_clubes_sorteados(self) -> list[int]:
        # extrai o ranking dos clubes a partir dos topos de frequencias e ausencias nos concursos:
        clubes_frequentes: list[int] = cb.calc_topos_frequencia(self.concursos,
                                                                self.loteria.qtd_bolas,
                                                                self.loteria.qtd_bolas)
        clubes_ausentes: list[int] = cb.calc_topos_ausencia(self.concursos,
                                                            self.loteria.qtd_bolas,
                                                            self.loteria.qtd_bolas)

        clubes_computados: list[int] = cb.merge_topos(clubes_frequentes, clubes_ausentes)
        return clubes_computados

    def add_clube_do_coracao(self, apostas: list[tuple]) -> list[tuple]:
        apostas_com_clube: list[tuple] = []

        last_idx: int = len(self.clubes) - 1  # idx_clube vai circular entre 0 ... 79
        idx_clube: int = last_idx
        for aposta in apostas:
            idx_clube = 0 if (idx_clube == last_idx) else (idx_clube + 1)
            clube_do_coracao: int = self.clubes[idx_clube]
            aposta += (clube_do_coracao,)  # mes no formato numerico (1 ... 80)
            apostas_com_clube.append(aposta)

        return apostas_com_clube

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, jogos: list[tuple], concursos: list[Concurso] = None) -> list[tuple]:
        # valida se possui concursos a serem analisados:
        if jogos is None or len(jogos) == 0:
            return []
        elif concursos is not None:
            if len(concursos) > 0:
                self.concursos = concursos
            else:
                return []
        _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = self.loteria.nome_loteria

        # eh preciso antes processar os meses da sorte nos sorteios ocorridos:
        logger.debug(f"{nmlot}: Executando computacao dos sorteios do Mes da Sorte...")
        self.clubes = self.compute_clubes_sorteados()
        logger.debug(f"{nmlot}: Ranking dos times do coracao conforme frequencias e ausencias:\n"
                     f"\t{self.clubes}")

        # com os jogos/boloes criados, adiciona o clube do coracao:
        jogos_com_clube: list[tuple] = self.add_clube_do_coracao(jogos)
        logger.debug(f"{nmlot}: Finalizada a inclusao de clube do coracao para a loteria.")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return jogos_com_clube

# ----------------------------------------------------------------------------
