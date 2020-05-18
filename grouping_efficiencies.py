import csv
from constants import constants
from models.base_model import ConstantBaseModel
from models.base_model import BaseModel
from utils.generators import generate_constants, generate_year_models, generate_dist_models, list_prod


f_type = constants.f_type

yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)
eff_band = generate_constants(fuel_type=f_type,constant_type=constants.f_band)

print(eff_band)
eff_band.sort(reverse = True)

#vehicle stock 0 - 14 } aggregate 1-5, 5-11, 12-14
#distance 0-4 {sum of (vehicle stock (0)*eff band (0))+vehicle stock (1) *eff band (1) +.../(sum of total vehicle stock in group 0 - 4)}


em_dict = []

if f_type == 'diesel' or 'petrol':
    for year_row in eff_band:
        year_row = list(map(float, year_row))
        year = year_row[0]
        less_than_1300cc = (year_row[1]+year_row[2]+year_row[3]+year_row[4]+year_row[5])/5
        between_1300cc_and_1900cc = (year_row[6]+year_row[7]+year_row[8]+year_row[10]+year_row[11])/6
        more_than_1900cc = (year_row[12]+year_row[13]+year_row[14])/3
    
        em_dict.append({"year": year, "<1300cc" : less_than_1300cc, "1300cc - 1900cc" : between_1300cc_and_1900cc, ">1900cc" : more_than_1900cc})

else:
    print("Fuel efficiencies available for petrol and diesel only.")
    
# this code outputs the year emissions to a csv
csv_file = f'model_output/{f_type}/fuel_efficiencies_grouped/fuel_efficiencies_grouped_engine_cc.csv'
csv_columns = ["year","<1300cc","1300cc - 1900cc",">1900cc"]
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for year in em_dict:
        writer.writerow(year)