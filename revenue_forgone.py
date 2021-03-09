import csv
from constants import constants
from models.base_model import ConstantBaseModel
from models.base_model import BaseModel
from utils.generators import generate_constants, generate_year_models


f_type = constants.f_type
scenario_no = constants.scenario_type

yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)

em_band = generate_constants(fuel_type=f_type, constant_type=constants.em_band)
rd_factor = generate_constants(fuel_type=f_type,constant_type=constants.r_factor)


dist_travelled = ConstantBaseModel(generate_constants(fuel_type=f_type,constant_type=constants.d_travelled))

new_rd_factor = [row[1:] for row in rd_factor]
new_em_band = [row[1:] for row in em_band]


consumption_per_km = [[(1+float(rf))*float(emb) for rf, emb in zip(r_fs, embs)] for r_fs, embs, in zip(new_rd_factor, new_em_band)]

consumption_per_km_no_orf = [[float(emb) for emb in embs] for embs in new_em_band]

pre_2008_tax_value =[199,299,330,358,385,413,514,544,636,673,710,994,1443]
em_tax_dict = {0:120,80:170,100:180,110:190,120:200,130:270,140:280,155:390,170:570,190:750,225:1200,1000:2350} 

em_dict = []
def get_tax_values(vintage, with_rf):
    if vintage >= 2008: #change this between 2008 / 2020 for inclusion of new tax rate / exclusion of new tax rate
        tax_values = []
        if with_rf:
            consumption_pkm = consumption_per_km
        else:
            consumption_pkm = consumption_per_km_no_orf

        gkm_list = consumption_pkm[(vintage - 1990)]
        
        for gkm in gkm_list:
            tax_values.append(em_tax_dict[next(x for x in em_tax_dict if x > gkm)])
        return tax_values
    else:
        return pre_2008_tax_value


for model in yr_models:
    taxvalue = []
    taxvalue_no = []
    for age in range(0,16):
        vintage = model.get_car_year(age)
        taxvalue.append(get_tax_values(vintage=vintage,with_rf=True))
        taxvalue_no.append(get_tax_values(vintage=vintage,with_rf=False))
    total_revenue_amt = [[car_count*tax for car_count, tax in zip(car_row, tax_row)] for car_row, tax_row in zip(model._data,taxvalue)]
    total_revenue_amt_norf = [[car_count*tax for car_count, tax in zip(car_row, tax_row)] for car_row, tax_row in zip(model._data,taxvalue_no)]
    annual_total_rev_amt =  sum(sum(total_revenue_amt,[]))
    annual_total_rev_amt_norf =  sum(sum(total_revenue_amt_norf,[]))
    print(f'{f_type} annual motor tax for year: {model._year} = {annual_total_rev_amt}')
    print(f'{f_type} annual motor tax for year no orf: {model._year} = {annual_total_rev_amt_norf}')
    em_dict.append({"year": model._year, "no_on_road" : annual_total_rev_amt_norf, "with_on_road_factor": annual_total_rev_amt  })

#this code outputs the year emissions to a csv
csv_file = f'model_output/{f_type}-revenueforgone{constants.name}-scenario{scenario_no}.csv'
csv_columns = ["year","no_on_road","with_on_road_factor"]
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for year in em_dict:
        writer.writerow(year)
