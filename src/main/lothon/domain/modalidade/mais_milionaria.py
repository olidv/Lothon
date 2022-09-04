"""
   Package lothon.domain.modalidade
   Module  mais_milionaria.py

"""

__all__ = [
    'MaisMilionaria'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from datetime import date
from dataclasses import dataclass

# Libs/Frameworks modules
from bs4.element import ResultSet

# Own/Project modules
from lothon.domain.modalidade.loteria import Loteria
from lothon.domain.sorteio.concurso import Concurso
from lothon.domain.bilhete.faixa import Faixa
from lothon.util.eve import *


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(order=True, slots=True)
class MaisMilionaria(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da modalidade +Milionaria.
    """

    # --- PROPRIEDADES -------------------------------------------------------

    # --- INICIALIZACAO ------------------------------------------------------

    # --- METODOS ------------------------------------------------------------

    def parse_concurso(self, td: ResultSet = None) -> list[Concurso]:
        # estes valores foram extraidos diretamente da pagina da loteria +Milionaria:
        self.concursos = [
            Concurso(1, date(2022, 5, 28), (23, 44, 1, 7, 3, 15), {}),
            Concurso(2, date(2022, 6, 4), (13, 35, 42, 41, 47, 16), {}),
            Concurso(3, date(2022, 6, 11), (9, 17, 30, 44, 1, 31), {}),
            Concurso(4, date(2022, 6, 18), (33, 23, 25, 47, 6, 34), {}),
            Concurso(5, date(2022, 6, 25), (26, 16, 21, 6, 45, 24), {}),
            Concurso(6, date(2022, 7, 2), (45, 39, 19, 1, 32, 22), {}),
            Concurso(7, date(2022, 7, 9), (12, 47, 35, 44, 48, 9), {}),
            Concurso(8, date(2022, 7, 16), (1, 4, 5, 38, 16, 50), {}),
            Concurso(9, date(2022, 7, 23), (15, 14, 6, 11, 18, 12), {}),
            Concurso(10, date(2022, 7, 30), (10, 47, 6, 48, 4, 42), {}),
            Concurso(11, date(2022, 8, 6), (31, 4, 15, 45, 39, 13), {}),
            Concurso(12, date(2022, 8, 13), (50, 26, 31, 24, 6, 20), {}),
            Concurso(13, date(2022, 8, 20), (44, 39, 31, 46, 14, 45), {}),
            Concurso(14, date(2022, 8, 27), (48, 49, 13, 46, 42, 12), {}),
            Concurso(15, date(2022, 9, 3), (37, 41, 3, 50, 39, 35), {})
        ]

        return self.concursos

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_tuple(value: tuple):
        if value is None or len(value) == 0:
            raise ValueError(f"Valor invalido para criar instancia de MaisMilionaria: {value}.")

        mais_milionaria = MaisMilionaria(id_loteria=value[0],
                                         nome_loteria=value[1],
                                         tag_loteria='r',
                                         tem_bolas=to_bool(value[2]),
                                         qtd_bolas=int(value[3]),
                                         qtd_bolas_sorteio=int(value[4]),
                                         dias_sorteio=tuple(map(int, value[5].split('|'))),
                                         faixas=Faixa.from_str(value[6], int(value[3])))

        # como nao ha ainda arquivo HTML de resultados, adiciona os concursos programaticamente:
        mais_milionaria.parse_concurso()

        return mais_milionaria

# ----------------------------------------------------------------------------
