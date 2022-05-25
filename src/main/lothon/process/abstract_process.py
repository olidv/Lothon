"""
   Package lothon.process
   Module  abstract_process.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from abc import ABC, abstractmethod
from typing import Optional

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain import Bola


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

    def init(self, options: dict):
        self.options = options

    @abstractmethod
    def execute(self, payload) -> int:
        pass

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def new_list_int(qtd_items: int) -> list[int]:
        list_zerado: list[int] = [0] * (qtd_items + 1)  # adiciona 1 para ignorar zero-index

        return list_zerado

    @staticmethod
    def new_list_float(qtd_items: int) -> list[float]:
        list_zerado: list[float] = [0.0] * (qtd_items + 1)  # adiciona 1 para ignorar zero-index

        return list_zerado

    @staticmethod
    def new_list_bolas(qtd_items: int) -> list[Optional[Bola]]:
        # valida os parametros:
        if qtd_items is None or qtd_items == 0:
            return []

        bolas: list[Optional[Bola]] = [None] * (qtd_items + 1)  # adiciona 1 para ignorar zero-index
        for i in range(0, qtd_items+1):
            bolas[i] = Bola(i)

        return bolas

# ----------------------------------------------------------------------------
