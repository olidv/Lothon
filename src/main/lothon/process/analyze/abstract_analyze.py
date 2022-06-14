"""
   Package lothon.process.analyze
   Module  abstract_analyze.py

"""

__all__ = [
    'AbstractAnalyze'
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

class AbstractAnalyze(AbstractProcess, ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de
    processos de analise de jogos.
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

# ----------------------------------------------------------------------------
