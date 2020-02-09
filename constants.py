import sys
class constants:
    BASE_YEAR = 2007

    PETROL="petrol"
    DIESEL="diesel"
    
    f_band = "efficiency_bands"
    r_factor = "on_road_factor"
    
    

    # change these
    f_type = PETROL
    scenario_type = 1

    baseline_d_travelled = "scenario_0_distance_travelled"
    baseline_path = "scenario_0"
    baseline_name = "-scenario_0"

    path = f'scenario_{scenario_type}'
    name = f'-scenario_{scenario_type}'
    d_travelled = f'scenario_{scenario_type}_distance_travelled'
    # scenario_1 = False
    # scenario_2 = True
    # if scenario_1 == True & scenario_2 == True:
    #     sys.exit("Error in constants.py, cannot have two scenarios running at the same time, set one to False")

         

    
    start_year=2001
    end_year=2019


    FUEL_CONSTANT = 1.065/1.325  if f_type is PETROL else 1.0344/1.183
    FUEL_ENERGY_CONSTANT = 251.9/3.6 if f_type is PETROL else 263.9/3.6


