[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "gold dim_state_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared #"gold dim_state" = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "a298258a-25c5-47b7-b809-d2c4b6246ebf"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "a2cf5112-d7cc-44e2-bd1f-0e270656104e"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "silver_dataflow.customer_churn_enriched", ItemKind = "Table"]}[Data],
  #"Removed other columns" = Table.SelectColumns(#"Navigation 2", {"State"}),
  #"Removed duplicates" = Table.Distinct(#"Removed other columns", {"State"}),
  #"Added index" = Table.AddIndexColumn(#"Removed duplicates", "Index", 1, 1, Int64.Type),
  #"Renamed columns" = Table.RenameColumns(#"Added index", {{"Index", "State Key"}, {"State", "State Code"}}),
  #"Reordered columns" = Table.ReorderColumns(#"Renamed columns", {"State Key", "State Code"})
in
  #"Reordered columns";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "gold dim_contracts_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared #"gold dim_contracts" = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "a298258a-25c5-47b7-b809-d2c4b6246ebf"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "a2cf5112-d7cc-44e2-bd1f-0e270656104e"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "silver_dataflow.customer_churn_enriched", ItemKind = "Table"]}[Data],
  #"Removed other columns" = Table.SelectColumns(#"Navigation 2", {"Contract Type", "Payment Method", "Contract Category"}),
  #"Removed duplicates" = Table.Distinct(#"Removed other columns", {"Contract Type", "Payment Method", "Contract Category"}),
  #"Added index" = Table.AddIndexColumn(#"Removed duplicates", "Index", 1, 1, Int64.Type),
  #"Renamed columns" = Table.RenameColumns(#"Added index", {{"Index", "Contract Key"}}),
  #"Reordered columns" = Table.ReorderColumns(#"Renamed columns", {"Contract Key", "Contract Type", "Contract Category", "Payment Method"})
in
  #"Reordered columns";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "gold dim_churn_descriptions_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared #"gold dim_churn_descriptions" = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "a298258a-25c5-47b7-b809-d2c4b6246ebf"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "a2cf5112-d7cc-44e2-bd1f-0e270656104e"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "silver_dataflow.customer_churn_enriched", ItemKind = "Table"]}[Data],
  #"Removed other columns" = Table.SelectColumns(#"Navigation 2", {"Churn Category", "Churn Reason"}),
  #"Removed duplicates" = Table.Distinct(#"Removed other columns", {"Churn Category", "Churn Reason"}),
  #"Added index" = Table.AddIndexColumn(#"Removed duplicates", "Index", 1, 1, Int64.Type),
  #"Reordered columns" = Table.ReorderColumns(#"Added index", {"Index", "Churn Reason", "Churn Category"}),
  #"Renamed columns" = Table.RenameColumns(#"Reordered columns", {{"Index", "Churn Key"}})
in
  #"Renamed columns";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "gold dim_customers_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared #"gold dim_customers" = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "a298258a-25c5-47b7-b809-d2c4b6246ebf"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "a2cf5112-d7cc-44e2-bd1f-0e270656104e"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "silver_dataflow.customer_churn_enriched", ItemKind = "Table"]}[Data],
  #"Removed other columns" = Table.SelectColumns(#"Navigation 2", {"Customer ID", "Churn Label", "International Active", "International Plan", "Unlimited Data Plan", "Phone Number", "Gender", "Age", "Group", "Number of Customers in Group", "Device Protection & Online Backup", "Churned", "Demographics", "Age Bin"}),
  #"Removed duplicates" = Table.Distinct(#"Removed other columns", {"Customer ID", "Churn Label", "International Active", "International Plan", "Unlimited Data Plan", "Phone Number", "Gender", "Age", "Group", "Number of Customers in Group", "Device Protection & Online Backup", "Churned", "Demographics", "Age Bin"}),
  #"Added index" = Table.AddIndexColumn(#"Removed duplicates", "Index", 1, 1, Int64.Type),
  #"Reordered columns" = Table.ReorderColumns(#"Added index", {"Index", "Customer ID", "Phone Number", "Gender", "Demographics", "Age", "Age Bin", "Group", "Number of Customers in Group", "International Active", "International Plan", "Unlimited Data Plan", "Device Protection & Online Backup", "Churn Label", "Churned"}),
  #"Renamed columns" = Table.RenameColumns(#"Reordered columns", {{"Index", "Customer Key"}, {"Group", "Is Contract Group"}, {"International Active", "Is International Calls Active"}, {"International Plan", "Is International Plan"}, {"Unlimited Data Plan", "Is Unlimited Data Plan"}, {"Device Protection & Online Backup", "Is Device Protection And Online Backup"}, {"Churn Label", "Is Churn"}, {"Churned", "Churn Flag"}})
in
  #"Renamed columns";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "gold fact_customer_subscriptions_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared #"gold fact_customer_subscriptions" = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "a298258a-25c5-47b7-b809-d2c4b6246ebf"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "a2cf5112-d7cc-44e2-bd1f-0e270656104e"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "silver_dataflow.customer_churn_enriched", ItemKind = "Table"]}[Data],
  #"Merged queries" = Table.NestedJoin(#"Navigation 2", {"State"}, #"gold dim_state", {"State Code"}, "Gold Dim State", JoinKind.LeftOuter),
  #"Expanded Gold Dim State" = Table.ExpandTableColumn(#"Merged queries", "Gold Dim State", {"State Key"}, {"State Key"}),
  #"Merged queries 1" = Table.NestedJoin(#"Expanded Gold Dim State", {"Contract Type", "Payment Method", "Contract Category"}, #"gold dim_contracts", {"Contract Type", "Payment Method", "Contract Category"}, "Gold Dim Contracts", JoinKind.LeftOuter),
  #"Expanded Gold_Dim_Contracts" = Table.ExpandTableColumn(#"Merged queries 1", "Gold Dim Contracts", {"Contract Key"}, {"Contract Key"}),
  #"Merged queries 2" = Table.NestedJoin(#"Expanded Gold_Dim_Contracts", {"Churn Reason", "Churn Category"}, #"gold dim_churn_descriptions", {"Churn Reason", "Churn Category"}, "Gold Dim Churn", JoinKind.LeftOuter),
  #"Expanded Gold_Dim_Churn" = Table.ExpandTableColumn(#"Merged queries 2", "Gold Dim Churn", {"Churn Key"}, {"Churn Key"}),
  #"Merged queries 3" = Table.NestedJoin(#"Expanded Gold_Dim_Churn", {"Customer ID", "Phone Number", "Gender", "Demographics", "Age", "Age Bin", "Group", "Number of Customers in Group", "International Active", "International Plan", "Unlimited Data Plan", "Device Protection & Online Backup", "Churn Label", "Churned"}, #"gold dim_customers", {"Customer ID", "Phone Number", "Gender", "Demographics", "Age", "Age Bin", "Is Contract Group", "Number of Customers in Group", "Is International Calls Active", "Is International Plan", "Is Unlimited Data Plan", "Is Device Protection And Online Backup", "Is Churn", "Churn Flag"}, "Gold Dim Customers", JoinKind.LeftOuter),
  #"Expanded Gold Dim Customers" = Table.ExpandTableColumn(#"Merged queries 3", "Gold Dim Customers", {"Customer Key"}, {"Customer Key"}),
  #"Removed other columns" = Table.SelectColumns(#"Expanded Gold Dim Customers", {"Account Length Months", "Local Calls", "Local Mins", "International Calls", "International Mins", "Extra International Charges", "Customer Service Calls", "Avg Monthly GB Download", "Extra Data Charges", "Monthly Charge", "Total Charges", "Loaded at", "Grouped Consumption", "Customer Key", "Contract Key", "Churn Key", "State Key"}),
  #"Added index" = Table.AddIndexColumn(#"Removed other columns", "Index", 1, 1, Int64.Type),
  #"Reordered columns" = Table.ReorderColumns(#"Added index", {"Index", "Customer Key", "State Key", "Contract Key", "Churn Key", "Grouped Consumption", "Avg Monthly GB Download", "Local Calls", "Local Mins", "International Calls", "International Mins", "Customer Service Calls", "Account Length Months", "Monthly Charge", "Extra International Charges", "Extra Data Charges", "Total Charges", "Loaded at"}),
  #"Renamed columns" = Table.RenameColumns(#"Reordered columns", {{"Index", "Customer Subscription Key"}})
in
  #"Renamed columns";
shared #"gold dim_state_DataDestination" = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "a298258a-25c5-47b7-b809-d2c4b6246ebf"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "a518a941-f003-43c3-a936-9782b007ae81"]}[Data],
  Navigation_3 = Navigation_2{[Id = "gold_dataflow", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "dim_state", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared #"gold dim_contracts_DataDestination" = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "a298258a-25c5-47b7-b809-d2c4b6246ebf"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "a518a941-f003-43c3-a936-9782b007ae81"]}[Data],
  Navigation_3 = Navigation_2{[Id = "gold_dataflow", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "dim_contracts", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared #"gold dim_customers_DataDestination" = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "a298258a-25c5-47b7-b809-d2c4b6246ebf"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "a518a941-f003-43c3-a936-9782b007ae81"]}[Data],
  Navigation_3 = Navigation_2{[Id = "gold_dataflow", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "dim_customers", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared #"gold dim_churn_descriptions_DataDestination" = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "a298258a-25c5-47b7-b809-d2c4b6246ebf"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "a518a941-f003-43c3-a936-9782b007ae81"]}[Data],
  Navigation_3 = Navigation_2{[Id = "gold_dataflow", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "dim_churn_descriptions", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
shared #"gold fact_customer_subscriptions_DataDestination" = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "a298258a-25c5-47b7-b809-d2c4b6246ebf"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "a518a941-f003-43c3-a936-9782b007ae81"]}[Data],
  Navigation_3 = Navigation_2{[Id = "gold_dataflow", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "fact_customer_subscriptions", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
