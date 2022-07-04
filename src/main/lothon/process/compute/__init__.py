"""
   Package lothon.process.compute
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
from lothon.process.compute.abstract_compute import AbstractCompute
from lothon.process.compute.compute_ordinal import ComputeOrdinal
from lothon.process.compute.compute_matricial import ComputeMatricial
from lothon.process.compute.compute_mediana import ComputeMediana
from lothon.process.compute.compute_paridade import ComputeParidade
from lothon.process.compute.compute_repetencia import ComputeRepetencia
from lothon.process.compute.compute_recorrencia import ComputeRecorrencia
from lothon.process.compute.compute_sequencia import ComputeSequencia
from lothon.process.compute.compute_decenario import ComputeDecenario
from lothon.process.compute.compute_ciclo import ComputeCiclo
from lothon.process.compute.compute_numerologia import ComputeNumerologia
from lothon.process.compute.compute_somatorio import ComputeSomatorio
from lothon.process.compute.compute_frequencia import ComputeFrequencia
from lothon.process.compute.compute_ausencia import ComputeAusencia
from lothon.process.compute.compute_colunario import ComputeColunario
from lothon.process.compute.compute_distancia import ComputeDistancia
from lothon.process.compute.compute_espacamento import ComputeEspacamento
from lothon.process.compute.compute_dispersao import ComputeDispersao


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# VARIAVEIS SINGLETON
# ----------------------------------------------------------------------------

_process_chain: list[AbstractCompute] = []


def get_process_chain() -> list[AbstractCompute]:
    global _process_chain
    if len(_process_chain) == 0:
        # inicia pelas computacoes que podem ser feitas de forma mais simples:
        _process_chain.append(ComputeAusencia())     # 0:00:
        _process_chain.append(ComputeCiclo())        # 0:00:
        _process_chain.append(ComputeColunario())    # 0:00:
        _process_chain.append(ComputeDecenario())    # 0:00:
        _process_chain.append(ComputeDispersao())    # 0:00:
        _process_chain.append(ComputeDistancia())    # 0:00:-13s
        _process_chain.append(ComputeEspacamento())  # 0:00:-03s
        _process_chain.append(ComputeFrequencia())   # 0:00:
        _process_chain.append(ComputeMatricial())    # 0:00:-22s
        _process_chain.append(ComputeMediana())      # 0:00:-22s
        _process_chain.append(ComputeNumerologia())  # 0:00:
        _process_chain.append(ComputeOrdinal())      # 0:00:-31s
        _process_chain.append(ComputeParidade())     # 0:00:-01s
        _process_chain.append(ComputeRepetencia())   # 0:00:-04s
        _process_chain.append(ComputeSequencia())    # 0:00:-23s
        _process_chain.append(ComputeSomatorio())    # 0:00:+06s

        # executado com cuidado, pois aumenta tempo de processamento:
        _process_chain.append(ComputeRecorrencia())  # 0:00:+25m  ...  30 min, 7 seg, 765 ms

    return _process_chain

# ----------------------------------------------------------------------------
