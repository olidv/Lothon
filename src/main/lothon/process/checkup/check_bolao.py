"""
   Package lothon.process
   Module  check_bolao.py

"""

__all__ = [
    'CheckBolao'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
import os
from datetime import date, datetime
import itertools as itt
import logging

# Libs/Frameworks modules
# Own/Project modules
from lothon.util.eve import *
from lothon.conf import app_config
from lothon.infra import parser_resultados
from lothon.domain import Loteria, Concurso
from lothon.process.checkup.abstract_checkup import AbstractCheckup

# ----------------------------------------------------------------------------
# VARIAVEIS GLOBAIS
# ----------------------------------------------------------------------------

# obtem uma instancia do logger para o modulo corrente:
logger = logging.getLogger(__name__)

# relacao de acertos com premiacoes das loterias:
acertos_premiacoes: dict[str: list[int]] = {
    "diadesorte": [4, 5, 6, 7],
    "lotofacil": [11, 12, 13, 14, 15],
    "duplasena": [3, 4, 5, 6],
    "quina": [2, 3, 4, 5],
    "megasena": [4, 5, 6],
}


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

class CheckBolao(AbstractCheckup):
    """
    Implementacao de classe para .
    """

    # --- PROPRIEDADES -------------------------------------------------------
    __slots__ = ()

    # --- INICIALIZACAO ------------------------------------------------------

    def __init__(self):
        super().__init__("Conferencia de Apostas de Bolao")

    # --- METODOS STATIC -----------------------------------------------------

    @classmethod
    def get_arquivos_boloes(cls, nmlot: str) -> list[str] | None:
        # verifica a presenca de arquivos CSV com jogos de boloes:
        bolao_path: str = app_config.DS_bolao_path
        bolao_mask: str = app_config.BA_bolao_csv_mask.format(nmlot)
        logger.debug(f"{nmlot}: Verificando a presenca de arquivos de boloes em '{bolao_path}' "
                     f"utilizando a mascara '{bolao_mask}'.")

        # se nao ha arquivos de boloes, entao nao ha apostas para conferir:
        dir_contents, len_dir_contents = parser_resultados.get_dir_contents(bolao_path, bolao_mask)
        if len_dir_contents == 0:
            logger.info(f"{nmlot}: Nao foram encontrados arquivos de boloes para conferencia.")
            return None
        else:
            logger.info(f"{nmlot}: Encontrados  {formatd(len_dir_contents)}  arquivos de boloes "
                        f"para conferencia de apostas: \n{dir_contents}")
            return dir_contents

    @classmethod
    def get_arquivo_resultado(cls, nmlot: str, dt_bolao: str) -> str | None:
        # verifica a presenca de arquivos CSV com resultados da loteria:
        caixa_path: str = app_config.DS_caixa_path
        resultado_mask: str = app_config.BA_resultado_csv_name.format(nmlot, dt_bolao)
        logger.debug(f"{nmlot}: Verificando a presenca de arquivos de resultados em "
                     f"'{caixa_path}' utilizando a mascara '{resultado_mask}'.")

        # se nao ha arquivo de resultados, entao nao ha apostas para conferir:
        caixa_contents, len_contents = parser_resultados.get_dir_contents(caixa_path,
                                                                          resultado_mask)
        if len_contents == 0:
            return None
        else:
            return caixa_contents[0]

    @classmethod
    def get_concursos_by_date(cls, date_bolao: date, concursos: list[Concurso]) -> list[Concurso]:
        # valida os parametros fornecidos:
        if concursos is None or len(concursos) == 0:
            return []

        # percorre a lista de concursos a partir do final, ja que esta em ordem crescente da data:
        lista_concursos: list[concursos] = []
        for i in range(len(concursos) - 1, -1, -1):
            concurso: Concurso = concursos[i]
            # pode ter mais de um sorteio na mesma data, como na Dupla Sena:
            if concurso.data_sorteio == date_bolao:
                lista_concursos.append(concurso)
            # se passou da data, entao todas as proximas sao menores, ja pode pular fora do 'for'...
            elif concurso.data_sorteio < date_bolao:
                break

        return lista_concursos

    @classmethod
    def check_premiacao(cls, jogo: tuple[int, ...], concurso: Concurso,
                        acertos_premios: list[int]) -> tuple[int, float]:
        # verifica quantas dezenas acertou no jogo, conferindo com as bolas sorteadas do concurso:
        qtd_acerto: int = 0
        for dezena in jogo:
            if any(bola for bola in concurso.bolas if bola == dezena):
                qtd_acerto += 1

        # verifica se a quantidade de acertos eh premiada:
        if qtd_acerto not in acertos_premios:
            return 0, 0.0

        # se o concurso ja possui as faixas de premiacoes, verifica quanto em dinheiro faturou:
        val_premio: float = 0
        if qtd_acerto in concurso.premios:
            val_premio = concurso.premios[qtd_acerto].premio

        return qtd_acerto, val_premio

    @classmethod
    def conferir_sorteio(cls, bolao_path: str, ultimos_sorteios: list[Concurso],
                         acertos_premios: list[int]) -> tuple[dict, float]:
        # identifica o numero de dezenas para o jogo simples, para comparacao do resultado:
        qtd_bolas_sorteio: int = len(ultimos_sorteios[0].bolas)

        # efetua a leitura do arquivo de bolao e confere se a leitura foi ok:
        bolao_dezenas: list[tuple[int, ...]] = parser_resultados.read_dezenas_csv(bolao_path)
        if bolao_dezenas is None or len(bolao_dezenas) == 0:
            return {}, 0.0

        # confere relacao de jogos do bolao com os sorteios de determinada loteria:
        rol_acertos: dict[int: int] = {}
        tot_premios: float = 0.00
        for concurso in ultimos_sorteios:
            # confere cada jogo do bolao, contabiliza os acertos e soma o valor das premiacoes:
            for jogo in bolao_dezenas:
                qtd_acerto: int = 0
                val_premio: float = 0.0

                # se o numero de bolas do jogo corresponde ao numero dezenas sorteadas da loteria:
                qt_bolas_jogo: int = len(jogo)
                if qt_bolas_jogo == qtd_bolas_sorteio:
                    # basta conferir cada jogo com o concurso:
                    qtd_acerto, val_premio = cls.check_premiacao(jogo, concurso,
                                                                 acertos_premios)
                # se o numero de bolas sorteadas for inferior ao tamanho de cada jogo,
                elif qt_bolas_jogo > qtd_bolas_sorteio:  # entao o bolao esta com jogos combinados
                    # deve-se gerar as combinacoes de BASE dezenas para cada jogo com x dezenas:
                    for jogob in itt.combinations(jogo, qtd_bolas_sorteio):
                        qtd_acerto, val_premio = cls.check_premiacao(jogob, concurso,
                                                                     acertos_premios)
                # acumula os valores dos premios:
                if qtd_acerto > 0:
                    qtd = rol_acertos.get(qtd_acerto, 0)
                    rol_acertos[qtd_acerto] = qtd + 1
                    tot_premios += val_premio

        return rol_acertos, tot_premios

    @classmethod
    def conferir_resultado(cls, id_concurso: int, date_concurso: date, bolao_path: str,
                           resultado_path: str, acertos_premios: list[int]) -> tuple[dict, float]:
        # efetua a leitura do arquivo de resultado e confere se a leitura foi ok:
        result_dezenas: list[tuple[int, ...]] = parser_resultados.read_dezenas_csv(resultado_path)
        if result_dezenas is None or len(result_dezenas) == 0:
            return {}, 0.0

        # gera lista de concursos para conferir os sorteios utilizando os metodos de Concursos:
        ultimos_sorteios: list[Concurso] = []
        for bolas in result_dezenas:
            # como nao se sabe os premios ainda, passa dict vazio para o Concurso:
            ultimos_sorteios.append(Concurso(id_concurso, date_concurso, bolas, {}))

        return cls.conferir_sorteio(bolao_path, ultimos_sorteios, acertos_premios)

    # --- PROCESSAMENTO ------------------------------------------------------

    def execute(self, loteria: Loteria) -> int:
        # nao ha necessidade de validar se possui concursos, pois nao serao analisados:
        if loteria is None:
            return -1
        else:
            _startWatch = startwatch()

        # identifica informacoes da loteria:
        nmlot: str = loteria.nome_loteria
        concursos: list[Concurso] = loteria.concursos
        acertos_premios: list[int] = acertos_premiacoes[loteria.id_loteria]

        # verifica a presenca de arquivos CSV com jogos de boloes:
        bolao_contents: list[str] = self.get_arquivos_boloes(nmlot)
        if bolao_contents is None:
            # se nao ha arquivos de boloes, entao nao ha apostas para conferir:
            return -1

        # busca todos os arquivos na pasta de boloes (\data) para conferencia:
        date_mask: str = app_config.BA_bolao_csv_name[-12:-4]
        for bolao_path in bolao_contents:
            # a partir do nome do arquivo CSV, obtem o id e data do bolao:
            file_csv: str = os.path.basename(bolao_path)
            id_bolao: str = file_csv[:3]
            dt_bolao: str = file_csv[-14:-4]
            date_bolao: date = datetime.strptime(dt_bolao, date_mask).date()
            logger.debug(f"{nmlot}: Processando arquivo CSV de bolao ID = {id_bolao} "
                         f"para a DATA = {dt_bolao}...")

            # verifica se o sorteio para as apostas do bolao ja foi realizado e carregado (HTML):
            ultimos_sorteios: list[Concurso] = self.get_concursos_by_date(date_bolao, concursos)
            if len(ultimos_sorteios) > 0:
                id_concurso = ultimos_sorteios[0].id_concurso
                logger.debug(f"{nmlot}: O concurso #{formatd(id_concurso)} da DATA = {dt_bolao} "
                             f"ja foi carregado e sera utilizado para conferir as apostas.")
                rol_acertos, val_premios = self.conferir_sorteio(bolao_path, ultimos_sorteios,
                                                                 acertos_premios)

            else:
                logger.debug(f"{nmlot}: O sorteio da DATA = {dt_bolao} ainda nao foi carregado.")
                # verifica a presenca de arquivos CSV com resultados da loteria:
                resultado_path: str = self.get_arquivo_resultado(nmlot, dt_bolao)
                if resultado_path is None:
                    continue  # prossegue para o proximo arquivo CSV de bolao...
                else:
                    logger.info(f"{nmlot}: Encontrou o arquivo '{resultado_path}' para "
                                f"conferencia do bolao ID = {id_bolao} na DATA = {dt_bolao}.")
                    id_proximo_concurso: int = concursos[-1].id_concurso + 1
                    rol_acertos, val_premios = self.conferir_resultado(id_proximo_concurso,
                                                                       date_bolao, bolao_path,
                                                                       resultado_path,
                                                                       acertos_premios)
            logger.info(f"{nmlot}: Resultado da conferencia das apostas:\n"
                        f"\n\t *** Bolao ID = {id_bolao}  .::.  DATA = {dt_bolao}\n"
                        f"\t\t ### Qtd de Jogos Premiados = {rol_acertos}\n"
                        f"\t\t $$$ Valor Total de Premios = {formatc(val_premios)}\n")

        _stopWatch = stopwatch(_startWatch)
        logger.info(f"{nmlot}: Tempo para executar {self.id_process.upper()}: {_stopWatch}")
        return 0

# ----------------------------------------------------------------------------
