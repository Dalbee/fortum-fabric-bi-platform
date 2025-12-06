Total MWh Produced = SUM(FactEnergyProduction[mwh_produced])

Total CO2 (kg) = SUM(FactCO2Emissions[co2_kg])

CO2 Intensity (kg/MWh) =
DIVIDE(
    [Total CO2 (kg)],
    [Total MWh Produced],
    0
)

Total Heating Produced = SUM(FactDistrictHeating[heating_produced_mwh])

Total Heating Consumed = SUM(FactDistrictHeating[heating_consumed_mwh])

Heating Balance (MWh) =
[Total Heating Produced] - [Total Heating Consumed]

Renewable Contribution (%) =
DIVIDE(
    CALCULATE([Total MWh Produced], DimPlant[energy_type] = "Renewable"),
    [Total MWh Produced],
    0
)

YoY Production Change (%) =
DIVIDE(
    [Total MWh Produced] - CALCULATE([Total MWh Produced], DATEADD(DimDate[date], -1, YEAR)),
    CALCULATE([Total MWh Produced], DATEADD(DimDate[date], -1, YEAR))
)
