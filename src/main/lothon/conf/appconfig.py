"""
   Package infinite.conf
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
# CLASSE
# ----------------------------------------------------------------------------

@dataclass
class AppConfig:
    """
       Classe contendo toda a configuracao INI da aplicacao.
    """

    # Estrutura de diretorios da aplicacao:
    RT_app_home: str = ''
    RT_log_path: str = ''
    RT_www_path: str = ''
    RT_tmp_path: str = ''
    RT_clock_logs: str = ''

    RT_mt5_platform_home: str = ''
    RT_mt5_terminal_home: str = ''
    RT_mt5_platform_crashes: str = ''
    RT_mt5_terminal_commons: str = ''

    RT_mt5_instances_id: list[tuple] = None
    RT_mt5_terminal_logs: str = ''
    RT_mt5_terminal_mql5_files: str = ''
    RT_mt5_terminal_mql5_logs: str = ''

    RT_files_csv_mask: str = ''
    RT_files_log_mask: str = ''
    RT_files_zip_mask: str = ''
    RT_files_all_mask: str = ''

    # Parametrizacao do scheduler utilizado para o agendamento de jobs:
    SC_job_delay: int = 0
    SC_loop_on: bool = False
    SC_time_wait: int = 0

    # Parametrizacao do mercado da bolsa B3:
    B3_uri_site: str = ''
    B3_uri_port: int = 0
    B3_feriados_bolsa: list[tuple] = None

    # Parametrizacao do job para baixa da Carteira Teorica do IBovespa:
    CI_job_interval: int = 0
    CI_url_carteira_ibov: str = ''
    CI_xpath_a_click: str = ''
    CI_timeout_download: int = 0
    CI_ibov_csv_mask: str = ''
    CI_derivativos: list[str] = None
    CI_ibov_txt_name: str = ''
    CI_ctrl_file_mask: str = ''

    # Parametrizacao do job para baixa das Cotacoes IntraDay da B3:
    IB_job_interval: int = 0
    IB_url_cotacoes_intraday: str = ''
    IB_intraday_url_mask: str = ''
    IB_intraday_zip_mask: str = ''
    IB_ctrl_file_mask: str = ''

    # Parametrizacao do job para compactar arquivos CSV nos terminais MT5:
    ZM_job_interval: int = 0
    ZM_ctrl_file_mask: str = ''

    # Parametrizacao do job para copiar/mover arquivos para outra estacao:
    MI_job_interval: int = 0

    MI_shared_folder: str = ''
    MI_cia_terminal_logs: str = ''
    MI_cia_mql5_files: str = ''
    MI_cia_mql5_logs: str = ''

    MI_shared_mt5_crashes: str = ''
    MI_shared_app_www: str = ''
    MI_shared_app_logs: str = ''
    MI_ctrl_file_mask: str = ''

    # Parametrizacao do mercado de FOREX:
    FX_feriados_forex: list[tuple] = None

    # .
    def load_properties(self, parser: ConfigParser) -> None:
        # nao faz nada se nao forneceu o parser...
        if parser is None:
            return

        # com o parser, carrega o arquivo INI nos parametros da dataclass:
        self.RT_app_home = parser.get("ROOT", "app_home")
        self.RT_log_path = parser.get("ROOT", "log_path")
        self.RT_www_path = parser.get("ROOT", "www_path")
        self.RT_tmp_path = parser.get("ROOT", "tmp_path")
        self.RT_clock_logs = parser.get("ROOT", "clock_logs")

        self.RT_mt5_platform_home = parser.get("ROOT", "mt5_platform_home")
        self.RT_mt5_terminal_home = parser.get("ROOT", "mt5_terminal_home")
        self.RT_mt5_platform_crashes = parser.get("ROOT", "mt5_platform_crashes")
        self.RT_mt5_terminal_commons = parser.get("ROOT", "mt5_terminal_commons")

        instances = parser.get("ROOT", "mt5_instances_id").split(',')
        self.RT_mt5_instances_id = [tuple(i.strip().split(':')) for i in instances]
        self.RT_mt5_terminal_logs = parser.get("ROOT", "mt5_terminal_logs")
        self.RT_mt5_terminal_mql5_files = parser.get("ROOT", "mt5_terminal_mql5_files")
        self.RT_mt5_terminal_mql5_logs = parser.get("ROOT", "mt5_terminal_mql5_logs")

        self.RT_files_csv_mask = parser.get("ROOT", "files_csv_mask")
        self.RT_files_log_mask = parser.get("ROOT", "files_log_mask")
        self.RT_files_zip_mask = parser.get("ROOT", "files_zip_mask")
        self.RT_files_all_mask = parser.get("ROOT", "files_all_mask")

        # Parametrizacao do scheduler utilizado para o agendamento de jobs:
        self.SC_job_delay = parser.getint("SCHEDULER", "job_delay")
        self.SC_loop_on = parser.getboolean("SCHEDULER", "loop_on")
        self.SC_time_wait = parser.getint("SCHEDULER", "time_wait")

        self.B3_uri_site = parser.get("B3", "uri_site")
        self.B3_uri_port = parser.getint("B3", "uri_port")

        datas = parser.get("B3", "feriados_bolsa").split(',')
        self.B3_feriados_bolsa = [tuple(map(int, dia.split('/'))) for dia in datas]

        # Parametrizacao do job para baixa da Carteira Teorica do IBovespa:
        self.CI_job_interval = parser.getint("CARTEIRA_IBOVESPA", "job_interval")
        self.CI_url_carteira_ibov = parser.get("CARTEIRA_IBOVESPA", "url_carteira_ibov")
        self.CI_xpath_a_click = parser.get("CARTEIRA_IBOVESPA", "xpath_a_click")
        self.CI_timeout_download = parser.getint("CARTEIRA_IBOVESPA", "timeout_download")
        self.CI_ibov_csv_mask = parser.get("CARTEIRA_IBOVESPA", "ibov_csv_mask")
        self.CI_derivativos = parser.get("CARTEIRA_IBOVESPA", "derivativos").split(',')
        self.CI_ibov_txt_name = parser.get("CARTEIRA_IBOVESPA", "ibov_txt_name")
        self.CI_ctrl_file_mask = parser.get("CARTEIRA_IBOVESPA", "ctrl_file_mask")

        # Parametrizacao do job para baixa das Cotacoes IntraDay da B3:
        self.IB_job_interval = parser.getint("INTRADAY_B3", "job_interval")
        self.IB_url_cotacoes_intraday = parser.get("INTRADAY_B3",
                                                   "url_cotacoes_intraday")
        self.IB_intraday_url_mask = parser.get("INTRADAY_B3", "intraday_url_mask")
        self.IB_intraday_zip_mask = parser.get("INTRADAY_B3", "intraday_zip_mask")
        self.IB_ctrl_file_mask = parser.get("INTRADAY_B3", "ctrl_file_mask")

        # Parametrizacao do job para compactar arquivos CSV nos terminais MT5:
        self.ZM_job_interval = parser.getint("ZIP_MQL5", "job_interval")
        self.ZM_ctrl_file_mask = parser.get("ZIP_MQL5", "ctrl_file_mask")

        # Parametrizacao do job para copiar/mover arquivos para outra estacao:
        self.MI_job_interval = parser.getint("MOVE_INTRANET", "job_interval")

        self.MI_shared_folder = parser.get("MOVE_INTRANET", "shared_folder")
        self.MI_cia_terminal_logs = parser.get("MOVE_INTRANET", "cia_terminal_logs")
        self.MI_cia_mql5_files = parser.get("MOVE_INTRANET", "cia_mql5_files")
        self.MI_cia_mql5_logs = parser.get("MOVE_INTRANET", "cia_mql5_logs")

        self.MI_shared_mt5_crashes = parser.get("MOVE_INTRANET", "shared_mt5_crashes")
        self.MI_shared_app_www = parser.get("MOVE_INTRANET", "shared_app_www")
        self.MI_shared_app_logs = parser.get("MOVE_INTRANET", "shared_app_logs")
        self.MI_ctrl_file_mask = parser.get("MOVE_INTRANET", "ctrl_file_mask")

        # Parametrizacao do mercado de FOREX:
        datas = parser.get("FOREX", "feriados_forex").split(',')
        self.FX_feriados_forex = [tuple(map(int, dia.split('/'))) for dia in datas]

# ----------------------------------------------------------------------------
