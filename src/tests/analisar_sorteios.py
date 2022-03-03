"""
   Test Package
   Module  analisar_sorteios.py

   Modulo para executar a analise dos dados de sorteios das loterias.
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.conf import app_config
from lothon.domain import DiaDeSorte, DuplaSena, Lotofacil, Lotomania, MegaSena, MesDaSorte, \
                          Quina, SuperSete, TimeDoCoracao, Timemania
from lothon.infra import parser_resultados

# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# FUNCOES HELPERS
# ----------------------------------------------------------------------------

# pesquisa o item (tupla) da loteira no array proveniente da configuracao INI:
def get_tuple_loteria(id_loteria: str) -> tuple[str, ...]:
    list_tuple = [item for item in app_config.LC_loterias_caixa if item[0] == id_loteria]

    if list_tuple is not None and len(list_tuple) > 0:
        return list_tuple[0]
    else:
        raise ValueError(f"Erro ao pesquisar loteria '{id_loteria}' na configuracao INI.")


# ----------------------------------------------------------------------------
# MAIN ENTRY-POINT
# ----------------------------------------------------------------------------

# entry-point de execucao para tarefas diarias:
def run():
    logger.info("Iniciando a analise dos dados de sorteios das loterias...")

    dia_de_sorte = DiaDeSorte(get_tuple_loteria("diadesorte"))
    dupla_sena = DuplaSena(get_tuple_loteria("duplasena"))
    lotofacil = Lotofacil(get_tuple_loteria("lotofacil"))
    lotomania = Lotomania(get_tuple_loteria("lotomania"))
    mega_sena = MegaSena(get_tuple_loteria("megasena"))
    quina = Quina(get_tuple_loteria("quina"))
    super_sete = SuperSete(get_tuple_loteria("supersete"))
    timemania = Timemania(get_tuple_loteria("timemania"))

    mes_da_sorte = MesDaSorte(get_tuple_loteria("mesdasorte"))
    time_do_coracao = TimeDoCoracao(get_tuple_loteria("timedocoracao"))

    print(dia_de_sorte)
    print(dupla_sena)
    print(lotofacil)
    print(lotomania)
    print(mega_sena)
    print(quina)
    print(super_sete)
    print(timemania)
    print(mes_da_sorte)
    print(time_do_coracao)

    parser_resultados.get_concursos_loteria(dia_de_sorte)
    parser_resultados.get_concursos_loteria(dupla_sena)
    parser_resultados.get_concursos_loteria(lotofacil)
    parser_resultados.get_concursos_loteria(lotomania)
    parser_resultados.get_concursos_loteria(mega_sena)
    parser_resultados.get_concursos_loteria(quina)
    parser_resultados.get_concursos_loteria(super_sete)
    parser_resultados.get_concursos_loteria(timemania)
    parser_resultados.get_concursos_loteria(time_do_coracao)
    parser_resultados.get_concursos_loteria(mes_da_sorte)

    print('Analise OK!')

    # finalizadas todas as tarefas, informa que o processamento foi ok:
    logger.info("Finalizada a analise dos dados de sorteios das loterias.")
    return 0

# ----------------------------------------------------------------------------
