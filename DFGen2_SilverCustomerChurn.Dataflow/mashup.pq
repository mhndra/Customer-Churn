[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "bronze customer_churn_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared #"silver customer_churn_enriched" = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "a298258a-25c5-47b7-b809-d2c4b6246ebf"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "a2cf5112-d7cc-44e2-bd1f-0e270656104e"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "bronze.customer_churn", ItemKind = "Table"]}[Data],
  #"Changed column type" = Table.TransformColumnTypes(#"Navigation 2", {{"Account Length (in months)", Int64.Type}, {"Local Calls", Int64.Type}, {"Local Mins", type number}, {"Intl Calls", Int64.Type}, {"Intl Mins", type number}, {"Customer Service Calls", Int64.Type}, {"Avg Monthly GB Download", Int64.Type}, {"Extra International Charges", type number}, {"Extra Data Charges", type number}, {"Age", Int64.Type}, {"Number of Customers in Group", Int64.Type}, {"Monthly Charge", type number}, {"Total Charges", type number}, {"Loaded at", type datetime}}),
  #"Renamed columns" = Table.RenameColumns(#"Changed column type", {{"Account Length (in months)", "Account Length Months"}, {"Intl Calls", "International Calls"}, {"Intl Mins", "International Mins"}, {"Intl Active", "International Active"}, {"Intl Plan", "International Plan"}}),
  #"Inserted Churned column" = Table.AddColumn(#"Renamed columns", "Churned", each if [Churn Label] = "Yes" then 1 else 0),
  #"Inserted Demographics column" = Table.AddColumn(#"Inserted Churned column", "Demographics", each if [Senior] = "Yes" then "Senior" else if [Under 30] = "Yes" then "Under 30" else "Other"),
  #"Inserted Contract Category column" = Table.AddColumn(#"Inserted Demographics column", "Contract Category", each if [Contract Type] = "Month-to-Month" then "Monthly Contracts" else if [Contract Type] = "One Year" then "Yearly Contracts" else if [Contract Type] = "Two Year" then "Yearly Contracts" else "Unknown"),
  #"Inserted Grouped Consumption column" = Table.AddColumn(#"Inserted Contract Category column", "Grouped Consumption", each if [Avg Monthly GB Download] < 5 then "Less than 5 GB" else if [Avg Monthly GB Download] < 10 then "Between 5 and 10 GB" else "10 or more GB"),
  #"Inserted Age Bin column" = Table.AddColumn(#"Inserted Grouped Consumption column", "Age Bin", each if [Age] >= 90 then 90 else if [Age] >= 85 then 85 else if [Age] >= 80 then 80 else if [Age] >= 75 then 75 else if [Age] >= 70 then 70 else if [Age] >= 65 then 65 else if [Age] >= 60 then 60 else if [Age] >= 55 then 55 else if [Age] >= 50 then 50 else if [Age] >= 45 then 45 else if [Age] >= 40 then 40 else if [Age] >= 35 then 35 else if [Age] >= 30 then 30 else if [Age] >= 25 then 25 else if [Age] >= 20 then 20 else if [Age] >= 15 then 15 else if [Age] >= 10 then 10 else if [Age] >= 5 then 5 else ""),
  #"Changed column type 1" = Table.TransformColumnTypes(#"Inserted Age Bin column", {{"Churned", Int64.Type}, {"Demographics", type text}, {"Contract Category", type text}, {"Grouped Consumption", type text}, {"Age Bin", Int64.Type}, {"Monthly Charge", type number}, {"Total Charges", type number}}),
  #"Replaced Churn Category value" = Table.ReplaceValue(#"Changed column type 1", null, "Empty", Replacer.ReplaceValue, {"Churn Category"}),
  #"Replaced Churn Reason value" = Table.ReplaceValue(#"Replaced Churn Category value", null, "Empty", Replacer.ReplaceValue, {"Churn Reason"}),
  #"Replaced International Plan value 1" = Table.ReplaceValue(#"Replaced Churn Reason value", "yes", "Yes", Replacer.ReplaceText, {"International Plan"}),
  #"Replaced International Plan value 2" = Table.ReplaceValue(#"Replaced International Plan value 1", "no", "No", Replacer.ReplaceText, {"International Plan"})
in
  #"Replaced International Plan value 2";
shared #"bronze customer_churn_DataDestination" = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "a298258a-25c5-47b7-b809-d2c4b6246ebf"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "a2cf5112-d7cc-44e2-bd1f-0e270656104e"]}[Data],
  Navigation_3 = Navigation_2{[Id = "silver", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "customer_churn_enriched", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
