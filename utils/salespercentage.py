from constants import constants

def get_sales_percentage(fuel_type, year, scenario_2=False):
    base_sales_petrol = 0.71
    if scenario_2:
        new_sales_percentage_petrol = base_sales_petrol- 0.03*(year - 2007)
    else:
        new_sales_percentage_petrol = base_sales_petrol
    result = new_sales_percentage_petrol if fuel_type is constants.PETROL else 1-new_sales_percentage_petrol
    print(f'fuel: {fuel_type}, year:{year}, scenario2={scenario_2}, {result}')
    return result
