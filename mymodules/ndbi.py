from google.appengine.ext import ndb
import cgi

class NDBIException(Exception):
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message

def make_ndb_condition(model, cond):
    if len(cond) == 0:
        raise NDBIException('condition is empty')

    cond_list = list(cond.iteritems())
    attr, value = cond_list[0]
    attribute = type(model).__getattribute__(model, attr)
    if len(cond) == 1:
        return ndb.AND(attribute == value)
    else:
        return ndb.AND(attribute == value,
                       make_ndb_condition(model, dict(cond_list[1:])))

def read_entities(model, max_count, cond):
    query = type(model).__getattribute__(model, 'query')
    condition = make_ndb_condition(model, cond)
    entities = list(query(condition).iter())
    return entities[:max_count]

def read_entity(model, cond):
    result = read_entities(model, 1, cond)
    if len(result) > 0:
        return result[0]
    else:
        raise NDBIException('Entity not found.')
