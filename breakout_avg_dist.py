from constants import constants
from models.base_model import ConstantBaseModel
from utils.generators import generate_year_models, generate_constants, list_prod, read_file, write_year_model_to_csv


f_type = constants.f_type

yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)
dist_travelled = ConstantBaseModel(generate_constants(fuel_type=f_type,constant_type=constants.d_travelled))

age_rate_path = f'static_constants/{f_type}/ageing_rates.csv'
age_rates = read_file(age_rate_path)

for sample_model in yr_models:
    print(sample_model._year)   

    # Getting pkm per cat for every year
    dist_for_yr = list(map(int,dist_travelled.get_constant(year=sample_model._year)))
    cars_per_cat = sample_model.get_cat_counts() 
    pkm_cat = list_prod(dist_for_yr,cars_per_cat)

    # getting the share of a car age for that cat

    converted_car_count = [list_prod(ar_row,cc_row) for ar_row, cc_row in zip(age_rates,sample_model.get_counts())]
    car_count_sum = [sum(int(row[i]) for row in converted_car_count) for i in range(len(converted_car_count[0]))]

    # [print(f'{pk}/{ccs}') for pk,ccs in zip(pkm_cat, car_count_sum)]
    new_avg_dists_zeros = [pk/ccs if ccs!= 0 else 0 for pk,ccs in zip(pkm_cat, car_count_sum)]
    # print(new_avg_dists_zeros)
    new_dists = [[nd*ar for nd,ar in zip(new_avg_dists_zeros, ar_row)] for ar_row in age_rates]

    filepath=f'static_constants/{f_type}/avg_dists/{sample_model._year}.csv'
    write_year_model_to_csv(new_dists, sample_model._year, f_type, path=filepath)
