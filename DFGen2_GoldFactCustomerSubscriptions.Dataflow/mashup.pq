[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Gold_Fact_Customer Subscriptions_DataDestination", IsNewTarget = true], Settings = [Kind = "Manual", AllowCreation = true, ColumnSettings = [Mappings = {[SourceColumnName = "Subscription Key", DestinationColumnName = "Subscription Key"], [SourceColumnName = "Customer Key", DestinationColumnName = "Customer Key"], [SourceColumnName = "State Key", DestinationColumnName = "State Key"], [SourceColumnName = "Contract Key", DestinationColumnName = "Contract Key"], [SourceColumnName = "Churn Key", DestinationColumnName = "Churn Key"], [SourceColumnName = "Grouped Consumption", DestinationColumnName = "Grouped Consumption"], [SourceColumnName = "Avg Monthly GB Download", DestinationColumnName = "Avg Monthly GB Download"], [SourceColumnName = "Local Calls", DestinationColumnName = "Local Calls"], [SourceColumnName = "Local Mins", DestinationColumnName = "Local Mins"], [SourceColumnName = "International Calls", DestinationColumnName = "International Calls"], [SourceColumnName = "International Mins", DestinationColumnName = "International Mins"], [SourceColumnName = "Customer Service Calls", DestinationColumnName = "Customer Service Calls"], [SourceColumnName = "Account Length Months", DestinationColumnName = "Account Length Months"], [SourceColumnName = "Monthly Charge", DestinationColumnName = "Monthly Charge"], [SourceColumnName = "Extra International Charges", DestinationColumnName = "Extra International Charges"], [SourceColumnName = "Extra Data Charges", DestinationColumnName = "Extra Data Charges"], [SourceColumnName = "Total Charges", DestinationColumnName = "Total Charges"], [SourceColumnName = "Loaded At", DestinationColumnName = "Loaded At"]}], DynamicSchema = false, UpdateMethod = [Kind = "Replace"], TypeSettings = [Kind = "Table"]]]}]
shared #"Gold_Fact_Customer Subscriptions" = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "Silver_Customer Churn", ItemKind = "Table"]}[Data],
  #"Merged queries" = Table.NestedJoin(#"Navigation 2", {"Customer ID", "Phone Number", "Gender", "Demographics", "Age", "Age Bin", "Group", "Number of Customers in Group", "Intl Active", "Intl Plan", "Unlimited Data Plan", "Device Protection & Online Backup", "Churn Label", "Churned"}, Gold_Dim_Customers, {"Customer ID", "Phone Number", "Gender", "Demographics", "Age", "Age Bin", "Is Contract Group", "Number of Customers in Group", "Is International Calls Active", "Is International Plan", "Is Unlimited Data Plan", "Is Device Protection And Online Backup", "Is Churn", "Churn Flag"}, "Gold_Dim_Customers", JoinKind.LeftOuter),
  #"Expanded Gold_Dim_Customers" = Table.ExpandTableColumn(#"Merged queries", "Gold_Dim_Customers", {"Customer Key"}, {"Customer Key"}),
  #"Merged queries 1" = Table.NestedJoin(#"Expanded Gold_Dim_Customers", {"Contract Type", "Contract Category", "Payment Method"}, Gold_Dim_Contracts, {"Contract Type", "Contract Category", "Payment Method"}, "Gold_Dim_Contracts", JoinKind.LeftOuter),
  #"Expanded Gold_Dim_Contracts" = Table.ExpandTableColumn(#"Merged queries 1", "Gold_Dim_Contracts", {"Contract Key"}, {"Contract Key"}),
  #"Merged queries 2" = Table.NestedJoin(#"Expanded Gold_Dim_Contracts", {"Churn Reason", "Churn Category"}, Gold_Dim_Churn, {"Churn Reason", "Churn Category"}, "Gold_Dim_Churn", JoinKind.LeftOuter),
  #"Expanded Gold_Dim_Churn" = Table.ExpandTableColumn(#"Merged queries 2", "Gold_Dim_Churn", {"Churn Key"}, {"Churn Key"}),
  #"Merged queries 3" = Table.NestedJoin(#"Expanded Gold_Dim_Churn", {"State"}, Gold_Dim_State, {"State Code"}, "Gold_Dim_State", JoinKind.LeftOuter),
  #"Expanded Gold_Dim_State" = Table.ExpandTableColumn(#"Merged queries 3", "Gold_Dim_State", {"State Key"}, {"State Key"}),
  #"Removed other columns" = Table.SelectColumns(#"Expanded Gold_Dim_State", {"Account Length Months", "Local Calls", "Local Mins", "Intl Calls", "Intl Mins", "Extra International Charges", "Customer Service Calls", "Avg Monthly GB Download", "Extra Data Charges", "Monthly Charge", "Total Charges", "Loaded At", "Grouped Consumption", "Customer Key", "Contract Key", "Churn Key", "State Key"}),
  #"Added index" = Table.AddIndexColumn(#"Removed other columns", "Index", 1, 1, Int64.Type),
  #"Reordered columns" = Table.ReorderColumns(#"Added index", {"Index", "Customer Key", "State Key", "Contract Key", "Churn Key", "Grouped Consumption", "Avg Monthly GB Download", "Local Calls", "Local Mins", "Intl Calls", "Intl Mins", "Customer Service Calls", "Account Length Months", "Monthly Charge", "Extra International Charges", "Extra Data Charges", "Total Charges", "Loaded At"}),
  #"Renamed columns" = Table.RenameColumns(#"Reordered columns", {{"Index", "Subscription Key"}, {"Intl Calls", "International Calls"}, {"Intl Mins", "International Mins"}})
in
  #"Renamed columns";
shared Gold_Dim_Customers = let
  Source = Fabric.Warehouse(null),
  Navigation = Source{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  #"Navigation 1" = Navigation{[warehouseId = "d6ec9ac5-ffc0-4b20-94c8-4f8d9b905df8"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Schema = "gold", Item = "Dim_Customers"]}[Data]
in
  #"Navigation 2";
shared Gold_Dim_State = let
  Source = Fabric.Warehouse(null),
  Navigation = Source{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  #"Navigation 1" = Navigation{[warehouseId = "d6ec9ac5-ffc0-4b20-94c8-4f8d9b905df8"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Schema = "gold", Item = "Dim_State"]}[Data]
in
  #"Navigation 2";
shared Gold_Dim_Churn = let
  Source = Fabric.Warehouse(null),
  Navigation = Source{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  #"Navigation 1" = Navigation{[warehouseId = "d6ec9ac5-ffc0-4b20-94c8-4f8d9b905df8"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Schema = "gold", Item = "Dim_Churn"]}[Data]
in
  #"Navigation 2";
shared Gold_Dim_Contracts = let
  Source = Fabric.Warehouse(null),
  Navigation = Source{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  #"Navigation 1" = Navigation{[warehouseId = "d6ec9ac5-ffc0-4b20-94c8-4f8d9b905df8"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Schema = "gold", Item = "Dim_Contracts"]}[Data]
in
  #"Navigation 2";
shared #"Gold_Fact_Customer Subscriptions_DataDestination" = let
  Pattern = Fabric.Warehouse([CreateNavigationProperties = false, HierarchicalNavigation = true]),
  Navigation_1 = Pattern{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  Navigation_2 = Navigation_1{[warehouseId = "d6ec9ac5-ffc0-4b20-94c8-4f8d9b905df8"]}[Data],
  Navigation_3 = Navigation_2{[Schema = "gold"]}[Data],
  TableNavigation = Navigation_3{[Name = "Fact_Customer Subscriptions"]}?[Data]?
in
  TableNavigation;
