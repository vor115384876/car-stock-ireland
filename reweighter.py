import csv
from utils.salespercentage import get_sales_percentage
from constants import constants
from models.base_model import ConstantBaseModel
from utils.generators import generate_constants, generate_year_models, list_prod, get_model_by_year


PERCENTAGE_ERROR = 0.001

bl_models_d = generate_year_models(fuel_type=constants.DIESEL, start_year=constants.BASE_YEAR,end_year=constants.end_year)
bl_models_p = generate_year_models(fuel_type=constants.PETROL, start_year=constants.BASE_YEAR,end_year=constants.end_year)

yr_models_d = generate_year_models(fuel_type=constants.DIESEL, start_year=constants.BASE_YEAR,end_year=constants.end_year, path=constants.path)
yr_models_p = generate_year_models(fuel_type=constants.PETROL, start_year=constants.BASE_YEAR,end_year=constants.end_year, path=constants.path)
#changes from start year 2001 to base year 2007
dist_travelled_d = ConstantBaseModel(generate_constants(fuel_type=constants.DIESEL,constant_type=constants.baseline_d_travelled))
dist_travelled_p = ConstantBaseModel(generate_constants(fuel_type=constants.PETROL,constant_type=constants.baseline_d_travelled))


def get_bl_avg_dists(base_model, fuel):
    if fuel is constants.DIESEL:
        dist_travelled = dist_travelled_d
    elif fuel is constants.PETROL:
        dist_travelled = dist_travelled_p
    baseline_avg_pass_km_by_cat = dist_travelled.get_constant(year=base_model._year)
    return list(map(int, baseline_avg_pass_km_by_cat))

def get_pkm_for_year(base_model, fuel):
    baseline_car_cat_counts = base_model.get_cat_counts()
    baseline_pass_kms_by_cat = list_prod(baseline_car_cat_counts, get_bl_avg_dists(base_model, fuel))
    return baseline_pass_kms_by_cat

def get_change(current, model):
    if current == model:
        return 1
    return ((current - model) / model)

def get_new_dist(bl_dist, future_year_model_d, future_year_model_p, step=0.05):
    yr = future_year_model_d._year
    new_pass_kms_diesel = get_pkm_for_year(future_year_model_d, constants.DIESEL)
    new_pass_kms_petrol= get_pkm_for_year(future_year_model_p, constants.PETROL)
    model_pass_kms = sum(new_pass_kms_diesel + new_pass_kms_petrol)
    diff = get_change(bl_dist, model_pass_kms)
    if abs(diff) < PERCENTAGE_ERROR:
        return dist_travelled_d.get_constant(yr), dist_travelled_p.get_constant(yr)
    else:
        old_diesel_avg_dist = dist_travelled_d.get_constant(yr)
        old_petrol_avg_dist = dist_travelled_p.get_constant(yr)
        if diff > 0:
            coeff = 1+step
        else:
            coeff = 1-step
        new_d_values = [float(val)*coeff for val in old_diesel_avg_dist]
        new_p_values = [float(val)*coeff for val in old_petrol_avg_dist]        
        dist_travelled_d.update_year_constant(yr, new_d_values)
        dist_travelled_p.update_year_constant(yr, new_p_values)
        return get_new_dist(bl_dist, future_year_model_d, future_year_model_p, step=step*0.75)


def write_to_csv(new_distances, fuel):
    base_dist = generate_constants(fuel_type=fuel,constant_type=constants.baseline_d_travelled)[:8]
    old_dist = [list(map(int, x)) for x in base_dist]
    full_new_distances = old_dist + new_distances
    with open(f'static_constants/{fuel}/{constants.path}_distance_travelled.csv', "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(full_new_distances)

d_dist = []
p_dist = []

for i in range(1,12):
    year = constants.BASE_YEAR+i
    bl_model_d = get_model_by_year(bl_models_d, year)
    bl_model_p = get_model_by_year(bl_models_p, year) 

    future_year_model_d = get_model_by_year(yr_models_d, year)
    future_year_model_p = get_model_by_year(yr_models_p, year)

    bl_pass_kms_diesel = get_pkm_for_year(bl_model_d, constants.DIESEL)
    bl_pass_kms_petrol= get_pkm_for_year(bl_model_p, constants.PETROL)

    bl_total_pass_kms = sum(bl_pass_kms_diesel + bl_pass_kms_petrol)

    new_diesel_avg, new_petrol_avg = get_new_dist(bl_total_pass_kms, future_year_model_d, future_year_model_p)

    print(f'Year:  {year}')
    print(new_diesel_avg, new_petrol_avg)
    print()

    final_cd = list(map(int, new_diesel_avg))
    final_cp = list(map(int, new_petrol_avg))

    final_cd.insert(0, year)
    final_cp.insert(0, year)

    d_dist.append(final_cd)
    p_dist.append(final_cp)

write_to_csv(d_dist, constants.DIESEL)
write_to_csv(p_dist, constants.PETROL)








   


