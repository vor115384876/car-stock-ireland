import csv
from models.base_model import BaseModel, ConstantBaseModel


PETROL="petrol"
DIESEL="diesel"

# change these
f_type = DIESEL
start_year=2001
end_year=2019



FUEL_CONSTANT = 1.065/1.325  if f_type is PETROL else 1.0344/1.183
FUEL_ENERGY_CONSTANT = 251.9/3.6 if f_type is PETROL else 263.9/3.6

f_band = "efficiency_bands"
r_factor = "on_road_factor"
d_travelled = "distance_travelled"

def generate_year_models(fuel_type,start_year,end_year):
    model_list = []
    for year in range(start_year,end_year):
        print(f'Opening the file: {year}.csv for fuel type: {fuel_type}')
        file_name = f'year_model_inputs/{fuel_type}/{year}.csv'
        with open(file_name, newline='', encoding='utf-8-sig') as f:
            reader = list(csv.reader(f))
            temp = list()
            for row in reader[1:]:
                temp.insert(0,row[1:])
            model_list.append(BaseModel(year, temp))
    return model_list


def generate_constants(fuel_type,constant_type):
    print(f'Opening the file: {constant_type}.csv for fuel type: {fuel_type}')
    file_name = f'static_constants/{fuel_type}/{constant_type}.csv'
    with open(file_name, newline='', encoding='utf-8-sig') as f:
        reader = list(csv.reader(f))
    return reader

yr_models = generate_year_models(fuel_type=f_type, start_year=start_year,end_year=end_year)
eff_band = generate_constants(fuel_type=f_type,constant_type=f_band)
rd_factor = generate_constants(fuel_type=f_type,constant_type=r_factor)

dist_travelled = ConstantBaseModel(generate_constants(fuel_type=f_type,constant_type=d_travelled))

new_rd_factor = [row[1:] for row in rd_factor]
new_eff_band = [row[1:] for row in eff_band]

# line below prints the (1+rf)*eb matrix (fuel efficiency)
# [[print(f'(1+rf:{fb})*ef{rf}') for fb, rf in zip(f_bs, r_fs)] for f_bs, r_fs in zip(new_rd_factor, new_eff_band)]

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

    # this code outputs the fuel efficiency to a csv
    # csv_file = f'output/{sample_model._year}-yr_consumption_per_km.csv'
    # with open(csv_file, 'w') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerows(yr_consumption_per_km)

    # this code outputs the car count fot the year to a csv
    # csv_file = f'output/{sample_model._year}-carcounts.csv'
    # with open(csv_file, 'w') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerows(sample_model._data)


    dist_for_yr = dist_travelled.get_constant(year=sample_model._year)
    total_consumption_lt = [[float(numcar)*float(cpk)*float(dt) for numcar,cpk,dt in zip(numcars,cpks, dist_for_yr)] for numcars, cpks in zip(sample_model._data, yr_consumption_per_km)]
    
    total_consumption_kgo = [[j*FUEL_CONSTANT for j in i] for i in total_consumption_lt]
    energy_consumption = [[j*42 for j in i] for i in total_consumption_kgo]
    emissions = [[j*FUEL_ENERGY_CONSTANT for j in i] for i in energy_consumption]
    total_em = sum(sum(emissions,[]))
    total_em_in_kt = total_em/1000000000
    print(f'{f_type} Emissions for year: {sample_model._year} = {total_em_in_kt} kilotonnes')
    em_dict.append({"year": str(sample_model._year), "emission" : total_em_in_kt})

# this code outputs the year emissions to a csv
csv_file = f'output/{f_type}-emissions.csv'
csv_columns = ["year","emission"]
with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for year in em_dict:
        writer.writerow(year)
