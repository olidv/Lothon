"""
   Package lothon.domain.basico
   Module  estrutura.py

"""

__all__ = [
    'LoteriaStruct',
    'PremiacaoStruct',
    'BolaoStruct'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from collections import namedtuple

# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# ESTRUTURAS DE DADOS
# ----------------------------------------------------------------------------

#
LoteriaStruct = namedtuple('LoteriaStruct', 'jogos fatores')

#
PremiacaoStruct = namedtuple('PremiacaoStruct', 'acertos premio')

#
BolaoStruct = namedtuple('BolaoStruct', 'bolas jogos premios')

# ----------------------------------------------------------------------------
