BEGIN TRANSACTION

-- create dimension schema if it does not exist
IF NOT EXISTS (SELECT schema_name FROM information_schema.schemata WHERE schema_name='dimension')
EXEC (N'CREATE SCHEMA [dimension]')

-- create fact schema if it does not exist
IF NOT EXISTS (SELECT schema_name FROM information_schema.schemata WHERE schema_name='fact')
EXEC (N'CREATE SCHEMA [fact]')

-- create geography dimension
-- use an input file to fill at a later step
CREATE TABLE [dimension].[geography] (
	[geography_id] int IDENTITY(0,1) NOT NULL,
	[mgra_13] nchar(20) NOT NULL,
	[taz_13] nchar(20) NOT NULL,
	[luz_13] nchar(20) NOT NULL,
	[region_2004] nchar(20) NOT NULL,
	CONSTRAINT pk_geography PRIMARY KEY([geography_id]),
	CONSTRAINT ixuq_geography UNIQUE([mgra_13], [taz_13]) WITH (DATA_COMPRESSION = PAGE))
ON reference_fg
WITH (DATA_COMPRESSION = PAGE)
GO

-- create geography role-playing views
-- household location
CREATE VIEW [dimension].[geography_household_location] AS
SELECT
	[geography_id] AS [geography_household_location_id]
	,[mgra_13] AS [household_location_mgra_13]
	,[taz_13] AS [household_location_taz_13]
	,[luz_13] AS [household_location_luz_13]
	,[region_2004] AS [household_location_region_2004]
FROM
	[dimension].[geography]
GO

-- school location
CREATE VIEW [dimension].[geography_school_location] AS
SELECT
	[geography_id] AS [geography_school_location_id]
	,[mgra_13] AS [school_location_mgra_13]
	,[taz_13] AS [school_location_taz_13]
	,[luz_13] AS [school_location_luz_13]
	,[region_2004] AS [school_location_region_2004]
FROM
	[dimension].[geography]
GO

-- tour end
CREATE VIEW [dimension].[geography_tour_end] AS
SELECT
	[geography_id] AS [geography_tour_end_id]
	,[mgra_13] AS [tour_end_mgra_13]
	,[taz_13] AS [tour_end_taz_13]
	,[luz_13] AS [tour_end_luz_13]
	,[region_2004] AS [tour_end_region_2004]
FROM
	[dimension].[geography]
GO

-- tour start
CREATE VIEW [dimension].[geography_tour_start] AS
SELECT
	[geography_id] AS [geography_tour_start_id]
	,[mgra_13] AS [tour_start_mgra_13]
	,[taz_13] AS [tour_start_taz_13]
	,[luz_13] AS [tour_start_luz_13]
	,[region_2004] AS [tour_start_region_2004]
FROM
	[dimension].[geography]
GO

-- trip end
CREATE VIEW [dimension].[geography_trip_end] AS
SELECT
	[geography_id] AS [geography_trip_end_id]
	,[mgra_13] AS [trip_end_mgra_13]
	,[taz_13] AS [trip_end_taz_13]
	,[luz_13] AS [trip_end_luz_13]
	,[region_2004] AS [trip_end_region_2004]
FROM
	[dimension].[geography]
GO

-- trip start
CREATE VIEW [dimension].[geography_trip_start] AS
SELECT
	[geography_id] AS [geography_trip_start_id]
	,[mgra_13] AS [trip_start_mgra_13]
	,[taz_13] AS [trip_start_taz_13]
	,[luz_13] AS [trip_start_luz_13]
	,[region_2004] AS [trip_start_region_2004]
FROM
	[dimension].[geography]
GO

-- work_location
CREATE VIEW [dimension].[geography_work_location] AS
SELECT
	[geography_id] AS [geography_work_location_id]
	,[mgra_13] AS [work_location_mgra_13]
	,[taz_13] AS [work_location_taz_13]
	,[luz_13] AS [work_location_luz_13]
	,[region_2004] AS [work_location_region_2004]
FROM
	[dimension].[geography]
GO

-- create household dimension
-- partitioned clustered columnstore
CREATE TABLE [dimension].[household] (
	[scenario_id] int NOT NULL,
	[household_id] int NOT NULL,
	[household_income] int NULL,
	[household_income_category] nchar(20) NOT NULL,
	[household_size] nchar(20) NOT NULL,
	[household_unit_type] nchar(50) NOT NULL,
	[household_autos] nchar(20) NOT NULL,
	[household_transponder] nchar(20) NOT NULL,
	[household_poverty] decimal(7,4) NULL,
	[geography_household_location_id] int NOT NULL,
	INDEX ccsi_household CLUSTERED COLUMNSTORE)
ON scenario_scheme([scenario_id])

-- create inbound dimension
CREATE TABLE [dimension].[inbound] (
	[inbound_id] tinyint IDENTITY(0,1) NOT NULL,
	[inbound_description] nchar(20) NOT NULL,
	CONSTRAINT pk_inbound PRIMARY KEY ([inbound_id]),
	CONSTRAINT ixuq_inbound UNIQUE ([inbound_description]) WITH (DATA_COMPRESSION = PAGE))
ON reference_fg
WITH (DATA_COMPRESSION = PAGE)
INSERT INTO [dimension].[inbound] VALUES
('Not Applicable'), ('Inbound'), ('Outbound')

-- create mode dimension
-- will add aggregations in later
CREATE TABLE [dimension].[mode] (
	[mode_id] tinyint IDENTITY(0,1) NOT NULL,
	[mode_description] nchar(75) NOT NULL,
	CONSTRAINT pk_mode PRIMARY KEY ([mode_id]),
	CONSTRAINT ixuq_mode UNIQUE ([mode_description]) WITH (DATA_COMPRESSION = PAGE))
ON reference_fg
WITH (DATA_COMPRESSION = PAGE)
INSERT INTO [dimension].[mode] VALUES
('Not Applicable'),
('Auto SOV (Non-Toll)'),
('Auto SOV (Toll)'),
('Auto 2 Person (Non-Toll, Non-HOV)'),
('Auto 2 Person (Non-Toll, HOV)'),
('Auto 2 Person (Toll, HOV)'),
('Auto 3+ Person (Non-Toll, Non-HOV)'),
('Auto 3+ Person (Non-Toll, HOV)'),
('Auto 3+ Person (Toll, HOV)'),
('Walk'),
('Bike'),
('Walk-Local Bus'),
('Walk-Express Bus'),
('Walk-Bus Rapid Transit'),
('Walk-Light Rail'),
('Walk-Heavy Rail'),
('PNR-Local Bus'),
('PNR-Express Bus'),
('PNR-Bus Rapid Transit'),
('PNR-Light Rail'),
('PNR-Heavy Rail'),
('KNR-Local Bus'),
('KNR-Express Bus'),
('KNR-Bus Rapid Transit'),
('KNR-Light Rail'),
('KNR-Heavy Rail'),
('School Bus'),
('Taxi'),
('Cross Border Tour: Drive Alone'),
('Cross Border Tour: Shared 2'),
('Cross Border Tour: Shared 3'),
('Cross Border Tour: Walk'),
('Light Heavy Duty Truck (Non-Toll)'),
('Light Heavy Duty Truck (Toll)'),
('Medium Heavy Duty Truck (Non-Toll)'),
('Medium Heavy Duty Truck (Toll)'),
('Heavy Heavy Duty Truck (Non-Toll)'),
('Heavy Heavy Duty Truck (Toll)'),
('Airport: Passing-Through'),
('Airport Arrival: Parking Lot Terminal'),
('Airport Arrival: Parking Lot off-site San Diego Airport area'),
('Airport Arrival: Parking Lot off-site Private'),
('Airport Arrival: Pickup/Drop-off Escort'),
('Airport Arrival: Pickup/Drop-off Curbside'),
('Airport Arrival: Rental Car'),
('Airport Arrival: Shuttle/Van/Courtesy Vehicle'),
('Airport Arrival: Transit')
GO

-- create mode role-playing views
-- tour mode
CREATE VIEW [dimension].[mode_tour] AS
SELECT
	[mode_id] AS [mode_tour_id]
	,[mode_description] AS [mode_tour_description]
FROM
	[dimension].[mode]
GO

-- trip mode
CREATE VIEW [dimension].[mode_trip] AS
SELECT
	[mode_id] AS [mode_trip_id]
	,[mode_description] AS [mode_trip_description]
FROM
	[dimension].[mode]
GO

-- create model dimension
-- will add aggregations in later
CREATE TABLE [dimension].[model] (
	[model_id] tinyint IDENTITY(0,1) NOT NULL,
	[model_description] nchar(20) NOT NULL,
	CONSTRAINT pk_model PRIMARY KEY ([model_id]),
	CONSTRAINT ixuq_model UNIQUE ([model_description]) WITH (DATA_COMPRESSION = PAGE))
ON reference_fg
WITH (DATA_COMPRESSION = PAGE)
INSERT INTO [dimension].[model] VALUES
('Not Applicable'),
('Individual'),
('Joint'),
('Visitor'),
('Internal-External'),
('Cross Border'),
('Airport'),
('Commercial Vehicle'),
('External-External'),
('External-Internal'),
('Truck')

-- create person dimension
-- partitioned clustered columnstore
CREATE TABLE [dimension].[person] (
	[scenario_id] int NOT NULL,
	[person_id] int NOT NULL,
	[household_id] int NOT NULL,
	[person_age] smallint NULL,
	[person_sex] nvarchar(20) NOT NULL,
	[person_employ_status] nchar(50) NOT NULL,
	[person_student_status] nchar(50) NOT NULL,
	[person_military_status] nchar(50) NOT NULL,
	[person_abm_person_type] nchar(50) NOT NULL,
	[person_hispanic] nchar(25) NOT NULL,
	[person_race] nchar(150) NOT NULL,
	[person_work_from_home] nchar(25) NOT NULL,
	[person_home_schooled] nchar(20) NOT NULL,
	[geography_work_location_id] int NOT NULL,
	[geography_school_location_id] int NOT NULL,
	INDEX ccsi_person CLUSTERED COLUMNSTORE)
ON scenario_scheme([scenario_id])

-- create purpose dimension
-- will add aggregations in later
CREATE TABLE [dimension].[purpose] (
	[purpose_id] tinyint IDENTITY(0,1) NOT NULL,
	[purpose_description] nchar(25) NOT NULL,
	CONSTRAINT pk_purpose PRIMARY KEY ([purpose_id]),
	CONSTRAINT ixuq_mpurpose UNIQUE ([purpose_description]) WITH (DATA_COMPRESSION = PAGE))
ON reference_fg
WITH (DATA_COMPRESSION = PAGE)
INSERT INTO [dimension].[purpose] VALUES
('Not Applicable'),
('None'),
('Work'),
('University'),
('School'),
('Escort'),
('Shop'),
('Maintenance'),
('Eating Out'),
('Visiting'),
('Discretionary'),
('Work-Based'),
('Work Related'),
('Home'),
('Other'),
('Dining'),
('Return to Origin'),
('External'),
('Cargo'),
('Visit'),
('Resident-Business'),
('Resident-Personal'),
('Visitor-Business'),
('Visitor-Personal'),
('Non-Work')
GO

-- create purpose role-playing views
-- tour purpose
CREATE VIEW [dimension].[purpose_tour] AS
SELECT
	[purpose_id] AS [purpose_tour_id],
	[purpose_description] AS [purpose_tour_description]
FROM
	[dimension].[purpose]
GO

-- trip start purpose
CREATE VIEW [dimension].[purpose_trip_end] AS
SELECT
	[purpose_id] AS [purpose_trip_end_id],
	[purpose_description] AS [purpose_trip_end_description]
FROM
	[dimension].[purpose]
GO

-- trip start purpose
CREATE VIEW [dimension].[purpose_trip_start] AS
SELECT
	[purpose_id] AS [purpose_trip_start_id],
	[purpose_description] AS [purpose_trip_start_description]
FROM
	[dimension].[purpose]
GO

-- create scenario dimension
CREATE TABLE [dimension].[scenario] (
	[scenario_id] int IDENTITY(1,1) NOT NULL,
	[scenario_desc] nchar(50) NOT NULL,
	[scenario_year] smallint NOT NULL,
	[scenario_iteration] tinyint NOT NULL,
	[scenario_sample_rate] decimal(6, 4) NOT NULL,
	[scenario_abm_version] nchar(50) NOT NULL,
	[scenario_path] nchar(200) NOT NULL,
	[scenario_user] nchar(100) NOT NULL,
	[scenario_complete] bit NULL,
	[scenario_date_loaded] smalldatetime NULL,
	CONSTRAINT pk_scenario PRIMARY KEY ([scenario_id]))
ON reference_fg
WITH (DATA_COMPRESSION = PAGE)

-- create time dimension
CREATE TABLE [dimension].[time] (
	[time_id] int IDENTITY(0,1) NOT NULL,
	[abm_half_hour] nchar(20) NOT NULL,
	[abm_half_hour_period_start] time(0) NULL,
	[abm_half_hour_period_end] time(0) NULL,
	[abm_5_tod] nchar(20) NOT NULL,
	[abm_5_tod_period_start] time(0) NULL,
	[abm_5_tod_period_end] time(0) NULL,
	[day] nchar(20) NOT NULL,
	[day_period_start] time(0) NULL,
	[day_period_end] time(0) NULL,
	CONSTRAINT pk_time PRIMARY KEY([time_id]),
	CONSTRAINT ixuq_time UNIQUE([time_id], [abm_half_hour], [abm_5_tod], [day]) WITH (DATA_COMPRESSION = PAGE))
ON reference_fg
WITH (DATA_COMPRESSION = PAGE)
INSERT INTO [dimension].[time] VALUES
('Not Applicable',NULL,NULL,'Not Applicable',NULL,NULL,'Not Applicable',NULL,NULL),
('Not Applicable',NULL,NULL,'Not Applicable',NULL,NULL,'1','00:00:00','23:59:59'),
('Not Applicable',NULL,NULL,'1','03:00:00','05:59:59','1','00:00:00','23:59:59'),
('Not Applicable',NULL,NULL,'2','06:00:00','08:59:59','1','00:00:00','23:59:59'),
('Not Applicable',NULL,NULL,'3','09:00:00','15:29:59','1','00:00:00','23:59:59'),
('Not Applicable',NULL,NULL,'4','15:30:00','18:59:59','1','00:00:00','23:59:59'),
('Not Applicable',NULL,NULL,'5','19:00:00','02:59:59','1','00:00:00','23:59:59'),
('0',NULL,NULL,'Not Applicable',NULL,NULL,'Not Applicable',NULL,NULL),
('1','03:00:00','04:59:59','1','03:00:00','05:59:59','1','00:00:00','23:59:59'),
('2','05:00:00','05:29:59','1','03:00:00','05:59:59','1','00:00:00','23:59:59'),
('3','05:30:00','05:59:59','1','03:00:00','05:59:59','1','00:00:00','23:59:59'),
('4','06:00:00','06:29:59','2','06:00:00','08:59:59','1','00:00:00','23:59:59'),
('5','06:30:00','06:59:59','2','06:00:00','08:59:59','1','00:00:00','23:59:59'),
('6','07:00:00','07:29:59','2','06:00:00','08:59:59','1','00:00:00','23:59:59'),
('7','07:30:00','07:59:59','2','06:00:00','08:59:59','1','00:00:00','23:59:59'),
('8','08:00:00','08:29:59','2','06:00:00','08:59:59','1','00:00:00','23:59:59'),
('9','08:30:00','08:59:59','2','06:00:00','08:59:59','1','00:00:00','23:59:59'),
('10','09:00:00','09:29:59','3','09:00:00','15:29:59','1','00:00:00','23:59:59'),
('11','09:30:00','09:59:59','3','09:00:00','15:29:59','1','00:00:00','23:59:59'),
('12','10:00:00','10:29:59','3','09:00:00','15:29:59','1','00:00:00','23:59:59'),
('13','10:30:00','10:59:59','3','09:00:00','15:29:59','1','00:00:00','23:59:59'),
('14','11:00:00','11:29:59','3','09:00:00','15:29:59','1','00:00:00','23:59:59'),
('15','11:30:00','11:59:59','3','09:00:00','15:29:59','1','00:00:00','23:59:59'),
('16','12:00:00','12:29:59','3','09:00:00','15:29:59','1','00:00:00','23:59:59'),
('17','12:30:00','12:59:59','3','09:00:00','15:29:59','1','00:00:00','23:59:59'),
('18','13:00:00','13:29:59','3','09:00:00','15:29:59','1','00:00:00','23:59:59'),
('19','13:30:00','13:59:59','3','09:00:00','15:29:59','1','00:00:00','23:59:59'),
('20','14:00:00','14:29:59','3','09:00:00','15:29:59','1','00:00:00','23:59:59'),
('21','14:30:00','14:59:59','3','09:00:00','15:29:59','1','00:00:00','23:59:59'),
('22','15:00:00','15:29:59','3','09:00:00','15:29:59','1','00:00:00','23:59:59'),
('23','15:30:00','15:59:59','4','15:30:00','18:59:59','1','00:00:00','23:59:59'),
('24','16:00:00','16:29:59','4','15:30:00','18:59:59','1','00:00:00','23:59:59'),
('25','16:30:00','16:59:59','4','15:30:00','18:59:59','1','00:00:00','23:59:59'),
('26','17:00:00','17:29:59','4','15:30:00','18:59:59','1','00:00:00','23:59:59'),
('27','17:30:00','17:59:59','4','15:30:00','18:59:59','1','00:00:00','23:59:59'),
('28','18:00:00','18:29:59','4','15:30:00','18:59:59','1','00:00:00','23:59:59'),
('29','18:30:00','18:59:59','4','15:30:00','18:59:59','1','00:00:00','23:59:59'),
('30','19:00:00','19:29:59','5','19:00:00','02:59:59','1','00:00:00','23:59:59'),
('31','19:30:00','19:59:59','5','19:00:00','02:59:59','1','00:00:00','23:59:59'),
('32','20:00:00','20:29:59','5','19:00:00','02:59:59','1','00:00:00','23:59:59'),
('33','20:30:00','20:59:59','5','19:00:00','02:59:59','1','00:00:00','23:59:59'),
('34','21:00:00','21:29:59','5','19:00:00','02:59:59','1','00:00:00','23:59:59'),
('35','21:30:00','21:59:59','5','19:00:00','02:59:59','1','00:00:00','23:59:59'),
('36','22:00:00','22:29:59','5','19:00:00','02:59:59','1','00:00:00','23:59:59'),
('37','22:30:00','22:59:59','5','19:00:00','02:59:59','1','00:00:00','23:59:59'),
('38','23:00:00','23:29:59','5','19:00:00','02:59:59','1','00:00:00','23:59:59'),
('39','23:30:00','23:59:59','5','19:00:00','02:59:59','1','00:00:00','23:59:59'),
('40','00:00:00','02:59:59','5','19:00:00','02:59:59','1','00:00:00','23:59:59')
GO

-- create time role-playing views
-- tour end time
CREATE VIEW [dimension].[time_tour_end] AS
SELECT
	[time_id] AS [time_tour_end_id]
    ,[abm_half_hour] AS [tour_end_abm_half_hour]
    ,[abm_half_hour_period_start] AS [tour_end_abm_half_hour_period_start]
    ,[abm_half_hour_period_end] AS [tour_end_abm_half_hour_period_end]
    ,[abm_5_tod] AS [tour_end_abm_5_tod]
    ,[abm_5_tod_period_start] AS [tour_end_abm_5_tod_period_start]
    ,[abm_5_tod_period_end] AS [tour_end_abm_5_tod_period_end]
    ,[day] AS [tour_end_day]
    ,[day_period_start] AS [tour_end_day_period_start]
    ,[day_period_end] AS [tour_end_day_period_end]
FROM
	[dimension].[time]
GO

-- tour start time
CREATE VIEW [dimension].[time_tour_start] AS
SELECT
	[time_id] AS [time_tour_start_id]
    ,[abm_half_hour] AS [tour_start_abm_half_hour]
    ,[abm_half_hour_period_start] AS [tour_start_abm_half_hour_period_start]
    ,[abm_half_hour_period_end] AS [tour_start_abm_half_hour_period_end]
    ,[abm_5_tod] AS [tour_start_abm_5_tod]
    ,[abm_5_tod_period_start] AS [tour_start_abm_5_tod_period_start]
    ,[abm_5_tod_period_end] AS [tour_start_abm_5_tod_period_end]
    ,[day] AS [tour_start_day]
    ,[day_period_start] AS [tour_start_day_period_start]
    ,[day_period_end] AS [tour_start_day_period_end]
FROM
	[dimension].[time]
GO

-- trip end time
CREATE VIEW [dimension].[time_trip_end] AS
SELECT
	[time_id] AS [time_trip_end_id]
    ,[abm_half_hour] AS [trip_end_abm_half_hour]
    ,[abm_half_hour_period_start] AS [trip_end_abm_half_hour_period_start]
    ,[abm_half_hour_period_end] AS [trip_end_abm_half_hour_period_end]
    ,[abm_5_tod] AS [trip_end_abm_5_tod]
    ,[abm_5_tod_period_start] AS [trip_end_abm_5_tod_period_start]
    ,[abm_5_tod_period_end] AS [trip_end_abm_5_tod_period_end]
    ,[day] AS [trip_end_day]
    ,[day_period_start] AS [trip_end_day_period_start]
    ,[day_period_end] AS [trip_end_day_period_end]
FROM
	[dimension].[time]
GO

-- trip start time
CREATE VIEW [dimension].[time_trip_start] AS
SELECT
	[time_id] AS [time_trip_start_id]
    ,[abm_half_hour] AS [trip_start_abm_half_hour]
    ,[abm_half_hour_period_start] AS [trip_start_abm_half_hour_period_start]
    ,[abm_half_hour_period_end] AS [trip_start_abm_half_hour_period_end]
    ,[abm_5_tod] AS [trip_start_abm_5_tod]
    ,[abm_5_tod_period_start] AS [trip_start_abm_5_tod_period_start]
    ,[abm_5_tod_period_end] AS [trip_start_abm_5_tod_period_end]
    ,[day] AS [trip_start_day]
    ,[day_period_start] AS [trip_start_day_period_start]
    ,[day_period_end] AS [trip_start_day_period_end]
FROM
	[dimension].[time]
GO

-- create tour dimension
-- partitioned clustered columnstore
CREATE TABLE [dimension].[tour] (
	[scenario_id] int NOT NULL,
	[tour_id] int IDENTITY(0,1) NOT NULL,
	[tour_category] nchar(50) NOT NULL,
	[tour_crossborder_point_of_entry] nchar(30) NOT NULL,
	[tour_crossborder_sentri] nchar(20) NOT NULL,
	[tour_weight] decimal(6,4) NOT NULL,
	INDEX ccsi_tour CLUSTERED COLUMNSTORE)
ON scenario_scheme([scenario_id])

-- create person trips fact
-- partitioned clustered columnstore
CREATE TABLE [fact].[person_trips] (
	[scenario_id] int NOT NULL,
	[person_id] int NOT NULL,
	[household_id] int NOT NULL,
	[tour_id] int NOT NULL,
	[model_id] tinyint NOT NULL,
	[mode_trip_id] tinyint NOT NULL,
	[mode_tour_id] tinyint NOT NULL,
	[purpose_trip_start_id] tinyint NOT NULL,
	[purpose_trip_end_id] tinyint NOT NULL,
	[purpose_tour_id] tinyint NOT NULL,
	[inbound_id] tinyint NOT NULL,
	[time_trip_start_id] int NOT NULL,
	[time_trip_end_id] int NOT NULL,
	[time_tour_start_id] int NOT NULL,
	[time_tour_end_id] int NOT NULL,
	[geography_trip_start_id] int NOT NULL,
	[geography_trip_end_id] int NOT NULL,
	[geography_tour_start_id] int NOT NULL,
	[geography_tour_end_id] int NOT NULL,
	[time_drive] decimal(10, 4) NOT NULL,
	[dist_drive] decimal(10, 4) NOT NULL,
	[cost_drive] decimal(4, 2) NOT NULL,
	[time_walk] decimal(10, 4) NOT NULL,
	[dist_walk] decimal(10, 4) NOT NULL,
	[time_bike] decimal(10, 4) NOT NULL,
	[dist_bike] decimal(10, 4) NOT NULL,
	[time_transit_in_vehicle] decimal(10, 4) NOT NULL,
	[dist_transit_in_vehicle] decimal(10, 4) NOT NULL,
	[cost_transit] decimal(4, 2) NOT NULL,
	[time_transit_walk_access] decimal(10, 4) NOT NULL,
	[dist_transit_walk_access] decimal(10, 4) NOT NULL,
	[time_transit_walk_egress] decimal(10, 4) NOT NULL,
	[dist_transit_walk_egress] decimal(10, 4) NOT NULL,
	[time_transit_transfer] decimal(10, 4) NOT NULL,
	[dist_transit_transfer] decimal(10, 4) NOT NULL,
	[time_transit_initial_wait] decimal(10, 4) NOT NULL,
	[time_total] decimal(10, 4) NOT NULL,
	[dist_total] decimal(10, 4) NOT NULL,
	[cost_total] decimal(4, 2) NOT NULL,
	[transit_transfers] tinyint NOT NULL,
	[weight_person_trip] decimal(6, 4) NOT NULL,
	[weight_trip] decimal(6, 4) NOT NULL,
	INDEX ccsi_tour CLUSTERED COLUMNSTORE)
ON scenario_scheme([scenario_id])

COMMIT TRANSACTION

