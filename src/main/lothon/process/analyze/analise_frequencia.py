"""
   Package lothon.process
   Module  analise_frequencia.py

"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
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
        super().__init__("Analise de Frequencia das Dezenas dos Concursos")

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def new_list_bolas(qtd_bolas: int) -> list[Bola]:
        # valida os parametros:
        if qtd_bolas is None or qtd_bolas == 0:
            return []

        bolas: list[Bola | None] = [None] * (qtd_bolas + 1)  # adiciona 1 para ignorar zero-index
        for i in range(1, qtd_bolas+1):
            bolas[i] = Bola(i)

        return bolas

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
        # qtd_sorteios: int = qtd_concursos * fator_sorteios

        # efetua analise de todas as dezenas dos sorteios da loteria:
        logger.debug("%s: Executando analise de frequencia de TODAS as dezenas nos  %d  concursos "
                     "da loteria.", payload.nome_loteria, qtd_concursos)

        # zera os contadores dos ciclos fechados:
        dezenas: list[Bola] = self.new_list_bolas(payload.qtd_bolas)

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
        output: str = f"\n\t BOLA:   #SORTEIOS   ULTIMO     #ATRASOS:   MAIOR   MENOR   MEDIA\n"
        for bola in dezenas:
            if bola is None:
                continue

            output += f"\t  {bola.id_bola:0>3}:         {bola.qtd_sorteios:0>3,}" \
                      f"     {bola.ultimo_sorteio:0>3}          {bola.qtd_atrasos:0>3,} " \
                      f"     {bola.maior_atraso:0>3}     {bola.menor_atraso:0>3}  " \
                      f" {bola.media_atraso:0>5.1f}\n"

        logger.debug("Frequencia de Dezenas Resultantes: %s", output)

        return 0

# ----------------------------------------------------------------------------
