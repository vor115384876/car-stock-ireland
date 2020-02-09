from constants import constants
import sys

def get_sales_percentage(fuel_type, year):
    base_sales_petrol = 0.71
    if constants.scenario_type is 1: 
        new_sales_percentage_petrol = base_sales_petrol   
    elif constants.scenario_type is 2: 
        new_sales_percentage_petrol = base_sales_petrol- 0.03*(year - constants.BASE_YEAR)
        print(new_sales_percentage_petrol)
    else:
        sys.exit("Undefined scenarios, entered new_scenario.py and get_sales_percentage.py without scenario 1 or 2 set to True")
    result = new_sales_percentage_petrol if fuel_type is constants.PETROL else 1-new_sales_percentage_petrol
    return result
