import json


class JSONResponse():

    def __init__(self):
        self.data = {}
        self.meta = {}
        self.errors = {}

    def send(self):
        response = {}
        if self.data:
            response["data"] = self.data
        if self.errors:
            response["errors"] = self.errors
        if self.meta:
            response["meta"] = self.meta
        return response

    def addData(self, field, parameter):
        if field in self.data.keys():
            return False
        else:
            self.data[field] = parameter
            return self

    def addError(self, id, description):
        if id in self.errors.keys():
            return False
        else:
            self.errors[id] = description
            return self

    def addMeta(self, field, parameter):
        if field in self.meta.keys():
            return False
        else:
            self.meta[field] = parameter
            return self