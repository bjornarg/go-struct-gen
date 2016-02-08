#!/usr/bin/env python3

import sys
import json

from structures import (Primitive, String, Int, Float, Boolean, List, Struct)
from naming import name_to_go, find_common_part

def print_json(struct):
    string = "type {} struct {{\n".format(struct.name)
    for name, field in struct.fields.items():
        string += "\t{} {} `json:\"{}\"`\n".format(name_to_go(name), field, name)
    string += "}"
    return string

def type_to_cls(data):
    if isinstance(data, bool):
        return Boolean()
    elif isinstance(data, str):
        return String()
    elif isinstance(data, int):
        return Int()
    elif isinstance(data, float):
        return Float()
    else:
        raise TypeError("Do not know how to handle type: {}".format(type(data)))

def build_structure(data, structures, name):
    fields = {}
    for key, value in data.items():
        if isinstance(value, dict):
            field = build_structure(value, structures, name=key)
        elif isinstance(value, list):
            if len(value) > 0:
                field = List(get_structure(value[0], structures, name=key))
            else:
                print("List {} does not have values to indicate type".format(key), file=sys.stderr)
                continue
        else:
            field = type_to_cls(value)
        fields[key] = field
    struct = Struct(name, fields)
    structures.append(struct)
    return struct

def get_structure(data, structures, name=None):
    if isinstance(data, dict):
        return build_structure(data, structures, name)
    else:
        return type_to_cls(data)


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
        if not found:
            non_equal.append(s1)
    return non_equal

def create_structures(fn, root=None):
    with open(fn, "r") as fo:
        data = json.load(fo)

        structures = []
        build_structure(data, structures, name=root)
        return remove_equal(structures)

def combine_structures(structures):
    used = []
    new = []
    for struct in structures:
        if struct in used:
            continue
        equal = []
        for s2 in structures:
            if s2 is struct:
                continue
            if struct.equal_fields(s2):
                equal.append(s2)
        if len(equal) > 0:
            equal.append(struct)
            common = find_common_part(s.name for s in equal)
            if common is not None:
                s = Struct(common, struct.fields)
                new.append(s)
                used.extend(equal)
                for e in equal:
                    replace_reference(structures, e, s)
                continue
        new.append(struct)
    return new

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Source file to create structures from")
    parser.add_argument("-r", "--root", help="Root structure of file")
    parser.add_argument("-c", "--combine", help="Combine equal structures on shortest common name part (if exists)", action="store_true")
    args = parser.parse_args()
    structures = create_structures(args.source, args.root)
    if args.combine:
        structures = combine_structures(structures)
    for struct in structures:
        print(print_json(struct))
