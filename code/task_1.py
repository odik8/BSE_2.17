#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import argparse
import os.path 

from jsonschema import ValidationError, validate


def add_person(
        contact_list: list,
        name: str,
        lastname: str,
        phone: str,
        bitrhdate: str,
    ):
    """
    Add a new person
    """

    contact_list.append(
        {
            "name": name,
            "lastname": lastname,
            "phone": phone,
            "bitrhdate": bitrhdate,
        }
    )

def display_contact_list(contact_list: list):
    """
    Displays contact list
    """

    if contact_list:
        line = '+-{}-+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 20,
            '-' * 20,
            '-' * 20,
            '-' * 10,
        )
        print(line)
        print(
            '| {:^4} | {:^20} | {:^20} | {:^20} | {:^10} |'.format(
                "№",
                "Name",
                "Lastname",
                "Phone numbers",
                "Birth date",
            )
        )
        print(line)
    
        for idx, person in enumerate(contact_list, 1):
            print(
                '| {:^4} | {:>20} | {:>20} | {:>20} | {:>10} |'.format(
                    idx,
                    person.get('name', ''),
                    person.get('lastname', ''),
                    person.get('phone', ''),
                    person.get('bitrhdate', ''),
                )
            )
            print(line)
    else:
        print("Contact list is empty.")
        
def select_person(contact_list: list, phone: str):
    """
    Displays person by phone numbers
    """

    selected_person = ''
    for person in contact_list:
        if person.get('phone') == phone:
            selected_person = person
    
    print(selected_person)
    

def save_contact_list(file_name, contact_list):
    """
    Save contact list into JSON file.
    """
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(contact_list, fout, ensure_ascii=False, indent=4)
    print("Data successfully saved to file", file_name)


def load_contact_list_json(file_name):
    """
    Load contact list from json
    """
    with open(file_name, "r", encoding="utf-8") as f:
        document = json.load(f)

    if all(list(map(lambda x: check_validation_json(x), document))):
        return document
    else:
        None


def check_validation_json(file_name):
    with open("schema.json") as fs:
        schema = json.load(fs)

    try:
        validate(instance=file_name, schema=schema)
        return True
    except ValidationError:
        return False


def main():
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        help="The data file name"
    )

    parser = argparse.ArgumentParser("Contact list")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    subparsers = parser.add_subparsers(dest="command")

    # Subparser for adding a new person
    add = subparsers.add_parser(
        'add',
        parents=[file_parser],
        help='Add a new worker',
    )

    add.add_argument(
        "-n",
        "--name",
        required=True,
        help="The person's name"
    )

    add.add_argument(
        "-ln",
        "--lastname",
        required=True,
        help="The person's lastname"
    )

    add.add_argument(
        "-ph",
        "--phone",
        required=True,
        help="The person's phone numbers"
    )

    add.add_argument(
        "-bd",
        "--birthdate",
        required=True,
        help="The person's birth date"
    )

    # Subparer for displaying contact list
    display = subparsers.add_parser(
        'display',
        parents=[file_parser],
        help="Display contact list"
    )

    # Subparser for selecting a person
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Selet a person by phone numbers"
    )

    select.add_argument(
        "-p",
        "--phone",
        required=True,
        help="The required phone numbers"
    )

    # Parse command line arguments
    args = parser.parse_args()

    # Load contact lisy from a file if the file exists.
    is_dirty = False

    if os.path.exists(args.filename):
        contact_list = load_contact_list_json(args.filename)
    else:
        contact_list = []

    match args.command:
        case "add":
            add_person(
                contact_list,
                args.name,
                args.lastname,
                args.phone,
                args.birthdate,
            )
            is_dirty = True

        case "display":
            display_contact_list(contact_list)

        case "select":
            select_person(contact_list, args.phone)
        
    if is_dirty:
        save_contact_list(args.filename, contact_list)

if __name__ == "__main__":
    main()