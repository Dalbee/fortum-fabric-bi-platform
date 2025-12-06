# Notebook: transform_energy_data
# Purpose: Transform raw energy datasets into curated Lakehouse tables for reporting.

from pyspark.sql import functions as F

# -------------------------------------------------------------------
# 1. Load raw tables
# -------------------------------------------------------------------

raw_energy = spark.read.table("raw.FactEnergyProduction")
raw_heating = spark.read.table("raw.FactDistrictHeating")
raw_co2 = spark.read.table("raw.FactCO2Emissions")
dim_date = spark.read.table("raw.DimDate")
dim_plant = spark.read.table("raw.DimPlant")

# -------------------------------------------------------------------
# 2. Clean and standardise key fields
# -------------------------------------------------------------------

raw_energy = (
    raw_energy
    .withColumn("date", F.to_date("date"))
    .withColumn("mwh_produced", F.col("mwh_produced").cast("double"))
)

raw_heating = (
    raw_heating
    .withColumn("date", F.to_date("date"))
    .withColumn("heating_produced_mwh", F.col("heating_produced_mwh").cast("double"))
    .withColumn("heating_consumed_mwh", F.col("heating_consumed_mwh").cast("double"))
)

raw_co2 = (
    raw_co2
    .withColumn("date", F.to_date("date"))
    .withColumn("co2_kg", F.col("co2_kg").cast("double"))
)

# -------------------------------------------------------------------
# 3. Create curated Dimension tables
# -------------------------------------------------------------------

curated_dim_date = (
    dim_date
    .dropDuplicates(["date"])
)

curated_dim_plant = (
    dim_plant
    .dropDuplicates(["plant_id"])
)

# -------------------------------------------------------------------
# 4. Build curated FactEnergyDaily
# -------------------------------------------------------------------

fact_energy_daily = (
    raw_energy
    .join(curated_dim_date, on="date", how="inner")
    .join(curated_dim_plant, on="plant_id", how="inner")
)

# -------------------------------------------------------------------
# 5. Build curated FactHeatingDaily
# -------------------------------------------------------------------

fact_heating_daily = (
    raw_heating
    .join(curated_dim_date, on="date", how="inner")
    .join(curated_dim_plant, on="plant_id", how="inner")
    .withColumn(
        "heating_balance_mwh",
        F.col("heating_produced_mwh") - F.col("heating_consumed_mwh")
    )
)

# -------------------------------------------------------------------
# 6. Build curated FactCO2Daily with intensity metric
# -------------------------------------------------------------------

# Join emissions with production to compute intensity
fact_co2_daily = (
    raw_co2.alias("c")
    .join(
        raw_energy.alias("e"),
        on=["date", "plant_id"],
        how="inner"
    )
    .join(curated_dim_date.alias("d"), on="date", how="inner")
    .join(curated_dim_plant.alias("p"), on="plant_id", how="inner")
    .select(
        F.col("c.date"),
        F.col("c.plant_id"),
        F.col("c.co2_kg"),
        F.col("e.mwh_produced"),
        (F.col("c.co2_kg") / F.col("e.mwh_produced")).alias("co2_intensity_kg_per_mwh")
    )
)

# -------------------------------------------------------------------
# 7. Add renewable / non-renewable flags
# -------------------------------------------------------------------

renewable_sources = ["Wind", "Solar", "Hydro", "Biomass"]

fact_energy_daily = fact_energy_daily.withColumn(
    "is_renewable",
    F.when(F.col("energy_source").isin(renewable_sources), F.lit(True)).otherwise(F.lit(False))
)

# -------------------------------------------------------------------
# 8. Write curated tables back to Lakehouse
#     (Adjust database / Lakehouse name as needed, e.g. 'lh_energy')
# -------------------------------------------------------------------

target_db = "curated"

(
    fact_energy_daily
    .write.mode("overwrite")
    .format("delta")
    .saveAsTable(f"{target_db}.FactEnergyDaily")
)

(
    fact_heating_daily
    .write.mode("overwrite")
    .format("delta")
    .saveAsTable(f"{target_db}.FactHeatingDaily")
)

(
    fact_co2_daily
    .write.mode("overwrite")
    .format("delta")
    .saveAsTable(f"{target_db}.FactCO2Daily")
)

(
    curated_dim_date
    .write.mode("overwrite")
    .format("delta")
    .saveAsTable(f"{target_db}.DimDate")
)

(
    curated_dim_plant
    .write.mode("overwrite")
    .format("delta")
    .saveAsTable(f"{target_db}.DimPlant")
)

# -------------------------------------------------------------------
# 9. Optional: basic data quality checks (row counts)
# -------------------------------------------------------------------

print("Raw Energy rows:", raw_energy.count())
print("Curated FactEnergyDaily rows:", fact_energy_daily.count())
print("Curated FactCO2Daily rows:", fact_co2_daily.count())
