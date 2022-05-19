
# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
# Libs/Frameworks modules
# Own/Project modules
from lothon.process.abstract_process import AbstractProcess
from lothon.process.analyze.analise_paridade import AnaliseParidade
from lothon.process.analyze.analise_repetencia import AnaliseRepetencia
from lothon.process.analyze.analise_sequencia import AnaliseSequencia
from lothon.process.analyze.analise_decenario import AnaliseDecenario
from lothon.process.analyze.analise_ciclica import AnaliseCiclica
from lothon.process.analyze.analise_somatoria import AnaliseSomatoria
from lothon.process.analyze.analise_frequencia import AnaliseFrequencia

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
        # _process_chain.append(AnaliseParidade())
        # _process_chain.append(AnaliseSequencia())
        _process_chain.append(AnaliseRepetencia())
        # _process_chain.append(AnaliseDecenario())
        # _process_chain.append(AnaliseCiclica())
        # _process_chain.append(AnaliseSomatoria())
        # _process_chain.append(AnaliseFrequencia())

    return _process_chain


# ----------------------------------------------------------------------------
