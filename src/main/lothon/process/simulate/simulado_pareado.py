"""
   Package lothon.process
   Module  simulado_pareado.py

"""

__all__ = [
    'SimuladoPareado'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import math
import random
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.stats import combinatoria as cb
from lothon.domain import Loteria, Concurso, Faixa
from lothon.process.simulate.abstract_simulate import AbstractSimulate


# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# medidas otimas de equilibrio de paridades para boloes:
pares: dict[int: int] = {11: 5, 10: 5, 9: 4, 8: 4, 7: 3}


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class SimuladoPareado(AbstractSimulate):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ('boloes_caixa',)

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Simulado com Dezenas Pareadas")

        # estrutura para auxilio na geracao de boles para simulacoes:
        self.boloes_caixa: dict[str: dict[int: int]] = None

    def setup(self, parms: dict):
        # absorve os parametros fornecidos:
        super().setup(parms)

        # inicializa as estruturas de processamento das simulacoes:
        self.boloes_caixa = self.options["boloes_caixa"]
        del self.options["boloes_caixa"]  # nao precisa no options, ja tem 'self.boloes_caixa'

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def sortear_bolas(cls, set_bolas: int, qtd_sorteadas: int) -> tuple[int, ...]:
        global pares
        bolas: tuple[int, ...] = ()

        # verifica a proporcao do numero de pares e impares:
        qt_pares: int = pares.get(qtd_sorteadas, qtd_sorteadas // 2)
        qt_impar: int = qtd_sorteadas - qt_pares

        # seleciona os pares primeiro:
        count: int = 0
        while count < qt_pares:
            bola = random.randint(1, set_bolas)
            if bola not in bolas and cb.is_par(bola):
                bolas = bolas + (bola,)
                count += 1

        # em seguida seleciona os impares:
        count = 0
        while count < qt_impar:
            bola = random.randint(1, set_bolas)
            if bola not in bolas and cb.is_impar(bola):
                bolas = bolas + (bola,)
                count += 1

        # print(f"*** SORTEIO DE {qtd_sorteadas} BOLAS: #{qt_pares} PARES, #{qt_impar} IMPARES ***")
        # print(f"*** JOGO GRERADO: {bolas} ***")
        return bolas

    @classmethod
    def gerar_bolao_pareado(cls, set_bolas: int, qtd_sorteadas: int, qtd_jogos: int,
                            concursos_passados: list[Concurso]) -> list[tuple[int, ...]]:
        bolao: list[tuple[int, ...]] = []
        
        # gera jogos com dezenas selecionadas apos analisar os concursos passados:
        if concursos_passados is not None:
            for i in range(0, qtd_jogos):
                bolao.append(SimuladoPareado.sortear_bolas(set_bolas, qtd_sorteadas))

        return bolao

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, loteria: Loteria) -> int:
        # valida se possui concursos a serem analisados:
        if loteria is None or loteria.concursos is None or len(loteria.concursos) == 0:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = loteria.nome_loteria
        concursos: list[Concurso] = loteria.concursos
        qtd_concursos: int = len(concursos)

        # efetua simulacao de jogos aleatorios em todos os sorteios da loteria:
        logger.debug(f"{nmlot}: Executando simulacao de jogos pareados em todos os"
                     f"  {formatd(qtd_concursos)}  concursos da loteria.")

        # zera os contadores dos ciclos fechados:
        boloes: dict[int: int] = self.boloes_caixa[loteria.id_loteria]
        faixas: dict[int, Faixa] = loteria.faixas
        bolas: int = loteria.qtd_bolas
        base: int = loteria.qtd_bolas_sorteio
        precob: float = faixas[base].preco

        total_gastosb: float = 0.00
        total_acertosb: int = 0
        total_acertosx: int = 0
        total_premiosb: float = 0.00
        total_premiosx: float = 0.00

        # concursos passados sao usados para gerar novos jogos:
        concursos_passados: list[Concurso] = []

        # efetua apostas apenas nos ultimos 500 concursos da loteria, mas de forma acumulativa:
        qtd_proc: int = self.options.get("qtd_proc", 100)  # default para os 100 ultimos concursos
        id_inicial: int = max(0, len(concursos) - qtd_proc)  # max para evitar numero negativo
        qtd_concursos = 0
        for concurso in concursos:
            # se o concurso esta abaixo do concurso inicial (id_inicial), entao ignora:
            if id_inicial > concurso.id_concurso:
                # ao menos este concurso sera usado como base para o proximo concurso:
                concursos_passados.append(concurso)
                continue
            else:  # no loop normal, contabiliza os concursos processados para calcular a media:
                qtd_concursos += 1

            # formatacao para apresentacao:
            output: str = f"\t#DEZENAS      #PAREADAS        GASTO R$          " \
                          f"#ACERTOS        PREMIOS R$\n"

            # para cada concurso, faz a comparacao entre jogos simples e com boloes:
            for qtd_dezenas, qtd_apostas in boloes.items():
                # *** APOSTAS BASE: MENOR PRECO ***
                qtd_jogosb: int = math.comb(qtd_dezenas, base) * qtd_apostas
                gastosb: float = precob * qtd_jogosb

                # gera os jogos simples, sem bolao:
                bolaob: list[tuple[int, ...]] = self.gerar_bolao_pareado(bolas, base, qtd_jogosb,
                                                                         concursos_passados)
                # confere os boloes de BASE jogos
                acertosb, premiosb = concurso.check_premiacao_jogos(bolaob)
                output += f"\t      {formatd(base,2)}         {formatd(qtd_jogosb,6)}" \
                          f"       {formatf(gastosb,'9.2')}                {formatd(acertosb,2)}" \
                          f"    {formatf(premiosb)}\n"

                # *** APOSTAS COM XX DEZENAS ***
                gastosx: float = faixas[qtd_dezenas].preco * qtd_apostas

                # gera os jogos para os boloes, usando analise estatistica:
                bolaox: list[tuple[int, ...]] = self.gerar_bolao_pareado(bolas, qtd_dezenas,
                                                                         qtd_apostas,
                                                                         concursos_passados)
                # confere os boloes de x jogos
                acertosx, premiosx = concurso.check_premiacao_jogos(bolaox, base)
                output += f"\t      {formatd(qtd_dezenas,2)}         {formatd(qtd_apostas,6)}" \
                          f"       {formatf(gastosx,'9.2')}                {formatd(acertosx,2)}" \
                          f"    {formatf(premiosx)}\n\n"

                total_gastosb += gastosb
                total_acertosb += acertosb
                total_acertosx += acertosx
                total_premiosb += premiosb
                total_premiosx += premiosx

            # logger.debug(f"{nmlot}: CONCURSO #{concurso.id_concurso}  .:.  "
            #              f"Data: {concurso.data_sorteio}\n"
            #              f"{output}")

            # este concurso sera usado como base para o proximo concurso:
            concursos_passados.append(concurso)

        media_gastosb: float = total_gastosb / qtd_concursos
        media_acertosb: int = total_acertosb // qtd_concursos
        media_acertosx: int = total_acertosx // qtd_concursos
        media_premiosb: float = total_premiosb / qtd_concursos
        media_premiosx: float = total_premiosx / qtd_concursos
        media_permiosb_percent: float = media_premiosb / media_gastosb * 100
        media_permiosx_percent: float = media_premiosx / media_gastosb * 100
        total_premiosb_percent: float = total_premiosb / total_gastosb * 100
        total_premiosx_percent: float = total_premiosx / total_gastosb * 100

        logger.info(f"{nmlot}: Comparando apostas de {base} dezenas com boloes de "
                    f"X dezenas em {qtd_concursos} concursos:\n"

                    f"\t\t MEDIA PAREADAS: Gasto medio com apostas   R$ = "
                    f"{formatf(media_gastosb,'17.2')}\n\n"
                    f"\t\t MEDIA PAREADAS: Acertos para {formatd(base,2)} dezenas    # = "
                    f"{formatd(media_acertosb,17)}\n"
                    f"\t\t MEDIA PAREADAS: Premios para {formatd(base,2)} dezenas   R$ = "
                    f"{formatf(media_premiosb,'17.2')}  ...  "
                    f"{formatf(media_permiosb_percent,'9.2')}%\n\n"
                    f"\t\t MEDIA PAREADAS: Acertos para XX dezenas    # = "
                    f"{formatd(media_acertosx,17)}\n"
                    f"\t\t MEDIA PAREADAS: Premios para XX dezenas   R$ = "
                    f"{formatf(media_premiosx,'17.2')}  ...  "
                    f"{formatf(media_permiosx_percent,'9.2')}%\n\n\n"

                    f"\t\t TOTAL PAREADAS: Gasto total com apostas   R$ = "
                    f"{formatf(total_gastosb,'17.2')}\n\n"
                    f"\t\t TOTAL PAREADAS: Acertos para {formatd(base,2)} dezenas    # = "
                    f"{formatd(total_acertosb,17)}\n"
                    f"\t\t TOTAL PAREADAS: Premios para {formatd(base,2)} dezenas   R$ = "
                    f"{formatf(total_premiosb,'17.2')}  ...  "
                    f"{formatf(total_premiosb_percent,'9.2')}%\n\n"
                    f"\t\t TOTAL PAREADAS: Acertos para XX dezenas    # = "
                    f"{formatd(total_acertosx,17)}\n"
                    f"\t\t TOTAL PAREADAS: Premios para XX dezenas   R$ = "
                    f"{formatf(total_premiosx,'17.2')}  ...  "
                    f"{formatf(total_premiosx_percent,'9.2')}%\n")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
