#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import sys
from random import randint
import json

def save_trains(trains, filename):
    """
    Сохраняет список поездов в файл в формате JSON.

    Args:
    - trains (list): Список поездов.
    - filename (str): Имя файла для сохранения.

    """
    with open(filename, 'w') as file:
        json.dump(trains, file)

def load_trains(filename):
    """
    Загружает список поездов из файла в формате JSON.

    Args:
    - filename (str): Имя файла для загрузки.

    Returns:
    - list: Список поездов.

    """
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def add_train(trains, train_num, destination, start_time):
    """
    Добавляет информацию о поезде в список trains.

    Args:
    - trains (list): Список поездов.
    - train_num (int): Номер поезда.
    - destination (str): Пункт назначения.
    - start_time (str): Время выезда.

    """
    trains.append({'num': train_num, 'destination': destination, 'start_time': start_time})
    if len(trains) > 1:
        trains.sort(key=lambda item: item['start_time'])

def list_trains(trains):
    """
    Выводит список поездов на экран.

    Args:
    - trains (list): Список поездов.

    """
    line = f'+-{"-" * 15}-+-{"-" * 30}-+-{"-" * 25}-+'
    print(line)
    header = f"| {'№ поезда':^15} | {'Пункт назначения':^30} | {'Время отъезда':^25} |"
    print(header)
    print(line)
    for train in trains:
        num = train.get('num', randint(1000, 10000))
        destination = train.get('destination', 'None')
        start_time = train.get('start_time', 'None')
        recording = f"| {num:^15} | {destination:^30} | {start_time:^25} |"
        print(recording)
    print(line)

def select_train(trains, cmd_destination):
    """
    Выводит информацию о поездах, направляющихся в указанный пункт.

    Args:
    - trains (list): Список поездов.
    - cmd_destination (str): Пункт назначения.

    """
    if select_trains := [
        train
        for train in trains
        if train['destination'].strip() == cmd_destination
    ]:
        for train in select_trains:
            print(f'{train["num"]:^15}: {train["start_time"]:^25}')
    else:
        print('Нет поездов едущих в данное место!', file=sys.stderr)

def show_help():
    """
    Выводит список доступных команд на экран.

    """
    print("Список команд:\n")
    print("add - добавить поезд;")
    print("list - вывести список поездов;")
    print("select <пункт назначения> - запросить поезда с пунктом назначения;")
    print("help - отобразить справку;")
    print("exit - завершить работу с программой.")

@click.command()
@click.option('--add', is_flag=True, help='Добавить поезд.')
@click.option('--list', 'list_trains', is_flag=True, help='Вывести список поездов.')
@click.option('--select', help='Запросить поезда с указанным пунктом назначения.')
def main(add, list_trains, select):
    filename = 'trains.json'
    trains = load_trains(filename)
    
    if add:
        train_num = int(input('Введите номер поезда: '))
        destination = input('Введите пункт назначения: ')
        start_time = input('Введите время выезда: ')
        add_train(trains, train_num, destination, start_time)
        save_trains(trains, filename)
    elif list_trains:
        list_trains(trains)
    elif select:
        select_train(trains, select)
    else:
        show_help()

if __name__ == '__main__':
    main()