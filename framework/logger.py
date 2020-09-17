import logging

logging.basicConfig(
    filename="logfile",
    filemode='w',
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO)
appLogger = logging
