"""
   Package lothon.process
   Module  abstract_simulate.py

"""

__all__ = [
    'AbstractSimulate'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from abc import ABC
import itertools as itt

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain import Concurso
from lothon.process.abstract_process import AbstractProcess


# ----------------------------------------------------------------------------
# CLASSE ABSTRATA
# ----------------------------------------------------------------------------

class AbstractSimulate(AbstractProcess, ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de
    processos de simulacao de jogos.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idp: str):
        super().__init__(idp)

    # --- METODOS ------------------------------------------------------------

    # --- METODOS STATIC -----------------------------------------------------

    # confere relacao de jogos de um bolao com o(s) sorteio(s) de determinado concurso:
    @classmethod
    def check_premiacao_jogos(cls, concurso: Concurso, bolao: list[tuple[int, ...]],
                              qt_base: int = None) -> tuple[int, float]:
        qt_acertos: int = 0
        premio_total: float = 0.00

        # confere cada jogo do bolao e soma o valor das premiacoes:
        for jogo in bolao:
            # se o numero de bolas de cada jogo corresponde ao numero basico de dezenas da loteria:
            qt_bolas_jogo: int = len(jogo)
            if qt_base is None or qt_base == qt_bolas_jogo:
                # basta conferir cada jogo com o concurso:
                premiacao: float = concurso.check_premiacao_total(jogo)
                if premiacao > 0:
                    premio_total += premiacao
                    qt_acertos += 1

            # se o numero de bolas for inferior ao tamanho de cada jogo,
            elif qt_base < qt_bolas_jogo:  # # entao o bolao esta com jogos combinados,
                # deve-se gerar as combinacoes de BASE dezenas para cada jogo com x dezenas:
                for jogob in itt.combinations(jogo, qt_base):
                    premiacao: float = concurso.check_premiacao_total(jogob)
                    if premiacao > 0:
                        premio_total += premiacao
                        qt_acertos += 1

        return qt_acertos, premio_total

# ----------------------------------------------------------------------------
