"""
   Package lothon.conf
   Module  __init__.py

"""

__all__ = [
    'app_config'
]

# ----------------------------------------------------------------------------
# DEPENDENCIAS
# ----------------------------------------------------------------------------

# Built-in/Generic modules
# Libs/Frameworks modules
# Own/Project modules
from lothon.conf.appconfig import AppConfig


# ----------------------------------------------------------------------------
# VARIAVEIS
# ----------------------------------------------------------------------------

# instancia global para leitura das configuracoes da aplicacao:
app_config: AppConfig = AppConfig()  # apenas para utilizar o code-assist (type hint)...

# ----------------------------------------------------------------------------
