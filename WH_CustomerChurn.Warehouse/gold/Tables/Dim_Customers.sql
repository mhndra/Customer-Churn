CREATE TABLE [gold].[Dim_Customers] (

	[Customer Key] bigint NULL, 
	[Customer ID] varchar(8000) NULL, 
	[Phone Number] varchar(8000) NULL, 
	[Gender] varchar(8000) NULL, 
	[Demographics] varchar(8000) NULL, 
	[Age] bigint NULL, 
	[Age Bin] bigint NULL, 
	[Is Contract Group] varchar(8000) NULL, 
	[Number of Customers in Group] bigint NULL, 
	[Is International Calls Active] varchar(8000) NULL, 
	[Is International Plan] varchar(8000) NULL, 
	[Is Unlimited Data Plan] varchar(8000) NULL, 
	[Is Device Protection And Online Backup] varchar(8000) NULL, 
	[Is Churn] varchar(8000) NULL, 
	[Churn Flag] bigint NULL
);