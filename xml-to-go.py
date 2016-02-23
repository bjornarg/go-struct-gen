#!/usr/bin/env python3

from naming import name_to_go
from structures import (Primitive, String, Int, Float, Boolean, List, Struct)
import xml.etree.ElementTree as ET

from utils import replace_reference, remove_equal, remove_similar, rename_duplicates

def print_xml(struct):
    string = "type {} struct {{\n".format(struct.name)
    for name, attribute in struct.attributes.items():
        string += "\t{} {} `xml:\"{},attrib\"`\n".format(name_to_go(name), attribute, name)
    for name, field in struct.fields.items():
        string += "\t{} {} `xml:\"{}\"`\n".format(name_to_go(name), field, name)
    string += "}"
    return string

def parse_xml(fn):
    tree = ET.parse(fn)
    return tree.getroot()

def build_structure(elem, structures):
    fields = {}
    attributes = {}
    for key, value in elem.attrib.items():
        attributes[key] = String()
    for child in elem:
        if len(child.attrib) == 0 and len(child) == 0:
            fields[child.tag] = String()
        else:
            fields[child.tag] = build_structure(child, structures)
    struct = Struct(elem.tag, fields, attributes)
    structures.append(struct)
    return struct

def create_structures(fn):
    root = parse_xml(fn)
    structures = []
    build_structure(root, structures)
    return structures

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Source file to create structures from")
    parser.add_argument("--merge-similar", help="Merge similar structures, not just equal", action="store_true")
    args = parser.parse_args()

    structures = create_structures(args.source)
    if args.merge_similar:
        structures = remove_similar(structures)
    else:
        structures = remove_equal(structures)
    structures = rename_duplicates(structures)
    for struct in structures:
        print(print_xml(struct))
