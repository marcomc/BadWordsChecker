import logging
import sys
from json_log_formatter import JSONFormatter
import io

class TqdmToLogger(io.StringIO):
    """
    Output stream for TQDM which will output to a logger.
    """
    logger = None
    level = None
    buf = ''
    def __init__(self, logger, level=None):
        super(TqdmToLogger, self).__init__()
        self.logger = logger
        self.level = level or logging.INFO
    def write(self, buf):
        self.buf = buf.strip('\r\n\t ')
    def flush(self):
        self.logger.log(self.level, self.buf)

def setup_logging(verbose: bool = False, log_format: str = "text"):
    level = logging.DEBUG if verbose else logging.INFO
    
    if log_format == "json":
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    # Remove existing handlers to avoid duplicate logs
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
    root_logger.addHandler(handler)
