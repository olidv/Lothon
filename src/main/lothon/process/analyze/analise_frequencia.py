"""
   Package lothon.process
   Module  analise_frequencia.py

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

# obtem uma instância do logger para o modulo corrente:
logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class AnaliseFrequencia(AbstractProcess):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_process', '_options'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Análise de Frequência dos Concursos")

    # --- METODOS STATIC -----------------------------------------------------

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

        # efetua analise de todas as dezenas dos sorteios da loteria:
        logger.debug(f"{payload.nome_loteria}: Executando análise de frequência de TODAS as "
                     f"dezenas nos  {qtd_concursos:,}  concursos da loteria.")

        # zera os contadores dos ciclos fechados:
        dezenas: list[Bola | None] = self.new_list_bolas(qtd_items)

        # contabiliza os ciclos fechados em todos os sorteios ja realizados:
        for concurso in concursos:
            # registra o concurso para cada dezena sorteada:
            for bola in concurso.bolas:
                dezenas[bola].add_sorteio(concurso.id_concurso)

            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                # se for concurso duplo, precisa comparar as bolas do segundo sorteio:
                for bola in concurso.bolas2:
                    dezenas[bola].add_sorteio(concurso.id_concurso)

        # printa o resultado:
        output: str = f"\n\t BOLA:   #SORTEIOS   ÚLTIMO     #ATRASOS:   MAIOR   MENOR    MÉDIA\n"
        for bola in dezenas:
            if bola is None or bola.id_bola == 0:
                continue

            output += f"\t  {bola.id_bola:0>3}:         {bola.qtd_sorteios:0>3,}" \
                      f"    {bola.ultimo_sorteio:0>3,}          {bola.qtd_atrasos:0>3,} " \
                      f"     {bola.maior_atraso:0>3}     {bola.menor_atraso:0>3}   " \
                      f" {bola.media_atraso:0>5.1f}\n"

        logger.debug(f"Frequência de Dezenas Resultantes: {output}")

        _totalTime: int = round(time.time() - _startTime)
        tempo_total: str = str(datetime.timedelta(seconds=_totalTime))
        logger.info(f"Tempo para executar {self.id_process.upper()}: {tempo_total} segundos.")
        return 0

# ----------------------------------------------------------------------------
