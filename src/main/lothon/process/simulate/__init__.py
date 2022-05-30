"""
   Package lothon.process.simulate
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
from lothon.process.abstract_process import AbstractProcess
from lothon.process.simulate.simulado_aleatorio import SimuladoAleatorio
from lothon.process.simulate.simulado_analisado import SimuladoAnalisado
from lothon.process.simulate.simulado_pareado import SimuladoPareado


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# VARIAVEIS SINGLETON
# ----------------------------------------------------------------------------

_process_chain: list[AbstractProcess] = []


def get_process_chain() -> list[AbstractProcess]:
    global _process_chain
    if len(_process_chain) == 0:
        # _process_chain.append(SimuladoAleatorio())
        # _process_chain.append(SimuladoPareado())
        _process_chain.append(SimuladoAnalisado())

    return _process_chain

# ----------------------------------------------------------------------------
