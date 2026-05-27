[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Gold_Dim_Churn_DataDestination", IsNewTarget = true], Settings = [Kind = "Manual", AllowCreation = true, ColumnSettings = [Mappings = {[SourceColumnName = "Churn Key", DestinationColumnName = "Churn Key"], [SourceColumnName = "Churn Reason", DestinationColumnName = "Churn Reason"], [SourceColumnName = "Churn Category", DestinationColumnName = "Churn Category"]}], DynamicSchema = false, UpdateMethod = [Kind = "Replace"], TypeSettings = [Kind = "Table"]]]}]
shared Gold_Dim_Churn = let
  Source = Lakehouse.Contents(null),
  Navigation = Source{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  #"Navigation 1" = Navigation{[lakehouseId = "28e8d742-e815-4575-842c-2d1645ba854c"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[Id = "Silver_Customer Churn", ItemKind = "Table"]}[Data],
  #"Removed other columns" = Table.SelectColumns(#"Navigation 2", {"Churn Category", "Churn Reason"}),
  #"Removed duplicates" = Table.Distinct(#"Removed other columns", {"Churn Category", "Churn Reason"}),
  #"Added index" = Table.AddIndexColumn(#"Removed duplicates", "Index", 1, 1, Int64.Type),
  #"Reordered columns" = Table.ReorderColumns(#"Added index", {"Index", "Churn Reason", "Churn Category"}),
  #"Renamed columns" = Table.RenameColumns(#"Reordered columns", {{"Index", "Churn Key"}})
in
  #"Renamed columns";
shared Gold_Dim_Churn_DataDestination = let
  Pattern = Fabric.Warehouse([CreateNavigationProperties = false, HierarchicalNavigation = true]),
  Navigation_1 = Pattern{[workspaceId = "9d91a240-6d39-4462-928b-e18c37e3049c"]}[Data],
  Navigation_2 = Navigation_1{[warehouseId = "d6ec9ac5-ffc0-4b20-94c8-4f8d9b905df8"]}[Data],
  Navigation_3 = Navigation_2{[Schema = "gold"]}[Data],
  TableNavigation = Navigation_3{[Name = "Dim_Churn"]}?[Data]?
in
  TableNavigation;
