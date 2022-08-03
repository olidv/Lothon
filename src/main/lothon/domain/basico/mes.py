"""
   Package lothon.domain.basico
   Module  mes.py

"""

__all__ = [
    'Mes'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from enum import Enum

# Libs/Frameworks modules
# Own/Project modules
from lothon.conf import app_config


# ----------------------------------------------------------------------------
# CLASSE ENUMERACAO
# ----------------------------------------------------------------------------

class Mes(Enum):
    """
    Implementacao de classe para .
    """

    # --- VALORES ENUMERADOS -------------------------------------------------
    JANEIRO = 1
    FEVEREIRO = 2
    MARCO = 3
    ABRIL = 4
    MAIO = 5
    JUNHO = 6
    JULHO = 7
    AGOSTO = 8
    SETEMBRO = 9
    OUTUBRO = 10
    NOVEMBRO = 11
    DEZEMBRO = 12

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_str(value: str):
        if value is not None:
            value = value.strip().lower()

        if value in app_config.MAP_MESES.keys():
            numero = app_config.MAP_MESES[value]
            return Mes(numero)
        else:
            raise ValueError(f"Valor invalido para criar instancia de Mes: {value}.")

    @staticmethod
    def tag(value: int) -> str:
        if value == 0 or value is None:
            value = 1

        return app_config.TAG_MESES[(value - 1) % 12]

    # ----------------------------------------------------------------------------
