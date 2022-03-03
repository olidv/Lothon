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
# Own/Project modules
from lothon.util.eve import *


# ----------------------------------------------------------------------------
# CLASSE ABSTRATA
# ----------------------------------------------------------------------------

class Loteria(ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de classes
    que representam as loterias da Caixa.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    @property
    def id_loteria(self) -> str:
        return self.id_loteria

    @id_loteria.setter
    def id_loteria(self, value):
        if isinstance(value, str):
            self.id_loteria = value
        else:
            self.id_loteria = str(value)

    @property
    def nome_loteria(self) -> str:
        return self.nome_loteria

    @nome_loteria.setter
    def nome_loteria(self, value):
        if isinstance(value, str):
            self.nome_loteria = value
        else:
            self.nome_loteria = str(value)

    @property
    def tem_bola(self) -> bool:
        return self.tem_bola

    @tem_bola.setter
    def tem_bola(self, value):
        if isinstance(value, bool):
            self.tem_bola = value
        else:
            self.tem_bola = to_bool(value)

    @property
    def faixa_bola(self) -> tuple[int, int]:
        return self.faixa_bola

    @faixa_bola.setter
    def faixa_bola(self, value):
        if isinstance(value, tuple):
            self.faixa_bola = value
        elif isinstance(value, str):
            self.faixa_bola = tuple(map(int, value.split('-')))
        else:
            raise ValueError(f"Valor invalido para a propriedade 'faixa_bola' = {value}")

    @property
    def qtd_bolas_sorteio(self) -> int:
        return self.qtd_bolas_sorteio

    @qtd_bolas_sorteio.setter
    def qtd_bolas_sorteio(self, value):
        if isinstance(value, int):
            self.qtd_bolas_sorteio = value
        else:
            self.qtd_bolas_sorteio = int(value)

    @property
    def dias_sorteio(self) -> tuple[int, ...]:
        return self.dias_sorteio

    @dias_sorteio.setter
    def dias_sorteio(self, value):
        if isinstance(value, tuple):
            self.dias_sorteio = value
        elif isinstance(value, str):
            self.faixa_bola = tuple(map(int, value.split('|')))
        else:
            raise ValueError(f"Valor invalido para a propriedade 'dias_sorteio' = {value}.")

    @property
    def faixa_aposta(self) -> tuple[int, int]:
        return self.faixa_aposta

    @faixa_aposta.setter
    def faixa_aposta(self, value):
        if isinstance(value, tuple):
            self.faixa_aposta = value
        elif isinstance(value, str):
            self.faixa_aposta = tuple(map(int, value.split('-')))
        else:
            raise ValueError(f"Valor invalido para a propriedade 'faixa_aposta' = {value}.")

    @property
    def preco_aposta(self) -> float:
        return self.preco_aposta

    @preco_aposta.setter
    def preco_aposta(self, value):
        if isinstance(value, float):
            self.preco_aposta = value
        else:
            self.preco_aposta = float(value)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, dados: tuple[str, ...]):
        self.id_loteria = dados[0]
        self.nome_loteria = dados[1]
        self.tem_bola = dados[2]
        self.faixa_bolas = dados[3]
        self.qtd_bolas_sorteadas = dados[4]
        self.dias_sorteio = dados[5]
        self.faixa_aposta = dados[6]
        self.preco_aposta = dados[7]

    # --- METODOS ------------------------------------------------------------

    def get_tag_resultados(self) -> str:
        return self.id_loteria

    def get_file_resultados(self) -> str:
        return self.nome_loteria

# ----------------------------------------------------------------------------
