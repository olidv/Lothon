"""
   Package lothon.process
   Module  abstract_process.py

"""

__all__ = [
    'AbstractProcess'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from abc import ABC, abstractmethod
from typing import Any

# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# CLASSE ABSTRATA
# ----------------------------------------------------------------------------

class AbstractProcess(ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de processos.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('id_process', 'options')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idp: str):
        self.id_process: str = idp
        self.options: dict = {}

    # --- METODOS ------------------------------------------------------------

    def set_options(self, parms: dict):
        # absorve os parametros fornecidos:
        if parms is not None:
            for k, v in parms.items():
                self.options[k] = v

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        self.set_options(parms)

    @abstractmethod
    def execute(self, payload: Any):
        pass

# ----------------------------------------------------------------------------
