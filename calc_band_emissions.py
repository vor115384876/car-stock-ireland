import csv
from constants import constants
from models.base_model import ConstantBaseModel
from utils.generators import generate_constants, generate_year_models





f_type = constants.f_type


yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)

em_band = generate_constants(fuel_type=f_type, constant_type=constants.em_band)
rd_factor = generate_constants(fuel_type=f_type,constant_type=constants.r_factor)


dist_travelled = ConstantBaseModel(generate_constants(fuel_type=f_type,constant_type=constants.d_travelled))

new_rd_factor = [row[1:] for row in rd_factor]
new_em_band = [row[1:] for row in em_band]
#breakpoint()
consumption_per_km = [[(1+float(fb))*float(rf) for fb, rf in zip(f_bs, r_fs)] for f_bs, r_fs in zip(new_rd_factor, new_em_band)]
new_consumption_per_km = []
#emissions bands are only recorded from 2004 onwards
base_year = 2004
for row in consumption_per_km:
    new_consumption_per_km.append([base_year]+row)
    base_year += 1

constant_model = ConstantBaseModel(new_consumption_per_km)


em_dict = []
for sample_model in yr_models:
    base_year = sample_model._year-3
    yr_consumption_per_km = []
    while base_year < sample_model._year:
        yr_consumption_per_km.append(constant_model.get_constant(year=base_year))
        base_year+=1
    dist_for_yr = dist_travelled.get_constant(year=sample_model._year)
    # [[print(float(numcar),float(cpk),float(dt)) for numcar,cpk,dt in zip(numcars,cpks, dist_for_yr)] for numcars, cpks in zip(sample_model._data, yr_consumption_per_km)]
     # [[print(float(numcar),float(cpk),float(dt)) for numcar,cpk,dt in zip(numcars,cpks, dist_for_yr)] for numcars, cpks in zip(sample_model._data, yr_consumption_per_km)]
    total_consumption_grams = [[float(numcar)*float(cpk)*float(dt) for numcar,cpk,dt in zip(numcars,cpks, dist_for_yr)] for numcars, cpks in zip(sample_model._data, yr_consumption_per_km)]
    annual_grams = sum(sum(total_consumption_grams,[]))
    
    print(f'{f_type} Emissions for year: {sample_model._year} = {annual_grams} grams_CO2')
   # em_dict.append({"year": str(sample_model._year), "grams_CO2" : {annual_grams})
    em_dict.append({"year": str(sample_model._year), "grams_CO2" : annual_grams})

# this code outputs the year emissions to a csv
csv_file = f'model_output/{f_type}-gramsCO2{constants.name}.csv'
csv_columns = ["year","grams_CO2"]
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for year in em_dict:
        writer.writerow(year)