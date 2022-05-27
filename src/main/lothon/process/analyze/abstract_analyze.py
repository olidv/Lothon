"""
   Package lothon.process
   Module  abstract_analyze.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from abc import ABC
from typing import Optional

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain import Bola
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

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idp: str):
        super().__init__(idp)

    # --- METODOS ------------------------------------------------------------

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
