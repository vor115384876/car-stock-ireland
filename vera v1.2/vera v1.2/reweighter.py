from constants import constants
from models.base_model import ConstantBaseModel
from utils.generators import generate_constants, generate_year_models, list_prod, get_model_by_year


f_type = constants.f_type

yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year)


dist_travelled = ConstantBaseModel(generate_constants(fuel_type=f_type,constant_type=constants.d_travelled))

bl_avg_pass_km_by_cat = dist_travelled.get_constant(year=constants.BASE_YEAR)
bl_year_model = get_model_by_year(yr_models, constants.BASE_YEAR)
bl_car_count_by_cat = bl_year_model.get_cat_counts()

bl_pass_kms_by_cat = list_prod(bl_avg_pass_km_by_cat,bl_car_count_by_cat)
# TODO need to take both fuel types into account 
bl_total_pass_kms = sum(bl_pass_kms_by_cat)
print(bl_total_pass_kms)

avg_pass_km = bl_total_pass_kms/sum(bl_car_count_by_cat)

A = [a/avg_pass_km for a in bl_avg_pass_km_by_cat]


# TODO: change this to look at generated model
for i in range(1,12):
    future_year_model = get_model_by_year(yr_models, constants.BASE_YEAR+i)
    future_avg_pass_km_by_cat = dist_travelled.get_constant(year=constants.BASE_YEAR+i)
    future_car_count_by_cat = future_year_model.get_cat_counts()

    pass_kms_by_cat = list_prod(future_avg_pass_km_by_cat, future_car_count_by_cat)
    # TODO need to take both fuel types into account 
    future_total_pass_kms = sum(pass_kms_by_cat)


    A_B = sum(list_prod(A,future_car_count_by_cat))

    X = future_total_pass_kms/A_B

    X = bl_total_pass_kms/A_B


    C = [a*X for a in A]

    print(f'Year: {constants.BASE_YEAR+i}. {C}')



