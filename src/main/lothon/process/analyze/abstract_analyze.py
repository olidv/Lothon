"""
   Package lothon.process
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
from lothon.domain import SerieSorteio
from lothon.process.abstract_process import AbstractProcess


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
    def setup(self, parms: dict):
        pass

    @abstractmethod
    def evaluate(self, payload) -> float:
        pass

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def new_list_int(cls, qtd_items: int) -> list[int]:
        list_zerado: list[int] = [0] * (qtd_items + 1)  # adiciona 1 para ignorar zero-index

        return list_zerado

    @classmethod
    def new_list_float(cls, qtd_items: int) -> list[float]:
        list_zerado: list[float] = [0.0] * (qtd_items + 1)  # adiciona 1 para ignorar zero-index

        return list_zerado

    @classmethod
    def new_list_series(cls, qtd_items: int) -> list[SerieSorteio | None]:
        # valida os parametros:
        if qtd_items is None or qtd_items == 0:
            return []

        bolas: list[SerieSorteio | None] = [None] * (qtd_items + 1)  # +1 para ignorar zero-index
        for i in range(0, qtd_items+1):
            bolas[i] = SerieSorteio(i)

        return bolas

# ----------------------------------------------------------------------------
