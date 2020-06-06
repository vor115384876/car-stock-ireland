import csv
from utils.salespercentage import get_sales_percentage
from models.base_model import BaseModel
from constants import constants
from models.base_model import ConstantBaseModel
from utils.generators import generate_constants, generate_year_models, list_prod, get_model_by_year





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

dist_dict = []
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
    annual_passenger_kilometers = sum(total_passenger_kilometers,[])
   # print(annual_passenger_kilometers)
    annual_pkm = list(map(int, annual_passenger_kilometers))
    print(annual_pkm)

PATH = constants.path
fuel_type = constants.f_type
year = base_year
readfile = f'{PATH}/{fuel_type}/average_distance_engine_cc/scenario_0_distance_travelled.csv'

# #opening a file of all the years
num_car_year = 0
for year in range(2001,2018):
    readfile = f'{PATH}/{fuel_type}/{year}.csv'
    with open(readfile, newline='', encoding='utf-8-sig') as ff:
        data = [row for row in csv.reader(ff)]
    
    readfile = f'{PATH}/{fuel_type}/average_distance_engine_cc/scenario_0_distance_travelled.csv'
    with open(readfile, newline='', encoding='utf-8-sig') as f:
            enginecc = [row for row in csv.reader(f)]
        #opens the 2001.csv car stock file and reads the first stock. This also needs to be put into a loop
    total_engine_cc_stock_for_year = 0
        #how do i change the range to automatically index to vertical length of csv file
    for yearrow in range(1,18):
        average_distance_list = []
        vehicle_stock_by_engine_cc = []   
        for enginecol in range(1,15):
            engine_cc_list = int(data[yearrow][enginecol])
            #adds up all the items in the 900cc engine band
            total_engine_cc_stock_for_year += engine_cc_list
            #print(total_engine_cc_stock_for_year)
            
            average_distance_for_engine_cc = enginecc[(year- 2000)][enginecol]
            
            average_distance_list.append(int(average_distance_for_engine_cc))
        
    engineccpklist = []
for listyear in average_distance_list:
    for engine_cc_mileage_average in average_distance_list:
        engineccpkitem = engine_cc_mileage_average*total_engine_cc_stock_for_year
        engineccpklist.append(engineccpkitem)
