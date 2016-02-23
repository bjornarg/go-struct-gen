from naming import name_to_go

class Primitive:
    pass

class String(Primitive):
    def __str__(self):
        return "string"

class Int(Primitive):
    def __str__(self):
        return "int"

class Float(Primitive):
    def __str__(self):
        return "float64"

class Boolean(Primitive):
    def __str__(self):
        return "bool"

class List:
    def __init__(self, element):
        self.element = element

    def __str__(self):
        return "[]{}".format(self.element)

def dict_equal(d1, d2):
    k1 = set(d1.keys())
    k2 = set(d2.keys())
    if k1 != k2:
        return False
    for key in k1:
        if type(d1[key]) is not type(d2[key]):
            return False
    return True

def dict_similar(d1, d2):
    k1 = set(d1.keys())
    k2 = set(d2.keys())
    if not k1.issubset(k2) and not k2.issubset(k1):
        return False
    intersect = k1 & k2
    for key in intersect:
        if type(d1[key]) is not type(d2[key]):
            return False
    return True

class Struct:
    def __init__(self, name, fields=None, attributes=None):
        self.name = name_to_go(name)
        self.fields = fields or {}
        self.attributes = attributes or {}

    def __str__(self):
        return self.name

    def __eq__(self, other):
        try:
            if self.name != other.name:
                return False
        except AttributeError:
            return False
        return self.equal_fields(other)

    def similar(self, other):
        try:
            if self.name != other.name:
                return False
        except AttributeError:
            return False
        return self.similar_fields(other)

    def _compare_fields(self, other, comparator):
        try:
            if not comparator(self.fields, other.fields):
                return False
        except AttributeError:
            return False
        try:
            if not comparator(self.attributes, other.attributes):
                return False
        except AttributeError:
            return False
        return True

    def equal_fields(self, other):
        return self._compare_fields(other, dict_equal)

    def similar_fields(self, other):
        return self._compare_fields(other, dict_similar)

    def merge(self, other):
        new_fields = set(other.fields.keys()) - set(self.fields.keys())
        for key in new_fields:
            self.fields[key] = other.fields[key]

        new_attributes = set(other.attributes.keys()) - set(self.attributes.keys())
        for key in new_attributes:
            self.attributes[key] = other.attributes[key]
