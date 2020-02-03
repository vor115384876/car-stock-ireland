class constants:
    BASE_YEAR = 2007

    PETROL="petrol"
    DIESEL="diesel"
    scenario_2 = False

    # change these
    f_type = DIESEL
    start_year=2001
    end_year=2019


    FUEL_CONSTANT = 1.065/1.325  if f_type is PETROL else 1.0344/1.183
    FUEL_ENERGY_CONSTANT = 251.9/3.6 if f_type is PETROL else 263.9/3.6


    f_band = "efficiency_bands"
    r_factor = "on_road_factor"
    d_travelled = "distance_travelled"
    new_d_travelled = "new_distance_travelled"