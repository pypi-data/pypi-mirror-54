import logging
import bunyan
from .MessageHandler import messageHandler

class customLogger():
    def __init__(self, loggerName="MESSAGE LOGGER", level="DEBUG", TOPIC = "", 
                BROKER = "", PORT = "", QoSLevel = 1):
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(level)
        handler = messageHandler(TOPIC=TOPIC, BROKER=BROKER, 
                    PORT=PORT, QoSLevel=QoSLevel)
        formatter = bunyan.BunyanFormatter()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)