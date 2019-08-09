class JMQTTError(Exception):
    def __init__(self, err=""):
        super(JMQTTError, self).__init__(self, err)

class JStateError(JMQTTError):
    """"""

class JTimeoutError(JMQTTError):
    """"""
