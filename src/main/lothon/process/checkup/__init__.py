"""
   Package lothon.process.checkup
   Module  __init__.py

"""

__all__ = [
    'get_process_chain'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
# Libs/Frameworks modules
# Own/Project modules
from lothon.process.checkup.abstract_checkup import AbstractCheckup
from lothon.process.checkup.check_bolao import CheckBolao


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# VARIAVEIS SINGLETON
# ----------------------------------------------------------------------------

_process_chain: list[AbstractCheckup] = []


def get_process_chain() -> list[AbstractCheckup]:
    global _process_chain
    if len(_process_chain) == 0:
        _process_chain.append(CheckBolao())

    return _process_chain

# ----------------------------------------------------------------------------
