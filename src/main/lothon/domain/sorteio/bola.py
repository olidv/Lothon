"""
   Package lothon.domain.sorteio
   Module  bola.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass, field
import statistics as stts

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
    sort_index: int = field(init=False, repr=False)

    ultimo_sorteio: int = field(init=False, default=0)
    sorteios: list[int] = field(init=False, default_factory=list)
    ultimo_atraso: int = field(init=False, default=0)
    atrasos: list[int] = field(init=False, default_factory=list)

    # medidas estatisticas
    len_sorteios: int = field(init=False, default=0)
    len_atrasos: int = field(init=False, default=0)
    max_atraso: int = field(init=False, default=0)
    min_atraso: int = field(init=False, default=0)
    mode_atraso: int = field(init=False, default=0)
    mean_atraso: float = field(init=False, default=0.0)
    hmean_atraso: float = field(init=False, default=0.0)
    gmean_atraso: float = field(init=False, default=0.0)
    median_atraso: float = field(init=False, default=0.0)
    varia_atraso: float = field(init=False, default=0.0)
    stdev_atraso: float = field(init=False, default=0.0)

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
            self.ultimo_atraso = atraso
            self.atrasos.append(atraso)

        # nao registra o ultimo sorteio mais de uma vez:
        if self.ultimo_sorteio != id_concurso:
            self.ultimo_sorteio = id_concurso
            self.sorteios.append(id_concurso)

    # ultimo concurso ocorrido da loteria, ainda sem sorteio (atraso) desta bola:
    def last_sorteio(self, id_concurso: int):
        # verifica se a bola ainda nao foi sorteada:
        if self.ultimo_sorteio == 0:
            atraso: int = id_concurso
        elif self.ultimo_sorteio == id_concurso:  # a bola foi sorteada no ultimo concurso:
            atraso: int = 0  # nao ha atraso aqui, ja foi calculado antes
        else:  # ou se a bola ja foi sorteada antes, mas nao no ultimo concurso:
            atraso: int = id_concurso - self.ultimo_sorteio

        # atualiza os atrasos da bola:
        if atraso > 0:
            self.ultimo_atraso = atraso
            self.atrasos.append(atraso)

        # atualiza as medidas estatisticas, para nao ficar calculando quando adiciona sorteio:
        self.len_sorteios = len(self.sorteios)
        self.len_atrasos = len(self.atrasos)
        self.max_atraso = max(self.atrasos)
        self.min_atraso = min(self.atrasos)
        self.mode_atraso = stts.mode(self.atrasos)
        self.mean_atraso = stts.fmean(self.atrasos)
        self.hmean_atraso = stts.harmonic_mean(self.atrasos)
        self.gmean_atraso = stts.geometric_mean(self.atrasos)
        self.median_atraso = stts.median(self.atrasos)
        self.varia_atraso = stts.pvariance(self.atrasos)
        self.stdev_atraso = stts.pstdev(self.atrasos)

# ----------------------------------------------------------------------------
