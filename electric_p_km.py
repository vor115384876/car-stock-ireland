import csv
from constants import constants
from models.base_model import ConstantBaseModel
from models.base_model import BaseModel
from utils.generators import generate_constants, generate_year_models, generate_dist_models, list_prod

em_dict = []
f_type = constants.f_type

yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)
dist_models = generate_dist_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)

base_year = 1990

for index,sample_model in enumerate(yr_models):
    csv_file = f'model_output/{f_type}/passenger_km.csv'
    while base_year < sample_model._year:
        	base_year+=1
    #do i need to create another for loop to go through the distances?

    dist_for_yr = dist_models[index]._data
    total_passenger_km = [[float(numcar)*1*float(dt) for numcar,dt in zip(numcars, dist_for_yr_cat)] for numcars, dist_for_yr_cat in zip(sample_model._data, dist_for_yr)]
    ev_passenger_km = sum(sum(total_passenger_km,[]))
    print(base_year)
    print(ev_passenger_km)

    em_dict.append({"year": str(base_year), "electric_passenger_km": ev_passenger_km })

# this code outputs the year emissions to a csv
csv_file = f'model_output/{f_type}-passenger_km.csv'
csv_columns = ["year","electric_passenger_km"]
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for year in em_dict:
        writer.writerow(year)
      