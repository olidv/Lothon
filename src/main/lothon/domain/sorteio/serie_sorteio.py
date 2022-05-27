"""
   Package lothon.domain.sorteio
   Module  serie_sorteio.py

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

@dataclass(slots=True)
class SerieSorteio:
    """
    Implementacao de classe para armazenar as ocorrencias de determinado
    numero (id) nos sorteios de uma ou mais loterias.
    """

    # --- PROPRIEDADES -------------------------------------------------------
    id: int

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

    # --- METODOS ------------------------------------------------------------

    # este numero ocorreu no concurso indicado:
    def add_sorteio(self, id_concurso: int, inclusive: bool = False):  # default eh nao-inclusivo
        dif: int = 0 if inclusive else 1
        # verifica se eh a primeira ocorrencia do numero:
        if self.ultimo_sorteio == 0:
            atraso: int = id_concurso - dif
        else:  # ou se o numero ja ocorreu em outros sorteios:
            atraso: int = id_concurso - self.ultimo_sorteio - dif

        # atualiza os atrasos da ocorrencia do numero:
        if atraso > 0:
            self.ultimo_atraso = atraso
            self.atrasos.append(atraso)

        # nao registra o ultimo sorteio mais de uma vez:
        if self.ultimo_sorteio != id_concurso:
            self.ultimo_sorteio = id_concurso
            self.sorteios.append(id_concurso)

    # ultimo concurso ocorrido da loteria, ainda sem ocorrencia deste numero:
    def last_sorteio(self, id_concurso: int):  # por default, o ultimo concurso eh inclusivo
        # verifica se eh a primeira ocorrencia do numero:
        if self.ultimo_sorteio == 0:
            atraso: int = id_concurso
        elif self.ultimo_sorteio == id_concurso:  # o numero ja ocorreu no ultimo concurso:
            atraso: int = 0  # nao ha atraso aqui, ja foi calculado antes
        else:  # ou se o numero ja ocorreu em outros sorteios, mas nao no ultimo concurso:
            atraso: int = id_concurso - self.ultimo_sorteio

        # atualiza os atrasos da ocorrencia do numero:
        if atraso > 0:
            self.ultimo_atraso = atraso
            self.atrasos.append(atraso)

        # aproveita e atualiza as medidas estatisticas:
        self.update_stats()

    # atualiza as medidas estatisticas, para nao ficar calculando quando adiciona sorteio:
    def update_stats(self):
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
