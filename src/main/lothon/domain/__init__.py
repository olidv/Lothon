
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

dia_de_sorte: typing.Optional[DiaDeSorte] = None
dupla_sena: typing.Optional[DuplaSena] = None
lotofacil: typing.Optional[Lotofacil] = None
lotomania: typing.Optional[Lotomania] = None
mega_sena: typing.Optional[MegaSena] = None
quina: typing.Optional[Quina] = None
super_sete: typing.Optional[SuperSete] = None
timemania: typing.Optional[Timemania] = None
mes_da_sorte: typing.Optional[MesDaSorte] = None
time_do_coracao: typing.Optional[TimeDoCoracao] = None


def DIA_DE_SORTE() -> DiaDeSorte:
    global dia_de_sorte
    if dia_de_sorte is None:
        dia_de_sorte = DiaDeSorte(get_tuple_loteria("diadesorte"))

    return dia_de_sorte


def DUPLA_SENA() -> DuplaSena:
    global dupla_sena
    if dupla_sena is None:
        dupla_sena = DuplaSena(get_tuple_loteria("duplasena"))

    return dupla_sena


def LOTOFACIL() -> Lotofacil:
    global lotofacil
    if lotofacil is None:
        lotofacil = Lotofacil(get_tuple_loteria("lotofacil"))

    return lotofacil


def LOTOMANIA() -> Lotomania:
    global lotomania
    if lotomania is None:
        lotomania = Lotomania(get_tuple_loteria("lotomania"))

    return lotomania


def MEGA_SENA() -> MegaSena:
    global mega_sena
    if mega_sena is None:
        mega_sena = MegaSena(get_tuple_loteria("megasena"))

    return mega_sena


def QUINA() -> Quina:
    global quina
    if quina is None:
        quina = Quina(get_tuple_loteria("quina"))

    return quina


def SUPER_SETE() -> SuperSete:
    global super_sete
    if super_sete is None:
        super_sete = SuperSete(get_tuple_loteria("supersete"))

    return super_sete


def TIMEMANIA() -> Timemania:
    global timemania
    if timemania is None:
        timemania = Timemania(get_tuple_loteria("timemania"))

    return timemania


def MES_DA_SORTE() -> MesDaSorte:
    global mes_da_sorte
    if mes_da_sorte is None:
        mes_da_sorte = MesDaSorte(get_tuple_loteria("mesdasorte"))

    return mes_da_sorte


def TIME_DO_CORACAO() -> TimeDoCoracao:
    global time_do_coracao
    if time_do_coracao is None:
        time_do_coracao = TimeDoCoracao(get_tuple_loteria("timedocoracao"))

    return time_do_coracao

# ----------------------------------------------------------------------------
