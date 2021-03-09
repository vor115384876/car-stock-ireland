import sys
class constants:
    BASE_YEAR = 2007

    PETROL="petrol"
    DIESEL="diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
    PETROLPLUGIN = "petrolplugin"

    
    em_band = "emissions_bands"
    f_band = "efficiency_bands"
    r_factor = "on_road_factor"
    biofuel_percentage = "biofuel_energy_content"
    
    

    # change these
    f_type = PETROL
    scenario_type = 0

    #scenario 0 = actual sales and emissions
    #scenario 1 = counterfactual - sales similar proportions relative to EU/Ireland relationship prior to 2007

    baseline_d_travelled = "scenario_0_distance_travelled"
    baseline_path = "scenario_0"
    baseline_name = "-scenario_0"

    path = f'scenario_{scenario_type}'
    name = f'-scenario_{scenario_type}'
    d_travelled = f'scenario_{scenario_type}_distance_travelled'


         
    FUEL_CONSTANT = 1.065/1.325  if f_type is PETROL else 1.0344/1.183
    FUEL_ENERGY_CONSTANT = 251.9/3.6 if f_type is PETROL else 263.9/3.6
    
    start_year=2001
    end_year=2019
    
    BIOFUEL = True #set to True or False if you want to include Biofuel as a carbon reduction measure
 


