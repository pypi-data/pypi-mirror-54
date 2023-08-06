import logging
import paho.mqtt as mqtt

class messageHandler(logging.Handler):
    def __init__(self, TOPIC = "", BROKER = "", 
                PORT = "", QoSLevel = 1):
        super(messageHandler, self).__init__()
        self.TOPIC = TOPIC
        self.BROKER = BROKER
        self.PORT = PORT
        self.QoSLevel = QoSLevel

    def emit(self, record):
        logEntry = self.format(record)
        logEntry = logEntry.replace(' ','')
        logEntry = logEntry.replace('\n', '')
        logEntry = logEntry.replace('\t','')
        client = mqtt.client.Client("MessageHandler")
        client.connect(self.BROKER, self.PORT, 60)
        return(client.publish(self.TOPIC, bytes(logEntry + '\0', 'utf-8'), self.QoSLevel))