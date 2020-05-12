import csv
from constants import constants
from models.base_model import ConstantBaseModel
from models.base_model import BaseModel
from utils.generators import generate_constants, generate_year_models, generate_dist_models, list_prod


f_type = constants.f_type

yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)
eff_band = generate_constants(fuel_type=f_type,constant_type=constants.f_band)

def replace_zeros(a, b):
    return 1 if a == 0 else b
smol_bois = [0,4]
medium_bois = [5,10]
fat_lads = [11,14]
total = [0,14]

#vehicle stock 0 - 14 } aggregate 0-4, 5-10, 11-14
#distance 0-4 {sum of (vehicle stock (0)*eff band (0))+vehicle stock (1) *eff band (1) +.../(sum of total vehicle stock in group 0 - 4)}

for model in yr_models:
    csv_file = f'model_output/{f_type}/fuel_efficiencies_grouped/{model._year}_distance_grouped_engine_cc.csv'
    eff_model = model._year * eff_band

    with open(csv_file, 'w', newline='') as csvfile:


        if f_type == ('diesel' or 'petrol'):
            splits = [smol_bois, medium_bois, fat_lads]
            header = ["year","<1300cc","1300cc - 1900cc",">1900cc"]
            eff_split = eff_model.give_engine_groupings(splits)
            car_count_split = model.give_engine_groupings(splits)
            car_count_filtered = [[replace_zeros(a, b) for a, b in zip(r1, r2)] for r1, r2 in zip(car_count_split, car_count_filtered)]

        else:
            print("Fuel efficiencies available for petrol and diesel only.")
            
            
        data_to_write = [[pkm/car_count for pkm,car_count in zip(p_row,c_row)] for p_row,c_row in zip(pkm_split,car_count_filtered)]

        ids = list(range(0,18))
        [row.insert(0, model.get_car_year(i)) for  i, row in zip(ids, data_to_write)]
        data_to_write.insert(0, header)
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data_to_write)

