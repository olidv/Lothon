"""
   Package lothon.domain.modalidade
   Module  dia_de_sorte.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass

# Libs/Frameworks modules
from bs4.element import ResultSet

# Own/Project modules
from lothon.conf import app_config
from lothon.domain.modalidade.loteria import Loteria
from lothon.domain.sorteio.concurso_duplo import ConcursoDuplo
from lothon.domain.sorteio.premio import Premio
from lothon.domain.bilhete.faixa import Faixa
from lothon.util.eve import *


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(order=True, slots=True)
class DiaDeSorte(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da modalidade Dia de Sorte.
    """

    # --- PROPRIEDADES -------------------------------------------------------

    # --- INICIALIZACAO ------------------------------------------------------

    # --- METODOS ------------------------------------------------------------

    def parse_concurso(self, td: ResultSet) -> ConcursoDuplo:
        id_concurso: int = int(td[0].text)
        data_sorteio: date = parse_dmy(td[2].text)

        # Primeiro sorteio, 7 bolas:
        bolas1: tuple[int, ...] = (int(td[3].text), int(td[4].text),
                                   int(td[5].text), int(td[6].text),
                                   int(td[7].text), int(td[8].text),
                                   int(td[9].text))

        premios1: dict[int, Premio] = {7: Premio(7, int(td[11].text), parse_money(td[16].text)),
                                       6: Premio(6, int(td[12].text), parse_money(td[17].text)),
                                       5: Premio(5, int(td[13].text), parse_money(td[18].text)),
                                       4: Premio(4, int(td[14].text), parse_money(td[19].text))}

        # Segundo sorteio, mes da sorte:
        mes = td[10].text.strip().lower()
        if mes not in app_config.MAP_MESES.keys():
            raise ValueError(f"*** ATENCAO: MES-DA-SORTE NAO IDENTIFICADO "
                             f"NO CONCURSO {td[0].text}: {mes} ***")

        bolas2: tuple[int, ...] = (app_config.MAP_MESES[mes])

        premios2: dict[int, Premio] = {1: Premio(1, int(td[15].text), parse_money(td[20].text))}

        return ConcursoDuplo(id_concurso, data_sorteio,
                             bolas=bolas1, premios=premios1,
                             bolas2=bolas2, premios2=premios2)

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_tuple(value: tuple):
        if value is None or len(value) == 0:
            raise ValueError(f"Valor invalido para criar instancia de DiaDeSorte: {value}.")

        dia_de_sorte = DiaDeSorte(id_loteria=value[0],
                                  nome_loteria=value[1],
                                  tem_bolas=to_bool(value[2]),
                                  qtd_bolas=int(value[3]),
                                  qtd_bolas_sorteio=int(value[4]),
                                  dias_sorteio=tuple(map(int, value[5].split('|'))),
                                  faixas=Faixa.from_str(value[6], int(value[3])))
        return dia_de_sorte

    # ----------------------------------------------------------------------------
