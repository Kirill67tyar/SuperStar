import json
import pandas as pd
import os
from pprint import pprint as pp
# from django.db import transaction
# from employees.models import ProxyEmployee



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

    unique_dict = {
        'positions': df['должность'].drop_duplicates().tolist(),
        'teams': df['команда'].drop_duplicates().tolist(),
    }
    pp(unique_dict)
    competence_dict = (
        df.groupby('компетенция_сокр')['навык']
        .apply(lambda x: x.drop_duplicates().tolist())
        .to_dict()
    )
    with open(f'../draft/competence.json', 'w', encoding='utf-8') as json_file:
        json.dump(competence_dict, json_file, indent=4, ensure_ascii=False)
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
    df['index'] = range(len(df))

# Формирование словаря с сохранением порядка
    levels_dict = (
        df.groupby('сотрудник', sort=False, group_keys=False)  # Отключаем сортировку
        .apply(lambda x: x[['навык', 'дата', 'оценка_', 'оценка', 'соответствие', 'index']]
            .sort_values('index')  # Восстанавливаем исходный порядок
            .drop(columns=['index'])  # Убираем вспомогательный индекс
            .to_dict('records'))
        .to_dict()
    )
    with open(f'../draft/levels.json', 'w', encoding='utf-8') as json_file:
        json.dump(levels_dict, json_file, indent=4, ensure_ascii=False)

    unique_employees = df.drop_duplicates(subset=['сотрудник'])
    employee_list = unique_employees[['сотрудник', 'должность', 'bus_factor', 'грейд', 'создан']].to_dict(orient='records')
    with open(f'../draft/employee.json', 'w', encoding='utf-8') as json_file:
        json.dump(employee_list, json_file, indent=4, ensure_ascii=False)

    employee_teams_dict = df.groupby('сотрудник')['команда'].apply(lambda x: list(set(x))).to_dict()
    with open(f'../draft/employee_teams.json', 'w', encoding='utf-8') as json_file:
        json.dump(employee_teams_dict, json_file, indent=4, ensure_ascii=False)


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
