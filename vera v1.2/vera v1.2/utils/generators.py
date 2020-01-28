import csv 
from models.base_model import BaseModel

def generate_year_models(fuel_type,start_year,end_year): #function to generate_year_models (args 2001/2007 - 2018) 
    model_list = [] #initialise array for model list
    for year in range(start_year,end_year): #
        # print(f'Opening the file: {year}.csv for fuel type: {fuel_type}')
        file_name = f'year_model_inputs/{fuel_type}/{year}.csv' #this is so you can find the csv 
        with open(file_name, newline='', encoding='utf-8-sig') as f: #matching the coding to suit the excel files numbers/letters, encoded as f
            reader = list(csv.reader(f)) #reader sets up a list of the csv.reader(f)  f is designed in the line above
            temp = list() 
            for row in reader[1:]:
                temp.insert(0,row[1:])
            model_list.append(BaseModel(year, temp))
    return model_list


def generate_constants(fuel_type,constant_type): 
    # print(f'Opening the file: {constant_type}.csv for fuel type: {fuel_type}')
    file_name = f'static_constants/{fuel_type}/{constant_type}.csv'
    with open(file_name, newline='', encoding='utf-8-sig') as f: #with is used to make code cleaner -
        reader = list(csv.reader(f))
    return reader 

def list_prod(list_a,list_b, logthis=False): #function to get the product - this is handy in carstock calcs.
    if logthis:
        [print(f'Mult {a} by {b}') for a,b in zip(list_a, list_b)]
    return [(a*b) for a,b in zip(list_a, list_b)] #this pairs a and b together, and multiplies them 

def list_add(list_a,list_b): #function to add the lists - handy for adding petrol and diesel for total car stock etc. 
    # [print(f'Mult {a} by {b}') for a,b in zip(list_a, list_b)]
    return [(a+b) for a,b in zip(list_a, list_b)]


def get_model_by_year(model_list, year): #function so I can get model by year 
    for model in model_list: 
        if model._year == year:
            return model 
    raise Exception("No model for that year found") #stops at a year that there is no model.
