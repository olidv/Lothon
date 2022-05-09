
# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
# Libs/Frameworks modules
# Own/Project modules
from lothon.process.abstract_process import AbstractProcess

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
        # _process_chain.append(FaixaSubsequente())
        pass

    return _process_chain


# ----------------------------------------------------------------------------
