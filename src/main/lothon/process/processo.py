"""
   Package lothon.process
   Module  processo.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from abc import ABC, abstractmethod

# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# CLASSE ABSTRATA
# ----------------------------------------------------------------------------

class Processo(ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de processos.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    @property
    def id_processo(self) -> str:
        return self.id_processo

    @id_processo.setter
    def id_processo(self, value):
        if isinstance(value, str):
            self.id_processo = value
        else:
            self.id_processo = str(value)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idp):
        self.id_processo = idp

    # --- METODOS ------------------------------------------------------------

    @abstractmethod
    def init(self, universo) -> None:
        pass

    @abstractmethod
    def execute(self) -> None:
        pass

# ----------------------------------------------------------------------------
