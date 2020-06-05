import csv
from models.base_model import BaseModel
from constants import constants
from models.base_model import ConstantBaseModel
from utils.generators import generate_constants, generate_year_models, list_prod, get_model_by_year


f_type = constants.f_type


yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)

dist_travelled = ConstantBaseModel(generate_constants(fuel_type=f_type,constant_type=constants.d_travelled))

#emissions bands are only recorded from 2004 onwards
base_year = 1990

dist_dict = []
for sample_model in yr_models:
    base_year = sample_model._year-17
    yr_consumption_per_km = []
    while base_year < sample_model._year:
        yr_consumption_per_km.append(constant_model.get_constant(year=base_year))
        base_year+=1
    dist_for_yr = dist_travelled.get_constant(year=sample_model._year)
    #breakpoint()
    total_passenger_kilometers = [[float(numcar)*1*float(dt) for numcar,cpk,dt in zip(numcars,cpks, dist_for_yr)] for numcars, cpks in zip(sample_model._data, yr_consumption_per_km)]
    annual_passenger_kilometers = sum(total_passenger_kilometers,[])
   # print(annual_passenger_kilometers)
    annual_pkm = list(map(int, annual_passenger_kilometers))
    print(base_year)
    print(annual_pkm)