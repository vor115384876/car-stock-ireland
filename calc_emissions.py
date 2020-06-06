import csv
from constants import constants
from models.base_model import ConstantBaseModel
from utils.generators import generate_constants, generate_year_models, generate_dist_models




biofuel = constants.BIOFUEL
f_type = constants.f_type
print(f_type)

yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)

dist_models = generate_dist_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)

eff_band = generate_constants(fuel_type=f_type,constant_type=constants.f_band)
rd_factor = generate_constants(fuel_type=f_type,constant_type=constants.r_factor)

if f_type == 'petrol':
    bio_fuel_dict = {2001: 0, 2002:0, 2003: 0, 2004:0, 2005:0, 2006:0, 2007:0, 2008:0, 2009:0, 2010:0.018, 2011: 0.034, 2012: 0.036, 2013: 0.039, 2014: 0.039, 2015: 0.046, 2016: 0.053, 2017: 0.054, 2018: 0.055}

if f_type == 'diesel':
    bio_fuel_dict = {2001: 0, 2002:0, 2003: 0, 2004:0, 2005:0, 2006:0, 2007:0, 2008:0, 2009:0, 2010:0.027, 2011: 0.038, 2012: 0.03, 2013: 0.038, 2014: 0.044, 2015: 0.044, 2016: 0.036, 2017: 0.054, 2018: 0.05}

print(bio_fuel_dict)
#need to figure out a way to chance how the distances are stored
new_rd_factor = [row[1:] for row in rd_factor]
new_eff_band = [row[1:] for row in eff_band]



#breakpoint()
consumption_per_km = [[((1+float(fb))*float(rf))/100 for fb, rf in zip(f_bs, r_fs)] for f_bs, r_fs in zip(new_rd_factor, new_eff_band)]
#print(bio_reduction)
#print(consumption_per_km)
new_consumption_per_km = []

base_year = 1990
for row in consumption_per_km:
    new_consumption_per_km.append([base_year]+row)
    base_year += 1
    

constant_model = ConstantBaseModel(new_consumption_per_km)


em_dict = []
for index,sample_model in enumerate(yr_models):
    #do i need to create another for loop to go through the distances?
    base_year = sample_model._year-17
    yr_consumption_per_km = []
    while base_year < sample_model._year:
        yr_consumption_per_km.append(constant_model.get_constant(year=base_year))
        base_year+=1
    
    dist_for_yr = dist_models[index]._data
    # [[print(float(numcar),float(cpk),float(dt)) for numcar,cpk,dt in zip(numcars,cpks, dist_for_yr)] for numcars, cpks in zip(sample_model._data, yr_consumption_per_km)]
    total_consumption_lt = [[float(numcar)*float(cpk)*float(dt) for numcar,cpk,dt in zip(numcars,cpks, dist_for_yr_cat)] for numcars, cpks, dist_for_yr_cat in zip(sample_model._data, yr_consumption_per_km, dist_for_yr)]
    annual_lt = sum(sum(total_consumption_lt,[]))
    total_consumption_kgo = [[j*constants.FUEL_CONSTANT for j in i] for i in total_consumption_lt]
    energy_consumption = [[j*42 for j in i] for i in total_consumption_kgo]
    total_ec = sum([sum(i) for i in energy_consumption])
  
    emissions = [[j*constants.FUEL_ENERGY_CONSTANT for j in i] for i in energy_consumption]
    total_em = sum(sum(emissions,[]))
    total_bio_em = total_em*(1- bio_fuel_dict[base_year])
    print(base_year)
    print('non bio')
    print('biofuel')
    print(total_em)
    print(total_bio_em)

    total_em_in_kt = total_em/1000000000
    total_biofuel_em_in_kt = total_bio_em/1000000000
    #print(f'{f_type} Emissions for year: {sample_model._year} = {total_em_in_kt} kilotonnes, "consumption in MJ": {total_ec}, "consumption in liters": {annual_lt}')
    em_dict.append({"year": str(sample_model._year), "emission" : total_em_in_kt, "emission with biofuel" : total_biofuel_em_in_kt, "consumption in MJ": total_ec, "consumption in liters":annual_lt})

# this code outputs the year emissions to a csv
csv_file = f'model_output/{f_type}-emissions{constants.name}.csv'
csv_columns = ["year","emission", "emission with biofuel","consumption in MJ", "consumption in liters"]
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for year in em_dict:
        writer.writerow(year)