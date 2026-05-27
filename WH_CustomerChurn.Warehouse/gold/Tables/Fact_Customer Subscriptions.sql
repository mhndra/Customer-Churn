CREATE TABLE [gold].[Fact_Customer Subscriptions] (

	[Subscription Key] bigint NULL, 
	[Customer Key] bigint NULL, 
	[State Key] bigint NULL, 
	[Contract Key] bigint NULL, 
	[Churn Key] bigint NULL, 
	[Grouped Consumption] varchar(8000) NULL, 
	[Avg Monthly GB Download] bigint NULL, 
	[Local Calls] bigint NULL, 
	[Local Mins] float NULL, 
	[International Calls] bigint NULL, 
	[International Mins] float NULL, 
	[Customer Service Calls] bigint NULL, 
	[Account Length Months] bigint NULL, 
	[Monthly Charge] float NULL, 
	[Extra International Charges] float NULL, 
	[Extra Data Charges] float NULL, 
	[Total Charges] float NULL, 
	[Loaded At] datetime2(6) NULL
);