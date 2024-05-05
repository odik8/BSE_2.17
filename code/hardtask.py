#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os.path

import click
from jsonschema import ValidationError, validate


def add_person(
    contact_list,
    name: str,
    lastname: str,
    phone: str,
    birthdate: str,
):
    """
    Add a new person
    """

    contact_list.append(
        {
            "name": name,
            "lastname": lastname,
            "phone": phone,
            "birthdate": birthdate,
        }
    )


def display_contact_list(contact_list):
    """
    Displays contact list
    """

    if contact_list:
        line = "+-{}-+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4,
            "-" * 20,
            "-" * 20,
            "-" * 20,
            "-" * 10,
        )
        print(line)
        print(
            "| {:^4} | {:^20} | {:^20} | {:^20} | {:^10} |".format(
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
                "| {:^4} | {:>20} | {:>20} | {:>20} | {:>10} |".format(
                    idx,
                    person.get("name", ""),
                    person.get("lastname", ""),
                    person.get("phone", ""),
                    person.get("birthdate", ""),
                )
            )
            print(line)
    else:
        print("Contact list is empty.")


def select_person(contact_list, phone: str):
    """
    Displays person by phone numbers
    """

    selected_person = ""
    for person in contact_list:
        if person.get("phone") == phone:
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
        print("Invalid data in the JSON file.")
        print(document)  # Добавим эту строку для отладочной информации
        return None


def check_validation_json(file_name):
    with open("schema.json") as fs:
        schema = json.load(fs)

        try:
            validate(instance=file_name, schema=schema)
            return True
        except ValidationError:
            return False


@click.group()
def cli():
    pass


@cli.command()
@click.argument("filename")
@click.option("-n", "--name", required=True, help="The person's name")
@click.option("-ln", "--lastname", required=True, help="The person's lastname")
@click.option(
    "-ph", "--phone", required=True, help="The person's phone numbers"
)
@click.option(
    "-bd", "--birthdate", required=True, help="The person's birth date"
)
def add(filename, name, lastname, phone, birthdate):
    """
    Add a new person
    """
    if os.path.exists(filename):
        contact_list = load_contact_list_json(filename)
        contact_list.append(
            add_person(contact_list, name, lastname, phone, birthdate)
        )
        save_contact_list(filename, contact_list)
        click.echo(f"{name} {lastname} added")
    else:
        click.echo("Invalid path entered.")


@cli.command()
@click.argument("filename")
def display(filename):
    """
    Displays contact list
    """
    if os.path.exists(filename):
        contact_list = load_contact_list_json(filename)
        display_contact_list(contact_list)
    else:
        click.echo("Invalid path entered.")


@cli.command()
@click.argument("filename")
@click.option("-p", "--phone", required=True)
def select(filename, phone):
    """
    Selet a person by phone numbers
    """
    if os.path.exists(filename):
        contact_list = load_contact_list_json(filename)
        select_person(contact_list, phone)
    else:
        click.echo("PathError: Invalid path entered.")


if __name__ == "__main__":
    cli()
