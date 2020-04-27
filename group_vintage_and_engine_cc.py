import csv
from constants import constants
from models.base_model import ConstantBaseModel
from models.base_model import BaseModel
from utils.generators import generate_constants, generate_year_models, generate_dist_models


engine_group_dict = []
f_type = constants.f_type
yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)

# small = range()


for index,sample_model in enumerate(yr_models):
    vintage_year = sample_model._year-17
    yr_consumption_per_km = []
    while vintage_year < sample_model._year:
        year = sample_model._year
        print("the year is"+str(year))
        vintage_year+=1
        
        print("the vintage is"+str(vintage_year))
        car_list = [numcars for numcars in sample_model._data]
        # print(car_list)
        vintage_year_word = vintage_year
        less_than_1300cc = []
        between_1300cc_and_1900cc = []
        greater_than_1900cc = []

        for year_row in car_list:

            print(year_row)
            
            less_than_1300cc.append(year_row[0] + year_row[1] + year_row[2] + year_row[3] + year_row[4])
            between_1300cc_and_1900cc.append(year_row[5] + year_row[6] + year_row[7]+ year_row[8] + year_row[9] + year_row[10])
            greater_than_1900cc.append(year_row[11] + year_row[12] + year_row[13])
            
        # print({"year": vintage_year_word, "<1300cc": less_than_1300cc, "1300cc - 1900cc": between_1300cc_and_1900cc, ">1900cc": greater_than_1900cc})
        engine_group_dict.append({"year": vintage_year_word, "<1300cc": less_than_1300cc, "1300cc - 1900cc": between_1300cc_and_1900cc, ">1900cc": greater_than_1900cc})
        vintage_year_number = vintage_year_word - 1
        print("")
        # print(engine_group_dict)

        csv_file = f'model_output/{f_type}/{sample_model._year}-vintage_grouped_engine_cc.csv'
        csv_columns = ["year","<1300cc","1300cc - 1900cc",">1900cc"]
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for year in engine_group_dict:
                writer.writerow(year)

        
#     car_list = [numcars for numcars in sample_model._data]
#     print(sample_model._year)
#     #print(car_list)
#     car_data = array(car_list)
#     print(car_data)
#     group_car_engine_cc = sum(car_data, 0)
#     less_than_1300cc = (group_car_engine_cc[0]+group_car_engine_cc[1]+group_car_engine_cc[2]+group_car_engine_cc[3] + group_car_engine_cc[4])
#     print(group_car_engine_cc)
#     #columns 0 - 4 (<1300cc, small)
#     between_1300cc_and_1900cc = group_car_engine_cc[5]+group_car_engine_cc[6]+group_car_engine_cc[7]+group_car_engine_cc[8]+group_car_engine_cc[9]+group_car_engine_cc[10]
#     #columns 5 - 10 (1300cc - 1900cc - medium)
#     greater_than_1900cc = (group_car_engine_cc[11] + group_car_engine_cc[12] + group_car_engine_cc[13])
#     #columns 11 - 13 (>1900cc - large)
#     engine_group_dict.append({"year": str(sample_model._year), "<1300cc": less_than_1300cc, "1300cc - 1900cc": between_1300cc_and_1900cc, ">1900cc": greater_than_1900cc})

# csv_file = f'model_output/{f_type}-grouped_vintage_and_engine_cc/{year}.csv'
# csv_columns = ["year","<1300cc","1300cc - 1900cc",">1900cc"]
# with open(csv_file, 'w', newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#     writer.writeheader()
#     for year in engine_group_dict:
#         writer.writerow(year)