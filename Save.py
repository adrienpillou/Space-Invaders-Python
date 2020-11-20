import json
from os import path

class Save():
    def __init__(self, file_name):
        self.content = dict()
        self.file_name = file_name
        self.extension = ".json"
        self.default_object = dict()
        pass

    def load(self):
        if not path.exists(self.file_name):
            self.save(self.default_object)
        else:
            self.content = json.load(open(self.file_name))

    def save(self, object):
        json_data = json.dumps(object)
        f = open(self.file_name, "w")
        f.write(json_data)
        f.close()
        self.content = object
        
    def set_file_name(self, file_name:str):
        self.file_name = file_name

    def set_default_object(self, default_object):
        self.default_object = default_object

    def get_value(self, key:str):
        if not key in self.content:
            return
        return self.content[key]
    
    def set_value(self, key:str, value):
        if key in self.content:
            self.content[key] = value
        
    def get_int_value(self, key:str):
        value = self.get_value(key)
        if value is None:
            return 0
        return int(value)

