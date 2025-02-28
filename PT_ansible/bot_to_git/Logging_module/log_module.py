import logging

# Логирование будет происходить путем передачи переменной logger различным обработчикам
log_file_name = './Logging_module/usage_report.log'
def get_logger():
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    log.addHandler(ch)
    fh = logging.FileHandler(log_file_name, encoding='utf-8')
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    log.addHandler(fh)
    return log

logger = get_logger()
