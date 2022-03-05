"""
   Package lothon.domain.bilhete
   Module  cota.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class Cota:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_cota', '_qtd_cotas', '_preco_unitario', '_preco_total'

    @property
    def id_cota(self) -> str:
        return self._id_cota

    @id_cota.setter
    def id_cota(self, value):
        if isinstance(value, str):
            self._id_cota = value
        else:
            self._id_cota = str(value)

    @property
    def qtd_cotas(self) -> int:
        return self._qtd_cotas

    @qtd_cotas.setter
    def qtd_cotas(self, value):
        if isinstance(value, int):
            self._qtd_cotas = value
        elif isinstance(value, str):
            self._qtd_cotas = int(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'qtd_cotas' = {value}.")

    @property
    def preco_unitario(self) -> float:
        return self._preco_unitario

    @preco_unitario.setter
    def preco_unitario(self, value):
        if isinstance(value, float):
            self._preco_unitario = value
        elif isinstance(value, str):
            self._preco_unitario = float(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'preco_unitario' = {value}.")

    @property
    def preco_total(self) -> float:
        return self._preco_total

    @preco_total.setter
    def preco_total(self, value):
        if isinstance(value, float):
            self._preco_total = value
        elif isinstance(value, str):
            self._preco_total = float(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'preco_total' = {value}.")

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idc, qtd, punt, ptot):
        self.id_cota = idc
        self.qtd_cotas = qtd
        self.preco_unitario = punt
        self.preco_total = ptot

    def __repr__(self):
        return f"Cota{{ {self.id_cota}, {self.qtd_cotas}, {self.preco_unitario}, " \
               f"{self.preco_total} }}"

# ----------------------------------------------------------------------------
