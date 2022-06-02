"""
   Package lothon.conf
   Module  appconfig.py

   Carga das configuracoes da aplicacao a partir de arquivo INI.
"""

__all__ = [
    'AppConfig'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass
from configparser import ConfigParser
from typing import Optional


# Libs/Frameworks modules
# Own/Project modules


# ----------------------------------------------------------------------------
# CLASSE CONCRETA
# ----------------------------------------------------------------------------

@dataclass
class AppConfig:
    """
       Classe contendo toda a configuracao INI da aplicacao.
    """

    # Estrutura de diretorios da aplicacao:
    RT_app_home: str = ''
    RT_bet_path: str = ''
    RT_dat_path: str = ''
    RT_log_path: str = ''
    RT_tmp_path: str = ''

    RT_files_htm_mask: str = ''
    RT_files_csv_mask: str = ''
    RT_files_log_mask: str = ''
    RT_files_all_mask: str = ''

    # Parametrizacao dos arquivos de dados para leitura e exportacao:
    DS_caixa_path: str = ''
    DS_input_path: str = ''
    DS_output_path: str = ''
    DS_pares_csv_name: str = ''
    DS_sorteios_csv_name: str = ''

    # Parametrizacao das loterias da Caixa EF:
    LC_loterias_caixa: Optional[list[tuple[str, ...]]] = None
    LC_loteria_htm_name: str = ''
    LC_table_class_find: str = ''

    # Parametrizacao para geracao de boloes de apostas:
    BA_bolao_csv_name: str = ''

    # .
    def load_properties(self, parser: ConfigParser):
        # nao faz nada se nao forneceu o parser...
        if parser is None:
            return

        # com o parser, carrega o arquivo INI nos parametros da dataclass:
        self.RT_app_home = parser.get("ROOT", "app_home")
        self.RT_bet_path = parser.get("ROOT", "bet_path")
        self.RT_dat_path = parser.get("ROOT", "dat_path")
        self.RT_log_path = parser.get("ROOT", "log_path")
        self.RT_tmp_path = parser.get("ROOT", "tmp_path")

        self.RT_files_htm_mask = parser.get("ROOT", "files_htm_mask")
        self.RT_files_csv_mask = parser.get("ROOT", "files_csv_mask")
        self.RT_files_log_mask = parser.get("ROOT", "files_log_mask")
        self.RT_files_all_mask = parser.get("ROOT", "files_all_mask")

        # Parametrizacao dos arquivos de dados para leitura e exportacao:
        self.DS_caixa_path = parser.get("DADOS", "caixa_path")
        self.DS_input_path = parser.get("DADOS", "input_path")
        self.DS_output_path = parser.get("DADOS", "output_path")
        self.DS_pares_csv_name = parser.get("DADOS", "pares_csv_name")
        self.DS_sorteios_csv_name = parser.get("DADOS", "sorteios_csv_name")

        # Parametrizacao das loterias da Caixa EF:
        self.LC_loteria_htm_name = parser.get("LOTERIA_CAIXA", "loteria_htm_name")
        self.LC_table_class_find = parser.get("LOTERIA_CAIXA", "table_class_find")

        loterias = parser.get("LOTERIA_CAIXA", "loterias_caixa").split(',')
        self.LC_loterias_caixa = [tuple(jogo.strip().split(';')) for jogo in loterias]

        # Parametrizacao para geracao de boloes de apostas:
        self.BA_bolao_csv_name = parser.get("BOLAO_APOSTA", "bolao_csv_name")

    # --- CONSTANTES ---------------------------------------------------------

    MAP_MESES = {'1':   1, 'janeiro':   1,
                 '2':   2, 'fevereiro': 2,
                 '3':   3, 'março':     3, 'marco': 3,
                 '4':   4, 'abril':     4,
                 '5':   5, 'maio':      5,
                 '6':   6, 'junho':     6,
                 '7':   7, 'julho':     7,
                 '8':   8, 'agosto':    8,
                 '9':   9, 'setembro':  9,
                 '10': 10, 'outubro':  10,
                 '11': 11, 'novembro': 11,
                 '12': 12, 'dezembro': 12}

    MAP_TIMES = {'abc/rn': 1, 'abc': 1, 'a b c/rn': 1, 'abcentusjoaoa': 1,
                 'america/rn': 2, 'america': 2, 'americase': 2,
                 'america/mg': 3,
                 'america/rj': 4, 'americanoeaba': 4, 'americaujoaoa': 4,
                 'americano/rj': 5, 'americano': 5,
                 'atletico/go': 6, 'atletico': 6,
                 'atletico/mg': 7, 'atleticoeta': 7,
                 'atletico/pr': 8, 'athletico/pr': 8, 'athleticoa': 8, 'athleticozseo': 8,
                                   'athletico': 8,
                 'avai/sc': 9, 'avai': 9, 'avaiipeoaoa': 9, 'avaiaicoeta': 9,
                 'bahia/ba': 10, 'bahia': 10, 'bahiaranco': 10, 'bahiaicoeta': 10,
                                 'bahiamundoe': 10, 'bahiacanoeaba': 10,
                 'bangu/rj': 11, 'bangu': 11,
                 'barueri/sp': 12, 'barueri': 12, 'barueriujoaoa': 12,
                 'botafogo/pb': 13, 'botafogo': 13,
                 'botafogo/rj': 14,
                 'bragantino/sp': 15, 'bragantino': 15, 'rb bragantino': 15,
                 'brasiliense/df': 16, 'brasiliense': 16, 'brasilienseba': 16,
                 'ceara/ce': 17, 'ceara': 17, 'cearasudese': 17, 'cearairenseno': 17,
                                 'cearatudeseno': 17,
                 'corinthians/sp': 18, 'corinthians': 18,
                 'coritiba/pr': 19, 'coritiba': 19, 'coritibantino': 19,
                 'crb/al': 20, 'crb': 20, 'crbiamundoe': 20, 'crbsandureara': 20,
                               'crbzeranacaba': 20,
                 'criciuma/sc': 21, 'criciuma': 21, 'criciumajoaoa': 21, 'criciumauzseo': 21,
                                    'criciumaozseo': 21,
                 'cruzeiro/mg': 22, 'cruzeiro': 22, 'cruzeiroaoa': 22,
                 'csa/al': 23, 'csa': 23, 'csarlandiasea': 23, 'csa brancorta': 23,
                                          'csatalezaesea': 23,
                 'desportiva/es': 24, 'desportiva': 24, 'desportivae': 24,
                 'figueirense/sc': 25, 'figueirense': 25, 'figueirenseno': 25, 'figueirensema': 25,
                 'flamengo/rj': 26, 'flamengo': 26,
                 'fluminense/rj': 27, 'fluminense': 27, 'fluminenseira': 27, 'fluminensesea': 27,
                                      'fluminenseaba': 27, 'fluminenseama': 27, 'fluminenseseo': 27,
                 'fortaleza/ce': 28, 'fortaleza': 28, 'fortalezaoa': 28, 'fortalezaze': 28,
                                     'fortalezaesea': 28,
                 'gama/df': 29, 'gama': 29, 'gama correara': 29,
                 'goias/go': 30, 'goias': 30, 'goiasoussoa': 30,
                 'gremio/rs': 31, 'gremio': 31, 'gremioussoa': 31, 'gremiogaese': 31,
                                  'gremioda gama': 31,
                 'guarani/sp': 32, 'guarani': 32, 'guaraninsesea': 32,
                 'inter de limeira/sp': 33, 'inter de limeira': 33, 'inter limeira/sp': 33,
                                            'inter limeira': 33,
                 'internacional/rs': 34, 'internacional': 34,
                 'ipatinga/mg': 35, 'ipatinga': 35, 'ipatingasoa': 35, 'ipatingaese': 35,
                 'ituano/sp': 36, 'ituano': 36,
                 'ji-parana/ro': 37, 'ji-parana': 37, 'ji-paranacaba': 37,
                 'joinville/sc': 38, 'joinville': 38, 'joinvillese': 38, 'joinvilleorta': 38,
                 'juventude/rs': 39, 'juventude': 39, 'juventudese': 39, 'juventudeseno': 39,
                 'juventus/sp': 40, 'juventus': 40, 'juventuse': 40, 'juventussoa': 40,
                                    'juventusjoaoa': 40,
                 'londrina/pr': 41, 'londrina': 41,
                 'marilia/sp': 42, 'marilia': 42, 'mariliareta': 42, 'marilianseama': 42,
                 'mixto/mt': 43, 'mixto': 43, 'mixtoranco': 43, 'mixto da gama': 43,
                 'moto clube/ma': 44, 'moto clube': 44,
                 'nautico/pe': 45, 'nautico': 45, 'nauticodia': 45,
                 'nacional/am': 46, 'nacional': 46, 'nacionalntino': 46, 'nacionalnseba': 46,
                 'olaria/rj': 47, 'olaria': 47, 'olariapreta': 47, 'olariapretano': 47,
                 'operario/ms': 48, 'operario': 48,
                 'palmas/to': 49, 'palmas': 49, 'palmasrense': 49, 'palmasudese': 49,
                                  'palmasalnseba': 49, 'palmasda gama': 49,
                 'palmeiras/sp': 50, 'palmeiras': 50, 'palmeirasoa': 50, 'palmeiraseseo': 50,
                 'parana/pr': 51, 'parana': 51, 'paranaensesea': 51,
                 'paulista/sp': 52, 'paulista': 52,
                 'paysandu/pa': 53, 'paysandu': 53, 'paysandueta': 53, 'paysandureara': 53,
                                    'paysanduaesea': 53, 'paysandujoaoa': 53, 'paysanduntino': 53,
                                    'paysanduozseo': 53,
                 'ponte preta/sp': 54, 'ponte preta': 54, 'ponte pretano': 54, 'ponte pretaeo': 54,
                 'portuguesa/sp': 55, 'portuguesa': 55, 'p. desportos/sp': 55, 'port desporta': 55,
                                      'port desport': 55,
                 'remo/pa': 56, 'remo': 56, 'remoimundoa': 56, 'remoipeoaoa': 56, 'remoasudese': 56,
                                'remoiapreta': 56, 'remobrancoara': 56, 'remoeirenseno': 56,
                 'rio branco/ac': 57, 'rio branco': 57, 'rio brancoino': 57, 'rio brancoaba': 57,
                 'rio branco/es': 58, 'rio brancoara': 58, 'rio brancorta': 58,
                 'river/pi': 59, 'river': 59, 'rivernenseira': 59, 'riverbarensea': 59,
                                 'river pretaeo': 59,
                 'roraima/rr': 60, 'roraima': 60, 'roraimalntino': 60, 'roraimaaseseo': 60,
                 'sao caetano/sp': 61, 'sao caetano': 61,
                 'sao paulo/sp': 62, 'sao paulo': 62, 's. paulo/sp': 62,
                 'sao raimundo/am': 63, 'sao raimundo': 63, 's raimundoa': 63, 's raimundoe': 63,
                                        's raimundoama': 63, 's raimundo': 63,
                 'sampaio correa/ma': 64, 'sampaio correa': 64, 'samp correara': 64,
                                          'samp correa': 64,
                 'santa cruz/pe': 65, 'santa cruz': 65, 'santa cruze': 65, 'santa cruzseo': 65,
                 'santo andre/sp': 66, 'santo andre': 66, 'santo andreba': 66,
                 'santos/sp': 67, 'santos': 67, 'santosudese': 67,
                 'sergipe/se': 68, 'sergipe': 68, 'sergipeoaoa': 68, 'sergipecicaba': 68,
                                   'sergiperuzseo': 68,
                 'sport/pe': 69, 'sport': 69, 'sporticoeta': 69,
                 'treze/pb': 70, 'treze': 70, 'trezeranacaba': 70, 'trezeperuzseo': 70,
                 'tuna luso/pa': 71, 'tuna luso': 71,
                 'uberlandia/mg': 72, 'uberlandia': 72, 'uberlandiaara': 72, 'uberlandiasea': 72,
                                      'uberlandiaseo': 72,
                 'uniao barbarense/sp': 73, 'uniao barbarense': 73, 'u barbarense': 73,
                                            'u barbarensea': 73, 'u barbarenseo': 73,
                 'uniao sao joao/sp': 74, 'uniao sao joao': 74, 'uniao s.joao/sp': 74,
                                          'uniao s joaoa': 74, 'uniao s joao': 74,
                 'vasco da gama/rj': 75, 'vasco da gama': 75,
                 'vila nova/go': 76, 'vila nova': 76, 'vila novaorta': 76, 'vila novaseno': 76,
                 'villa nova/mg': 77, 'villa nova': 77, 'vila nova/mg': 77,
                 'vitoria/ba': 78, 'vitoria': 78, 'vitoriaujoaoa': 78,
                 'xv de piracicaba/sp': 79, 'xv de piracicaba': 79, 'xv piracicaba/sp': 79,
                                            'xv piracicaba': 79,
                 'ypiranga/ap': 80, 'ypiranga': 80}

# ----------------------------------------------------------------------------
