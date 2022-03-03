"""
   Package lothon.domain.produto
   Module  loteria.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from abc import ABC, abstractmethod

# Libs/Frameworks modules
from bs4.element import Tag

# Own/Project modules
from lothon.util.eve import *
from lothon.domain.sorteio.concurso import Concurso


# ----------------------------------------------------------------------------
# CLASSE ABSTRATA
# ----------------------------------------------------------------------------

class Loteria(ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de classes
    que representam as loterias da Caixa.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    # __slots__ = ()

    @property
    def id_loteria(self) -> str:
        return self._id_loteria

    @id_loteria.setter
    def id_loteria(self, value):
        if isinstance(value, str):
            self._id_loteria = value
        else:
            self._id_loteria = str(value)

    @property
    def nome_loteria(self) -> str:
        return self._nome_loteria

    @nome_loteria.setter
    def nome_loteria(self, value):
        if isinstance(value, str):
            self._nome_loteria = value
        else:
            self._nome_loteria = str(value)

    @property
    def tem_bola(self) -> bool:
        return self._tem_bola

    @tem_bola.setter
    def tem_bola(self, value):
        if isinstance(value, bool):
            self._tem_bola = value
        else:
            self._tem_bola = to_bool(value)

    @property
    def faixa_bola(self) -> tuple[int, int]:
        return self._faixa_bola

    @faixa_bola.setter
    def faixa_bola(self, value):
        if isinstance(value, tuple):
            self._faixa_bola = value
        elif isinstance(value, str):
            self._faixa_bola = tuple(map(int, value.split('-')))
        else:
            raise ValueError(f"Valor invalido para a propriedade 'faixa_bola' = {value}")

    @property
    def qtd_bolas_sorteio(self) -> int:
        return self._qtd_bolas_sorteio

    @qtd_bolas_sorteio.setter
    def qtd_bolas_sorteio(self, value):
        if isinstance(value, int):
            self._qtd_bolas_sorteio = value
        else:
            self._qtd_bolas_sorteio = int(value)

    @property
    def dias_sorteio(self) -> tuple[int, ...]:
        return self._dias_sorteio

    @dias_sorteio.setter
    def dias_sorteio(self, value):
        if isinstance(value, tuple):
            self._dias_sorteio = value
        elif isinstance(value, str):
            self._dias_sorteio = tuple(map(int, value.split('|')))
        else:
            raise ValueError(f"Valor invalido para a propriedade 'dias_sorteio' = {value}.")

    @property
    def faixa_aposta(self) -> tuple[int, int]:
        return self._faixa_aposta

    @faixa_aposta.setter
    def faixa_aposta(self, value):
        if isinstance(value, tuple):
            self._faixa_aposta = value
        elif isinstance(value, str):
            self._faixa_aposta = tuple(map(int, value.split('-')))
        else:
            raise ValueError(f"Valor invalido para a propriedade 'faixa_aposta' = {value}.")

    @property
    def preco_aposta(self) -> float:
        return self._preco_aposta

    @preco_aposta.setter
    def preco_aposta(self, value):
        if isinstance(value, float):
            self._preco_aposta = value
        else:
            self._preco_aposta = float(value)

    @property
    def concursos(self) -> list[Concurso]:
        return self._concursos

    @concursos.setter
    def concursos(self, value):
        if isinstance(value, list) or value is None:
            self._concursos = value
        else:
            raise ValueError(f"Valor invalido para a propriedade 'concursos' = {value}.")

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, dados: tuple[str, ...]):
        self.id_loteria = dados[0]
        self.nome_loteria = dados[1]
        self.tem_bola = dados[2]
        self.faixa_bola = dados[3]
        self.qtd_bolas_sorteio = dados[4]
        self.dias_sorteio = dados[5]
        self.faixa_aposta = dados[6]
        self.preco_aposta = dados[7]
        self.concursos = None

    # --- METODOS ------------------------------------------------------------

    def get_tag_resultados(self) -> str:
        return self.id_loteria

    def get_file_resultados(self) -> str:
        return self.nome_loteria

    @abstractmethod
    def parse_concurso(self, td: Tag) -> Concurso:
        pass

# ----------------------------------------------------------------------------
