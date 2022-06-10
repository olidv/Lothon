"""
   Package lothon.process.analyze
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
from lothon.process.analyze.abstract_analyze import AbstractAnalyze
from lothon.process.analyze.analise_ordinal import AnaliseOrdinal
from lothon.process.analyze.analise_matricial import AnaliseMatricial
from lothon.process.analyze.analise_paridade import AnaliseParidade
from lothon.process.analyze.analise_repetencia import AnaliseRepetencia
from lothon.process.analyze.analise_recorrencia import AnaliseRecorrencia
from lothon.process.analyze.analise_sequencia import AnaliseSequencia
from lothon.process.analyze.analise_decenario import AnaliseDecenario
from lothon.process.analyze.analise_ciclo import AnaliseCiclo
from lothon.process.analyze.analise_numerologia import AnaliseNumerologia
from lothon.process.analyze.analise_somatorio import AnaliseSomatorio
from lothon.process.analyze.analise_frequencia import AnaliseFrequencia
from lothon.process.analyze.analise_colunario import AnaliseColunario
from lothon.process.analyze.analise_distancia import AnaliseDistancia
from lothon.process.analyze.analise_espacamento import AnaliseEspacamento
from lothon.process.analyze.analise_semanal import AnaliseSemanal
from lothon.process.analyze.analise_dispersao import AnaliseDispersao


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# VARIAVEIS SINGLETON
# ----------------------------------------------------------------------------

_process_chain: list[AbstractAnalyze] = []


def get_process_chain() -> list[AbstractAnalyze]:
    global _process_chain
    if len(_process_chain) == 0:
        # inicia pelas analises que podem ser feitas de forma mais simples:
        # _process_chain.append(AnaliseMatricial())    # 0:00:32
        # _process_chain.append(AnaliseParidade())     # 0:00:32
        # _process_chain.append(AnaliseSequencia())    # 0:00:47
        # _process_chain.append(AnaliseSomatorio())    # 0:00:11
        # _process_chain.append(AnaliseDistancia())    # 0:00:40
        # _process_chain.append(AnaliseEspacamento())  # 0:01:03
        # _process_chain.append(AnaliseOrdinal())      # 0:00:32
        # _process_chain.append(AnaliseRepetencia())   # 0:00:24
        # _process_chain.append(AnaliseRecorrencia())  # 0:00:31

        # _process_chain.append(AnaliseFrequencia())   # 0:00:00
        _process_chain.append(AnaliseDispersao())    # 0:00:00
        # _process_chain.append(AnaliseCiclo())        # 0:00:00
        # _process_chain.append(AnaliseNumerologia())  # 0:00:08
        # _process_chain.append(AnaliseColunario())    # 0:00:45
        # _process_chain.append(AnaliseDecenario())    # 0:00:45
        # _process_chain.append(AnaliseSemanal())      # 0:00:00

    return _process_chain

# ----------------------------------------------------------------------------
