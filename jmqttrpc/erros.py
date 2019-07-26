
class StateError(Exception):
    def __init__(self, err):
        Exception.__init__(self, err)
