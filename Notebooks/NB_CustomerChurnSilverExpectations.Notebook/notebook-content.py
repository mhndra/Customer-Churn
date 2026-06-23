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
# META       "environmentId": "c00b6cbb-b777-9712-4648-78f2fdc08225",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Data Quality in Silver Layer Using Great Expectations

# MARKDOWN ********************

# ## 00 Import packages and get the tables in LH_CustomerChurnETL.silver schema

# CELL ********************

import great_expectations as gx
import great_expectations.expectations as gxe

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 00-1 customer_churn_enriched

# CELL ********************

df_customer_churn_enriched = spark.read.table("LH_CustomerChurnETL.silver.customer_churn_enriched")
df_customer_churn_enriched_cols = df_customer_churn_enriched.columns 

display("===== customer_churn_enriched =====")
display(len(df_customer_churn_enriched_cols))
display(df_customer_churn_enriched.printSchema())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 00-2 state_enriched

# CELL ********************

df_state_enriched = spark.read.table("LH_CustomerChurnETL.silver.state_enriched")
df_state_enriched_cols = df_state_enriched.columns 

display("===== state_enriched =====")
display(len(df_state_enriched_cols))
display(df_state_enriched.printSchema())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 01 Get or add data asset and batch definition

# CELL ********************

context = gx.get_context(
    mode="file",
    project_root_dir="/lakehouse/default/Files/gx"
)

try:
    data_source = context.data_sources.get(
        name="spark_source"
    )
except:
    data_source = context.data_sources.add_spark(
        name="spark_source"
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 01-1 customer_churn_enriched

# CELL ********************

try:
    data_asset = data_source.get_asset(
        name="customer_churn_silver_asset"
    )
except:
    data_asset = data_source.add_dataframe_asset(
        name="customer_churn_silver_asset"
    )

try:
    batch_definition = data_asset.get_batch_definition(
        name="customer_churn_silver_batch_def"
    )
except:
    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        name="customer_churn_silver_batch_def"
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 01-2 state_enriched

# CELL ********************

try:
    state_enriched_asset = data_source.get_asset(
        name="state_enriched_asset"
    )
except:
    state_enriched_asset = data_source.add_dataframe_asset(
        name="state_enriched_asset"
    )

try:
    state_enriched_batch_def = state_enriched_asset.get_batch_definition(
        name="state_enriched_batch_def"
    )
except:
    state_enriched_batch_def = state_enriched_asset.add_batch_definition_whole_dataframe(
        name="state_enriched_batch_def"
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 02 Get or add Expectation Suite and add Expectations

# MARKDOWN ********************

# ### 02-1 customer_churn_enriched

# CELL ********************

try:
    suite = context.suites.get(
        name="customer_churn_silver_suite"
    )
    suite.expectations = []
    suite.save()
except:
    suite = context.suites.add(
        gx.ExpectationSuite(
            name="customer_churn_silver_suite"
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### > Column values to not be null

# CELL ********************

for col in df_customer_churn_enriched_cols:
    suite.add_expectation(
        gxe.ExpectColumnValuesToNotBeNull(
            column=col
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### > Column values to be unique

# CELL ********************

suite.add_expectation(
    gxe.ExpectColumnValuesToBeUnique(
        column="`Customer ID`"
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### > Column values to be in set

# MARKDOWN ********************

# - Columns containing "Yes" or "No"

# CELL ********************

is_cols = [col for col in df_customer_churn_enriched_cols if "Is" in col]
print(is_cols)

for col in is_cols:
    suite.add_expectation(
        gxe.ExpectColumnValuesToBeInSet(
            column=col,
            value_set=["Yes", "No"]
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# - Columns containing specific values

# CELL ********************

# Demographics column
suite.add_expectation(
    gxe.ExpectColumnValuesToBeInSet(
        column="Demographics",
        value_set=["Senior", "Under 30", "Other"]
    )
)

# Gender column
suite.add_expectation(
     gxe.ExpectColumnValuesToBeInSet(
        column="Gender",
        value_set=["Female", "Male", "Prefer not to say"]
    )
)

# Contract Type
suite.add_expectation(
    gxe.ExpectColumnValuesToBeInSet(
        column="Contract Type",
        value_set=["Month-to-Month", "One Year", "Two Year"]
    )
)

# Payment Method column
suite.add_expectation(
    gxe.ExpectColumnValuesToBeInSet(
        column="Payment Method",
        value_set=["Direct Debit", "Credit Card", "Paper Check"]
    )
)

# Churn Category column
suite.add_expectation(
    gxe.ExpectColumnValuesToBeInSet(
        column="Churn Category",
        value_set=["Price", "Dissatisfaction", "Other", "Competitor", "Attitude", "Not Churned"]
    )
)

# Contract Category column
suite.add_expectation(
    gxe.ExpectColumnValuesToBeInSet(
        column="Contract Category",
        value_set=["Monthly Contracts", "Yearly Contracts", "Unknown"]
    )
)

# Grouped Consumption column
suite.add_expectation(
    gxe.ExpectColumnValuesToBeInSet(
        column="Grouped Consumption",
        value_set=["Less than 5 GB", "Between 5 and 10 GB", "10 or more GB"]
    )
)

# Churn Flag
suite.add_expectation(
    gxe.ExpectColumnValuesToBeInSet(
        column="Churn Flag",
        value_set=[0, 1]
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### > Column values to match regex

# CELL ********************

# Phone Number
suite.add_expectation(
    gxe.ExpectColumnValuesToMatchRegex(
        column="Phone Number",
        regex="^[1-4][0-9]{2}-[0-9]{3,5}$"
    )
)

# State Code
suite.add_expectation(
    gxe.ExpectColumnValuesToMatchRegex(
        column="State Code",
        regex="^[A-Z]{2}$"
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### > Column values to be between

# CELL ********************

age_cols = [col for col in df_customer_churn_enriched_cols if "Age" in col]
print(age_cols)

for col in age_cols:
    suite.add_expectation(
        gxe.ExpectColumnValuesToBeBetween(
            column=col,
            min_value=5,
            max_value=95
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

suite.save()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(suite)
display(len(suite.expectations))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 02-2 state_enriched

# CELL ********************

try:
    state_enriched_suite = context.suites.get(
        name="state_enriched_suite"
    )
    state_enriched_suite.expectations = []
    state_enriched_suite.save()
except:
    state_enriched_suite = context.suites.add(
        gx.ExpectationSuite(
            name="state_enriched_suite"
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### > Column values to not be null

# CELL ********************

for col in df_state_enriched_cols:
    state_enriched_suite.add_expectation(
        gxe.ExpectColumnValuesToNotBeNull(
            column=col
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### > Column values to be unique

# CELL ********************

state_enriched_suite.add_expectation(
    gxe.ExpectColumnValuesToBeUnique(
        column="`State Code`"
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

state_enriched_suite.save()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(state_enriched_suite)
display(len(state_enriched_suite.expectations))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 03 Get or add Validation Definition

# MARKDOWN ********************

# ### 03-1 customer_churn_enriched

# CELL ********************

try:
    validation_definition = context.validation_definitions.get(
        name="customer_churn_silver_validation"
    )
except:
    validation_definition = context.validation_definitions.add(
        gx.ValidationDefinition(
            name="customer_churn_silver_validation",
            data=batch_definition,
            suite=suite
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 03-2 state_enriched

# CELL ********************

try:
    state_enriched_validation = context.validation_definitions.get(
        name="state_enriched_validation"
    )
except:
    state_enriched_validation = context.validation_definitions.add(
        gx.ValidationDefinition(
            name="state_enriched_validation",
            data=state_enriched_batch_def,
            suite=state_enriched_suite
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 04 Get or add Checkpoint

# MARKDOWN ********************

# ### 04-1 customer_churn_enriched

# CELL ********************

try:
    checkpoint = context.checkpoints.get(
        name="customer_churn_silver_checkpoint"
    )
except:
    checkpoint = context.checkpoints.add(
        gx.Checkpoint(
            name="customer_churn_silver_checkpoint",
            validation_definitions=[validation_definition],
            actions=[gx.checkpoint.UpdateDataDocsAction(name="update_data_docs")]
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 04-2 state_enriched

# CELL ********************

try:
    state_enriched_checkpoint = context.checkpoints.get(
        name="state_enriched_checkpoint"
    )
except:
    state_enriched_checkpoint = context.checkpoints.add(
        gx.Checkpoint(
            name="state_enriched_checkpoint",
            validation_definitions=[state_enriched_validation],
            actions=[gx.checkpoint.UpdateDataDocsAction(name="update_data_docs")]
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 05 Run the Checkpoint

# MARKDOWN ********************

# ### 05-1 customer_churn_enriched

# CELL ********************

result = checkpoint.run(
    batch_parameters={
        "dataframe": df_customer_churn_enriched
    }
)

print(f"customer_churn_silver_checkpoint successful: {result.success}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

customer_churn_silver_validation_result = list(result.run_results.values())[0]

failed_summary = {}

if not customer_churn_silver_validation_result["success"]:
    failed_summary["suite"] = validation_definition.suite.name
    failed_summary["details"] = []
    for result in customer_churn_silver_validation_result["results"]:
        if not result["success"]:
            failed_summary["details"].append({
                "column": result["expectation_config"]["kwargs"]["column"],
                "expectation": result["expectation_config"]["type"],
                "result": {
                    "element_count": result["result"]["element_count"],
                    "unexpected_count": result["result"]["unexpected_count"],
                    "partial_unexpected_counts": result["result"]["partial_unexpected_counts"]
                },
                "severity": result["expectation_config"]["severity"]
            })

    raise Exception(f"Expectations failed:{failed_summary}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 05-2 state_enriched

# CELL ********************

state_enriched_result = state_enriched_checkpoint.run(
    batch_parameters={
        "dataframe": df_state_enriched
    }
)

print(f"state_enriched_checkpoint successful: {state_enriched_result.success}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

state_enriched_validation_result = list(state_enriched_result.run_results.values())[0]

failed_summary = {}

if not state_enriched_validation_result["success"]:
    failed_summary["suite"] = state_enriched_validation.suite.name
    failed_summary["details"] = []
    for result in state_enriched_validation_result["results"]:
        if not result["success"]:
            failed_summary["details"].append({
                "column": result["expectation_config"]["kwargs"]["column"],
                "expectation": result["expectation_config"]["type"],
                "result": {
                    "element_count": result["result"]["element_count"],
                    "unexpected_count": result["result"]["unexpected_count"]
                },
                "severity": result["expectation_config"]["severity"]
            })

    raise Exception(f"Expectations failed:{failed_summary}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import os

base_path = "/lakehouse/default/Files/gx/gx/uncommitted/data_docs/local_site/validations/state_enriched_suite/__none__"
timestamps = sorted(os.listdir(base_path), reverse=True)
latest_timestamp = timestamps[0]

data_docs_path = f"{base_path}/{latest_timestamp}/spark_source-state_enriched_asset.html"

display(f"Loading validation from: {latest_timestamp}")

# Render inline
with open(data_docs_path, "r") as f:
    html_content = f.read()

displayHTML(html_content)

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
