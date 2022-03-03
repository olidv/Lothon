"""
   Package lothon.conf
   Module  appconfig.py

   Carga das configuracoes da aplicacao a partir de arquivo INI.
"""

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
from dataclasses import dataclass
from configparser import ConfigParser


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
    RT_dat_path: str = ''
    RT_bet_path: str = ''
    RT_log_path: str = ''
    RT_tmp_path: str = ''

    RT_files_htm_mask: str = ''
    RT_files_csv_mask: str = ''
    RT_files_log_mask: str = ''
    RT_files_all_mask: str = ''

    # Parametrizacao das loterias da Caixa EF:
    LC_loterias_caixa: list[tuple[str, ...]] = None
    LC_loteria_htm_name: str = ''
    LC_table_class_find: str = ''

    # Parametrizacao para geracao de boloes de apostas:
    BA_bolao_csv_name: str = ''

    # .
    def load_properties(self, parser: ConfigParser) -> None:
        # nao faz nada se nao forneceu o parser...
        if parser is None:
            return

        # com o parser, carrega o arquivo INI nos parametros da dataclass:
        self.RT_app_home = parser.get("ROOT", "app_home")
        self.RT_dat_path = parser.get("ROOT", "dat_path")
        self.RT_bet_path = parser.get("ROOT", "bet_path")
        self.RT_log_path = parser.get("ROOT", "log_path")
        self.RT_tmp_path = parser.get("ROOT", "tmp_path")

        self.RT_files_htm_mask = parser.get("ROOT", "files_htm_mask")
        self.RT_files_csv_mask = parser.get("ROOT", "files_csv_mask")
        self.RT_files_log_mask = parser.get("ROOT", "files_log_mask")
        self.RT_files_all_mask = parser.get("ROOT", "files_all_mask")

        # Parametrizacao das loterias da Caixa EF:
        self.LC_loteria_htm_name = parser.get("LOTERIA_CAIXA", "loteria_htm_name")
        self.LC_table_class_find = parser.get("LOTERIA_CAIXA", "table_class_find")

        loterias = parser.get("LOTERIA_CAIXA", "loterias_caixa").split(',')
        self.LC_loterias_caixa = [tuple(jogo.strip().split(';')) for jogo in loterias]

        # Parametrizacao para geracao de boloes de apostas:
        self.BA_bolao_csv_name = parser.get("BOLAO_APOSTA", "bolao_csv_name")

# ----------------------------------------------------------------------------
