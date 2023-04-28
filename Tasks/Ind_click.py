#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import os.path
import click


@click.group()
def main():
    pass


@main.command('add')
@click.argument('filename')
@click.option('--name',  help="The human's name")
@click.option('--number',  type=int, help="The human's number")
@click.option('--bday', help="Birthday of a person")
def add_person(filename, name, number, bday):
    """
    Запросить данные о человеке.
    """
    if os.path.exists(filename):
        people = load_people(filename)
    else:
        people = []

    b_day = list(map(int, bday.split(".")))
    date_bday = datetime.date(b_day[2], b_day[1], b_day[0])
    people.append(
        {
            "name": name,
            "number": number,
            "birthday": date_bday
        }
    )
    save_people(filename, people)
    click.secho("Данные добавлены")


@main.command("display")
@click.argument('filename')
def display_cli(filename):
    if os.path.exists(filename):
        people = load_people(filename)
    else:
        people = []
    display_people(people)


@main.command("find")
@click.argument('filename')
@click.option('--nomer', help="The human's name")
def find_nomer(filename, nomer):
    """
    Выбрать работников с заданным стажем.
    """
    people = load_people(filename)
    # Сформировать список людей.
    result = []
    for n in people:
        if nomer in str(n.values()):
            result.append(n)

    # Проверка на наличие записей
    if len(result) == 0:
        return print("Запись не найдена")

    # Возвратить список выбранных работников.
    display_people(result)


def display_people(staff):
    """
    Отобразить список работников.
    """
    # Проверить, что список работников не пуст.
    if staff:
        # Заголовок таблицы.
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4,
            "-" * 30,
            "-" * 15,
            "-" * 15
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^15} | {:^15} |".format(
                "№",
                "Фамилия и имя",
                "Телефон",
                "День рождения"
            )
        )
        print(line)

        # Вывести данные о всех сотрудниках.
        for idx, human in enumerate(staff, 1):
            print(
                f"| {idx:>4} |"
                f' {human.get("name", ""):<30} |'
                f' {human.get("number", 0):<15} |'
                f' {human.get("birthday")}      |'
            )
            print(line)

    else:
        print("Список пуст.")


def json_deserial(obj):
    """
    Деериализация объектов datetime
    """
    for i in obj:
        if isinstance(i["birthday"], str):
            i["birthday"] = datetime.datetime.strptime(i["birthday"], '%Y-%m-%d').date()


def json_serial(obj):
    """
    Сериализация объектов datetime
    """
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()


def load_people(file_name):
    """
    Загрузить всех работников из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def save_people(file_name, staff):
    """
    Сохранить всех работников в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4, default=json_serial)


if __name__ == "__main__":
    main()
