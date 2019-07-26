import json

class RPCProtocol():

    @classmethod
    def parse_requset(cls, data):
        pass

    @classmethod
    def parse_reply(cls, data):
        pass

    @classmethod
    def create_request(cls, method, dict_params):
        assert type(dict_params) == dict

        return json.dumps({"method":method,
                           "params": dict_params})

    @classmethod
    def create_reply(cls, code, msg, data):
        return json.dumps({"code":code,
                          "msg": msg,
                          "data": data})


# class RpcRequest():
    # __slots__ = ("method", "params", "serialize")

    # def __init__(self, method, params):
        # self.method = method
        # self.params = params

    # def serialize(self):
        # return json.dumps({"method":self.method,
                           # "params":self.params})

