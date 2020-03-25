import csv
from constants import constants
from models.base_model import ConstantBaseModel
from models.base_model import BaseModel
from utils.generators import generate_constants, generate_year_models


f_type = constants.f_type


yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year, path=constants.path)

em_band = generate_constants(fuel_type=f_type, constant_type=constants.em_band)
rd_factor = generate_constants(fuel_type=f_type,constant_type=constants.r_factor)


dist_travelled = ConstantBaseModel(generate_constants(fuel_type=f_type,constant_type=constants.d_travelled))

new_rd_factor = [row[1:] for row in rd_factor]
new_em_band = [row[1:] for row in em_band]


consumption_per_km = [[(1+float(rf))*float(emb) for rf, emb in zip(r_fs, embs)] for r_fs, embs, in zip(new_rd_factor, new_em_band)]
#print(consumption_per_km)
consumption_per_km_no_orf = [[(1+0)*float(emb) for rf, emb in zip(r_fs, embs)] for r_fs, embs, in zip(new_rd_factor, new_em_band)]

taxvaluearray = [[]]
taxvaluearray_no_orf = [[]]
taxvalue = []
taxvalue_no = []

for year in consumption_per_km:
#check if year of registration is before 2008 if so, check engine cc of the group
#how do I store vintage from the arrays in the lists?

        # for engine_cc in year:

        #     if engine_cc < 1001:
        #         taxvalue.append(199)
        #     elif engine_cc < 1101:
        #         taxvalue.append(299)
        #     elif engine_cc < 1201:
        #         taxvalue.append(330)
        #     elif engine_cc < 1301:
        #         taxvalue.append(358)
        #     elif engine_cc < 1401:
        #         taxvalue.append(385)
        #     elif engine_cc < 1501:
        #         taxvalue.append(413)
        #     elif engine_cc < 1601:
        #         taxvalue.append(514)
        #     elif engine_cc < 1701:
        #         taxvalue.append(544)
        #     elif engine_cc < 1801:
        #         taxvalue.append(636)
        #     elif engine_cc < 1901:
        #         taxvalue.append(673)
        #     elif engine_cc < 2001:
        #         taxvalue.append(710)
        #     elif engine_cc < 2501:
        #         taxvalue.append((994))
        #         #value for median 2201 - 2301 selected
        #     elif engine_cc > 2501 :
        #         taxvalue.append(1443)
        #         #value for 2801 - 2900 selected
      

    taxvaluearray.append(taxvalue)

    for gkm in year:
    
        if gkm <= 0:
            taxvalue.append(120)
            break
        elif gkm <= 80:
            taxvalue.append(170)
            break
        elif gkm <= 100:
            taxvalue.append(180)
            break
        elif gkm <= 110:
            taxvalue.append(190)
            break
        elif gkm <= 120:
            taxvalue.append(200)
            break
        elif gkm <= 130:
            taxvalue.append(270)
            break
        elif gkm <= 140:
            taxvalue.append(280)
            break
        elif gkm <= 155:
            taxvalue.append(390)
            break
        elif gkm <= 170:
            taxvalue.append(570)
            break
        elif gkm <= 190:
            taxvalue.append(750)
            break
        elif gkm <= 225:
            taxvalue.append(1200)
            #break
        elif gkm > 225:
            taxvalue.append(2350)
            #break
            
#print(taxvaluearray)

for year in consumption_per_km_no_orf:
    taxvaluearray_no_orf.append(taxvalue_no)

    for gkm_no in year:
        
        if gkm_no <= 0:
            taxvalue_no.append(120)
            break
        elif gkm_no <= 80:
            taxvalue_no.append(170)
            break
        elif gkm_no <= 100:
            taxvalue_no.append(180)
            break
        elif gkm_no <= 110:
            taxvalue_no.append(190)
            break
        elif gkm_no <= 120:
            taxvalue_no.append(200)
            break
        elif gkm_no <= 130:
            taxvalue_no.append(270)
            break
        elif gkm_no <= 140:
            taxvalue_no.append(280)
            break
        elif gkm_no <= 155:
            taxvalue_no.append(390)
            break
        elif gkm_no <= 170:
            taxvalue_no.append(570)
            break
        elif gkm_no <= 190:
            taxvalue_no.append(750)
            break
        elif gkm_no <= 225:
            taxvalue_no.append(1200)
            break
        elif gkm_no > 225:
            taxvalue_no.append(2350)
            break


        # for engine_cc in year:

        #     if engine_cc < 1001:
        #         taxvalue.append(199)
        #     elif engine_cc < 1101:
        #         taxvalue.append(299)
        #     elif engine_cc < 1201:
        #         taxvalue.append(330)
        #     elif engine_cc < 1301:
        #         taxvalue.append(358)
        #     elif engine_cc < 1401:
        #         taxvalue.append(385)
        #     elif engine_cc < 1501:
        #         taxvalue.append(413)
        #     elif engine_cc < 1601:
        #         taxvalue.append(514)
        #     elif engine_cc < 1701:
        #         taxvalue.append(544)
        #     elif engine_cc < 1801:
        #         taxvalue.append(636)
        #     elif engine_cc < 1901:
        #         taxvalue.append(673)
        #     elif engine_cc < 2001:
        #         taxvalue.append(710)
        #     elif engine_cc < 2501:
        #         taxvalue.append((994))
        #         #value for median 2201 - 2301 selected
        #     elif engine_cc > 2501 :
        #         taxvalue.append(1443)
        #         #value for 2801 - 2900 selected




em_dict = []

#print(taxvaluearray_no_orf)
new_consumption_per_km = []
base_year = 1990
for row in consumption_per_km:
    new_consumption_per_km.append([base_year]+row)
    base_year += 1

constant_model = ConstantBaseModel(new_consumption_per_km)
for sample_model in yr_models:
    base_year = sample_model._year-17
    yr_consumption_per_km = []
    while base_year < sample_model._year:
        yr_consumption_per_km.append(constant_model.get_constant(year=base_year))
        base_year+=1
    dist_for_yr = dist_travelled.get_constant(year=sample_model._year)
    #breakpoint()
    total_revenue_amt = [[float(numcar)*1*float(taxvaluearray_no_orfss) for numcar,taxvaluearray_no_orfss in zip(numcars, taxvaluearray_no_orfs)] for numcars, taxvaluearray_no_orfs in zip(sample_model._data,taxvaluearray_no_orf)]
    numlist = BaseModel.get_counts(self=sample_model)
    numcars = sum(sum(numlist,[]))
    total_revenue_amt_with_on_road = [[float(numcar)*1*float(taxvaluearrayss) for numcar,taxvaluearrayss in zip(numcars, taxvaluearrays)] for numcars, taxvaluearrays in zip(sample_model._data,taxvaluearray)]
    #print(total_revenue_amt_with_on_road)
    annual_total_rev_amt =  sum(sum(total_revenue_amt,[]))
    annual_total_rev_amt_with_on_road = sum(sum(total_revenue_amt_with_on_road,[]))

    #print(annual_total_rev_amt)
    #print(annual_total_rev_amt_with_on_road) 

    print(f'{f_type} annual motor tax for year: {sample_model._year} = {annual_total_rev_amt}')
    print(f'{f_type} annual motor tax for year with orf: {sample_model._year} = {annual_total_rev_amt_with_on_road}')
 
    em_dict.append({"year": str(sample_model._year), "no_on_road" : annual_total_rev_amt, "number_cars":numcars, "with_on_road_factor": annual_total_rev_amt_with_on_road  })

# this code outputs the year emissions to a csv
csv_file = f'model_output/{f_type}-revenueforgone{constants.name}.csv'
csv_columns = ["year","no_on_road","number_cars","with_on_road_factor"]
with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for year in em_dict:
        writer.writerow(year)

