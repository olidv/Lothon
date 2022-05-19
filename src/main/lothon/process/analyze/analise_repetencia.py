"""
   Package lothon.process
   Module  analise_repetencia.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain import Loteria, Concurso, ConcursoDuplo
from lothon.process.abstract_process import AbstractProcess


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseRepetencia(AbstractProcess):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_process', '_options'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Repetencia nos Concursos")

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def count_repeticoes(bolas1: tuple[int, ...], bolas2: tuple[int, ...]) -> int:
        # valida os parametros:
        if bolas1 is None or len(bolas1) == 0 or bolas2 is None or len(bolas2) == 0:
            return 0

        qtd_repete: int = 0
        for num1 in bolas1:
            if num1 in bolas2:
                qtd_repete += 1

        return qtd_repete

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, payload: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if payload is None or payload.concursos is None or len(payload.concursos) == 0:
            return -1

        # o numero de sorteios realizados pode dobrar se for instancia de ConcursoDuplo:
        concursos: list[Concurso | ConcursoDuplo] = payload.concursos
        qtd_concursos: int = len(concursos)
        eh_duplo: bool = ([0] is ConcursoDuplo)
        if eh_duplo:
            fator_sorteios: int = 2
        else:
            fator_sorteios: int = 1
        qtd_sorteios: int = qtd_concursos * fator_sorteios

        # efetua analise de todas as repetencias nos sorteios da loteria:
        logger.debug(f"{payload.nome_loteria}: Executando analise de TODAS repetencias nos  "
                     f"{qtd_concursos}  concursos da loteria.")

        # zera os contadores de cada repetencia:
        repetencia_tudo: dict[int, int] = self.new_dict_int(payload.qtd_bolas_sorteio)
        percentos_tudo: dict[int, float] = self.new_dict_float(payload.qtd_bolas_sorteio)
        repetencia_max: dict[int, int] = self.new_dict_int(payload.qtd_bolas_sorteio)
        percentos_max: dict[int, float] = self.new_dict_float(payload.qtd_bolas_sorteio)

        # contabiliza repetencias de cada sorteio com todos os sorteios ja realizados:
        for concurso_atual in concursos:
            max_repete: int = 0

            # efetua varredura dupla nos concursos para comparar as dezenas entre os concursos:
            for outro_concurso in concursos:
                # ignora o concurso atual, nao precisa comparar consigo mesmo:
                if concurso_atual.id_concurso == outro_concurso.id_concurso:
                    continue

                qt_repeticoes = self.count_repeticoes(concurso_atual.bolas, outro_concurso.bolas)
                repetencia_tudo[qt_repeticoes] += 1
                max_repete = max(max_repete, qt_repeticoes)
                # verifica se o concurso eh duplo (dois sorteios):
                if eh_duplo:
                    # se for concurso duplo, precisa comparar as bolas do segundo sorteio:
                    qt_repeticoes = self.count_repeticoes(concurso_atual.bolas,
                                                          outro_concurso.bolas2)
                    repetencia_tudo[qt_repeticoes] += 1
                    max_repete = max(max_repete, qt_repeticoes)
                    qt_repeticoes = self.count_repeticoes(concurso_atual.bolas2,
                                                          outro_concurso.bolas)
                    repetencia_tudo[qt_repeticoes] += 1
                    max_repete = max(max_repete, qt_repeticoes)
                    qt_repeticoes = self.count_repeticoes(concurso_atual.bolas2,
                                                          outro_concurso.bolas2)
                    repetencia_tudo[qt_repeticoes] += 1
                    max_repete = max(max_repete, qt_repeticoes)

            repetencia_max[max_repete] += 1

        # printa o resultado:
        output: str = f"\n\t ? REPETE  PERC%    #MAX%     #TOTAL\n"
        total = qtd_sorteios * (qtd_sorteios - fator_sorteios)
        for key, value in repetencia_tudo.items():
            percent: float = round((value / total) * 1000) / 10
            percentos_tudo[key] = percent
            rmax: int = repetencia_max[key]
            percent_max: float = round((rmax / qtd_sorteios) * 1000) / 10
            percentos_max[key] = percent_max
            output += f"\t {key} repete: {percent:0>4.1f}%    {percent_max:0>4.1f}% ... #{rmax:,}\n"
        logger.debug(f"Repetencias Resultantes: {output}")

        return 0

# ----------------------------------------------------------------------------
