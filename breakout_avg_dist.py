from constants import constants
from models.base_model import ConstantBaseModel
from utils.generators import generate_year_models, generate_constants, list_prod, read_file


f_type = constants.f_type

yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)
dist_travelled = ConstantBaseModel(generate_constants(fuel_type=f_type,constant_type=constants.d_travelled))

age_rate_path = f'static_constants/{f_type}/ageing_rates.csv'
age_rates = read_file(age_rate_path)

for sample_model in yr_models:
    print(sample_model._year)

    # Getting pkm per cat for every year
    dist_for_yr = list(map(int,dist_travelled.get_constant(year=sample_model._year)))
    #print(dist_for_yr)
    cars_per_cat = sample_model.get_cat_counts()
    #print(cars_per_cat) 
    pkm_cat = list_prod(dist_for_yr,cars_per_cat)
    #print(pkm_cat)
    
    # getting the share of a car age for that cat
    car_share_weightings = [[car_count/cat_count for car_count, cat_count in zip(cars_per_age,cars_per_cat)] for cars_per_age in  sample_model.get_counts()]
    #car_share_weightings = [[car_count/1 for car_count, cat_count in zip(cars_per_age,cars_per_cat)] for cars_per_age in  sample_model.get_counts()]
    #print(car_share_weightings)
    #print(car_share_weightings)

    # multiply the two weightings together
    overall_weightings = [[float(ar)*car_share for ar,car_share in zip(ar_row, cs_row)] for ar_row,cs_row in zip(age_rates,car_share_weightings)]
    #print(overall_weightings)
    # multiply the total pkm on top of each weighting to get the final avg dist
    total_dist_breakout_by_car = [[o_w*pkm for o_w,pkm in zip(weight_row,pkm_cat)] for weight_row in overall_weightings]
    #print(total_dist_breakout_by_car)
    #breakpoint()
    
    #print(car_share_weightings)
    
           
    avg_dist_per_car = [[fadb*car_share for fadb, car_share in zip(cs_row,fadb_row)] for fadb_row,cs_row in zip(final_avg_dist_breakout,car_share_weightings)]
    #avg_dist_per_car_ans = [[avg_dist_per_car*car_coun for avg_dist_per_car, car_coun in zip(avg_dist_per_car,cars_per_cat)]]
    

    print(avg_dist_per_car)
    #print(final_avg_dist_breakout)