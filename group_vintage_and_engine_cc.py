import csv
from constants import constants
from models.base_model import ConstantBaseModel
from models.base_model import BaseModel
from utils.generators import generate_constants, generate_year_models, generate_dist_models


engine_group_dict = []
f_type = constants.f_type
yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)


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
            
        engine_group_dict.append({"year": vintage_year_word, "<1300cc": less_than_1300cc, "1300cc - 1900cc": between_1300cc_and_1900cc, ">1900cc": greater_than_1900cc})
        vintage_year_number = vintage_year_word - 1
        print("")

        csv_file = f'model_output/{f_type}/{sample_model._year}-vintage_grouped_engine_cc.csv'
        csv_columns = ["year","<1300cc","1300cc - 1900cc",">1900cc"]
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for year in engine_group_dict:
                writer.writerow(year)
