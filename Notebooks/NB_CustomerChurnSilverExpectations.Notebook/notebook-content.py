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

# ## 00 Import packages and get the LH_CustomerChurnETL.silver.customer_churn_enriched table

# CELL ********************

import great_expectations as gx
import great_expectations.expectations as gxe

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df_customer_churn_enriched = spark.read.table("LH_CustomerChurnETL.silver.customer_churn_enriched")
df_customer_churn_enriched_cols = df_customer_churn_enriched.columns 

display(len(df_customer_churn_enriched_cols))
display(df_customer_churn_enriched.printSchema())

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

# ## 02 Get or add Expectation Suite and add Expectations

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

# ### 02-1 Column values to not be null

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

# ### 02-2 Column values to be unique

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

# ### 02-3 Column values to be in set

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

# ### 02-4 Column values to match regex

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

# ### 02-5 Column values to be between

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

# ## 03 Get or add Validation Definition

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

# ## 04 Get or add Checkpoint

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

# ## 05 Run the Checkpoint

# CELL ********************

result = checkpoint.run(
    batch_parameters={
        "dataframe": df_customer_churn_enriched
    }
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

data_docs_path = "/lakehouse/default/Files/gx/gx/uncommitted/data_docs/local_site/validations/customer_churn_silver_suite/__none__/20260621T235220.689681Z/spark_source-customer_churn_silver_asset.html"

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


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
