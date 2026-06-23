# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "a2cf5112-d7cc-44e2-bd1f-0e270656104e",
# META       "default_lakehouse_name": "LH_CustomerChurnETL",
# META       "default_lakehouse_workspace_id": "a298258a-25c5-47b7-b809-d2c4b6246ebf",
# META       "known_lakehouses": [
# META         {
# META           "id": "a2cf5112-d7cc-44e2-bd1f-0e270656104e"
# META         }
# META       ]
# META     },
# META     "environment": {
# META       "environmentId": "d7a13147-0ca4-b54c-48da-38ee5e544dcb",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Data Transformation in Silver Layer

# MARKDOWN ********************

# ## 00 Import packages and create loading_enriched_table

# CELL ********************

from pyspark.sql.functions import *
from pyspark.sql.types import *
from delta.tables import *

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def loading_enriched_table(df_source, target_table, candidate_key):
    try:
        deltaTable = DeltaTable.forName(spark, target_table)
    except Exception:
        try:
            df_source.write.format("delta").mode("overwrite").option("delta.columnMapping.mode", "name").saveAsTable(f"{target_table}")
        except Exception as e:
            print(f":Load for table {target_table} failed with error: {str(e)}")
            raise
        return
    
    try:
        match_condition = " AND ".join([f"target.`{col}` = source.`{col}`" for col in candidate_key])

        change_detection_columns = [col for col in df_source.columns if col not in candidate_key]
        update_condition = " OR ".join([f"target.`{col}` != source.`{col}`" for col in change_detection_columns])
        update_expressions = {col: f"source.`{col}`" for col in df_source.columns}

        merge_operation = deltaTable.alias("target").merge(
            source=df_source.alias("source"),
            condition=match_condition
        ).whenMatchedUpdate(
            condition=update_condition,
            set=update_expressions
        ).whenNotMatchedInsertAll()

        merge_operation.execute()
    except Exception as e:
        print(f"Insert operation for table {target_table} failed with error: {str(e)}")
    return

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 01 Data Transformation for LH_CustomerChurnETL.silver.customer_churn_enriched

# MARKDOWN ********************

# ### 01-1 Get the LH_CustomerChurnETL.bronze.customer_churn table

# CELL ********************

df = spark.read.table("LH_CustomerChurnETL.bronze.customer_churn")

display(df.limit(20))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 01-2 Rename the columns from the DataFrame

# CELL ********************

df_renamed = df.select(
    col("Customer ID").cast(StringType()).alias("Customer ID"),
    col("Churn Label").cast(StringType()).alias("Is Churn"),
    col("Account Length (in months)").cast(LongType()).alias("Account Length Months"),
    col("Local Calls").cast(LongType()).alias("Local Calls"),
    col("Local Mins").cast(DoubleType()).alias("Local Mins"),
    col("Intl Calls").cast(LongType()).alias("International Calls"),
    col("Intl Mins").cast(DoubleType()).alias("International Mins"),
    col("Intl Active").cast(StringType()).alias("Is International Calls Active"),
    # Replace inconsistent values in Intl Plan column
    when(
        col("Intl Plan") == "yes",
        lit("Yes")
    ).when(
        col("Intl Plan") == "no",
        lit("No")
    ).cast(StringType()).alias("Is International Plan"),
    col("Extra International Charges").cast(DoubleType()).alias("Extra International Charges"),
    col("Customer Service Calls").cast(LongType()).alias("Customer Service Calls"),
    col("Avg Monthly GB Download").cast(LongType()).alias("Avg Monthly GB Download"),
    col("Unlimited Data Plan").cast(StringType()).alias("Is Unlimited Data Plan"),
    col("Extra Data Charges").cast(DoubleType()).alias("Extra Data Charges"),
    col("State").cast(StringType()).alias("State Code"),
    col("Phone Number").cast(StringType()).alias("Phone Number"),
    col("Gender").cast(StringType()).alias("Gender"),
    col("Age").cast(IntegerType()).alias("Age"),
    # Unpivot the Senior and Under 30 columns
    when(
        col("Senior") == "Yes",
        lit("Senior")
    ).when(
        col("Under 30") == "Yes",
        lit("Under 30")
    ).otherwise(
        lit("Other")
    ).cast(StringType()).alias("Demographics"),
    col("Group").cast(StringType()).alias("Is Contract Group"),
    col("Number of Customers in Group").cast(LongType()).alias("Number of Customers in Group"),
    col("Device Protection & Online Backup").cast(StringType()).alias("Is Device Protection and Online Backup"),
    col("Contract Type").cast(StringType()).alias("Contract Type"),
    col("Payment Method").cast(StringType()).alias("Payment Method"),
    col("Monthly Charge").cast(DoubleType()).alias("Monthly Charges"),
    col("Total Charges").cast(DoubleType()).alias("Total Charges"),
    # Impute the missing values in Churn Category and Churn Reason
    coalesce(col("Churn Category"), lit("Not Churned")).cast(StringType()).alias("Churn Category"),
    coalesce(col("Churn Reason"), lit("Not Churned")).cast(StringType()).alias("Churn Reason"),
    col("Loaded at").cast(TimestampType()).alias("Loaded at"),
    col("File Name").cast(StringType()).alias("File Name")
)

display(df_renamed.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_renamed.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 01-3 Add conditional columns to the renamed DataFrame

# CELL ********************

df_enriched = df_renamed.withColumn(
    "Churn Flag",
    when(
        col("Is Churn") == "Yes", 
        lit(1)
    ).otherwise(
        lit(0)
    ).cast(IntegerType())
).withColumn(
    "Contract Category",
    when(
        col("Contract Type") == "Month-to-Month",
        lit("Monthly Contracts")
    ).when(
        col("Contract Type").isin("One Year", "Two Year"),
        lit("Yearly Contracts")
    ).otherwise(
        lit("Unknown")
    ).cast(StringType())
).withColumn(
    "Grouped Consumption",
    when(
        col("Avg Monthly GB Download") < 5,
        lit("Less than 5 GB")
    ).when(
        col("Avg Monthly GB Download") < 10,
        lit("Between 5 and 10 GB")
    ).otherwise(
        lit("10 or more GB")
    ).cast(StringType())
).withColumn(
    "Age Bin",
    when(
        col("Age") >= 90,
        lit(90)
    ).when(
        col("Age") >= 85,
        lit(85)
    ).when(
        col("Age") >= 80,
        lit(80)
    ).when(
        col("Age") >= 75,
        lit(75)
    ).when(
        col("Age") >= 70,
        lit(70)
    ).when(
        col("Age") >= 65,
        lit(65)
    ).when(
        col("Age") >= 60,
        lit(60)
    ).when(
        col("Age") >= 55,
        lit(55)
    ).when(
        col("Age") >= 50,
        lit(50)
    ).when(
        col("Age") >= 45,
        lit(45)
    ).when(
        col("Age") >= 40,
        lit(40)
    ).when(
        col("Age") >= 35,
        lit(35)
    ).when(
        col("Age") >= 30,
        lit(30)
    ).when(
        col("Age") >= 25,
        lit(25)
    ).when(
        col("Age") >= 20,
        lit(20)
    ).when(
        col("Age") >= 15,
        lit(15)
    ).when(
        col("Age") >= 10,
        lit(10)
    ).when(
        col("Age") >= 5,
        lit(5)
    ).cast(IntegerType())
)

display(df_enriched.count())
display(df_enriched.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_enriched.select("Customer ID").distinct().count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 01-4 Load the enriched DataFrame into the target table in silver layer

# CELL ********************

loading_enriched_table(
    df_source=df_enriched,
    target_table="LH_CustomerChurnETL.silver.customer_churn_enriched",
    candidate_key=["Customer ID"]
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_target = spark.read.table("LH_CustomerChurnETL.silver.customer_churn_enriched")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.count() == df_target.count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 02 Data Transformation for LH_CustomerChurnETL.silver.state_enriched

# MARKDOWN ********************

# ### 02-1 Get the LH_CustomerChurnETL.bronze.state_abbreviations table

# CELL ********************

df_state_abbreviations = spark.read.table("LH_CustomerChurnETL.bronze.state_abbreviations")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 02-2 Join the enriched DataFrame with the state_abbreviations DataFrame

# CELL ********************

df_state_joined = df_enriched.alias("e").join(
    df_state_abbreviations.alias("s"),
    (df_enriched["State Code"] == df_state_abbreviations["State Code"]),
    "left"
).select(
    col("e.`State Code`"),
    col("s.`State Name`")
).distinct()

display(df_state_joined)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 02-3 Load the state_joined DataFrame into the target table in silver layer

# CELL ********************

loading_enriched_table(
    df_source=df_state_joined,
    target_table="LH_CustomerChurnETL.silver.state_enriched",
    candidate_key=["State Code"]
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

mssparkutils.session.stop()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
