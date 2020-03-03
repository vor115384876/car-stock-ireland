import csv
from constants import constants
from models.base_model import ConstantBaseModel
from models.base_model import BaseModel
from utils.generators import generate_constants, generate_year_models





f_type = constants.f_type


yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)

em_band = generate_constants(fuel_type=f_type, constant_type=constants.em_band)
rd_factor = generate_constants(fuel_type=f_type,constant_type=constants.r_factor)


dist_travelled = ConstantBaseModel(generate_constants(fuel_type=f_type,constant_type=constants.d_travelled))

new_rd_factor = [row[1:] for row in rd_factor]
new_em_band = [row[1:] for row in em_band]
consumption_per_km = [[(1+float(rf))*float(emb) for rf, emb in zip(r_fs, embs)] for r_fs, embs, in zip(new_rd_factor, new_em_band)]
new_consumption_per_km = []
#emissions bands are only recorded from 2004 onwards
base_year = 1990
for row in consumption_per_km:
    new_consumption_per_km.append([base_year]+row)
    base_year += 1

constant_model = ConstantBaseModel(new_consumption_per_km)

em_dict = []
for sample_model in yr_models:
    base_year = sample_model._year-17
    yr_consumption_per_km = []
    while base_year < sample_model._year:
        yr_consumption_per_km.append(constant_model.get_constant(year=base_year))
        base_year+=1
    dist_for_yr = dist_travelled.get_constant(year=sample_model._year)
    #breakpoint()
    total_consumption_grams = [[float(numcar)*float(cpk)*float(dt) for numcar,cpk,dt in zip(numcars,cpks, dist_for_yr)] for numcars, cpks in zip(sample_model._data, yr_consumption_per_km)]
    total_passenger_kilometers = [[float(numcar)*1*float(dt) for numcar,cpk,dt in zip(numcars,cpks, dist_for_yr)] for numcars, cpks in zip(sample_model._data, yr_consumption_per_km)]
    total_consumption_unweighted_list = [[float(numcar)*1*float(cpk) for numcar,cpk,dt in zip(numcars,cpks, dist_for_yr)] for numcars, cpks in zip(sample_model._data, yr_consumption_per_km)]
    #print(total_passenger_kilometers)
    #totalvehicles = [float(numcars) for numcars in zip(sample_model._data)]
    #sumtotalvehicles = sum(sum(totalvehicles))
    annual_grams = sum(sum(total_consumption_grams,[]))
    total_travel = sum(sum(total_passenger_kilometers,[]))
    total_consumption_unweighted = sum(sum(total_consumption_unweighted_list,[]))
    #totalnumcars = get_counts(self)
    numlist = BaseModel.get_counts(self=sample_model)
    numcars = sum(sum(numlist,[]))
    emissions_intensity = annual_grams/(numcars)

    emissions_intensity_per_km = annual_grams/(total_travel)

    emissions_intensity_per_km_unweighted = total_consumption_unweighted/(numcars)
    
    print(numcars)

    print(f'{f_type} Emissions for year: {sample_model._year} = {annual_grams} grams_CO2')
    # em_dict.append({"year": str(sample_model._year), "grams_CO2" : {annual_grams})
    em_dict.append({"year": str(sample_model._year), "grams_CO2" : annual_grams, "number_cars":numcars, "g_per_car_average": emissions_intensity, "g_per_km_per_car_weighted": emissions_intensity_per_km, "g_per_km_per_car_unweighted":emissions_intensity_per_km_unweighted })

# this code outputs the year emissions to a csv
csv_file = f'model_output/{f_type}-gramsCO2{constants.name}.csv'
csv_columns = ["year","grams_CO2","number_cars","g_per_car_average", "g_per_km_per_car_weighted", "g_per_km_per_car_unweighted"]
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for year in em_dict:
        writer.writerow(year)

# total_consumption_grams = []
# # this for loop will run through a 14 length row 17 team times (per age)
# for numcars_per_age, cpks_per_age in zip(sample_model._data, yr_consumption_per_km):
#     row_per_age = []
#     # this for loop will run through every category on a row
#     for numcars_per_age_cat, cpks_per_age_cat, dist_for_yr_per_cat in zip(numcars_per_age,cpks_per_age, dist_for_yr):
#         row_per_age.append(float(cpks_per_age_cat)*float(cpks_per_age_cat)*float(dist_for_yr_per_cat)) 
#     total_consumption_grams.append(row_per_age)