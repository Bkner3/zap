from src.zap_path import PathManager

log_file = PathManager.get("log_file")
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
    from src.core.config import read_config
    config = read_config()
    if not config.get("is_on_debug", True):
        return
    write_log(message, "DEBUG")
        