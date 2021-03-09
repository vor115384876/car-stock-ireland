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
        less_than_900cc = year_row[1]
        between_900cc_and_1200cc = (year_row[2]+year_row[3]+year_row[4])/3
        between_1200cc_and_1500cc =(year_row[5]+year_row[6] + year_row[7])/3
        between_1500cc_and_1700cc = (year_row[8]+year_row[9])/2
        between_1700cc_and_1900cc = (year_row[10]+year_row[11])/2
        between_1900_and_2000cc = year_row[12]
        greater_than_2000cc = (year_row[13]+year_row[14])/2
    
        em_dict.append({"year": year, "900" : less_than_900cc, "900-1200" : between_900cc_and_1200cc, "1200-1500" : between_1200cc_and_1500cc, "1500-1700": between_1500cc_and_1700cc, "1700-1900": between_1700cc_and_1900cc, "1900-2100": between_1900_and_2000cc, "2100": greater_than_2000cc})

else:
    print("Fuel efficiencies available for petrol and diesel only.")
    
# this code outputs the year emissions to a csv
csv_file = f'leap_transport_inputs/{f_type}_fuel_efficiencies_grouped_engine_cc.csv'
csv_columns = ["year","900","900-1200","1200-1500","1500-1700", "1700-1900", "1900-2100", "2100"]
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for year in em_dict:
        writer.writerow(year)