def replace_reference(structs, old, new):
    for struct in structs:
        for key, value in struct.fields.items():
            if value is old:
                struct.fields[key] = new

def remove_equal(structures):
    non_equal = []
    for s1 in structures:
        found = False
        for s2 in non_equal:
            if s1 == s2:
                found = True
                replace_reference(structures, s1, s2)
                s2.merge(s1)
        if not found:
            non_equal.append(s1)
    return non_equal

def remove_similar(structures):
    non_equal = []
    for s1 in structures:
        found = False
        for s2 in non_equal:
            if s1.similar(s2):
                found = True
                replace_reference(structures, s1, s2)
                s2.merge(s1)
        if not found:
            non_equal.append(s1)
    return non_equal


def rename_duplicates(structures):
    """Renames any duplicated struct names by appending a number."""
    non_duplicates = []
    for s1 in structures:
        count = 1
        base = s1.name
        while s1.name in non_duplicates:
            count += 1
            s1.name = "{}{}".format(base, count)
        non_duplicates.append(s1.name)
    return structures
