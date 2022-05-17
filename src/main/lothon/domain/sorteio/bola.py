"""
   Package lothon.domain.sorteio
   Module  bola.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass, field

# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(order=True, slots=True)
class Bola:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    id_bola: int

    sorteios: list[int] = field(init=False, default_factory=list)
    qtd_sorteios: int = field(init=False, default=0)
    ultimo_sorteio: int = field(init=False, default=0)

    atrasos: list[int] = field(init=False, default_factory=list)
    qtd_atrasos: int = field(init=False, default=0)
    ultimo_atraso: int = field(init=False, default=0)
    maior_atraso: int = field(init=False, default=0)
    menor_atraso: int = field(init=False, default=9999)
    media_atraso: float = field(init=False, default=0.0)

    sort_index: int = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.id_bola)

    # --- METODOS ------------------------------------------------------------

    # esta bola foi sorteada no concurso indicado:
    def add_sorteio(self, id_concurso: int):
        # verifica se eh o primeiro sorteio da bola:
        if self.ultimo_sorteio == 0:
            atraso: int = id_concurso - 1
        else:  # ou se a bola ja foi sorteada antes:
            atraso: int = id_concurso - self.ultimo_sorteio - 1

        # atualiza os atrasos da bola:
        if atraso > 0:
            self.atrasos.append(atraso)
            self.qtd_atrasos += 1
            self.ultimo_atraso = atraso
            self.maior_atraso = max(self.maior_atraso, atraso)
            self.menor_atraso = min(self.menor_atraso, atraso)
            self.media_atraso = round((sum(self.atrasos) / self.qtd_atrasos) * 10) / 10

        # atualiza os sorteios da bola:
        self.sorteios.append(id_concurso)
        self.qtd_sorteios += 1
        self.ultimo_sorteio = id_concurso

    # ultimo concurso ocorrido da loteria, ainda sem sorteio (atraso) desta bola:
    def last_concurso(self, id_concurso: int):
        # verifica se a bola ainda nao foi sorteada:
        if self.ultimo_sorteio == 0:
            atraso: int = id_concurso
        else:  # ou se a bola ja foi sorteada antes:
            atraso: int = id_concurso - self.ultimo_sorteio

        # atualiza os atrasos da bola:
        if atraso > 0:
            self.atrasos.append(atraso)
            self.qtd_atrasos += 1
            self.ultimo_atraso = atraso
            self.maior_atraso = max(self.maior_atraso, atraso)
            self.menor_atraso = min(self.menor_atraso, atraso)
            self.media_atraso = round((sum(self.atrasos) / self.qtd_atrasos) * 10) / 10

# ----------------------------------------------------------------------------
