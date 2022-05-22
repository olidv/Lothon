"""
   Package lothon.process
   Module  analise_ciclo.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import datetime
import time
import logging
import statistics

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

class AnaliseCiclo(AbstractProcess):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_process', '_options'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Análise de Ciclo Fechado dos Concursos")

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def count_dezenas(bolas: tuple[int, ...], dezenas: list[int]) -> None:
        # valida os parametros:
        if bolas is None or len(bolas) == 0 or dezenas is None or len(dezenas) == 0:
            return

        for num in bolas:
            dezenas[num] += 1

        return

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
        # qtd_sorteios: int = qtd_concursos * fator_sorteios
        qtd_items: int = payload.qtd_bolas

        # efetua analise de todas os ciclos fechados ao longo dos sorteios da loteria:
        logger.debug(f"{payload.nome_loteria}: Executando análise de TODOS os ciclos fechados nos  "
                     f"{qtd_concursos:,}  concursos da loteria.")

        # zera os contadores dos ciclos fechados:
        dezenas: list[int | None] = self.new_list_int(qtd_items)
        dezenas[0] = None
        ciclos: list[tuple[int, ...]] = []
        maior_intervalo: int = 0
        menor_intervalo: int = 10000
        qtd_intervalos: int = 0
        sum_intervalos: int = 0

        # contabiliza os ciclos fechados em todos os sorteios ja realizados:
        init_intervalo: int = 0
        for concurso in concursos:
            # registra o inicio do intervalo:
            if init_intervalo == 0:
                init_intervalo = concurso.id_concurso

            self.count_dezenas(concurso.bolas, dezenas)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                # se for concurso duplo, precisa registrar as bolas do segundo sorteio:
                self.count_dezenas(concurso.bolas2, dezenas)

            # se ainda tem algum zero, entao nao fechou o ciclo:
            if 0 in dezenas:
                continue

            # fechando o ciclo, contabiliza o ciclo fechado:
            intervalo_ciclo: int = concurso.id_concurso - init_intervalo + 1
            maior_intervalo = max(maior_intervalo, intervalo_ciclo)
            menor_intervalo = min(menor_intervalo, intervalo_ciclo)
            qtd_intervalos += 1
            sum_intervalos += intervalo_ciclo
            ciclos.append((init_intervalo, concurso.id_concurso, intervalo_ciclo))

            # zera contadores para proximo ciclo:
            dezenas: list[int | None] = self.new_list_int(qtd_items)
            dezenas[0] = None
            init_intervalo = 0

        # printa o resultado:
        output: str = f"\n\t INICIO     FINAL   INTERVALO \n"
        for (inicio, final, intervalo) in ciclos:
            output += f"\t  {inicio:0>5,} ... {final:0>5,}         {intervalo:0>3}\n"

        output += f"\n\t #INTERVALOS   MENOR   MAIOR   MÉDIA\n"
        media_intervalo: float = round((sum_intervalos / qtd_intervalos) * 10) / 10
        output += f"\t     {qtd_intervalos:0>3,}         {menor_intervalo:0>3,}   " \
                  f"  {maior_intervalo:0>3,}    {media_intervalo:0>4.1f}\n"

        logger.debug(f"Ciclos Fechados Resultantes: {output}")

        _totalTime: int = round(time.time() - _startTime)
        tempo_total: str = str(datetime.timedelta(seconds=_totalTime))
        logger.info(f"Tempo para executar {self.id_process.upper()}: {tempo_total} segundos.")
        return 0

# ----------------------------------------------------------------------------
