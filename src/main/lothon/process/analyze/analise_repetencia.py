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
from lothon.util.eve import *
from lothon.domain import Loteria, Concurso, ConcursoDuplo, SerieSorteio
from lothon.process.analyze.abstract_analyze import AbstractAnalyze


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseRepetencia(AbstractAnalyze):
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
        else:
            _startWatch = startwatch()

        # o numero de sorteios realizados pode dobrar se for instancia de ConcursoDuplo:
        nmlot: str = payload.nome_loteria
        concursos: list[Concurso | ConcursoDuplo] = payload.concursos
        qtd_concursos: int = len(concursos)
        eh_duplo: bool = ([0] is ConcursoDuplo)
        if eh_duplo:
            fator_sorteios: int = 2
        else:
            fator_sorteios: int = 1
        qtd_sorteios: int = qtd_concursos * fator_sorteios
        qtd_items: int = payload.qtd_bolas_sorteio

        # efetua analise de repetencias de todos os sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de TODAS repetencias nos  "
                     f"{formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de cada repetencia:
        repetencia_tudo: list[int] = self.new_list_int(qtd_items)
        repetencia_max: list[int] = self.new_list_int(qtd_items)
        percentos_tudo: list[float] = self.new_list_float(qtd_items)
        percentos_max: list[float] = self.new_list_float(qtd_items)

        # contabiliza repetencias de cada sorteio com todos os sorteios ja realizados:
        for concurso in concursos:
            max_repete: int = 0

            # efetua varredura dupla nos concursos para comparar as dezenas entre os concursos:
            for outro_concurso in concursos:
                # somente compara com os concursos passados, simulando a evolucao real dos sorteios:
                if outro_concurso.id_concurso >= concurso.id_concurso:
                    break  # pode pular fora pq concursos esta ordenado pelo id_concurso.

                qt_repeticoes: int = self.count_repeticoes(concurso.bolas, outro_concurso.bolas)
                repetencia_tudo[qt_repeticoes] += 1
                max_repete = max(max_repete, qt_repeticoes)
                # verifica se o concurso eh duplo (dois sorteios):
                if eh_duplo:
                    # se for concurso duplo, precisa comparar as bolas do segundo sorteio:
                    qt_repeticoes = self.count_repeticoes(concurso.bolas, outro_concurso.bolas2)
                    repetencia_tudo[qt_repeticoes] += 1
                    max_repete = max(max_repete, qt_repeticoes)
                    qt_repeticoes = self.count_repeticoes(concurso.bolas2, outro_concurso.bolas)
                    repetencia_tudo[qt_repeticoes] += 1
                    max_repete = max(max_repete, qt_repeticoes)
                    qt_repeticoes = self.count_repeticoes(concurso.bolas2, outro_concurso.bolas2)
                    repetencia_tudo[qt_repeticoes] += 1
                    max_repete = max(max_repete, qt_repeticoes)

            repetencia_max[max_repete] += 1

        # printa o resultado:
        output: str = f"\n\t  ? REPETE    #MAX%      PERC%     #TOTAL\n"
        total = qtd_sorteios * (qtd_sorteios - fator_sorteios)
        for key, value in enumerate(repetencia_tudo):
            percent: float = round((value / total) * 1000) / 10
            percentos_tudo[key] = percent
            rmax: int = repetencia_max[key]
            percent_max: float = round((rmax / qtd_sorteios) * 1000) / 10
            percentos_max[key] = percent_max
            output += f"\t {formatd(key,2)} repete:  {formatf(percent_max,'5.1')}%     " \
                      f"{formatf(percent,'5.1')}% ... " \
                      f"#{formatd(value)}\n"
        logger.debug(f"{nmlot}: Repetencias Resultantes: {output}")

        # efetua analise de todas as repeticoes dos sorteios da loteria:
        logger.debug(f"{nmlot}: Executando analise de FREQUENCIA de repetencias"
                     f"de dezenas nos  {formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores de frequencias e atrasos das repetencias:
        repetencias: list[SerieSorteio | None] = self.new_list_series(qtd_items)
        repetencias[0] = SerieSorteio(0)  # neste caso especifico tem a repetencia zero!

        # contabiliza as frequencias e atrasos das repetencias em todos os sorteios ja realizados:
        concurso_anterior: Concurso | ConcursoDuplo | None = None
        for concurso in concursos:
            # o primeiro concurso soh eh registrado para teste no proximo:
            if concurso_anterior is None:
                concurso_anterior = concurso
                continue

            # verifica se o concurso eh duplo (dois sorteios) pois tem ordem de comparacao:
            if eh_duplo:  # se for concurso duplo, precisa registrar as repetencias na ordem:
                # o primeiro sorteio do concurso atual segue o segundo sorteio do concurdo anterior:
                qt_repeticoes: int = self.count_repeticoes(concurso.bolas,
                                                           concurso_anterior.bolas2)
                repetencias[qt_repeticoes].add_sorteio(concurso.id_concurso)
                # o segundo sorteio do concurso atual segue o primeiro sorteio do concurso atual:
                qt_repeticoes: int = self.count_repeticoes(concurso.bolas2,
                                                           concurso.bolas)
                repetencias[qt_repeticoes].add_sorteio(concurso.id_concurso)
            else:
                # contabiliza o numero de dezenas repetidas desde o ultimo concurso:
                qt_repeticoes: int = self.count_repeticoes(concurso.bolas, concurso_anterior.bolas)
                repetencias[qt_repeticoes].add_sorteio(concurso.id_concurso)

        # registra o ultimo concurso para contabilizar os atrasos ainda nao fechados:
        ultimo_concurso: Concurso | ConcursoDuplo = concursos[-1]
        for serie in repetencias:
            # vai aproveitar e contabilizar as medidas estatisticas para a repetencia:
            serie.last_sorteio(ultimo_concurso.id_concurso)

        # printa o resultado:
        output: str = f"\n\tREPETE:   #SORTEIOS   ULTIMO     #ATRASOS   ULTIMO   MENOR   " \
                      f"MAIOR   MODA    MEDIA   H.MEDIA   G.MEDIA   MEDIANA   " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for serie in repetencias:
            output += f"\t    {formatd(serie.id,2)}:       " \
                      f"{formatd(serie.len_sorteios,5)}    " \
                      f"{formatd(serie.ultimo_sorteio,5)}        " \
                      f"{formatd(serie.len_atrasos,5)}    " \
                      f"{formatd(serie.ultimo_atraso,5)}   " \
                      f"{formatd(serie.min_atraso,5)}  " \
                      f"{formatd(serie.max_atraso,5)}   " \
                      f"{formatd(serie.mode_atraso,5)}  " \
                      f"{formatf(serie.mean_atraso,'7.1')}   " \
                      f"{formatf(serie.hmean_atraso,'7.1')}   " \
                      f"{formatf(serie.gmean_atraso,'7.1')}   " \
                      f"{formatf(serie.median_atraso,'7.1')}   " \
                      f"{formatf(serie.varia_atraso,'9.1')}         " \
                      f"{formatf(serie.stdev_atraso,'7.1')} \n"

        logger.debug(f"{nmlot}: FREQUENCIA de Repetencias Resultantes: {output}")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
