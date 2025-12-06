# Star Schema for Energy BI Project

## Dimensions
### DimPlant
- plant_id (PK)
- plant_name
- region
- energy_type

### DimDate
- date (PK)
- year
- quarter
- month
- day
- day_of_week

## Facts
### FactEnergyProduction
- date (FK)
- plant_id (FK)
- mwh_produced

### FactDistrictHeating
- date (FK)
- plant_id (FK)
- heating_produced_mwh
- heating_consumed_mwh

### FactCO2Emissions
- date (FK)
- plant_id (FK)
- co2_kg
