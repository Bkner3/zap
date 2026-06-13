from src.zap_path import PathManager

log_file = PathManager.get("log_file")
_config = None

def write_log(message, level="INFO"):
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"[{level}] {message}\n")

def log_info(message):
    write_log(message, "INFO")

def log_warning(message):
    write_log(message, "WARNING")

def log_error(message):
    write_log(message, "ERROR")

def log_debug(message):
    global _config
    from src.core.config import read_config

    if _config is None:
        _config = read_config()

    if not _config.get("is_on_debug", True):
        return

    write_log(message, "DEBUG")
        