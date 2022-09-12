"""
   Package lothon.process.betting
   Module  bet_mes_da_sorte.py

"""

__all__ = [
    'BetMesDaSorte'
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

class BetMesDaSorte(AbstractBetting):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('meses',)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, loteria: Loteria):
        super().__init__("Complemento de Boloes para Dia de Sorte", loteria)

        # mantem as informacoes dos meses computados:
        self.meses: list[int] = []

    # --- METODOS HELPERS ----------------------------------------------------

    def compute_meses_sorteados(self) -> list[int]:
        # extrai o ranking dos meses a partir dos topos de frequencias e ausencias nos concursos:
        meses_frequentes: list[int] = cb.calc_topos_frequencia(self.concursos,
                                                               self.loteria.qtd_bolas,
                                                               self.loteria.qtd_bolas)
        meses_ausentes: list[int] = cb.calc_topos_ausencia(self.concursos,
                                                           self.loteria.qtd_bolas,
                                                           self.loteria.qtd_bolas)

        meses_computados: list[int] = cb.merge_topos(meses_frequentes, meses_ausentes)
        return meses_computados

    def add_mes_da_sorte(self, apostas: list[tuple]) -> list[tuple]:
        apostas_com_mes: list[tuple] = []

        last_idx: int = len(self.meses) - 1  # idx_mes vai circular entre 0 ... 11
        idx_mes: int = last_idx
        for aposta in apostas:
            idx_mes = 0 if (idx_mes == last_idx) else (idx_mes + 1)
            mes_da_sorte: int = self.meses[idx_mes]
            aposta += (mes_da_sorte,)  # mes no formato numerico (1 ... 12)
            apostas_com_mes.append(aposta)

        return apostas_com_mes

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
        self.meses = self.compute_meses_sorteados()
        logger.debug(f"{nmlot}: Ranking dos meses da sorte conforme frequencias e ausencias:\n"
                     f"\t{self.meses}")

        # com os jogos/boloes criados, adiciona o mes da sorte:
        jogos_com_mes: list[tuple] = self.add_mes_da_sorte(jogos)
        logger.debug(f"{nmlot}: Finalizada a inclusao de mes da sorte para a loteria.")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return jogos_com_mes

# ----------------------------------------------------------------------------
