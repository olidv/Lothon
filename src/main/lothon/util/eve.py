"""
   Package lothon.util
   Module  eve.py

   Funcoes utilitarias para manipulacao de valores (enumerators e evaluators).
"""

__all__ = [
    'numerology',
    'is_par',
    'is_impar',
    'str_to_bool',
    'to_bool',
    'strip_accents',
    'to_fator',
    'parse_money',
    'parse_dmy',
    'formatd',
    'formatf',
    'formatc',
    'formatb',
    'startwatch',
    'stopwatch'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import locale
import unicodedata
from math import log, floor
from datetime import date, datetime, timedelta
from typing import Optional

# Libs/Frameworks modules
# Own/Project modules


locale.setlocale(locale.LC_ALL, '')


# ----------------------------------------------------------------------------
# FUNCOES PARA CALCULOS ESPECIAIS
# ----------------------------------------------------------------------------

def numerology(numeros: tuple[int, ...]) -> int:
    # condicao de saida da recursividade:
    if numeros is None or len(numeros) == 0:
        return 0
    elif len(numeros) == 1 and numeros[0] < 10:
        return numeros[0]

    # calcula a soma os numeros:
    soma: int = sum(numeros)

    # extrai os digitos da soma:
    digitos: tuple[int, ...] = ()
    while soma > 0:
        digito: int = soma % 10
        digitos += (digito,)
        soma = soma // 10

    return numerology(digitos)


def is_par(val: int | float) -> bool:
    if val is None:
        return False
    elif isinstance(val, int):
        return (val % 2) == 0
    else:
        return (int(val) % 2) == 0


def is_impar(val: int | float) -> bool:
    if val is None:
        return False
    elif isinstance(val, int):
        return (val % 2) != 0
    else:
        return (int(val) % 2) != 0


# ----------------------------------------------------------------------------
# FUNCOES PARA CONVERSAO DE VALORES
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


def to_fator(percent: float) -> float:
    return 1 + (percent / 100)


# ----------------------------------------------------------------------------
# FUNCOES PARA PARSING DE VALORES
# ----------------------------------------------------------------------------

def parse_money(val: str) -> float:
    # se o valor for nulo (None), entao considera zero:
    if val is None:
        return 0.0

    # elimina as formatacoes e converte para numero decimal:
    val = val.strip().lower().replace("r$", "").replace(".", "").replace(",", ".")
    return float(val)


def parse_dmy(val: str) -> Optional[date]:
    # se o valor for nulo (None), entao considera tudo nulo:
    if val is None:
        return

    # converte para data a partir do formato  DD/MM/YYYY:
    return datetime.strptime(val, "%d/%m/%Y").date()


# ----------------------------------------------------------------------------
# FUNCOES PARA FORMATACAO DE VALORES
# ----------------------------------------------------------------------------

def formatd(val, size: int = None) -> str:
    str_val: str = locale.format_string('%d', val, grouping=True)
    if size is not None and size > len(str_val):
        return str_val.rjust(size, ' ')
    else:
        return str_val


def formatf(val, fmt: str = '14.2') -> str:
    return locale.format_string(f"%{fmt}f", val, grouping=True)


def formatc(val: float) -> str:
    return locale.currency(val, grouping=True)


def formatb(number):
    units = ['', 'K', 'M', 'G', 'T', 'P']
    k = 1000.0
    magnitude = int(floor(log(number, k)))

    return '%.2f%s' % (number / k**magnitude, units[magnitude])


# ----------------------------------------------------------------------------
# FUNCOES PARA MEDICAO DE TEMPO DE PROCESSAMENTO
# ----------------------------------------------------------------------------

# 
def startwatch() -> datetime:
    return datetime.now()


#
def stopwatch(start: datetime) -> str:
    # evita erros e retorno de nulos
    if start is None:
        return ''

    difer: timedelta = datetime.now() - start
    dias: int = difer.days
    segundos: int = difer.seconds
    milisegs: int = difer.microseconds // 1000

    tempo: str = ''
    if dias > 0:
        tempo += f"{dias} dia, "

    horas: int = segundos // 3600
    if horas > 0:
        tempo += f"{horas} hor, "
        segundos -= horas * 3600

    minutos: int = segundos // 60
    if minutos > 0:
        tempo += f"{minutos} min, "
        segundos -= minutos * 60

    tempo += f"{segundos} seg, {milisegs} ms"
    return tempo

# ----------------------------------------------------------------------------
