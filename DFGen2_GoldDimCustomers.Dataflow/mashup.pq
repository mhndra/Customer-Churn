[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Gold_Dim_Customers_DataDestination", IsNewTarget = true], Settings = [Kind = "Manual", AllowCreation = true, ColumnSettings = [Mappings = {[SourceColumnName = "Customer Key", DestinationColumnName = "Customer Key"], [SourceColumnName = "Customer ID", DestinationColumnName = "Customer ID"], [SourceColumnName = "Phone Number", DestinationColumnName = "Phone Number"], [SourceColumnName = "Gender", DestinationColumnName = "Gender"], [SourceColumnName = "Demographics", DestinationColumnName = "Demographics"], [SourceColumnName = "Age", DestinationColumnName = "Age"], [SourceColumnName = "Age Bin", DestinationColumnName = "Age Bin"], [SourceColumnName = "Is Contract Group", DestinationColumnName = "Is Contract Group"], [SourceColumnName = "Number of Customers in Group", DestinationColumnName = "Number of Customers in Group"], [SourceColumnName = "Is International Calls Active", DestinationColumnName = "Is International Calls Active"], [SourceColumnName = "Is International Plan", DestinationColumnName = "Is International Plan"], [SourceColumnName = "Is Unlimited Data Plan", DestinationColumnName = "Is Unlimited Data Plan"], [SourceColumnName = "Is Device Protection And Online Backup", DestinationColumnName = "Is Device Protection And Online Backup"], [SourceColumnName = "Is Churn", DestinationColumnName = "Is Churn"], [SourceColumnName = "Churn Flag", DestinationColumnName = "Churn Flag"]}], DynamicSchema = false, UpdateMethod = [Kind = "Replace"], TypeSettings = [Kind = "Table"]]]}]
shared Gold_Dim_Customers = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "Silver_Customer Churn", ItemKind = "Table"]}[Data],
  #"Removed other columns" = Table.SelectColumns(#"Navigation 2", {"Customer ID", "Churn Label", "Intl Active", "Intl Plan", "Unlimited Data Plan", "Phone Number", "Gender", "Age", "Group", "Number of Customers in Group", "Device Protection & Online Backup", "Churned", "Demographics", "Age Bin"}),
  #"Removed duplicates" = Table.Distinct(#"Removed other columns", {"Customer ID", "Churn Label", "Intl Active", "Intl Plan", "Unlimited Data Plan", "Phone Number", "Gender", "Age", "Group", "Number of Customers in Group", "Device Protection & Online Backup", "Churned", "Demographics", "Age Bin"}),
  #"Added index" = Table.AddIndexColumn(#"Removed duplicates", "Index", 1, 1, Int64.Type),
  #"Reordered columns" = Table.ReorderColumns(#"Added index", {"Index", "Customer ID", "Phone Number", "Gender", "Demographics", "Age", "Age Bin", "Group", "Number of Customers in Group", "Intl Active", "Intl Plan", "Unlimited Data Plan", "Device Protection & Online Backup", "Churn Label", "Churned"}),
  #"Renamed columns" = Table.RenameColumns(#"Reordered columns", {{"Index", "Customer Key"}, {"Group", "Is Contract Group"}, {"Intl Active", "Is International Calls Active"}, {"Intl Plan", "Is International Plan"}, {"Unlimited Data Plan", "Is Unlimited Data Plan"}, {"Device Protection & Online Backup", "Is Device Protection And Online Backup"}, {"Churn Label", "Is Churn"}, {"Churned", "Churn Flag"}})
in
  #"Renamed columns";
shared Gold_Dim_Customers_DataDestination = let
  Pattern = Fabric.Warehouse([CreateNavigationProperties = false, HierarchicalNavigation = true]),
  Navigation_1 = Pattern{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  Navigation_2 = Navigation_1{[warehouseId = "d6ec9ac5-ffc0-4b20-94c8-4f8d9b905df8"]}[Data],
  Navigation_3 = Navigation_2{[Schema = "gold"]}[Data],
  TableNavigation = Navigation_3{[Name = "Dim_Customers"]}?[Data]?
in
  TableNavigation;
