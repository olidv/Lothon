"""
   Package lothon.process
   Module  abstract_betting.py

"""

__all__ = [
    'AbstractBetting'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from abc import ABC, abstractmethod

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain import Loteria, Concurso
from lothon.process.abstract_process import AbstractProcess


# ----------------------------------------------------------------------------
# CLASSE ABSTRATA
# ----------------------------------------------------------------------------

class AbstractBetting(AbstractProcess, ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de
    processos de computacao e calculo de jogos.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('loteria', 'concursos')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idp: str, loteria: Loteria):
        super().__init__(idp)

        # auxiliares para avaliacao de jogos combinados e concursos da loteria:
        self.loteria: Loteria = loteria
        self.concursos: list[Concurso] = loteria.concursos

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

    # --- METODOS ------------------------------------------------------------

    @abstractmethod
    def execute(self, bolao: dict[int: int],
                concursos: list[Concurso] = None) -> list[tuple[int, ...]]:
        pass

# ----------------------------------------------------------------------------
