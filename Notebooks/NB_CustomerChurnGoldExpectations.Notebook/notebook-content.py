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
# META       "environmentId": "c00b6cbb-b777-9712-4648-78f2fdc08225",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Data Quality in Gold Layer Using Great Expectations

# MARKDOWN ********************

# ## 00 Import packages and get the tables in LH_CustomerChurnAnalytics.gold schema

# CELL ********************

import great_expectations as gx
import great_expectations.expectations as gxe

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 00-1 dim_churn_descriptions

# CELL ********************

df_dim_churn_descriptions = spark.read.table("LH_CustomerChurnAnalytics.gold.dim_churn_descriptions")
df_dim_churn_descriptions_cols = df_dim_churn_descriptions.columns
display("===== dim_churn_descriptions =====")
display(len(df_dim_churn_descriptions_cols))
display(df_dim_churn_descriptions.printSchema())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 00-2 dim_contracts

# CELL ********************

df_dim_contracts = spark.read.table("LH_CustomerChurnAnalytics.gold.dim_contracts")
df_dim_contracts_cols = df_dim_contracts.columns
display("===== dim_contracts =====")
display(len(df_dim_contracts_cols))
display(df_dim_contracts.printSchema())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 00-3 dim_customers

# CELL ********************

df_dim_customers = spark.read.table("LH_CustomerChurnAnalytics.gold.dim_customers")
df_dim_customers_cols = df_dim_customers.columns
display("===== dim_customers =====")
display(len(df_dim_customers_cols))
display(df_dim_customers.printSchema())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 00-4 dim_state

# CELL ********************

df_dim_state = spark.read.table("LH_CustomerChurnAnalytics.gold.dim_state")
df_dim_state_cols = df_dim_state.columns
display("===== dim_state =====")
display(len(df_dim_state_cols))
display(df_dim_state.printSchema())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 00-5 fact_customer_subscriptions

# CELL ********************

df_fact_customer_subscriptions = spark.read.table("LH_CustomerChurnAnalytics.gold.fact_customer_subscriptions")
df_fact_customer_subscriptions_cols = df_fact_customer_subscriptions.columns
display("===== fact_customer_subscriptions =====")
display(len(df_fact_customer_subscriptions_cols))
display(df_fact_customer_subscriptions.printSchema())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 01 Get or add data assets and batch definitions

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

# ### 01-1 dim_churn_descriptions

# CELL ********************

try:
    dim_churn_descriptions_asset = data_source.get_asset(
        name="dim_churn_descriptions_asset"
    )
except:
    dim_churn_descriptions_asset = data_source.add_dataframe_asset(
        name="dim_churn_descriptions_asset"
    )

try:
    dim_churn_descriptions_batch_def = dim_churn_descriptions_asset.get_batch_definition(
        name="dim_churn_descriptions_batch_def"
    )
except:
    dim_churn_descriptions_batch_def = dim_churn_descriptions_asset.add_batch_definition_whole_dataframe(
        name="dim_churn_descriptions_batch_def"
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 01-2 dim_contracts

# CELL ********************

try:
    dim_contracts_asset = data_source.get_asset(
        name="dim_contracts_asset"
    )
except:
    dim_contracts_asset = data_source.add_dataframe_asset(
        name="dim_contracts_asset"
    )

try:
    dim_contracts_batch_def = dim_contracts_asset.get_batch_definition(
        name="dim_contracts_batch_def"
    )
except:
    dim_contracts_batch_def = dim_contracts_asset.add_batch_definition_whole_dataframe(
        name="dim_contracts_batch_def"
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 01-3 dim_customers

# CELL ********************

try:
    dim_customers_asset = data_source.get_asset(
        name="dim_customers_asset"
    )
except:
    dim_customers_asset = data_source.add_dataframe_asset(
        name="dim_customers_asset"
    )

try:
    dim_customers_batch_def = dim_customers_asset.get_batch_definition(
        name="dim_customers_batch_def"
    )
except:
    dim_customers_batch_def = dim_customers_asset.add_batch_definition_whole_dataframe(
        name="dim_customers_batch_def"
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 01-4 dim_state

# CELL ********************

try:
    dim_state_asset = data_source.get_asset(
        name="dim_state_asset"
    )
except:
    dim_state_asset = data_source.add_dataframe_asset(
        name="dim_state_asset"
    )

try:
    dim_state_batch_def = dim_state_asset.get_batch_definition(
        name="dim_state_batch_def"
    )
except:
    dim_state_batch_def = dim_state_asset.add_batch_definition_whole_dataframe(
        name="dim_state_batch_def"
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 01-5 fact_customer_subscriptions

# CELL ********************

try:
    fact_customer_subscriptions_asset = data_source.get_asset(
        name="fact_customer_subscriptions_asset"
    )
except:
    fact_customer_subscriptions_asset = data_source.add_dataframe_asset(
        name="fact_customer_subscriptions_asset"
    )

try:
    fact_customer_subscriptions_batch_def = fact_customer_subscriptions_asset.get_batch_definition(
        name="fact_customer_subscriptions_batch_def"
    )
except:
    fact_customer_subscriptions_batch_def = fact_customer_subscriptions_asset.add_batch_definition_whole_dataframe(
        name="fact_customer_subscriptions_batch_def"
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 02 Get or add Expectation Suites and add Expectations

# MARKDOWN ********************

# ### 02-1 dim_churn_descriptions

# CELL ********************

try:
    dim_churn_descriptions_suite = context.suites.get(
        name="dim_churn_descriptions_suite"
    )
    dim_churn_descriptions_suite.expectations = []
    dim_churn_descriptions_suite.save()
except:
    dim_churn_descriptions_suite = context.suites.add(
        gx.ExpectationSuite(
            name="dim_churn_descriptions_suite"
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

for col in df_dim_churn_descriptions_cols:
    dim_churn_descriptions_suite.add_expectation(
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

dim_churn_descriptions_suite.add_expectation(
    gxe.ExpectColumnValuesToBeUnique(
        column="`Churn Description Key`"
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

dim_churn_descriptions_suite.save()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(dim_churn_descriptions_suite)
display(len(dim_churn_descriptions_suite.expectations))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 02-2 dim_contracts

# CELL ********************

try:
    dim_contracts_suite = context.suites.get(
        name="dim_contracts_suite"
    )
    dim_contracts_suite.expectations = []
    dim_contracts_suite.save()
except:
    dim_contracts_suite = context.suites.add(
        gx.ExpectationSuite(
            name="dim_contracts_suite"
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

for col in df_dim_contracts_cols:
    dim_contracts_suite.add_expectation(
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

dim_contracts_suite.add_expectation(
    gxe.ExpectColumnValuesToBeUnique(
        column="`Contract Key`"
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

dim_contracts_suite.save()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(dim_contracts_suite)
display(len(dim_contracts_suite.expectations))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 02-3 dim_customers

# CELL ********************

try:
    dim_customers_suite = context.suites.get(
        name="dim_customers_suite"
    )
    dim_customers_suite.expectations = []
    dim_customers_suite.save()
except:
    dim_customers_suite = context.suites.add(
        gx.ExpectationSuite(
            name="dim_customers_suite"
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

for col in df_dim_customers_cols:
    dim_customers_suite.add_expectation(
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

unique_cols = ["`Customer Key`", "`Customer ID`"]

for col in unique_cols:
    dim_customers_suite.add_expectation(
        gxe.ExpectColumnValuesToBeUnique(
            column=col
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

dim_customers_suite.add_expectation(
    gxe.ExpectColumnValuesToBeBetween(
        column="Number of Customers in Group",
        min_value=0,
        strict_min=False
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

dim_customers_suite.save()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(dim_customers_suite)
display(len(dim_customers_suite.expectations))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 02-4 dim_state

# CELL ********************

try:
    dim_state_suite = context.suites.get(
        name="dim_state_suite"
    )
    dim_state_suite.expectations = []
    dim_state_suite.save()
except:
    dim_state_suite = context.suites.add(
        gx.ExpectationSuite(
            name="dim_state_suite"
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

for col in df_dim_state_cols:
    dim_state_suite.add_expectation(
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

dim_state_suite.add_expectation(
    gxe.ExpectColumnValuesToBeUnique(
        column="`State Key`"
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

dim_state_suite.save()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(dim_state_suite)
display(len(dim_state_suite.expectations))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 02-5 fact_customer_subscriptions

# CELL ********************

try:
    fact_customer_subscriptions_suite = context.suites.get(
        name="fact_customer_subscriptions_suite"
    )
    fact_customer_subscriptions_suite.expectations = []
    fact_customer_subscriptions_suite.save()
except:
    fact_customer_subscriptions_suite = context.suites.add(
        gx.ExpectationSuite(
            name="fact_customer_subscriptions_suite"
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

for col in df_fact_customer_subscriptions_cols:
    fact_customer_subscriptions_suite.add_expectation(
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

fact_customer_subscriptions_suite.add_expectation(
    gxe.ExpectColumnValuesToBeUnique(
        column="`Customer Subscription Key`"
    )
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### > Column values to be between

# MARKDOWN ********************

# - Columns containing values greater than 0

# CELL ********************

greater_than_0_cols = [
    "Account Length Months",
    "Monthly Charges",
    "Total Charges"
]

for col in greater_than_0_cols:
    fact_customer_subscriptions_suite.add_expectation(
        gxe.ExpectColumnValuesToBeBetween(
            column=col,
            min_value=0,
            strict_min=True
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# - Columns containing values greater than or equal to 0

# CELL ********************

greater_or_equal_0_cols = [
    "Avg Monthly GB Download",
    "Local Calls",
    "Local Mins",
    "International Calls",
    "International Mins",
    "Customer Service Calls",
    "Extra International Charges",
    "Extra Data Charges"
]

for col in greater_or_equal_0_cols:
    fact_customer_subscriptions_suite.add_expectation(
        gxe.ExpectColumnValuesToBeBetween(
            column=col,
            min_value=0,
            strict_min=False
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

fact_customer_subscriptions_suite.save()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(fact_customer_subscriptions_suite)
display(len(fact_customer_subscriptions_suite.expectations))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 03 Get or add Validation Definitions

# MARKDOWN ********************

# ### 03-1 dim_churn_descriptions

# CELL ********************

try:
    dim_churn_descriptions_validation = context.validation_definitions.get(
        name="dim_churn_descriptions_validation"
    )
except:
    dim_churn_descriptions_validation = context.validation_definitions.add(
        gx.ValidationDefinition(
            name="dim_churn_descriptions_validation",
            data=dim_churn_descriptions_batch_def,
            suite=dim_churn_descriptions_suite
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 03-2 dim_contracts

# CELL ********************

try:
    dim_contracts_validation = context.validation_definitions.get(
        name="dim_contracts_validation"
    )
except:
    dim_contracts_validation = context.validation_definitions.add(
        gx.ValidationDefinition(
            name="dim_contracts_validation",
            data=dim_contracts_batch_def,
            suite=dim_contracts_suite
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 03-3 dim_customers

# CELL ********************

try:
    dim_customers_validation = context.validation_definitions.get(
        name="dim_customers_validation"
    )
except:
    dim_customers_validation = context.validation_definitions.add(
        gx.ValidationDefinition(
            name="dim_customers_validation",
            data=dim_customers_batch_def,
            suite=dim_customers_suite
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 03-4 dim_state

# CELL ********************

try:
    dim_state_validation = context.validation_definitions.get(
        name="dim_state_validation"
    )
except:
    dim_state_validation = context.validation_definitions.add(
        gx.ValidationDefinition(
            name="dim_state_validation",
            data=dim_state_batch_def,
            suite=dim_state_suite
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### 03-5 fact_customer_subscriptions

# CELL ********************

try:
    fact_customer_subscriptions_validation = context.validation_definitions.get(
        name="fact_customer_subscriptions_validation"
    )
except:
    fact_customer_subscriptions_validation = context.validation_definitions.add(
        gx.ValidationDefinition(
            name="fact_customer_subscriptions_validation",
            data=fact_customer_subscriptions_batch_def,
            suite=fact_customer_subscriptions_suite
        )
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 04 Add or update Checkpoints and run the Checkpoints

# CELL ********************

validation_runs = [
    ("dim_churn_descriptions_checkpoint", dim_churn_descriptions_validation, df_dim_churn_descriptions),
    ("dim_contracts_checkpoint", dim_contracts_validation, df_dim_contracts),
    ("dim_customers_checkpoint", dim_customers_validation, df_dim_customers),
    ("dim_state_checkpoint", dim_state_validation, df_dim_state),
    ("fact_customer_subscriptions_checkpoint", fact_customer_subscriptions_validation, df_fact_customer_subscriptions)
]

for checkpoint_name, validation, dataframe in validation_runs:
    checkpoint = context.checkpoints.add_or_update(
        gx.Checkpoint(
            name=checkpoint_name,
            validation_definitions=[validation],
            actions=[gx.checkpoint.UpdateDataDocsAction(name="update_data_docs")]
        )
    )
    result = checkpoint.run(
        batch_parameters={
            "dataframe": dataframe
        }
    )

    print(f"{checkpoint_name} successful: {result.success}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

data_docs_path = "/lakehouse/default/Files/gx/gx/uncommitted/data_docs/local_site/validations/dim_customers_suite/__none__/20260621T234506.700684Z/spark_source-dim_customers_asset.html"

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
