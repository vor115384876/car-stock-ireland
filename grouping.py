import csv
from constants import constants
from models.base_model import ConstantBaseModel
from models.base_model import BaseModel
from utils.generators import generate_constants, generate_year_models, generate_dist_models


f_type = constants.f_type
yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)

smol_bois = [1,4]
normal_bois = [5,10]
fat_lads = [11,13]
splits = [smol_bois, normal_bois, fat_lads]
header = ["year","<1300cc","1300cc - 1900cc",">1900cc"]


for model in yr_models:
    csv_file = f'model_output/{f_type}/{model._year}-vintage_grouped_engine_cc.csv'
    with open(csv_file, 'w', newline='') as csvfile:
        data_to_write = model.give_engine_groupings(splits)
        ids = list(range(1,18))
        [row.insert(0, model.get_car_year(i)) for  i, row in zip(ids, data_to_write)]
        data_to_write.insert(0, header)
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data_to_write)