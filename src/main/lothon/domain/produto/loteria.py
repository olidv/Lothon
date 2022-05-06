"""
   Package lothon.domain.produto
   Module  loteria.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

# Libs/Frameworks modules
from bs4.element import ResultSet

# Own/Project modules
from lothon.domain.sorteio.concurso import Concurso
from lothon.domain.bilhete.faixa import Faixa


# ----------------------------------------------------------------------------
# CLASSE ABSTRATA
# ----------------------------------------------------------------------------

@dataclass(order=True)
class Loteria(ABC):
    """
    Classe abstrata com definicao de propriedades e metodos para criacao de classes
    que representam as loterias da Caixa.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    id_loteria: str
    nome_loteria: str
    tem_bolas: bool
    intervalo_bolas: tuple[int, ...]
    qtd_bolas: int = field(init=False)
    qtd_bolas_sorteio: int
    dias_sorteio: tuple[int, ...]
    faixas: list[Faixa]
    concursos: Optional[list[Concurso]] = None

    sort_index: str = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        object.__setattr__(self, 'qtd_bolas', self.intervalo_bolas[1] - self.intervalo_bolas[0] + 1)
        object.__setattr__(self, 'sort_index', self.id_loteria)

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
            print(concurso)
            list_concursos.append(concurso)

        self.concursos = list_concursos

    @abstractmethod
    def parse_concurso(self, td: ResultSet) -> Concurso:
        pass

    # ----------------------------------------------------------------------------
