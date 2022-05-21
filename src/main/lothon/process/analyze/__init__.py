
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
from lothon.process.analyze.analise_ciclo import AnaliseCiclo
from lothon.process.analyze.analise_somatorio import AnaliseSomatorio
from lothon.process.analyze.analise_frequencia import AnaliseFrequencia
from lothon.process.analyze.analise_colunario import AnaliseColunario
from lothon.process.analyze.analise_distancia import AnaliseDistancia
from lothon.process.analyze.analise_espacamento import AnaliseEspacamento

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
        _process_chain.append(AnaliseCiclo())        # 0:00:00
        _process_chain.append(AnaliseFrequencia())   # 0:00:00
        _process_chain.append(AnaliseSomatorio())    # 0:00:11
        _process_chain.append(AnaliseRepetencia())   # 0:00:24
        _process_chain.append(AnaliseParidade())     # 0:00:32
        _process_chain.append(AnaliseDistancia())    # 0:00:40
        _process_chain.append(AnaliseColunario())    # 0:00:45
        _process_chain.append(AnaliseDecenario())    # 0:00:45
        _process_chain.append(AnaliseSequencia())    # 0:00:47
        _process_chain.append(AnaliseEspacamento())  # 0:01:03

    return _process_chain


# ----------------------------------------------------------------------------
