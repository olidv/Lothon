"""
   Package lothon.process
   Module  abstract_compute.py

"""

__all__ = [
    'AbstractCompute'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from abc import ABC, abstractmethod

# Libs/Frameworks modules
# Own/Project modules
from lothon.process.abstract_process import AbstractProcess
from lothon.domain import Loteria


# ----------------------------------------------------------------------------
# CLASSE ABSTRATA
# ----------------------------------------------------------------------------

class AbstractCompute(AbstractProcess, ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de
    processos de computacao e calculo de jogos.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idp: str):
        super().__init__(idp)

    # --- METODOS ------------------------------------------------------------

    @abstractmethod
    def execute(self, loteria: Loteria) -> int:
        pass

    @abstractmethod
    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        pass

# ----------------------------------------------------------------------------
