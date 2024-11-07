#!/usr/bin/env python3
from collections import Counter

def make_stat(filename):
    """
    Функция вычисляет статистику по именам за каждый год с учётом пола.
    """
    stat = {}
    with open(filename, 'r') as f:
        lines = f.readlines()
    year = None
    for line in lines:
        line = line.strip()
        if '<h3>' in line and '</h3>' in line:
            st= line.find('<h3>') + 4
            end = line.find('</h3>', st)
            year = line[st:end]
            if year not in stat:
                stat[year] = {'M': {}, 'F': {}}
        elif '<a href="' in line and '</a>' in line:
            if year is None:
                continue
            st = line.find('<a href="')
            start_name = line.find('>', st) + 1
            end_name = line.find('</a>', start_name)
            full_name = line[start_name:end_name]
            razdel = full_name.strip().split(' ')
            if len(razdel) == 2:
                sname, name = razdel
                gender = determine_gender(name)
                if name in stat[year][gender]:
                    stat[year][gender][name] += 1
                else:
                    stat[year][gender][name] = 1
    print(stat)
    return stat


def determine_gender(name):
    if name.endswith('а') or name.endswith('я') or name == "Любовь":
        return 'F'
    else:
        return 'M'


def extract_years(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список годов,
    упорядоченный по возрастанию.
    """
    return sorted(int(year) for year in stat.keys())


def extract_general(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для всех имён.
    Список должен быть отсортирован по убыванию количества.
    """
    sp = []
    for year in stat.keys():
        sp.append(Counter(stat[year]['F']))



def extract_general_male(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён мальчиков.
    Список должен быть отсортирован по убыванию количества.
    """
    pass


def extract_general_female(stat):
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён девочек.
    Список должен быть отсортирован по убыванию количества.
    """
    pass


def extract_year(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    pass


def extract_year_male(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён мальчиков в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    pass


def extract_year_female(stat, year):
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён девочек в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    pass


extract_years(make_stat("CS _ home.html"))
