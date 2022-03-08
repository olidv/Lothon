"""
   Package lothon.domain.sorteio
   Module  faixa.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import math

# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class Faixa:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_faixa', '_preco', '_qtd_apostas'

    @property
    def id_faixa(self) -> int:
        return self._id_faixa

    @id_faixa.setter
    def id_faixa(self, value):
        if isinstance(value, int):
            self._id_faixa = value
        elif isinstance(value, str):
            self._id_faixa = int(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'id_faixa' = {value}.")

    @property
    def preco(self) -> float:
        return self._preco

    @preco.setter
    def preco(self, value):
        if isinstance(value, float):
            self._preco = value
        elif isinstance(value, str):
            self._preco = float(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'preco' = {value}.")

    @property
    def qtd_apostas(self) -> int:
        return self._qtd_apostas

    @qtd_apostas.setter
    def qtd_apostas(self, value):
        if isinstance(value, int):
            self._qtd_apostas = value
        elif isinstance(value, str):
            self._qtd_apostas = int(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'qtd_apostas' = {value}.")

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, idf, prec, qtda):
        self.id_faixa = idf
        self.preco = prec
        self.qtd_apostas = qtda

    def __repr__(self):
        return f"Faixa{{ {self.id_faixa}, R${self.preco}, {self.qtd_apostas} }}"

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_str(vals: str) -> list:
        if vals is None:
            raise ValueError(f"Valor invalido para criar instancia de Faixa: {vals}.")

        # 7-15:2.00   |   10-10:3.00   |   1-1:2.00
        termos = vals.split(':')
        if len(termos) == 0:
            raise ValueError(f"Valor invalido para criar instancia de Faixa: {vals}.")

        interval = termos[0].split('-')
        if len(interval) == 0:
            raise ValueError(f"Valor invalido para criar instancia de Faixa: {vals}.")

        qtd_min = int(interval[0])
        qtd_max = int(interval[1])
        preco_min = float(termos[1])

        faixas: list[Faixa] = [Faixa(qtd_min, preco_min, 1)]
        if qtd_max > qtd_min:
            for qtd in range(qtd_min + 1, qtd_max + 1):
                jogos = math.comb(qtd, qtd_min)
                preco = jogos * preco_min

                fx = Faixa(qtd, preco, jogos)
                faixas.append(fx)

        return faixas

# ----------------------------------------------------------------------------
