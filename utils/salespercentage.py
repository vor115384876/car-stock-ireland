from constants import constants
import sys

breakpoint()
def get_sales_percentage(fuel_type, year, scenario_1, scenario_2):
    breakpoint()
    base_sales_petrol = 0.71
    if scenario_1 == True: 
        new_sales_percentage = base_sales_petrol
        
    elif scenario_2 == True:
        new_sales_percentage_petrol = base_sales_petrol- 0.03*(year - constants.BASE_YEAR)
        print(new_sales_percentage_petrol)
    else:
        sys.exit("Undefined scenarios, entered new_scenario.py and get_sales_percentage.py without scenario 1 or 2 set to True")
        
    result = new_sales_percentage_petrol if f_type is constants.PETROL else 1-new_sales_percentage_petrol
    print(f'fuel: {f_type}, year:{year}, scenario2={scenario_2}, {result}')
    return result
