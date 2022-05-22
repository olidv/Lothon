"""
   Package lothon.process
   Module  analise_repetencia.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import datetime
import time
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.domain import Loteria, Concurso, ConcursoDuplo, Bola
from lothon.process.abstract_process import AbstractProcess


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
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
        else:
            _startTime: float = time.time()

        # o numero de sorteios realizados pode dobrar se for instancia de ConcursoDuplo:
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
        logger.debug(f"{payload.nome_loteria}: Executando analise de TODAS repetencias nos  "
                     f"{qtd_concursos:,}  concursos da loteria.")

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
            output += f"\t {key:0>2} repete:  {percent_max:0>5.1f}%     {percent:0>5.1f}% ... " \
                      f"#{value:,}\n"
        logger.debug(f"Repetencias Resultantes: {output}")

        # efetua analise de todas as repeticoes dos sorteios da loteria:
        logger.debug(f"{payload.nome_loteria}: Executando analise de FREQUENCIA de repetencias"
                     f"de dezenas nos  {qtd_concursos:,}  concursos da loteria.")

        # zera os contadores de frequencias e atrasos das repetencias:
        repetencias: list[Bola | None] = self.new_list_bolas(qtd_items)
        repetencias[0] = Bola(0)  # neste caso especifico tem a repetencia zero!

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
        for bola in repetencias:
            # vai aproveitar e contabilizar as medidas estatisticas para a bola:
            bola.last_concurso(ultimo_concurso.id_concurso)

        # printa o resultado:
        output: str = f"\n\tREPETE:   #SORTEIOS   ULTIMO     #ATRASOS   ULTIMO   MAIOR   " \
                      f"MENOR   MODA    MEDIA   H.MEDIA   G.MEDIA   MEDIANA   " \
                      f"VARIANCIA   DESVIO-PADRAO\n"
        for bola in repetencias:
            output += f"\t    {bola.id_bola:0>2}:       {bola.len_sorteios:0>5,}    " \
                      f"{bola.ultimo_sorteio:0>5,}        {bola.len_atrasos:0>5,}    " \
                      f"{bola.ultimo_atraso:0>5,}   {bola.max_atraso:0>5,}   " \
                      f"{bola.min_atraso:0>5,}  {bola.mode_atraso:0>5,}   " \
                      f"{bola.mean_atraso:0>6.1f}    {bola.hmean_atraso:0>6.1f}    " \
                      f"{bola.gmean_atraso:0>6.1f}    {bola.median_atraso:0>6.1f}    " \
                      f"{bola.varia_atraso:0>8.1f}          {bola.stdev_atraso:0>6.1f} \n"

        logger.debug(f"FREQUENCIA de Repetencias Resultantes: {output}")

        _totalTime: int = round(time.time() - _startTime)
        tempo_total: str = str(datetime.timedelta(seconds=_totalTime))
        logger.info(f"Tempo para executar {self.id_process.upper()}: {tempo_total} segundos.")
        return 0

# ----------------------------------------------------------------------------
