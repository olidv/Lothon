"""
   Package lothon.domain.sorteio
   Module  concurso.py

"""

__all__ = [
    'Concurso'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from datetime import date
from dataclasses import dataclass, field
from typing import Optional
import itertools as itt

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain.sorteio.premio import Premio


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass(frozen=True, order=True, slots=True)
class Concurso:
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    id_concurso: int
    data_sorteio: date
    bolas: tuple[int, ...]
    premios: dict[int, Premio]

    sort_index: int = field(init=False, repr=False)

    # --- INICIALIZACAO ------------------------------------------------------

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', self.id_concurso)

    # --- METODOS ------------------------------------------------------------

    def get_ganhadores_premio(self, qt_acertos: int) -> int:
        # verifica se ha premiacao para o numero de acertos indicado:
        if qt_acertos is None or qt_acertos not in self.premios:
            return 0
        else:
            return self.premios.get(qt_acertos).qtd_ganhadores

    def check_premiacao(self, numeros: tuple[int, ...]) -> Optional[Premio]:
        acertos: int = 0
        for numero in numeros:
            if any(bola for bola in self.bolas if bola == numero):
                acertos += 1

        if acertos in self.premios:
            return self.premios[acertos]
        else:
            return None

    def check_premiacao_total(self, numeros: tuple[int, ...]) -> float:
        # confere o jogo com o sorteio do concurso:
        premio: Optional[Premio] = self.check_premiacao(numeros)
        if premio is None:
            return 0.00
        else:
            return premio.premio

    # confere relacao de jogos de um bolao com o(s) sorteio(s) de determinado concurso:
    def check_premiacao_jogos(self, bolao: list[tuple[int, ...]],
                              qt_base: int = None) -> tuple[int, float]:
        qt_acertos: int = 0
        premio_total: float = 0.00

        # confere cada jogo do bolao e soma o valor das premiacoes:
        for jogo in bolao:
            # se o numero de bolas de cada jogo corresponde ao numero basico de dezenas da loteria:
            qt_bolas_jogo: int = len(jogo)
            if qt_base is None or qt_base == qt_bolas_jogo:
                # basta conferir cada jogo com o concurso:
                premiacao: float = self.check_premiacao_total(jogo)
                if premiacao > 0:
                    premio_total += premiacao
                    qt_acertos += 1

            # se o numero de bolas for inferior ao tamanho de cada jogo,
            elif qt_base < qt_bolas_jogo:  # # entao o bolao esta com jogos combinados,
                # deve-se gerar as combinacoes de BASE dezenas para cada jogo com x dezenas:
                for jogob in itt.combinations(jogo, qt_base):
                    premiacao: float = self.check_premiacao_total(jogob)
                    if premiacao > 0:
                        premio_total += premiacao
                        qt_acertos += 1

        return qt_acertos, premio_total

# ----------------------------------------------------------------------------
