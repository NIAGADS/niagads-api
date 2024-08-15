""" field storing arbitrary dictionary item 
see https://github.com/python-restx/flask-restx/issues/115
"""
from marshmallow import fields
from werkzeug.exceptions import BadRequest

class DictItem(fields.Raw):
    def output(self, key, obj, *args, **kwargs):
        try:
            dct = getattr(obj, self.attribute)
        except AttributeError:
            return None # return {}
        return dct or None