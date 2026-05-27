[DefaultOutputDestinationSettings = [DestinationDefinition = [Kind = "Reference", QueryName = "DefaultDestination", IsNewTarget = true], UpdateMethod = [Kind = "Replace"], DestinationTypeSettings = [Kind = "Table"]], StagingDefinition = [Kind = "FastCopy"]]
section Section1;
shared DefaultDestination = Lakehouse.Contents([EnableFolding = false]){[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data]{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data];
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Silver_Customer Churn_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared #"Silver Customer Churn" = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "Bronze_Customer Churn", ItemKind = "Table"]}[Data],
  #"Changed column type" = Table.TransformColumnTypes(#"Navigation 2", {{"Account Length (in months)", Int64.Type}, {"Local Calls", Int64.Type}, {"Local Mins", type number}, {"Intl Calls", Int64.Type}, {"Intl Mins", type number}, {"Customer Service Calls", Int64.Type}, {"Avg Monthly GB Download", Int64.Type}, {"Extra International Charges", type number}, {"Extra Data Charges", type number}, {"Age", Int64.Type}, {"Number of Customers in Group", Int64.Type}, {"Monthly Charge", Currency.Type}, {"Total Charges", Currency.Type}, {"Loaded At", type datetime}}),
  #"Renamed columns" = Table.RenameColumns(#"Changed column type", {{"Account Length (in months)", "Account Length Months"}}),
  #"Inserted conditional column" = Table.AddColumn(#"Renamed columns", "Churned", each if [Churn Label] = "Yes" then 1 else 0),
  #"Inserted conditional column 1" = Table.AddColumn(#"Inserted conditional column", "Demographics", each if [Senior] = "Yes" then "Senior" else if [Under 30] = "Yes" then "Under 30" else "Other"),
  #"Inserted conditional column 2" = Table.AddColumn(#"Inserted conditional column 1", "Contract Category", each if [Contract Type] = "Month-to-Month" then "Monthly Contracts" else if [Contract Type] = "One Year" then "Yearly Contracts" else if [Contract Type] = "Two Year" then "Yearly Contracts" else "Unknown"),
  #"Inserted conditional column 3" = Table.AddColumn(#"Inserted conditional column 2", "Grouped Consumption", each if [Avg Monthly GB Download] < 5 then "Less than 5 GB" else if [Avg Monthly GB Download] < 10 then "Between 5 and 10 GB" else "10 or more GB"),
  #"Inserted conditional column 4" = Table.AddColumn(#"Inserted conditional column 3", "Age Bin", each if [Age] >= 90 then 90 else if [Age] >= 85 then 85 else if [Age] >= 80 then 80 else if [Age] >= 75 then 75 else if [Age] >= 70 then 70 else if [Age] >= 65 then 65 else if [Age] >= 60 then 60 else if [Age] >= 55 then 55 else if [Age] >= 50 then 50 else if [Age] >= 45 then 45 else if [Age] >= 40 then 40 else if [Age] >= 35 then 35 else if [Age] >= 30 then 30 else if [Age] >= 25 then 25 else if [Age] >= 20 then 20 else if [Age] >= 15 then 15 else if [Age] >= 10 then 10 else if [Age] >= 5 then 5 else ""),
  #"Changed column type 1" = Table.TransformColumnTypes(#"Inserted conditional column 4", {{"Churned", Int64.Type}, {"Demographics", type text}, {"Contract Category", type text}, {"Grouped Consumption", type text}, {"Age Bin", Int64.Type}, {"Monthly Charge", type number}, {"Total Charges", type number}}),
  #"Replaced value" = Table.ReplaceValue(#"Changed column type 1", null, "Empty", Replacer.ReplaceValue, {"Churn Category"}),
  #"Replaced value 1" = Table.ReplaceValue(#"Replaced value", null, "Empty", Replacer.ReplaceValue, {"Churn Reason"}),
  #"Replaced value 2" = Table.ReplaceValue(#"Replaced value 1", "yes", "Yes", Replacer.ReplaceText, {"Intl Plan"}),
  #"Replaced value 3" = Table.ReplaceValue(#"Replaced value 2", "no", "No", Replacer.ReplaceText, {"Intl Plan"})
in
  #"Replaced value 3";
shared #"Silver_Customer Churn_DataDestination" = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  Navigation_3 = Navigation_2{[Id = "silver", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "customer_churn", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
