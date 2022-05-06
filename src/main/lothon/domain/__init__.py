
# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import typing

# Libs/Frameworks modules
# Own/Project modules
from lothon.conf import app_config
from .universo.numeral import Numeral
from .universo.dezena import Dezena
from .universo.jogo import Jogo
from .sorteio.bola import Bola
from .sorteio.concurso import Concurso
from .produto.loteria import Loteria
from .produto.dia_de_sorte import DiaDeSorte
from .produto.dupla_sena import DuplaSena
from .produto.lotofacil import Lotofacil
from .produto.lotomania import Lotomania
from .produto.mega_sena import MegaSena
from .produto.mes_da_sorte import MesDaSorte
from .produto.quina import Quina
from .produto.super_sete import SuperSete
from .produto.time_do_coracao import TimeDoCoracao
from .produto.timemania import Timemania
from .bilhete.cota import Cota
from .bilhete.volante import Volante
from .bilhete.bolao import Bolao
from .bilhete.faixa import Faixa
from lothon.util.eve import *


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

_dia_de_sorte: typing.Optional[DiaDeSorte] = None
_dupla_sena: typing.Optional[DuplaSena] = None
_lotofacil: typing.Optional[Lotofacil] = None
_lotomania: typing.Optional[Lotomania] = None
_mega_sena: typing.Optional[MegaSena] = None
_quina: typing.Optional[Quina] = None
_super_sete: typing.Optional[SuperSete] = None
_timemania: typing.Optional[Timemania] = None
_mes_da_sorte: typing.Optional[MesDaSorte] = None
_time_do_coracao: typing.Optional[TimeDoCoracao] = None


def dia_de_sorte() -> DiaDeSorte:
    global _dia_de_sorte
    if _dia_de_sorte is None:
        tupla = get_tuple_loteria("diadesorte")
        intervalo_bolas = tuple(map(int, tupla[3].split('-')))
        dias_sorteio = tuple(map(int, tupla[5].split('|')))
        _dia_de_sorte = DiaDeSorte(id_loteria=tupla[0],
                                   nome_loteria=tupla[1],
                                   tem_bolas=to_bool(tupla[2]),
                                   intervalo_bolas=intervalo_bolas,
                                   qtd_bolas_sorteio=int(tupla[4]),
                                   dias_sorteio=dias_sorteio,
                                   faixas=Faixa.from_str(tupla[6]))

    return _dia_de_sorte


def dupla_sena() -> DuplaSena:
    global _dupla_sena
    if _dupla_sena is None:
        tupla = get_tuple_loteria("duplasena")
        intervalo_bolas = tuple(map(int, tupla[3].split('-')))
        dias_sorteio = tuple(map(int, tupla[5].split('|')))
        _dupla_sena = DuplaSena(id_loteria=tupla[0],
                                nome_loteria=tupla[1],
                                tem_bolas=to_bool(tupla[2]),
                                intervalo_bolas=intervalo_bolas,
                                qtd_bolas_sorteio=int(tupla[4]),
                                dias_sorteio=dias_sorteio,
                                faixas=Faixa.from_str(tupla[6]))

    return _dupla_sena


def lotofacil() -> Lotofacil:
    global _lotofacil
    if _lotofacil is None:
        tupla = get_tuple_loteria("lotofacil")
        intervalo_bolas = tuple(map(int, tupla[3].split('-')))
        dias_sorteio = tuple(map(int, tupla[5].split('|')))
        _lotofacil = Lotofacil(id_loteria=tupla[0],
                               nome_loteria=tupla[1],
                               tem_bolas=to_bool(tupla[2]),
                               intervalo_bolas=intervalo_bolas,
                               qtd_bolas_sorteio=int(tupla[4]),
                               dias_sorteio=dias_sorteio,
                               faixas=Faixa.from_str(tupla[6]))

    return _lotofacil


def lotomania() -> Lotomania:
    global _lotomania
    if _lotomania is None:
        tupla = get_tuple_loteria("lotomania")
        intervalo_bolas = tuple(map(int, tupla[3].split('-')))
        dias_sorteio = tuple(map(int, tupla[5].split('|')))
        _lotomania = Lotomania(id_loteria=tupla[0],
                               nome_loteria=tupla[1],
                               tem_bolas=to_bool(tupla[2]),
                               intervalo_bolas=intervalo_bolas,
                               qtd_bolas_sorteio=int(tupla[4]),
                               dias_sorteio=dias_sorteio,
                               faixas=Faixa.from_str(tupla[6]))

    return _lotomania


def mega_sena() -> MegaSena:
    global _mega_sena
    if _mega_sena is None:
        tupla = get_tuple_loteria("megasena")
        intervalo_bolas = tuple(map(int, tupla[3].split('-')))
        dias_sorteio = tuple(map(int, tupla[5].split('|')))
        _mega_sena = MegaSena(id_loteria=tupla[0],
                              nome_loteria=tupla[1],
                              tem_bolas=to_bool(tupla[2]),
                              intervalo_bolas=intervalo_bolas,
                              qtd_bolas_sorteio=int(tupla[4]),
                              dias_sorteio=dias_sorteio,
                              faixas=Faixa.from_str(tupla[6]))

    return _mega_sena


def quina() -> Quina:
    global _quina
    if _quina is None:
        tupla = get_tuple_loteria("quina")
        intervalo_bolas = tuple(map(int, tupla[3].split('-')))
        dias_sorteio = tuple(map(int, tupla[5].split('|')))
        _quina = Quina(id_loteria=tupla[0],
                       nome_loteria=tupla[1],
                       tem_bolas=to_bool(tupla[2]),
                       intervalo_bolas=intervalo_bolas,
                       qtd_bolas_sorteio=int(tupla[4]),
                       dias_sorteio=dias_sorteio,
                       faixas=Faixa.from_str(tupla[6]))

    return _quina


def super_sete() -> SuperSete:
    global _super_sete
    if _super_sete is None:
        tupla = get_tuple_loteria("supersete")
        intervalo_bolas = tuple(map(int, tupla[3].split('-')))
        dias_sorteio = tuple(map(int, tupla[5].split('|')))
        _super_sete = SuperSete(id_loteria=tupla[0],
                                nome_loteria=tupla[1],
                                tem_bolas=to_bool(tupla[2]),
                                intervalo_bolas=intervalo_bolas,
                                qtd_bolas_sorteio=int(tupla[4]),
                                dias_sorteio=dias_sorteio,
                                faixas=Faixa.from_str(tupla[6]))

    return _super_sete


def timemania() -> Timemania:
    global _timemania
    if _timemania is None:
        tupla = get_tuple_loteria("timemania")
        intervalo_bolas = tuple(map(int, tupla[3].split('-')))
        dias_sorteio = tuple(map(int, tupla[5].split('|')))
        _timemania = Timemania(id_loteria=tupla[0],
                               nome_loteria=tupla[1],
                               tem_bolas=to_bool(tupla[2]),
                               intervalo_bolas=intervalo_bolas,
                               qtd_bolas_sorteio=int(tupla[4]),
                               dias_sorteio=dias_sorteio,
                               faixas=Faixa.from_str(tupla[6]))

    return _timemania


def mes_da_sorte() -> MesDaSorte:
    global _mes_da_sorte
    if _mes_da_sorte is None:
        tupla = get_tuple_loteria("mesdasorte")
        intervalo_bolas = tuple(map(int, tupla[3].split('-')))
        dias_sorteio = tuple(map(int, tupla[5].split('|')))
        _mes_da_sorte = MesDaSorte(id_loteria=tupla[0],
                                   nome_loteria=tupla[1],
                                   tem_bolas=to_bool(tupla[2]),
                                   intervalo_bolas=intervalo_bolas,
                                   qtd_bolas_sorteio=int(tupla[4]),
                                   dias_sorteio=dias_sorteio,
                                   faixas=Faixa.from_str(tupla[6]))

    return _mes_da_sorte


def time_do_coracao() -> TimeDoCoracao:
    global _time_do_coracao
    if _time_do_coracao is None:
        tupla = get_tuple_loteria("timedocoracao")
        intervalo_bolas = tuple(map(int, tupla[3].split('-')))
        dias_sorteio = tuple(map(int, tupla[5].split('|')))
        _time_do_coracao = TimeDoCoracao(id_loteria=tupla[0],
                                         nome_loteria=tupla[1],
                                         tem_bolas=to_bool(tupla[2]),
                                         intervalo_bolas=intervalo_bolas,
                                         qtd_bolas_sorteio=int(tupla[4]),
                                         dias_sorteio=dias_sorteio,
                                         faixas=Faixa.from_str(tupla[6]))

    return _time_do_coracao

# ----------------------------------------------------------------------------
