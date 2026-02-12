import logging

class Log:
    def initalize():
        logger = logging.getLogger("mylogger")
        logger.setLevel(logging.DEBUG)

        # Konsole
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Datei
        fh = logging.FileHandler("app.log")
        fh.setLevel(logging.DEBUG)

        # Format
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

        logger.info("Info in Konsole und Datei")
