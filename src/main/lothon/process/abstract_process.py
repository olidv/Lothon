"""
   Package lothon.process
   Module  abstract_process.py

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

class AbstractProcess(ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de processos.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    @property
    def id_process(self) -> str:
        return self._id_process

    @id_process.setter
    def id_process(self, value):
        if isinstance(value, str):
            self._id_process = value
        else:
            self._id_process = str(value)

    @property
    def options(self) -> dict:
        return self._options

    @options.setter
    def options(self, value):
        if value is None or isinstance(value, dict):
            self._options = value
        else:
            raise ValueError(f"Valor invalido para a propriedade  options : dict = {value}.")

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idp: str):
        self.id_process = idp
        self.options = None

    # --- METODOS ------------------------------------------------------------

    def init(self, options: dict) -> None:
        self.options = options

    @abstractmethod
    def execute(self, payload) -> None:
        pass

# ----------------------------------------------------------------------------
