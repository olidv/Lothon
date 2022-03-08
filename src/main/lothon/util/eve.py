"""
   Package lothon.util
   Module  eve.py

   Funcoes utilitarias para manipulacao de valores (enumerators e evaluators).
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import unicodedata
from math import log, floor

# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# FUNCOES UTILITARIAS
# ----------------------------------------------------------------------------

def str_to_bool(val: str) -> bool:
    """Convert a string representation of truth to true (1) or false (0).

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false values
    are 'n', 'no', 'f', 'false', 'off', and '0'.  Raises ValueError if
    'val' is anything else.
    """

    # se o valor for nulo (None), entao considera falso:
    if val is None:
        return False

    # elimina os espacos nas extremidades e converte para minusculo para comparar:
    val = val.strip().lower()

    # se depois do strip ficou vazio, entao considera falso:
    if not val:
        return False

    # valores padronizados para True ou Falso:
    elif val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    elif val in ('n', 'no', 'f', 'false', 'off', '0'):
        return False

    # qualquer outro valor eh considerado True por nao ser uma string vazia:
    else:
        return True


def to_bool(val) -> bool:
    """Converte um valor de qualquer tipo para true (1) ou false (0).
    """

    # se o valor for nulo (None), entao ja considera falso:
    if val is None:
        return False

    # se valor ja for bool, entao nada a fazer aqui:
    elif isinstance(val, bool):
        return val

    # faz as comparacoes dependendo do tipo do valor:
    elif isinstance(val, str):
        return str_to_bool(val)

    # se for numerico, basta testar se maior q zero para true ou igual a zero para false:
    elif isinstance(val, int) or isinstance(val, float):
        return val > 0

    # se for uma colecao, entao verifica o tamanho:
    elif isinstance(val, list) or isinstance(val, tuple) or isinstance(val, dict):
        return len(val) > 0

    # para qualquer outro valor deixa o comportamento padrao do Python decidir:
    else:
        return bool(val)


def human_format(number):
    units = ['', 'K', 'M', 'G', 'T', 'P']
    k = 1000.0
    magnitude = int(floor(log(number, k)))

    return '%.2f%s' % (number / k**magnitude, units[magnitude])


def strip_accents(text) -> str:
    """
    Strip accents from input String.

    :param text: The input string.

    :returns: The processed String.
    """
    try:
        text = str(text, 'utf-8')
    except (TypeError, NameError):  # unicode is a default on python 3
        pass

    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")

    return str(text)


def parse_money(val: str) -> float:
    # se o valor for nulo (None), entao considera zero:
    if val is None:
        return 0.0

    # elimina as formatacoes e converte para numero decimal:
    val = val.strip().lower().replace("r$", "").replace(".", "").replace(",", ".")
    return float(val)

# ----------------------------------------------------------------------------
