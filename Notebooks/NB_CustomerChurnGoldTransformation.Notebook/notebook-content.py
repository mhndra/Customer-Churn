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
# META         },
# META         {
# META           "id": "a518a941-f003-43c3-a936-9782b007ae81"
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

# # Data Transformation in Gold Layer

# MARKDOWN ********************

# ## 00 Import packages and create the loading_to_table function

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

def loading_to_table(df_source, target_table, unique_key):
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
        match_condition = " AND ".join([f"target.`{col}` = source.`{col}`" for col in unique_key])

        change_detection_columns = [col for col in df_source.columns if col not in unique_key]
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

# ## 01 Get the LH_CsutomerChurnELT.silver.customer_churn_enriched table

# CELL ********************

df = spark.read.table("LH_CustomerChurnETL.silver.customer_churn_enriched")

display(df.limit(20))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 02 Data Transformation for LH_CustomerChurnAnalytics.gold.dim_state

# MARKDOWN ********************

# ### 02-1 Deduplicate data, generate surrogate key, and join the customer_churn_enriched DataFrame with the state_enriched table

# CELL ********************

df_state_enriched = spark.read.table("LH_CustomerChurnETL.silver.state_enriched")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_state_keyed = df.alias("c").join(
    df_state_enriched.alias("s"),
    (df["State Code"] == df_state_enriched["State Code"]),
    "left"
).select(
    md5(concat_ws("||", col("c.`State Code`"))).alias("State Key"),
    col("c.`State Code`"),
    col("s.`State Name`")
).distinct()

display(df_state_keyed.count())
display(df_state_keyed.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_state_keyed.select("State Key").distinct().count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_state_keyed.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 02-2 Load the state DataFrame into the target state table in gold layer

# CELL ********************

loading_to_table(
    df_source=df_state_keyed,
    target_table="LH_CustomerChurnAnalytics.gold.dim_state",
    unique_key=["State Key"]
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 03 Data Transformation for LH_CustomerChurnAnalytics.gold.dim_contracts

# MARKDOWN ********************

# ### 03-1 Deduplicate data and generate surrogate key

# CELL ********************

df_contracts_keyed = df.select(
    md5(concat_ws("||", col("Contract Type"), col("Payment Method"))).alias("Contract Key"),
    "Contract Type",
    "Contract Category",
    "Payment Method"
).distinct()

display(df_contracts_keyed.count())
display(df_contracts_keyed.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_contracts_keyed.select("Contract Key").distinct().count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_contracts_keyed.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 03-2 Load the contracts_keyed DataFrame into the target table in gold layer

# CELL ********************

loading_to_table(
    df_source=df_contracts_keyed,
    target_table="LH_CustomerChurnAnalytics.gold.dim_contracts",
    unique_key=["Contract Key"]
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 04 Data Transformation for LH_CustomerChurnAnalytics.gold.dim_churn_descriptions

# MARKDOWN ********************

# ### 04-1 Deduplicate data and generate surrogate key

# CELL ********************

df_churn_descriptions_keyed = df.select(
    md5(concat_ws("||", col("Churn Reason"), col("Churn Category"))).alias("Churn Description Key"),
    "Churn Reason",
    "Churn Category"
).distinct()

display(df_churn_descriptions_keyed.count())
display(df_churn_descriptions_keyed.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_churn_descriptions_keyed.select("Churn Description Key").distinct().count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_churn_descriptions_keyed.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 04-2 Load the churn_descriptions_keyed DataFrame into the target table in gold layer

# CELL ********************

loading_to_table(
    df_source=df_churn_descriptions_keyed,
    target_table="LH_CustomerChurnAnalytics.gold.dim_churn_descriptions",
    unique_key=["Churn Description Key"]
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 05 Data Transformation for LH_CustomerChurnAnalytics.gold.dim_customers

# MARKDOWN ********************

# ### 05-1 Deduplicate data and generate surrogate key

# CELL ********************

df_customers_keyed = df.select(
    md5(concat_ws("||", col("Customer ID"))).alias("Customer Key"),
    "Customer ID",
    "Phone Number",
    "Gender",
    "Demographics",
    "Age",
    "Age Bin",
    "Is Contract Group",
    "Number of Customers in Group",
    "Is International Calls Active",
    "Is International Plan",
    "Is Unlimited Data Plan",
    "Is Device Protection and Online Backup",
    "Is Churn",
    "Churn Flag"
).distinct()

display(df_customers_keyed.count())
display(df_customers_keyed.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_customers_keyed.select("Customer Key").distinct().count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_customers_keyed.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 05-2 Load the customers_keyed DataFrame into the target table in gold layer

# CELL ********************

loading_to_table(
    df_source=df_customers_keyed,
    target_table="LH_CustomerChurnAnalytics.gold.dim_customers",
    unique_key=["Customer Key"]
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 06 Data Transformation for LH_CustomerChurnAnalytics.gold.fact_customer_subscriptions

# MARKDOWN ********************

# ### 06-1 Generate surrogate key

# CELL ********************

df_customer_subscriptions_keyed = df.select(
    md5(concat_ws(
            "||", 
            col("Customer ID"),
            col("State Code"),
            col("Contract Type"),
            col("Payment Method"),
            col("Churn Reason"),
            col("Churn Category")
        )
    ).alias("Customer Subscription Key"),
    "Customer ID",
    "State Code",
    "Contract Type",
    "Payment Method",
    "Churn Reason",
    "Churn Category",
    "Grouped Consumption",
    "Avg Monthly GB Download", 
    "Local Calls", 
    "Local Mins", 
    "International Calls", 
    "International Mins", 
    "Customer Service Calls", 
    "Account Length Months", 
    "Monthly Charges", 
    "Extra International Charges", 
    "Extra Data Charges", 
    "Total Charges", 
    "Loaded at"
).distinct()

display(df_customer_subscriptions_keyed.count())
display(df_customer_subscriptions_keyed.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 06-2 Join the customer_subscriptions_keyed DataFrame with dimension tables

# CELL ********************

df_dim_customers = spark.read.table("LH_CustomerChurnAnalytics.gold.dim_customers")
df_dim_state = spark.read.table("LH_CustomerChurnAnalytics.gold.dim_state")
df_dim_contracts = spark.read.table("LH_CustomerChurnAnalytics.gold.dim_contracts")
df_dim_churn_descriptions = spark.read.table("LH_CustomerChurnAnalytics.gold.dim_churn_descriptions")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_customer_subscriptions_joined = df_customer_subscriptions_keyed.alias(
    "cs"
).join(
    df_dim_customers.alias("cu"), 
    (df_customer_subscriptions_keyed["Customer ID"] == df_dim_customers["Customer ID"]),
    "left"
).join(
    df_dim_state.alias("s"),
    (df_customer_subscriptions_keyed["State Code"] == df_dim_state["State Code"]),
    "left"
).join(
    df_dim_contracts.alias("co"),
    (df_customer_subscriptions_keyed["Contract Type"] == df_dim_contracts["Contract Type"]) &
    (df_customer_subscriptions_keyed["Payment Method"] == df_dim_contracts["Payment Method"]),
    "left"
).join(
    df_dim_churn_descriptions.alias("cd"),
    (df_customer_subscriptions_keyed["Churn Reason"] == df_dim_churn_descriptions["Churn Reason"]) &
    (df_customer_subscriptions_keyed["Churn Category"] == df_dim_churn_descriptions["Churn Category"]),
    "left"
).select(
    col("cs.`Customer Subscription Key`"),
    col("cu.`Customer Key`"),
    col("s.`State Key`"),
    col("co.`Contract Key`"),
    col("cd.`Churn Description Key`"),
    col("cs.`Grouped Consumption`"),
    col("cs.`Avg Monthly GB Download`"), 
    col("cs.`Local Calls`"), 
    col("cs.`Local Mins`"), 
    col("cs.`International Calls`"), 
    col("cs.`International Mins`"), 
    col("cs.`Customer Service Calls`"), 
    col("cs.`Account Length Months`"), 
    col("cs.`Monthly Charges`"), 
    col("cs.`Extra International Charges`"), 
    col("cs.`Extra Data Charges`"), 
    col("cs.`Total Charges`"), 
    col("cs.`Loaded at`")
)

display(df_customer_subscriptions_joined.count())
display(df_customer_subscriptions_joined.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_customer_subscriptions_joined.select("Customer Subscription Key").distinct().count()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_customer_subscriptions_joined.printSchema()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 06-3 Load the customer_subscriptions_joined DataFrame into the target table in gold layer

# CELL ********************

loading_to_table(
    df_source=df_customer_subscriptions_joined,
    target_table="LH_CustomerChurnAnalytics.gold.fact_customer_subscriptions",
    unique_key=["Customer Subscription Key"]
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
