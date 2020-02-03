import csv
from constants import constants
from models.base_model import ConstantBaseModel
from utils.generators import generate_constants, generate_year_models


f_type = constants.PETROL

simulation = True

if simulation is True:
    path = "new_models"
    dist = constants.new_d_travelled
    name = "-sim"
else:
    path = None
    dist = constants.d_travelled
    name = ""


yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=path)
eff_band = generate_constants(fuel_type=f_type,constant_type=constants.f_band)
rd_factor = generate_constants(fuel_type=f_type,constant_type=constants.r_factor)


dist_travelled = ConstantBaseModel(generate_constants(fuel_type=f_type,constant_type=dist))

new_rd_factor = [row[1:] for row in rd_factor]
new_eff_band = [row[1:] for row in eff_band]

consumption_per_km = [[((1+float(fb))*float(rf))/100 for fb, rf in zip(f_bs, r_fs)] for f_bs, r_fs in zip(new_rd_factor, new_eff_band)]
new_consumption_per_km = []

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
    # [[print(float(numcar),float(cpk),float(dt)) for numcar,cpk,dt in zip(numcars,cpks, dist_for_yr)] for numcars, cpks in zip(sample_model._data, yr_consumption_per_km)]
    total_consumption_lt = [[float(numcar)*float(cpk)*float(dt) for numcar,cpk,dt in zip(numcars,cpks, dist_for_yr)] for numcars, cpks in zip(sample_model._data, yr_consumption_per_km)]
    total_consumption_kgo = [[j*constants.FUEL_CONSTANT for j in i] for i in total_consumption_lt]
    energy_consumption = [[j*42 for j in i] for i in total_consumption_kgo]
    total_ec = sum([sum(i) for i in energy_consumption])
    emissions = [[j*constants.FUEL_ENERGY_CONSTANT for j in i] for i in energy_consumption]
    total_em = sum(sum(emissions,[]))
    total_em_in_kt = total_em/1000000000
    print(f'{f_type} Emissions for year: {sample_model._year} = {total_em_in_kt} kilotonnes, "consumption": {total_ec}')
    em_dict.append({"year": str(sample_model._year), "emission" : total_em_in_kt, "consumption": total_ec})

# this code outputs the year emissions to a csv
csv_file = f'model_output/{f_type}-emissions{name}.csv'
csv_columns = ["year","emission", "consumption"]
with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for year in em_dict:
        writer.writerow(year)