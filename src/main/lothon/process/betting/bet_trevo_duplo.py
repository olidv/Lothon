"""
   Package lothon.process.betting
   Module  bet_trevo_duplo.py

"""

__all__ = [
    'BetTrevoDuplo'
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
from lothon.domain import Loteria, Concurso, Trevo
from lothon.process.betting.abstract_betting import AbstractBetting

# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class BetTrevoDuplo(AbstractBetting):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('trevos',)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, loteria: Loteria):
        super().__init__("Complemento de Boloes para +Milionaria", loteria)

        # mantem as informacoes dos trevos computados:
        self.trevos: list[int] = []

    # --- METODOS HELPERS ----------------------------------------------------

    def compute_trevos_sorteados(self) -> list[int]:
        # extrai o ranking dos trevos a partir dos topos de frequencias e ausencias nos concursos:
        trevos_frequentes: list[int] = cb.calc_topos_frequencia(self.concursos,
                                                                self.loteria.qtd_bolas,
                                                                self.loteria.qtd_bolas)
        trevos_ausentes: list[int] = cb.calc_topos_ausencia(self.concursos,
                                                            self.loteria.qtd_bolas,
                                                            self.loteria.qtd_bolas)

        trevos_computados: list[int] = cb.merge_topos(trevos_frequentes, trevos_ausentes)
        return trevos_computados

    def add_trevo_duplo(self, apostas: list[tuple]) -> list[tuple]:
        apostas_com_trevo: list[tuple] = []

        last_idx: int = len(self.trevos) - 1  # idx_trevo vai circular entre 0 ... 14
        idx_trevo: int = last_idx
        for aposta in apostas:
            idx_trevo = 0 if (idx_trevo == last_idx) else (idx_trevo + 1)
            enum_trevo: int = self.trevos[idx_trevo]
            aposta += Trevo.pair(enum_trevo)  # trevos no formato tupla: (1, 2) ... (5, 6)
            apostas_com_trevo.append(aposta)

        return apostas_com_trevo

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

        # eh preciso antes processar os trevos numerados nos sorteios ocorridos:
        logger.debug(f"{nmlot}: Executando computacao dos sorteios do Trevo Duplo...")
        self.trevos = self.compute_trevos_sorteados()
        logger.debug(f"{nmlot}: Ranking dos trevos da sorte conforme frequencias e ausencias:\n"
                     f"\t{self.trevos}")

        # com os jogos criados, adiciona o trevo duplo:
        jogos_com_trevo: list[tuple] = self.add_trevo_duplo(jogos)
        logger.debug(f"{nmlot}: Finalizada a inclusao de trevos duplos para a loteria.")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return jogos_com_trevo

# ----------------------------------------------------------------------------
