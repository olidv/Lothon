"""
   Package lothon.domain
   Module  __init__.py

"""

__all__ = [
    'Loteria',
    'Concurso',
    'ConcursoDuplo',
    'Bola',
    'get_dia_de_sorte',
    'get_dupla_sena',
    'get_lotofacil',
    'get_lotomania',
    'get_mega_sena',
    'get_quina',
    'get_super_sete',
    'get_timemania',
    'get_mes_da_sorte',
    'get_time_do_coracao'
]


# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from typing import Optional

# Libs/Frameworks modules
# Own/Project modules
from lothon.conf import app_config
from .basico.dezena import Dezena
from .basico.jogo import Jogo
from .basico.estrutura import LoteriaStruct
from .sorteio.bola import Bola
from .sorteio.concurso import Concurso
from .sorteio.concurso_duplo import ConcursoDuplo
from .sorteio.premio import Premio
from .modalidade.loteria import Loteria
from .modalidade.dia_de_sorte import DiaDeSorte
from .modalidade.dupla_sena import DuplaSena
from .modalidade.lotofacil import Lotofacil
from .modalidade.lotomania import Lotomania
from .modalidade.mega_sena import MegaSena
from .modalidade.mes_da_sorte import MesDaSorte
from .modalidade.quina import Quina
from .modalidade.super_sete import SuperSete
from .modalidade.time_do_coracao import TimeDoCoracao
from .modalidade.timemania import Timemania
from .bilhete.cota import Cota
from .bilhete.volante import Volante
from .bilhete.bolao import Bolao
from .bilhete.faixa import Faixa
# from lothon.util.eve import *


# ----------------------------------------------------------------------------
# ESTRUTURA DE DADOS
# ----------------------------------------------------------------------------

#
def new_loteria_struct() -> LoteriaStruct:
    jogos: list[tuple[int, ...]] = []
    fatores: list[int] = []
    return LoteriaStruct(jogos, fatores)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# pesquisa o item (tupla) da loteira no array proveniente da configuracao INI:
def get_tuple_loteria(id_loteria: str) -> tuple[str, ...]:
    list_item = [item for item in app_config.LC_loterias_caixa if item[0] == id_loteria]

    if (list_item is not None) and len(list_item) > 0:
        return list_item[0]
    else:
        raise ValueError(f"Erro ao pesquisar loteria '{id_loteria}' na configuracao INI.")


# ----------------------------------------------------------------------------
# VARIAVEIS SINGLETON
# ----------------------------------------------------------------------------

_dia_de_sorte: Optional[DiaDeSorte] = None
_dupla_sena: Optional[DuplaSena] = None
_lotofacil: Optional[Lotofacil] = None
_lotomania: Optional[Lotomania] = None
_mega_sena: Optional[MegaSena] = None
_quina: Optional[Quina] = None
_super_sete: Optional[SuperSete] = None
_timemania: Optional[Timemania] = None
_mes_da_sorte: Optional[MesDaSorte] = None
_time_do_coracao: Optional[TimeDoCoracao] = None


def get_dia_de_sorte() -> DiaDeSorte:
    global _dia_de_sorte
    if _dia_de_sorte is None:
        tupla_loteria = get_tuple_loteria("diadesorte")
        _dia_de_sorte = DiaDeSorte.from_tuple(tupla_loteria)

    return _dia_de_sorte


def get_dupla_sena() -> DuplaSena:
    global _dupla_sena
    if _dupla_sena is None:
        tupla_loteria = get_tuple_loteria("duplasena")
        _dupla_sena = DuplaSena.from_tuple(tupla_loteria)

    return _dupla_sena


def get_lotofacil() -> Lotofacil:
    global _lotofacil
    if _lotofacil is None:
        tupla_loteria = get_tuple_loteria("lotofacil")
        _lotofacil = Lotofacil.from_tuple(tupla_loteria)

    return _lotofacil


def get_lotomania() -> Lotomania:
    global _lotomania
    if _lotomania is None:
        tupla_loteria = get_tuple_loteria("lotomania")
        _lotomania = Lotomania.from_tuple(tupla_loteria)

    return _lotomania


def get_mega_sena() -> MegaSena:
    global _mega_sena
    if _mega_sena is None:
        tupla_loteria = get_tuple_loteria("megasena")
        _mega_sena = MegaSena.from_tuple(tupla_loteria)

    return _mega_sena


def get_quina() -> Quina:
    global _quina
    if _quina is None:
        tupla_loteria = get_tuple_loteria("quina")
        _quina = Quina.from_tuple(tupla_loteria)

    return _quina


def get_super_sete() -> SuperSete:
    global _super_sete
    if _super_sete is None:
        tupla_loteria = get_tuple_loteria("supersete")
        _super_sete = SuperSete.from_tuple(tupla_loteria)

    return _super_sete


def get_timemania() -> Timemania:
    global _timemania
    if _timemania is None:
        tupla_loteria = get_tuple_loteria("timemania")
        _timemania = Timemania.from_tuple(tupla_loteria)

    return _timemania


def get_mes_da_sorte() -> MesDaSorte:
    global _mes_da_sorte
    if _mes_da_sorte is None:
        tupla_loteria = get_tuple_loteria("mesdasorte")
        _mes_da_sorte = MesDaSorte.from_tuple(tupla_loteria)

    return _mes_da_sorte


def get_time_do_coracao() -> TimeDoCoracao:
    global _time_do_coracao
    if _time_do_coracao is None:
        tupla_loteria = get_tuple_loteria("timedocoracao")
        _time_do_coracao = TimeDoCoracao.from_tuple(tupla_loteria)

    return _time_do_coracao

# ----------------------------------------------------------------------------
