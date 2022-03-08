"""
   Package lothon.domain.produto
   Module  loteria.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from abc import ABC, abstractmethod

# Libs/Frameworks modules
from bs4.element import ResultSet

# Own/Project modules
from lothon.util.eve import *
from lothon.domain.sorteio.concurso import Concurso
from lothon.domain.bilhete.faixa import Faixa


# ----------------------------------------------------------------------------
# CLASSE ABSTRATA
# ----------------------------------------------------------------------------

class Loteria(ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de classes
    que representam as loterias da Caixa.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    @property
    def id_loteria(self) -> str:
        return self._id_loteria

    @id_loteria.setter
    def id_loteria(self, value):
        if isinstance(value, str):
            self._id_loteria = value
        else:
            self._id_loteria = str(value)

    @property
    def nome_loteria(self) -> str:
        return self._nome_loteria

    @nome_loteria.setter
    def nome_loteria(self, value):
        if isinstance(value, str):
            self._nome_loteria = value
        else:
            self._nome_loteria = str(value)

    @property
    def tem_bolas(self) -> bool:
        return self._tem_bolas

    @tem_bolas.setter
    def tem_bolas(self, value):
        if isinstance(value, bool):
            self._tem_bolas = value
        else:
            self._tem_bolas = to_bool(value)

    @property
    def intervalo_bolas(self) -> tuple[int, int]:
        return self._intervalo_bolas

    @intervalo_bolas.setter
    def intervalo_bolas(self, value):
        if isinstance(value, tuple):
            self._intervalo_bolas = value
        elif isinstance(value, str):
            self._intervalo_bolas = tuple(map(int, value.split('-')))
        else:
            raise ValueError(f"Valor invalido para a propriedade 'intervalo_bolas' = {value}")

        self._qtd_bolas = self._intervalo_bolas[1] - self._intervalo_bolas[0] + 1

    @property
    def qtd_bolas(self) -> int:
        return self._qtd_bolas

    @qtd_bolas.setter
    def qtd_bolas(self, value):
        if isinstance(value, int):
            self._qtd_bolas = value
        elif isinstance(value, str):
            self._qtd_bolas = int(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'qtd_bolas' = {value}.")

    @property
    def qtd_bolas_sorteio(self) -> int:
        return self._qtd_bolas_sorteio

    @qtd_bolas_sorteio.setter
    def qtd_bolas_sorteio(self, value):
        if isinstance(value, int):
            self._qtd_bolas_sorteio = value
        elif isinstance(value, str):
            self._qtd_bolas_sorteio = int(value)
        else:
            raise ValueError(f"Valor invalido para a propriedade 'qtd_bolas_sorteio' = {value}.")

    @property
    def dias_sorteio(self) -> tuple[int, ...]:
        return self._dias_sorteio

    @dias_sorteio.setter
    def dias_sorteio(self, value):
        if isinstance(value, tuple):
            self._dias_sorteio = value
        elif isinstance(value, str):
            self._dias_sorteio = tuple(map(int, value.split('|')))
        else:
            raise ValueError(f"Valor invalido para a propriedade 'dias_sorteio' = {value}.")

    @property
    def faixas(self) -> list[Faixa]:
        return self._faixas

    @faixas.setter
    def faixas(self, value):
        if value is None or isinstance(value, list):
            self._faixas = value
        else:
            raise ValueError(f"Valor invalido para a propriedade 'faixas' = {value}.")

    @property
    def concursos(self) -> list[Concurso]:
        return self._concursos

    @concursos.setter
    def concursos(self, value):
        if value is None or isinstance(value, list):
            self._concursos = value
        else:
            raise ValueError(f"Valor invalido para a propriedade 'concursos' = {value}.")

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self, dados: tuple[str, ...]):
        self.id_loteria = dados[0]
        self.nome_loteria = dados[1]
        self.tem_bolas = dados[2]
        self.intervalo_bolas = dados[3]
        self.qtd_bolas_sorteio = dados[4]
        self.dias_sorteio = dados[5]
        self.faixas = None
        self.concursos = None

    # --- METODOS ------------------------------------------------------------

    def get_tag_resultados(self) -> str:
        return self.id_loteria

    def get_file_resultados(self) -> str:
        return self.nome_loteria

    def set_resultados(self, table_body: ResultSet) -> None:
        # dentro do TBODY tem uma unica TR contendo os dados relacionados em elementos TD:
        list_concursos: list[Concurso] = []
        for tbody in table_body:
            tr = tbody.find("tr", recursive=False)
            # print("tr = ", type(tr), len(tr))
            td = tr.find_all("td", recursive=False)
            # print("td = ", type(td), len(td))
            # print("td[0] = ", type(td[0]), len(td[0]), td[0].text)

            concurso = self.parse_concurso(td)
            print("Concurso = ", concurso)
            list_concursos.append(concurso)

        self.concursos = list_concursos

    @abstractmethod
    def parse_concurso(self, td: ResultSet) -> Concurso:
        pass

# ----------------------------------------------------------------------------
