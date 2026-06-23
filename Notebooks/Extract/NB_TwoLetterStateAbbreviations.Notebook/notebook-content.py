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
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Extract Two-letter State Abbreviations Data from Federal Aviation Administration (FAA) Website

# MARKDOWN ********************

# ## 00 Import packages

# CELL ********************

import requests
from bs4 import BeautifulSoup
from pyspark.sql.functions import col

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 01 Get request to the website

# CELL ********************

response = requests.get("https://www.faa.gov/air_traffic/publications/atpubs/cnt_html/appendix_a.html")
soup = BeautifulSoup(response.text, "html.parser")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 02 Convert the data to the list of two-letter state abbreviations and their name

# CELL ********************

states = [state.text.strip() for state in soup.find_all("td")]
print(states)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 03 Convert the list to a DataFrame

# CELL ********************

state_pairs = list(zip(states[::2], states[1::2]))
print(state_pairs)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Reorder columns

# CELL ********************

df_state_pairs = spark.createDataFrame(data=state_pairs, schema=["State Name", "State Code"])
df_reordered = df_state_pairs.select(
    "State Code",
    "State Name"
)
display(df_reordered)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## 05 Load the reordered DataFrame to the target table in bronze layer

# CELL ********************

df_reordered.write.format("delta").mode("overwrite").option("delta.columnMapping.mode", "name").saveAsTable("LH_CustomerChurnETL.bronze.state_abbreviations")

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
