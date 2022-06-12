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
from abc import ABC, abstractmethod

# Libs/Frameworks modules
# Own/Project modules
from lothon.process.abstract_process import AbstractProcess
from lothon.domain import Loteria


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

    @abstractmethod
    def execute(self, payload: Loteria) -> int:
        pass

# ----------------------------------------------------------------------------
