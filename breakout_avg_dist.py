from constants import constants
from models.base_model import ConstantBaseModel
from utils.generators import generate_year_models, generate_constants, list_prod, get_model_by_year, read_file


f_type = constants.f_type

yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)
dist_travelled = ConstantBaseModel(generate_constants(fuel_type=f_type,constant_type=constants.d_travelled))

age_rate_path = f'static_constants/{f_type}/ageing_rates.csv'

age_rates = read_file(age_rate_path)

# print(age_rates)

for sample_model in yr_models:
    print(sample_model._year)

    # Getting pkm per cat for every year
    dist_for_yr = list(map(int,dist_travelled.get_constant(year=sample_model._year)))
    cars_per_cat = sample_model.get_cat_counts() 
    pkm_cat = list_prod(dist_for_yr,cars_per_cat)
    # print(pkm_cat)

    car_share_weightings = [[car_count/cat_count for car_count, cat_count in zip(cars_per_age,cars_per_cat)] for cars_per_age in  sample_model.get_counts()]

    overall_weightings = [[float(ar)*car_share for ar,car_share in zip(ar_row, cs_row)] for ar_row,cs_row in zip(age_rates,car_share_weightings)]

    final_avg_dist_breakout = [[o_w*pkm for o_w,pkm in zip(weight_row,pkm_cat)] for weight_row in overall_weightings]

    print(final_avg_dist_breakout)