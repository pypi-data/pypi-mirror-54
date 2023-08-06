import os

RESOURCE_DIR = ".bento"
CONFIG_PATH = ".bento.yml"
LOCAL_RUN_CACHE = f"{RESOURCE_DIR}/cache"

GLOBAL_CONFIG_DIR = os.path.expanduser("~/.bento")
GLOBAL_CONFIG_PATH = os.path.join(GLOBAL_CONFIG_DIR, "config.yml")

DEFAULT_LOG_PATH = os.path.join(GLOBAL_CONFIG_DIR, "last.log")

BASELINE_FILE_PATH = ".bento-whitelist.yml"

TERMS_OF_SERVICE_KEY = "terms_of_service"
TERMS_OF_SERVICE_VERSION = "0.0.1"

BENTO_TEMPLATE_HASH = "3a04e0f0cd9243d20b1e33da7ac13115"
