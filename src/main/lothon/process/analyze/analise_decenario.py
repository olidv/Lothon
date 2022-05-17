"""
   Package lothon.process
   Module  analise_decenario.py

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

class AnaliseDecenario(AbstractProcess):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = '_id_process', '_options'

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Analise de Decenario nos Concursos")

    # --- METODOS STATIC -----------------------------------------------------

    @staticmethod
    def count_decenarios(bolas: tuple[int, ...], decenario: dict[int, int]) -> None:
        # valida os parametros:
        if bolas is None or len(bolas) == 0 or decenario is None or len(decenario) == 0:
            return

        for num in bolas:
            decenario[(num - 1) // 10] += 1

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

        # efetua analise de todas os sorteios da loteria:
        logger.debug("%s: Executando analise de decenario dos  %d  concursos da loteria.",
                     payload.nome_loteria, qtd_concursos)

        # zera os contadores de cada sequencia:
        decenario_tudo: dict[int, int] = self.new_dict_int((payload.qtd_bolas-1) // 10)
        percentos_tudo: dict[int, float] = self.new_dict_float((payload.qtd_bolas-1) // 10)

        # contabiliza decenarios de cada sorteio ja realizado:
        for concurso in concursos:
            self.count_decenarios(concurso.bolas, decenario_tudo)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                self.count_decenarios(concurso.bolas2, decenario_tudo)

        # printa o resultado:
        output: str = f"\n\t ? DECENARIO   PERC%     #TOTAL\n"
        total: int = payload.qtd_bolas_sorteio * qtd_sorteios
        for key, value in decenario_tudo.items():
            percent: float = round((value / total) * 10000) / 100
            percentos_tudo[key] = percent
            output += f"\t {key} decenario: {percent:0>5.2f}% ... #{value:,}\n"
        logger.debug("Decenarios Resultantes: %s", output)

        #
        logger.debug("%s: Executando analise EVOLUTIVA de decenario dos  %d  concursos da loteria.",
                     payload.nome_loteria, qtd_concursos)

        # contabiliza decenarios de cada evolucao de concurso:
        concursos_passados: list[Concurso | ConcursoDuplo] = []
        qtd_concursos_passados = 1  # evita divisao por zero
        concurso_atual: Concurso | ConcursoDuplo
        for concurso_atual in payload.concursos:
            # zera os contadores de cada decenario:
            decenarios_passados: dict[int, int] = self.new_dict_int((payload.qtd_bolas-1) // 10)

            # calcula a decenario dos concursos passados até o concurso anterior:
            for concurso_passado in concursos_passados:
                self.count_decenarios(concurso_passado.bolas, decenarios_passados)
                # verifica se o concurso eh duplo (dois sorteios):
                if eh_duplo:
                    self.count_decenarios(concurso_passado.bolas2, decenarios_passados)

            # calcula a decenario do concurso atual para comparar a evolucao:
            decenario_atual: dict[int, int] = self.new_dict_int((payload.qtd_bolas-1) // 10)
            self.count_decenarios(concurso_atual.bolas, decenario_atual)
            # verifica se o concurso eh duplo (dois sorteios):
            if eh_duplo:
                self.count_decenarios(concurso_atual.bolas2, decenario_atual)

            # printa o resultado:
            output: str = f"\n\t ? DECENARIO   PERC%       %DIF%  " \
                          f"----->  CONCURSO Nº {concurso_atual.id_concurso} :  " \
                          f"Ultimo Decenario == {decenario_atual}\n"
            total: int = payload.qtd_bolas_sorteio * (qtd_concursos_passados * fator_sorteios)
            for key, value in decenarios_passados.items():
                percent: float = round((value / total) * 10000) / 100
                dif: float = percent - percentos_tudo[key]
                output += f"\t {key} decenario: {percent:0>5.2f}% ... {dif:6.2f}%\n"
            logger.debug("Decenarios Resultantes da EVOLUTIVA: %s", output)

            # inclui o concurso atual para ser avaliado na proxima iteracao:
            concursos_passados.append(concurso_atual)
            qtd_concursos_passados = len(concursos_passados)

        return 0

# ----------------------------------------------------------------------------
