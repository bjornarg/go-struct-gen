import re

def name_parts(name):
    return re.sub("([A-Z_]+)", r" \1", name).split()

def name_to_go(name):
    parts = name_parts(name)
    name = "".join(part.title() for part in parts)
    return name

def find_common_part(names):
    """Finds the largest common part of all names in names.

    If no part is found, returns None.
    """
    common = []
    parts = []
    for name in names:
        parts.append(name_parts(name))
    if len(parts) <= 0:
        return None
    for part in parts[0]:
        if all(part in p for p in parts[1:]):
            return part

    return None
