from constants import constants
from utils.generators import generate_year_models

f_type = constants.f_type

yr_models = generate_year_models(fuel_type=f_type, start_year=constants.start_year,end_year=constants.end_year)

def calc_survival_rate(year_models, age:int, cat):
    s_rates = []
    for index, model in enumerate(year_models[:-1]):
        next_model = year_models[index+1]
        old_pop = model.get_counts(age=age, cat=cat)
        new_pop = next_model.get_counts(age=age+1, cat=cat)
        s_rate = new_pop/old_pop if old_pop != 0 else 1
        # if s_rate > 5:
        #     print(f'new_pop: {new_pop} over old_pop: {old_pop}')
        #     print(age,cat, s_rate)
        s_rates.append(s_rate)
    s_rates.sort()
    trimmed_s_rates = s_rates[:-2]
    return trimmed_s_rates

sr = calc_survival_rate(yr_models, 11, 11)
print(sum(sr)/len(sr))

    