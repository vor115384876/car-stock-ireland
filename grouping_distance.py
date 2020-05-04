import csv
from constants import constants
from models.base_model import ConstantBaseModel
from models.base_model import BaseModel
from utils.generators import generate_constants, generate_year_models, generate_dist_models, list_prod


f_type = constants.f_type
yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)
dist_models = generate_dist_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)

smol_bois = [0,4]
medium_bois = [5,10]
fat_lads = [11,14]
splits = [smol_bois, medium_bois, fat_lads]
header = ["year","<1300cc","1300cc - 1900cc",">1900cc"]
#vehicle stock 0 - 14 } aggregate 0-4, 5-10, 11-14
#distance 0-4 {sum of (vehicle stock (0)*average distance (0))+vehicle stock (1) *average distance (1) +.../(sum of total vehicle stock in group 0 - 4)}

for model, dist_models in zip(yr_models, dist_models):
    csv_file = f'model_output/{f_type}/{model._year}_distance_grouped_engine_cc.csv'
    pkm_model = model * dist_models
    with open(csv_file, 'w', newline='') as csvfile:
        pkm_split = pkm_model.give_engine_groupings(splits)
        car_count_split = model.give_engine_groupings(splits)
        data_to_write = [[pkm/car_count for pkm,car_count in zip(p_row,c_row)] for p_row,c_row in zip(pkm_split,car_count_split)]
        ids = list(range(0,18))
        [row.insert(0, model.get_car_year(i)) for  i, row in zip(ids, data_to_write)]
        data_to_write.insert(0, header)
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data_to_write)