from constants import constants
from models.base_model import BaseModel
from survival_rate import calc_survival_rate
from utils.generators import generate_year_models, list_prod, get_model_by_year, write_year_model_to_csv
from utils.salespercentage import get_sales_percentage


yr_models_d = generate_year_models(fuel_type=constants.DIESEL, start_year=constants.start_year,end_year=constants.BASE_YEAR+1)
yr_models_p = generate_year_models(fuel_type=constants.PETROL, start_year=constants.start_year,end_year=constants.BASE_YEAR+1)
baseline_models_d = generate_year_models(fuel_type=constants.DIESEL, start_year=constants.BASE_YEAR,end_year=constants.end_year)
baseline_models_p = generate_year_models(fuel_type=constants.PETROL, start_year=constants.BASE_YEAR,end_year=constants.end_year)


def add_models(model_a, model_b):
    comb_model = {}
    yr =constants.start_year
    for d_model,p_model in zip(model_a,model_a):
        both_model = [[d+p for d,p in zip(dies,petr)] for dies, petr in zip(d_model._data, p_model._data)]
        comb_model[yr] = both_model
        yr +=1
    return comb_model

def get_s_rates(latest_year, baseline_models):
    s_rate_matrix = []
    for i in range(len(latest_year.get_counts())-1):
        row = []
        for j in range(len(latest_year.get_cat_counts())):
            surv_rates = calc_survival_rate(baseline_models, age=i, cat=j)
            s_rate = (sum(surv_rates)/len(surv_rates))
            row.append(s_rate)
        s_rate_matrix.append(row)
    return s_rate_matrix
    

def generate_year_after_s_rate(latest_year, baseline_models):
    s_rate_matrix = get_s_rates(latest_year, baseline_models)
    year_with_oldest_removed = latest_year.get_counts()[:-1]
    yr_floats = [list(map(float, row)) for row in year_with_oldest_removed]
    year_post_s_rate = [list_prod(yrf, srm) for yrf,srm in zip(yr_floats, s_rate_matrix)]
    return [list(map(int, map(round, row))) for row in year_post_s_rate]

def get_new_car_weighting(fuel):
    if fuel is constants.DIESEL:
        basemodel = baseline_models_d
    elif fuel is constants.PETROL:
        basemodel = baseline_models_p
    base_year = get_model_by_year(basemodel, constants.BASE_YEAR)
    baseline_new_cars = base_year.get_counts(age=0)
    return [x/sum(baseline_new_cars) for x in baseline_new_cars]
    
    
def get_new_car_count(year_models, baseline_models):
    latest_year = year_models[-1]
    rounded_car_count = generate_year_after_s_rate(latest_year, baseline_models)

    year = latest_year._year + 1
    baseline_counterpart = get_model_by_year(baseline_models, year)
    # print(f'baseline: {baseline_counterpart.get_counts()}')
    # print(f'prev scenario year: {rounded_car_count}')
    car_count_old = sum([sum(cc) for cc in zip(*rounded_car_count)])
    car_count_new = sum([sum(cc) for cc in zip(*baseline_counterpart.get_counts())])
    new_cars = car_count_new - car_count_old
    print(f'baseline: {car_count_new}')
    print(f'prev scenario year: {car_count_old}')
    print(f'new cars: {new_cars}')
    return new_cars, rounded_car_count


def generate_next_year(year_models, full_sales, rounded_car_count, fuel):
    latest_year = year_models[-1]
    year = latest_year._year + 1
    SALE_PERCENTAGE = get_sales_percentage(fuel_type=fuel,year=year)
    
    new_cars_by_f_type = round(full_sales*SALE_PERCENTAGE)
    

    weightings = get_new_car_weighting(fuel)
    scenario_new_cars = [round(weight*new_cars_by_f_type) for weight in weightings]
    rounded_car_count.insert(0, scenario_new_cars)
    return year, rounded_car_count


def final_step(year, cc, fuel):
    new_year_model = BaseModel(year, cc)
    return new_year_model


year = constants.BASE_YEAR
while year < constants.end_year-1:
    print(year)
    diesel_car_diff, diesel_count_car_count = get_new_car_count(yr_models_d, baseline_models_d)
    petrol_car_diff, petrol_count_car_count = get_new_car_count(yr_models_p, baseline_models_p)
    full_sales = diesel_car_diff + petrol_car_diff
    print(f'sales {full_sales}')
    year+=1
    year_d, cc_d = generate_next_year(yr_models_d, full_sales, diesel_count_car_count, constants.DIESEL)
    year_p, cc_p = generate_next_year(yr_models_p, full_sales, petrol_count_car_count, constants.PETROL)
    
    new_year_model_d = final_step(year_d, cc_d, constants.DIESEL)
    new_year_model_p = final_step(year_p, cc_p, constants.PETROL)

    yr_models_d.append(new_year_model_d)
    yr_models_p.append(new_year_model_p)

for model in yr_models_d:
    write_year_model_to_csv(model.get_counts(), model._year, constants.DIESEL)

for model in yr_models_p:
    write_year_model_to_csv(model.get_counts(), model._year, constants.PETROL)


    

    



