import csv
from models.base_model import BaseModel

def generate_year_models(fuel_type,start_year,end_year, path=None):
#why is the path set to None here when in scenario mode in main.py path could be set to new_models
    model_list = []
    PATH = path or "year_model_inputs"
    for year in range(start_year,end_year):
        # print(f'Opening the file: {year}.csv for fuel type: {fuel_type}')
        file_name = f'{PATH}/{fuel_type}/{year}.csv'
        with open(file_name, newline='', encoding='utf-8-sig') as f:
            reader = list(csv.reader(f))
            temp = list()
            for row in reader[1:]:
                temp.insert(0,row[1:])
            model_list.append(BaseModel(year, temp))
    return model_list


def generate_constants(fuel_type,constant_type):
    print(f'Opening the file: {constant_type}.csv for fuel type: {fuel_type}')
    file_name = f'static_constants/{fuel_type}/{constant_type}.csv'
    with open(file_name, newline='', encoding='utf-8-sig') as f:
        reader = list(csv.reader(f))
    return reader

def list_prod(list_a,list_b, logthis=False):
    if logthis:
        [print(f'Mult {a} by {b}') for a,b in zip(list_a, list_b)]
    return [(a*b) for a,b in zip(list_a, list_b)]

def list_add(list_a,list_b):
    [print(f'Mult {a} by {b}') for a,b in zip(list_a, list_b)]
    return [(a+b) for a,b in zip(list_a, list_b)]


def get_model_by_year(model_list, year):
    for model in model_list:
        if model._year == year:
            return model
    raise Exception("No model for that year found")