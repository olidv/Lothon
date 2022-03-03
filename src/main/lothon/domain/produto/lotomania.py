"""
   Package lothon.domain.produto
   Module  lotomania.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain.produto.loteria import Loteria


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class Lotomania(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da produto Lotomania.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = 'id_loteria', 'nome_loteria', 'tem_bola', 'faixa_bola', 'qtd_bolas_sorteio', \
                'dias_sorteio', 'faixa_aposta', 'preco_aposta'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, dados: tuple[str, ...]):
        super().__init__(dados)

# ----------------------------------------------------------------------------
