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
from lothon.domain import Concurso
from lothon.process.abstract_process import AbstractProcess


# ----------------------------------------------------------------------------
# CLASSE ABSTRATA
# ----------------------------------------------------------------------------

class AbstractCompute(AbstractProcess, ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de
    processos de computacao e calculo de jogos.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('min_threshold', 'qtd_bolas', 'qtd_bolas_sorteio', 'qtd_jogos', 'qtd_zerados')

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idp: str, threshold: int = 0):
        super().__init__(idp)

        # auxiliares para avaliacao de jogos combinados e concursos da loteria:
        self.min_threshold: int = threshold
        self.qtd_bolas: int = 0
        self.qtd_bolas_sorteio: int = 0
        self.qtd_jogos: int = 0
        self.qtd_zerados: int = 0

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

        # verifica se algum valor das propriedades foi fornecido:
        self.qtd_bolas = self.options.get('qtd_bolas', 0)
        self.qtd_bolas_sorteio = self.options.get('qtd_bolas_sorteio', 0)
        self.qtd_jogos = self.options.get('qtd_jogos', 0)
        self.qtd_zerados = self.options.get('qtd_zerados', 0)

    # --- METODOS ------------------------------------------------------------

    @abstractmethod
    def execute(self, concursos: list[Concurso]) -> int:
        pass

    @abstractmethod
    def set_concursos_passados(self, concursos: list[Concurso]):
        pass

    @abstractmethod
    def rate(self, ordinal: int, jogo: tuple) -> int:
        pass

    @abstractmethod
    def eval(self, ordinal: int, jogo: tuple) -> float:
        pass

    @abstractmethod
    def evaluate(self, ordinal: int, jogo: tuple) -> float:
        pass

# ----------------------------------------------------------------------------
