import json


class RPCProtocol():

    @classmethod
    def parse_requset(cls, msg):
        return RPCRequest.parse(msg)

    @classmethod
    def parse_reply(cls, msg):
        return RPCReply.parse(msg)

    @classmethod
    def create_request(cls, func, dict_params):
        assert type(dict_params) == dict

        return json.dumps({"func": func,
                           "params": dict_params})

    @classmethod
    def create_reply(cls, code, msg="", data=""):
        return json.dumps({"code": code,
                           "msg": msg,
                           "data": data})


class RPCRequest():
    __slots__ = ("func", "params", "topic", "pid")

    def __init__(self, func, params, pid, topic=""):
        self.func = func
        self.params = params
        self.pid = pid
        self.topic = topic

    @classmethod
    def parse(cls, msg):
        _, _, _, version, service, device_id, func, pid = msg.topic.split("/")
        payload = json.loads(msg.payload)
        return RPCRequest(payload["func"], payload["params"],
                          pid, msg.topic)

    # def serialize(self):
        # return json.dumps({"func": self.func,
                           # "params": self.params})


class RPCReply():
    __slots__ = ("pid", "code", "data", "msg", "pid","source")

    def __init__(self, code=0, msg="", data="", source="", pid=None):
        self.pid = pid
        self.code = code
        self.msg = msg
        self.data = data
        self.source = source

    @classmethod
    def parse(cls, msg):
        _, _, _, version, service, device_id, func, pid, _ = msg.topic.split("/")
        payload = json.loads(msg.payload)
        return RPCReply(
                        payload["code"],
                        payload.get("msg",""),
                        payload.get("data", ""),
                        msg.topic,
                        pid
                        )

    # def serialize(self):
        # return json.dumps({"code": self.code,
                          # "data": self.data,
                          # "msg": self.msg})


