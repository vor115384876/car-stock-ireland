# Car stock model scenario analysis

This project has 3 primary components.

- `Emmissions Calculations`: TODO
- `Car count scenario generation`: TODO
- `Distance reweighting scenario generation`: TODO

## Supported scenarios:

This project currently has 3 supported scenarios.

- `Baseline Scenario`: Emissions are calculated off real scenario.
- `No diesel uptake`: Scenario assumes diesel and petrol car split remains at 2007 levels (71% Petrol sales, 29% Diesel sales)
- `Reduced diesel uptake`: Scenario assumes diesel and petrol car split at 2007 levels (71% Petrol sales, 29% Diesel sales), with a 3% shift from Petrol to Diesel every year post 2007.

## Calculating the emmsions for a scenario

For the baseline: set the `scenario_type` in `constants.py` to `0` and run the `calc_emissions.py` script.

For scenario X: set the `scenario_type` in `constants.py` to `X`. Then run `new_scenario.py`. Then run `reweighter.py`. Finally run `calc_emissions.py`.
    scenario 0 = actual sales and emissions
    scenario 1 = no growth
    scenario 2 = 3% diesel sale growth
    scenario 3 = 2% diesel sale growth
    scenario 4 = 1% diesel sale growth