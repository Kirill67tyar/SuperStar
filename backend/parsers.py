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
        # "сотрудник",
        # "должность",
        # "команда",
        # "bus_factor",
        # "грейд",
        # "создан",
        # "навык",
        'компетенция',
        "компетенция_сокр",
        # "домен",
        # "дата",
        # "оценка_",
        # "оценка",
        # "соответствие"
    ]

    df = pd.read_excel(xls, sheet_name=0, usecols=columns_to_load)

     
    


    # df_dict = pd.read_excel(xls, sheet_name=None)  # Получите словарь DataFrames для всех листов

    # Преобразуем столбцы в формат datetime, заменяя некорректные значения на NaT
    # ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= смена даты
    # df['создан'] = pd.to_datetime(df['создан'], errors='coerce')
    # df['дата'] = pd.to_datetime(df['дата'], errors='coerce')

    # # Преобразуем в строку, обработав NaT
    # # fillna('') заменяет NaT пустыми строками.
    # df['создан'] = df['создан'].dt.strftime('%Y-%m-%d').fillna('')
    # df['дата'] = df['дата'].dt.strftime('%Y-%m-%d').fillna('')
    # ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    # ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= список должностей и команл
    # positions_and_teams = {
    #     'positions': df['должность'].drop_duplicates().tolist(),
    #     'teams': df['команда'].drop_duplicates().tolist(),
    # }
    # positions = [Position(name=name) for name in positions_and_teams['positions']]
    # teams = [Team(name=name) for name in positions_and_teams['teams']]
    # Position.objects.bulk_create(positions)
    # Team.objects.bulk_create(teams)
    # with open(f'../draft/positions_and_teams.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(positions_and_teams, json_file, indent=4, ensure_ascii=False)
    # ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= 
    
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
    # df['index'] = range(len(df))
    # levels_dict = (
    #     df.groupby('сотрудник', sort=False, group_keys=False)  # Отключаем сортировку
    #     .apply(lambda x: x[['навык', 'дата', 'оценка_', 'оценка', 'соответствие', 'index']]
    #         .sort_values('index')  # Восстанавливаем исходный порядок
    #         .drop(columns=['index'])  # Убираем вспомогательный индекс
    #         .to_dict('records'))
    #     .to_dict()
    # )
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
    # ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= какой компетенции соответствует кникальная компетенция
    df_unique = df.drop_duplicates()

    # Преобразуем DataFrame в словарь
    competence_dict = dict(zip(df_unique['компетенция'], df_unique['компетенция_сокр']))

    
    # with open(f'../draft/competence_and_unique_competence.json', 'w', encoding='utf-8') as json_file:
    #     json.dump(competence_dict, json_file, indent=4, ensure_ascii=False)
    # ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= position_requirements
# position_requirements = 'tempr_data/position_requirements.xlsx'
# with pd.ExcelFile(position_requirements, engine='openpyxl') as xls:
#     pass
#     columns_to_load = [
#         "должность",
#         "грейд",
#         "домен",
#         'компетенция',
#         'навык',
#         "оценка_",
#     ]

#     df = pd.read_excel(xls, sheet_name=0, usecols=columns_to_load)
#     position_requirements_dict = df.to_dict(orient='records')
#     """
#     {
#         "должность": "Бизнес Аналитик",
#         "грейд": "Junior",
#         "домен": "Hard skills",
#         "компетенция": "Знание иностранных языков",
#         "навык": "Английский язык",
#         "оценка_": 4.0
#     }
#     """
#     # with open(f'../draft/position_requirements_dict.json', 'w', encoding='utf-8') as json_file:
#     #     json.dump(position_requirements_dict, json_file, indent=4, ensure_ascii=False)
#     requiremets = [
#         PositionRequirement(
#             position=Position.objects.get(name=position['должность']),
#             grade=Grade.objects.get(name=position['грейд']),
#             skill=Skill.objects.get(name=position['навык']),
#             score=position['оценка_'],
#         ) 
#         for position in position_requirements_dict
#         ]
#     PositionRequirement.objects.bulk_create(requiremets)
# ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= target
# target = 'tempr_data/target.xlsx'
# with pd.ExcelFile(target, engine='openpyxl') as xls:
#     pass
#     columns_to_load = [
#         "сотрудник",
#         "должность",
#         "уровень должности",
#     ]

#     df = pd.read_excel(xls, sheet_name=0, usecols=columns_to_load)
#     target_dict = df.to_dict(orient='records')

#     target_list = [
#         Target(
#             employee=Employee.objects.get(name=target['сотрудник']),
#             position=Position.objects.get(name=target['должность']),
#             grade=Grade.objects.get(name=target['уровень должности']),
#         )
#         for target in target_dict
#         ]
#     Target.objects.bulk_create(target_list)
#     # with open(f'../draft/target.json', 'w', encoding='utf-8') as json_file:
#     #     json.dump(target_dict, json_file, indent=4, ensure_ascii=False)
# ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= training_requests
#? изменить модели TrainigRequest, добавить две колонки с часами
#? распарсить и загрузить файл
training_requests = 'tempr_data/training_requests.xlsx'
with pd.ExcelFile(training_requests, engine='openpyxl') as xls:
    pass
    columns_to_load = [
        "сотрудник",
        "должность",
        "уровень должности",
    ]

    df = pd.read_excel(xls, sheet_name=0, usecols=columns_to_load)
    training_requests_dict = df.to_dict(orient='records')
# ! =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=