import csv
from utils.salespercentage import get_sales_percentage
from constants import constants
from models.base_model import ConstantBaseModel
from utils.generators import generate_constants, generate_year_models, list_prod, get_model_by_year
#breakpoint()

bl_models_d = generate_year_models(fuel_type=constants.DIESEL, start_year=constants.start_year,end_year=constants.end_year)
bl_models_p = generate_year_models(fuel_type=constants.PETROL, start_year=constants.start_year,end_year=constants.end_year)

yr_models_d = generate_year_models(fuel_type=constants.DIESEL, start_year=constants.start_year,end_year=constants.end_year, path="new_models")
yr_models_p = generate_year_models(fuel_type=constants.PETROL, start_year=constants.start_year,end_year=constants.end_year, path="new_models")

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
    
def get_A_matrices(baseline_model_d, baseline_model_p):
    bl_avg_dists_diesel = get_bl_avg_dists(baseline_model_d, constants.DIESEL)
    bl_avg_dists_petrol = get_bl_avg_dists(baseline_model_p, constants.PETROL)
    print("ah")
    print(bl_avg_dists_petrol)

    bl_pass_kms_diesel = get_pkm_for_year(baseline_model_d, constants.DIESEL)
    bl_pass_kms_petrol= get_pkm_for_year(baseline_model_p, constants.PETROL)

    bl_total_pass_kms = sum(bl_pass_kms_diesel + bl_pass_kms_petrol)

    total_cars = sum(baseline_model_d.get_cat_counts())+sum(baseline_model_p.get_cat_counts())
    overall_avg = bl_total_pass_kms/total_cars

    Ad = [a/overall_avg for a in bl_avg_dists_diesel]
    Ap = [a/overall_avg for a in bl_avg_dists_petrol]
    return Ad, Ap, bl_total_pass_kms, overall_avg


def get_c(A, B, bl_tot_kms):
    A_B = sum(list_prod(A,B))
    X = bl_tot_kms/A_B
    return [a*X for a in A]



def write_to_csv(new_distances, fuel):
    base_dist = generate_constants(fuel_type=fuel,constant_type=constants.baseline_d_travelled)[:8]
    old_dist = [list(map(int, x)) for x in base_dist]
    full_new_distances = old_dist + new_distances
    # print(full_new_distances)
    with open(f'static_constants/{fuel}/{constants.path}_distance_travelled.csv', "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(full_new_distances)

d_dist = []
p_dist = []

for i in range(1,12):
    bl_model_d = get_model_by_year(bl_models_d, constants.BASE_YEAR+i)
    bl_model_p = get_model_by_year(bl_models_p, constants.BASE_YEAR+i)  

    # Adiesel, Apetrol, bl_total_pass_kms, overall_avg = get_A_matrices(bl_model_d, bl_model_p)

    bl_pass_kms_diesel = get_pkm_for_year(bl_model_d, constants.DIESEL)
    bl_pass_kms_petrol= get_pkm_for_year(bl_model_p, constants.PETROL)
    car_total_d = sum(bl_model_d.get_cat_counts())
    car_total_p = sum(bl_model_p.get_cat_counts())
    bl_total_pass_kms = sum(bl_pass_kms_diesel + bl_pass_kms_petrol)
    total_cars = car_total_d + car_total_p

    d_share = car_total_d/total_cars
    d_dist_share = sum(bl_pass_kms_diesel)/bl_total_pass_kms
    d_avg = sum(bl_pass_kms_diesel)/car_total_d
    d_co_eff = d_dist_share/d_share

    print(f'Year: {constants.BASE_YEAR+i}.')
    # print(d_share)
    # print(d_dist_share)
    # print(d_avg)
    # print(d_co_eff)
    # print(d_co_eff)

    total_new_diesel_pc = d_co_eff*get_sales_percentage(fuel_type=constants.DIESEL,year=bl_model_d._year)
    
    # print(total_new_diesel_pc)
    total_new_diesel_pk = round(total_new_diesel_pc* bl_total_pass_kms)
    total_new_petrol_pk = bl_total_pass_kms - total_new_diesel_pk
    # print(bl_total_pass_kms)
    # print()
    # print(total_new_diesel_pk)
    # print()
    # print(total_new_petrol_pk)
    # print()
    # print(total_new_diesel_pk+total_new_petrol_pk)
    future_year_model_d = get_model_by_year(yr_models_d, constants.BASE_YEAR+i)
    future_year_model_p = get_model_by_year(yr_models_p, constants.BASE_YEAR+i)

    future_car_count_d = future_year_model_d.get_cat_counts()
    future_car_count_p = future_year_model_p.get_cat_counts()

    new_diesel_avg = total_new_diesel_pk/sum(future_car_count_d)
    new_petrol_avg = total_new_petrol_pk/sum(future_car_count_p)

    print(new_diesel_avg)
    print()
    print(new_petrol_avg)


    Cd = [new_diesel_avg]*14
    Cp = [new_petrol_avg]*14

    print(f'Year: {constants.BASE_YEAR+i}. Diesel: {Cd}')
    print(f'Year: {constants.BASE_YEAR+i}. Petrol: {Cp}')
    print()


    # print("baseline")
    # print(bl_total_pass_kms)
    # print("new")
    # dist_d = list_prod(future_car_count_d, Cd)
    # dist_p = list_prod(future_car_count_p, Cp)
   # print(sum(dist_d)+sum(dist_p)-bl_total_pass_kms)

    final_cd = list(map(int, Cd))
    final_cp = list(map(int, Cp))

    final_cd.insert(0, constants.BASE_YEAR+i)
    final_cp.insert(0, constants.BASE_YEAR+i)

    d_dist.append(final_cd)
    # print(f'd_dist: {d_dist}')
    p_dist.append(final_cp)
    # print(f'p_dist: {p_dist}')

write_to_csv(d_dist, constants.DIESEL)
write_to_csv(p_dist, constants.PETROL)








   


