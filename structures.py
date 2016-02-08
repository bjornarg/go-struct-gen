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

class Struct:
    def __init__(self, name, fields=None):
        self.name = name_to_go(name)
        self.fields = fields or {}

    def __str__(self):
        return self.name

    def __eq__(self, other):
        try:
            if self.name != other.name:
                return False
        except AttributeError:
            return False
        return self.equal_fields(other)

    def equal_fields(self, other):
        for name, field in self.fields.items():
            try:
                if not type(other.fields[name]) is type(field):
                    return False
            except (AttributeError, KeyError):
                return False
        return True
