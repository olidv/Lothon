"""
   Package lothon.domain.sorteio
   Module  premio.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class Premio:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_acertos', '_qtd_ganhadores', '_premio'

    @property
    def acertos(self) -> int:
        return self._acertos

    @acertos.setter
    def acertos(self, value):
        if isinstance(value, int):
            self._acertos = value
        elif isinstance(value, str):
            self._acertos = int(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'acertos' = {value}.")

    @property
    def qtd_ganhadores(self) -> int:
        return self._qtd_ganhadores

    @qtd_ganhadores.setter
    def qtd_ganhadores(self, value):
        if isinstance(value, int):
            self._qtd_ganhadores = value
        elif isinstance(value, str):
            self._qtd_ganhadores = int(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'qtd_ganhadores' = {value}.")

    @property
    def premio(self) -> float:
        return self._premio

    @premio.setter
    def premio(self, value):
        if isinstance(value, float):
            self._premio = value
        elif isinstance(value, str):
            self._premio = parse_money(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'premio' = {value}.")

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, acert, qtdg, prem):
        self.acertos = acert
        self.qtd_ganhadores = qtdg
        self.premio = prem

    def __repr__(self):
        return f"Premio{{ acertos={self.acertos}, qtd_ganhadores={self.qtd_ganhadores}, " \
               f"premio=R${self.premio} }}"

# ----------------------------------------------------------------------------
