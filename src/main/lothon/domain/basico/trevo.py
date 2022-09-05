"""
   Package lothon.domain.basico
   Module  trevo.py

"""

__all__ = [
    'Trevo'
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

class Trevo(Enum):
    """
    Implementacao de classe para .
    """

    # --- VALORES ENUMERADOS -------------------------------------------------
    TREVOS_12 = 1
    TREVOS_13 = 2
    TREVOS_14 = 3
    TREVOS_15 = 4
    TREVOS_16 = 5
    TREVOS_23 = 6
    TREVOS_24 = 7
    TREVOS_25 = 8
    TREVOS_26 = 9
    TREVOS_34 = 10
    TREVOS_35 = 11
    TREVOS_36 = 12
    TREVOS_45 = 13
    TREVOS_46 = 14
    TREVOS_56 = 15

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_str(value: str):
        if value is not None:
            value = value.strip().lower()

        if value in app_config.MAP_TREVOS.keys():
            numero = app_config.MAP_TREVOS[value]
            return Trevo(numero)
        else:
            raise ValueError(f"Valor invalido para criar instancia de Trevo: {value}.")

    @staticmethod
    def tag(value: int) -> str:
        if value == 0 or value is None:
            value = 1

        return app_config.TAG_TREVOS[(value - 1) % 15]

    @staticmethod
    def pair(value: int) -> tuple[int, ...]:
        if value == 0 or value is None:
            value = 1

        tag_trevos: str = app_config.TAG_TREVOS[(value - 1) % 15]
        list_trevos: list[int] = [int(t) for t in tag_trevos.split(' ')]

        return tuple(list_trevos)

    @staticmethod
    def str_pair(value: int) -> tuple[str, ...]:
        if value == 0 or value is None:
            value = 1

        tag_trevos: str = app_config.TAG_TREVOS[(value - 1) % 15]
        list_trevos: list[str] = [t for t in tag_trevos.split(' ')]

        return tuple(list_trevos)

    # ----------------------------------------------------------------------------
