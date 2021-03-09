import csv
from constants import constants
from models.base_model import ConstantBaseModel
from models.base_model import BaseModel
from utils.generators import generate_constants, generate_year_models, generate_dist_models, list_prod


f_type = constants.f_type

yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)
dist_models = generate_dist_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)

def replace_zeros(a, b):
    return 1 if a == 0 else b
group_1 = [0,0]
group_2 = [1,3]
group_3 = [4,6]
group_4 = [7,8]
group_5 = [9,10]
group_6 = [11,11]
group_7 = [12,13]


for model, dist_models in zip(yr_models, dist_models):
    csv_file = f'model_output/{f_type}/distance_grouped/{model._year}_distance_grouped_engine_cc.csv'
    pkm_model = model * dist_models

    with open(csv_file, 'w', newline='') as csvfile:


        if f_type != 'electric':
            splits = [group_1, group_2, group_3, group_4, group_5, group_6, group_7]
            header = ["year","900","900 - 1200","1201 - 1500", "1501 - 1700", "1701-1900", "1901-2100", "2100"]
            pkm_split = pkm_model.give_engine_groupings(splits)
            car_count_split = model.give_engine_groupings(splits)
            car_count_filtered = car_count_split
            car_count_filtered = [[replace_zeros(a, b) for a, b in zip(r1, r2)] for r1, r2 in zip(car_count_split, car_count_filtered)]

        else:
            electric_split = [total]
            header = ["year","average mileage"]
            pkm_split = pkm_model.give_engine_groupings(electric_split)
            car_count_split = model.give_engine_groupings(electric_split)
            car_count_filtered = car_count_split
            car_count_filtered = [[replace_zeros(a, b) for a, b in zip(r1, r2)] for r1, r2 in zip(car_count_split, car_count_filtered)]
            
            
        data_to_write = [[pkm/car_count for pkm,car_count in zip(p_row,c_row)] for p_row,c_row in zip(pkm_split,car_count_filtered)]

        ids = list(range(0,18))
        [row.insert(0, model.get_car_year(i)) for  i, row in zip(ids, data_to_write)]
        data_to_write.insert(0, header)
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data_to_write)
