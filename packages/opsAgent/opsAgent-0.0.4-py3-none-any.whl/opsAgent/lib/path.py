import os

from opsAgent.config import settings

from opsAgent.lib.vars import GlobalVars


def log_file_path():
    """
    :return: 返回日志文件路径
    """
    var = GlobalVars()
    if var.__dict__.get("LOG_PATH", None):  # 优先使用配置文件中的日志路径
        path = var.__dict__.get("LOG_PATH")
    else:
        path = settings.LOG_PATH

    if not os.path.exists(path):
        os.makedirs(path)
    return path
