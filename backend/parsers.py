# ------------------------------------------------------- Запуск Django в не самого проекта
import os, sys


proj = os.path.dirname(os.path.abspath('manage.py'))    # устанавливаем абсолютный путь

# тут мы добавляем путь в системные переменные путей
sys.path.append(proj)

os.environ['DJANGO_SETTINGS_MODULE'] = 'super_star.settings'
# for p in os.environ:
#     print(f'{p} - {os.environ[p]}')
import django

django.setup()
# ------------------------------------------------------- Запуск Django в не самого проекта

import json
import pandas as pd
import os
from pprint import pprint as pp
# from django.db import transaction
from employees.models import (
    Grade,
    Position,
    Team,
    Employee,
    Competence,
    Skill,
    TrainigRequest,
    PositionRequirement,
    Target,
    Level,
)



BATCH_SIZE = 100

# python parsers.py
file_path = 'tempr_data/test_data.xlsx'
# file_path = 'backend/tempr_data/test_data.xlsx'  # для дебагинга

with pd.ExcelFile(file_path, engine='openpyxl') as xls:
    columns_to_load = [
        "сотрудник",
        "должность",
        "команда",
        "bus_factor",
        "грейд",
        "создан",
        "навык",
        "компетенция_сокр",
        "домен",
        "дата",
        "оценка_",
        "оценка",
        "соответствие"
    ]

    df = pd.read_excel(xls, sheet_name=0, usecols=columns_to_load)
    # df_dict = pd.read_excel(xls, sheet_name=None)  # Получите словарь DataFrames для всех листов

    # Преобразуем столбцы в формат datetime, заменяя некорректные значения на NaT
    df['создан'] = pd.to_datetime(df['создан'], errors='coerce')
    df['дата'] = pd.to_datetime(df['дата'], errors='coerce')

    # Преобразуем в строку, обработав NaT
    # fillna('') заменяет NaT пустыми строками.
    df['создан'] = df['создан'].dt.strftime('%Y-%m-%d').fillna('')
    df['дата'] = df['дата'].dt.strftime('%Y-%m-%d').fillna('')

    positions_and_teams = {
        'positions': df['должность'].drop_duplicates().tolist(),
        'teams': df['команда'].drop_duplicates().tolist(),
    }
    # positions = [Position(name=name) for name in positions_and_teams['positions']]
    # teams = [Team(name=name) for name in positions_and_teams['teams']]
    # Position.objects.bulk_create(positions)
    # Team.objects.bulk_create(teams)
    # with open(f'../draft/positions_and_teams.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(positions_and_teams, json_file, indent=4, ensure_ascii=False)
    
    # ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    """
    "Базы данных": {
            "навыки": [
                "MS SQL Server",
                "MySQL",
                "Clickhouse"
            ],
            "тип": "Hard skills"
        },
    """
    # competence_dict = {}
    # for comp, group in df.groupby('компетенция_сокр'):
    #     # Получаем уникальные навыки
    #     skills = group['навык'].drop_duplicates().tolist()
    #     # Получаем тип (предполагаем, что все записи для одной компетенции имеют один тип)
    #     skill_type = group['домен'].iloc[0] if not group['домен'].empty else None
        
    #     # Добавляем в итоговый словарь
    #     competence_dict[comp] = {
    #         'навыки': skills,
    #         'тип': skill_type
    #     }
    # competences = [Competence(name=name, type=competence_dict[name]['тип']) for name in competence_dict]
    # Competence.objects.bulk_create(competences)
    # skills = [
    #     [
    #         Skill(name=sk, competence=Competence.objects.get(name=name)) 
    #      for sk in competence_dict[name]['навыки']
    #      ] 
    #      for name in competence_dict
    #      ]
    # skills_ls = []
    # for sk_ls in skills:
    #     skills_ls.extend(sk_ls)
    # Skill.objects.bulk_create(skills_ls)
    # with open(f'../draft/competence1.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(competence_dict, json_file, indent=4, ensure_ascii=False)
    # ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # ? =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # levels_dict = (
    #     df.groupby('сотрудник')
    #     .apply(lambda x: x[['навык', 'дата', 'оценка_', 'оценка', 'соответствие']]
    #         .to_dict('records'))
    #     .to_dict()
    # )
    # levels_dict = (
    #     df.groupby('сотрудник', group_keys=False)
    #     .apply(lambda x: x[['навык', 'дата', 'оценка_', 'оценка', 'соответствие']]
    #         .to_dict('records'))
    #     .to_dict()
    # )
    # ? =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    

    # ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # unique_employees = df.drop_duplicates(subset=['сотрудник'])
    # employee_list = unique_employees[['сотрудник', 'должность', 'bus_factor', 'грейд', 'создан']].to_dict(orient='records')
    # employees = [
    #     Employee(
    #         name=e['сотрудник'],
    #         position=Position.objects.get(name=e['должность']),
    #         bus_factor=e['bus_factor'],
    #         grade=Grade.objects.get(name=e['грейд']),
    #         created=e['создан'],
    #         )
    #         for e in employee_list
    #     ]
    # Employee.objects.bulk_create(employees)
    # with open(f'../draft/employee.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(employee_list, json_file, indent=4, ensure_ascii=False)
    # ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    # ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # employee_teams_dict = df.groupby('сотрудник')['команда'].apply(lambda x: list(set(x))).to_dict()
    # for emp in employee_teams_dict:
    #     employee = Employee.objects.get(name=emp)
    #     team = Team.objects.get(name=employee_teams_dict[emp][0])
    #     employee.team.add(team)

        # employee.team.add(*list(Team.objects.filter(name=[employee_teams_dict[emp]])))
    # with open(f'../draft/employee_teams.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(employee_teams_dict, json_file, indent=4, ensure_ascii=False)
    # ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    # Формирование словаря с сохранением порядка
    df['index'] = range(len(df))
    levels_dict = (
        df.groupby('сотрудник', sort=False, group_keys=False)  # Отключаем сортировку
        .apply(lambda x: x[['навык', 'дата', 'оценка_', 'оценка', 'соответствие', 'index']]
            .sort_values('index')  # Восстанавливаем исходный порядок
            .drop(columns=['index'])  # Убираем вспомогательный индекс
            .to_dict('records'))
        .to_dict()
    )
    """
    "Соколов Тимур": [
        {
            "навык": "CorelDraw",
            "дата": "2023-07-31",
            "оценка_": 5,
            "оценка": "Экспертный",
            "соответствие": "да"
        },
    """
    # levels = [
    #     [
    #       Level(
    #         employee=Employee.objects.get(name=emp),
    #         skill=Skill.objects.get(name=l['навык']),
    #         date=l['дата'],
    #         score=l['оценка_'],
    #         name=l['оценка'],
    #         accordance=l['соответствие'],
    #     )  
    #         for l in levels_dict[emp]
    #      ]
    #     for emp in levels_dict
    # ]
    # for data in levels:
    #     Level.objects.bulk_create(data)
    # with open(f'../draft/levels.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(levels_dict, json_file, indent=4, ensure_ascii=False)
    # ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    # total_records = len(df)
    # counter = 0
    # # df_subset = df.head(20)
    # # df_subset.to_dict(orient='records')
    # for start in range(0, total_records, BATCH_SIZE):
    #     end = min(start + BATCH_SIZE, total_records)
    #     df_subset = df.iloc[start:end]

    #     # Преобразуем текущую партию в список словарей
    #     data_batch = df_subset.to_dict(orient='records')

    #     # Сохраняем партию в базу данных
    #     valid_data = []
    #     counter += 1
    #     with open(f'../draft/data{counter}.json', 'w', encoding='utf-8') as json_file:
    #         json.dump(df_subset.to_dict(orient='records'), json_file, indent=4, ensure_ascii=False)


#         for record in data_batch:
#             serializer = EmployeeSerializer(data=record)
#             if serializer.is_valid():
#                 # Добавляем валидные объекты в список
#                 employee = Employee(**serializer.validated_data)
#                 valid_data.append(employee)
#             else:
#                 print(f"Ошибка валидации: {serializer.errors}")

#         # Если есть валидные данные, сохраняем их в БД
#         if valid_data:
#             with transaction.atomic():
#                 Employee.objects.bulk_create(valid_data, batch_size=BATCH_SIZE)

    # with open('../draft/data.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(df_subset.to_dict(orient='records'), json_file, indent=4, ensure_ascii=False)

# import pandas as pd
# from django.db import transaction
# from .models import Employee
# from .serializers import EmployeeSerializer

# BATCH_SIZE = 100  # Размер партии

# Чтение Excel файла
# with pd.ExcelFile(file_path, engine='openpyxl') as xls:
#     df = pd.read_excel(xls, sheet_name=0)

#     # Обработка столбцов с датами
#     df['создан'] = df['создан'].dt.strftime('%Y-%m-%d')
#     df['дата'] = df['дата'].dt.strftime('%Y-%m-%d')

#     # Определим количество строк в датафрейме
#     total_records = len(df)

#     # Итерируем по партиям
#     for start in range(0, total_records, BATCH_SIZE):
#         end = min(start + BATCH_SIZE, total_records)
#         df_subset = df.iloc[start:end]

#         # Преобразуем текущую партию в список словарей
#         data_batch = df_subset.to_dict(orient='records')

#         # Сохраняем партию в базу данных
#         valid_data = []

#         for record in data_batch:
#             serializer = EmployeeSerializer(data=record)
#             if serializer.is_valid():
#                 # Добавляем валидные объекты в список
#                 employee = Employee(**serializer.validated_data)
#                 valid_data.append(employee)
#             else:
#                 print(f"Ошибка валидации: {serializer.errors}")

#         # Если есть валидные данные, сохраняем их в БД
#         if valid_data:
#             with transaction.atomic():
#                 Employee.objects.bulk_create(valid_data, batch_size=BATCH_SIZE)

#         print(f"Сохранено {len(valid_data)} записей из {total_records} (партия {start // BATCH_SIZE + 1}).")

# print("Загрузка завершена.")

# class ProxyEmployee(models.Model):
#     employee = ...
#     position = ...
#     team = ...
#     bus_factor = ...
#     grade = ...
#     created = ...
#     skill = ...
#     competence = ...
#     competence_short = ...
#     domain = ...
#     date = ...
#     score_numeric = ...
#     score_level = ...
#     compliance = ...
#     employee_score = ...
