import json
from bubbles import user
from bubbles import snapshot


class Serializer:
    def __init__(self, data_type, config):
        self.data_type = data_type.lower()
        self.config = config
        self.driver = self.find_driver()

    def find_driver(self):
        if self.data_type == 'json':
            return JsonSerializer(self.config)
        
        raise TypeError('unknown serialization format')

    def serialize(self, user, snapshot):
        return self.driver.serialize(user, snapshot)

    def deserialize(self, data):
        return self.driver.deserialize()


class JsonSerializer:
    def __init__(self, config):
        self.config = config

    def serialize(self, user, snapshot):
        ret = user.dict()
        json.dumps(ret)
        ret['snapshot'] = snapshot.dict()
        return json.dumps(ret)

    def deserialize(self, data):
        json_obj = json.loads(data)
        return user.User(json_obj), snapshot.Snapshot(json_obj['snapshot'])