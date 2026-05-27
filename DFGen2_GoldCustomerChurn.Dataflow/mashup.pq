[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Gold Dim State_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared #"Gold Dim State" = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "silver.customer_churn", ItemKind = "Table"]}[Data],
  #"Removed other columns" = Table.SelectColumns(#"Navigation 2", {"State"}),
  #"Removed duplicates" = Table.Distinct(#"Removed other columns", {"State"}),
  #"Added index" = Table.AddIndexColumn(#"Removed duplicates", "Index", 1, 1, Int64.Type),
  #"Renamed columns" = Table.RenameColumns(#"Added index", {{"Index", "State Key"}, {"State", "State Code"}}),
  #"Reordered columns" = Table.ReorderColumns(#"Renamed columns", {"State Key", "State Code"})
in
  #"Reordered columns";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Gold Dim Contracts_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared #"Gold Dim Contracts" = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "silver.customer_churn", ItemKind = "Table"]}[Data],
  #"Removed other columns" = Table.SelectColumns(#"Navigation 2", {"Contract Type", "Payment Method", "Contract Category"}),
  #"Removed duplicates" = Table.Distinct(#"Removed other columns", {"Contract Type", "Payment Method", "Contract Category"}),
  #"Added index" = Table.AddIndexColumn(#"Removed duplicates", "Index", 1, 1, Int64.Type),
  #"Renamed columns" = Table.RenameColumns(#"Added index", {{"Index", "Contract Key"}}),
  #"Reordered columns" = Table.ReorderColumns(#"Renamed columns", {"Contract Key", "Contract Type", "Contract Category", "Payment Method"})
in
  #"Reordered columns";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Gold Dim Churn_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared #"Gold Dim Churn" = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "silver.customer_churn", ItemKind = "Table"]}[Data],
  #"Removed other columns" = Table.SelectColumns(#"Navigation 2", {"Churn Category", "Churn Reason"}),
  #"Removed duplicates" = Table.Distinct(#"Removed other columns", {"Churn Category", "Churn Reason"}),
  #"Added index" = Table.AddIndexColumn(#"Removed duplicates", "Index", 1, 1, Int64.Type),
  #"Reordered columns" = Table.ReorderColumns(#"Added index", {"Index", "Churn Reason", "Churn Category"}),
  #"Renamed columns" = Table.RenameColumns(#"Reordered columns", {{"Index", "Churn Key"}})
in
  #"Renamed columns";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Gold Dim Customers_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared #"Gold Dim Customers" = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "silver.customer_churn", ItemKind = "Table"]}[Data],
  #"Removed other columns" = Table.SelectColumns(#"Navigation 2", {"Customer ID", "Churn Label", "Intl Active", "Intl Plan", "Unlimited Data Plan", "Phone Number", "Gender", "Age", "Group", "Number of Customers in Group", "Device Protection & Online Backup", "Churned", "Demographics", "Age Bin"}),
  #"Removed duplicates" = Table.Distinct(#"Removed other columns", {"Customer ID", "Churn Label", "Intl Active", "Intl Plan", "Unlimited Data Plan", "Phone Number", "Gender", "Age", "Group", "Number of Customers in Group", "Device Protection & Online Backup", "Churned", "Demographics", "Age Bin"}),
  #"Added index" = Table.AddIndexColumn(#"Removed duplicates", "Index", 1, 1, Int64.Type),
  #"Reordered columns" = Table.ReorderColumns(#"Added index", {"Index", "Customer ID", "Phone Number", "Gender", "Demographics", "Age", "Age Bin", "Group", "Number of Customers in Group", "Intl Active", "Intl Plan", "Unlimited Data Plan", "Device Protection & Online Backup", "Churn Label", "Churned"}),
  #"Renamed columns" = Table.RenameColumns(#"Reordered columns", {{"Index", "Customer Key"}, {"Group", "Is Contract Group"}, {"Intl Active", "Is International Calls Active"}, {"Intl Plan", "Is International Plan"}, {"Unlimited Data Plan", "Is Unlimited Data Plan"}, {"Device Protection & Online Backup", "Is Device Protection And Online Backup"}, {"Churn Label", "Is Churn"}, {"Churned", "Churn Flag"}})
in
  #"Renamed columns";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Gold Fact Customer Subscriptions_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared #"Gold Fact Customer Subscriptions" = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "silver.customer_churn", ItemKind = "Table"]}[Data],
  #"Merged queries" = Table.NestedJoin(#"Navigation 2", {"State"}, #"Gold Dim State", {"State Code"}, "Gold Dim State", JoinKind.LeftOuter),
  #"Expanded Gold Dim State" = Table.ExpandTableColumn(#"Merged queries", "Gold Dim State", {"State Key"}, {"State Key"}),
  #"Merged queries 1" = Table.NestedJoin(#"Expanded Gold Dim State", {"Contract Type", "Payment Method", "Contract Category"}, #"Gold Dim Contracts", {"Contract Type", "Payment Method", "Contract Category"}, "Gold Dim Contracts", JoinKind.LeftOuter),
  #"Expanded Gold_Dim_Contracts" = Table.ExpandTableColumn(#"Merged queries 1", "Gold Dim Contracts", {"Contract Key"}, {"Contract Key"}),
  #"Merged queries 2" = Table.NestedJoin(#"Expanded Gold_Dim_Contracts", {"Churn Reason", "Churn Category"}, #"Gold Dim Churn", {"Churn Reason", "Churn Category"}, "Gold Dim Churn", JoinKind.LeftOuter),
  #"Expanded Gold_Dim_Churn" = Table.ExpandTableColumn(#"Merged queries 2", "Gold Dim Churn", {"Churn Key"}, {"Churn Key"}),
  #"Merged queries 3" = Table.NestedJoin(#"Expanded Gold_Dim_Churn", {"Customer ID", "Phone Number", "Gender", "Demographics", "Age", "Age Bin", "Group", "Number of Customers in Group", "Intl Active", "Intl Plan", "Unlimited Data Plan", "Device Protection & Online Backup", "Churn Label", "Churned"}, #"Gold Dim Customers", {"Customer ID", "Phone Number", "Gender", "Demographics", "Age", "Age Bin", "Is Contract Group", "Number of Customers in Group", "Is International Calls Active", "Is International Plan", "Is Unlimited Data Plan", "Is Device Protection And Online Backup", "Is Churn", "Churn Flag"}, "Gold Dim Customers", JoinKind.LeftOuter),
  #"Expanded Gold Dim Customers" = Table.ExpandTableColumn(#"Merged queries 3", "Gold Dim Customers", {"Customer Key"}, {"Customer Key"}),
  #"Removed other columns" = Table.SelectColumns(#"Expanded Gold Dim Customers", {"Account Length Months", "Local Calls", "Local Mins", "Intl Calls", "Intl Mins", "Extra International Charges", "Customer Service Calls", "Avg Monthly GB Download", "Extra Data Charges", "Monthly Charge", "Total Charges", "Loaded At", "Grouped Consumption", "Customer Key", "Contract Key", "Churn Key", "State Key"}),
  #"Added index" = Table.AddIndexColumn(#"Removed other columns", "Index", 1, 1, Int64.Type),
  #"Reordered columns" = Table.ReorderColumns(#"Added index", {"Index", "Customer Key", "State Key", "Contract Key", "Churn Key", "Grouped Consumption", "Avg Monthly GB Download", "Local Calls", "Local Mins", "Intl Calls", "Intl Mins", "Customer Service Calls", "Account Length Months", "Monthly Charge", "Extra International Charges", "Extra Data Charges", "Total Charges", "Loaded At"}),
  #"Renamed columns" = Table.RenameColumns(#"Reordered columns", {{"Index", "Subscription Key"}, {"Intl Calls", "International Calls"}, {"Intl Mins", "International Mins"}})
in
  #"Renamed columns";
shared #"Gold Dim State_DataDestination" = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  Navigation_3 = Navigation_2{[Id = "gold", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "Dim_State", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared #"Gold Dim Contracts_DataDestination" = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  Navigation_3 = Navigation_2{[Id = "gold", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "Dim_Contracts", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared #"Gold Dim Churn_DataDestination" = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  Navigation_3 = Navigation_2{[Id = "gold", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "Dim_Churn", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared #"Gold Dim Customers_DataDestination" = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  Navigation_3 = Navigation_2{[Id = "gold", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "Dim_Customers", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared #"Gold Fact Customer Subscriptions_DataDestination" = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  Navigation_3 = Navigation_2{[Id = "gold", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "Fact_Customer Subscriptions", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
