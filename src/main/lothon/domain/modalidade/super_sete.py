"""
   Package lothon.domain.modalidade
   Module  super_sete.py

"""

__all__ = [
    'SuperSete'
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
from lothon.domain.sorteio.premio import Premio
from lothon.domain.bilhete.faixa import Faixa
from lothon.util.eve import *


# ----------------------------------------------------------------------------
# CONSTANTES GLOBAIS
# ----------------------------------------------------------------------------

# A tabela de precos do Super Sete eh linear:
_TABELA_PRECOS: dict = {7: 1, 8: 2, 9: 4, 10: 8, 11: 16,
                        12: 32, 13: 64, 14: 128, 15: 192, 16: 288,
                        17: 432, 18: 648, 19: 972, 20: 1458, 21: 2187}

_PROB_ACERTOS = 10000000


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(order=True, slots=True)
class SuperSete(Loteria):
    """
    Implementacao de classe para tratamento da logica e regras da modalidade Super Sete.
    """

    # --- PROPRIEDADES -------------------------------------------------------

    # --- INICIALIZACAO ------------------------------------------------------

    # --- METODOS ------------------------------------------------------------

    def parse_concurso(self, td: ResultSet) -> Concurso:
        id_concurso: int = int(td[0].text)
        data_sorteio: date = parse_dmy(td[1].text)

        bolas: tuple[int, ...] = (int(td[2].text), int(td[3].text),
                                  int(td[4].text), int(td[5].text),
                                  int(td[6].text), int(td[7].text),
                                  int(td[8].text))

        premios: dict[int, Premio] = {7: Premio(7, int(td[10].text), parse_money(td[16].text)),
                                      6: Premio(6, int(td[12].text), parse_money(td[17].text)),
                                      5: Premio(5, int(td[13].text), parse_money(td[18].text)),
                                      4: Premio(4, int(td[14].text), parse_money(td[19].text)),
                                      3: Premio(3, int(td[15].text), parse_money(td[20].text))}

        return Concurso(id_concurso, data_sorteio, bolas=bolas, premios=premios)

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def from_tuple(value: tuple):
        if value is None or len(value) == 0:
            raise ValueError(f"Valor invalido para criar instancia de SuperSete: {value}.")

        # As faixas para o Super Sete seguem um padrao linear...from
        termos = value[6].split(':')
        if len(termos) == 0:
            raise ValueError(f"Valor invalido para criar instancia de Faixa: {value}.")

        preco_min = float(termos[1])
        faixas: dict[int, Faixa] = {}

        for qtd_dezenas, qtd_apostas in _TABELA_PRECOS.items():
            preco = qtd_apostas * preco_min
            prob = round(_PROB_ACERTOS / qtd_apostas)
            fx = Faixa(qtd_dezenas, preco, qtd_apostas, prob)
            faixas[qtd_dezenas] = fx

        _super_sete = SuperSete(id_loteria=value[0],
                                nome_loteria=value[1],
                                tag_loteria='s',
                                tem_bolas=to_bool(value[2]),
                                qtd_bolas=int(value[3]),
                                qtd_bolas_sorteio=int(value[4]),
                                dias_sorteio=tuple(map(int, value[5].split('|'))),
                                faixas=faixas)
        return _super_sete

# ----------------------------------------------------------------------------
