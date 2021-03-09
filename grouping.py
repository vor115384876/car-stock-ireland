import csv
from constants import constants
from models.base_model import ConstantBaseModel
from models.base_model import BaseModel
from utils.generators import generate_constants, generate_year_models, generate_dist_models


f_type = constants.f_type
yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)

group_1 = [0,0]
group_2 = [1,3]
group_3 = [4,6]
group_4 = [7,8]
group_5 = [9,10]
group_6 = [11,11]
group_7 = [12,13]

splits = [group_1, group_2, group_3, group_4, group_5, group_6, group_7]
header = ["year","900","900 - 1200","1201 - 1500", "1501 - 1700", "1701-1900", "1901-2100", "2100"]


for model in yr_models:
    csv_file = f'model_output/{f_type}/{model._year}-vintage_grouped_engine_cc_for_leap.csv'
    with open(csv_file, 'w', newline='') as csvfile:
        data_to_write = model.give_engine_groupings(splits)
        ids = list(range(0,18))
        [row.insert(0, model.get_car_year(i)) for  i, row in zip(ids, data_to_write)]
        data_to_write.insert(0, header)
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data_to_write)
