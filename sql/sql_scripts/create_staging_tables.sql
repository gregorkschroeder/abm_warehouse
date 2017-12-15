BEGIN TRANSACTION

-- Create staging schema if it does not exist
IF NOT EXISTS (SELECT schema_name FROM information_schema.schemata WHERE schema_name='staging')
BEGIN
	EXEC (N'CREATE SCHEMA [staging]')
END

PRINT 'create airport_out staging table'
IF OBJECT_ID('staging.airport_out','U') IS NOT NULL
DROP TABLE [staging].[airport_out]
CREATE TABLE [staging].[airport_out] (
	[id] int NOT NULL,
	[direction] bit NOT NULL,
    [purpose] tinyint NOT NULL,
    [size] tinyint NOT NULL,
    [income] tinyint NOT NULL,
    [nights] tinyint NOT NULL,
    [departTime] tinyint NOT NULL,
    [originMGRA] int NOT NULL,
    [destinationMGRA] int NOT NULL,
    [tripMode] smallint NOT NULL,
    [arrivalMode] smallint NOT NULL,
    [boardingTAP] int NOT NULL,
	[alightingTAP] int NOT NULL,
	CONSTRAINT pk_staging_airportout PRIMARY KEY([id]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create bikeMgraLogsum staging table'
IF OBJECT_ID('staging.bikeMgraLogsum','U') IS NOT NULL
DROP TABLE [staging].[bikeMgraLogsum]
CREATE TABLE [staging].[bikeMgraLogsum] (
	[i] int NOT NULL,
    [j] int NOT NULL,
	[time] decimal(6,3) NOT NULL,
	CONSTRAINT pk_staging_bikeMgraLogsum PRIMARY KEY([i], [j]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create commtrip staging table'
IF OBJECT_ID('staging.commtrip','U') IS NOT NULL
DROP TABLE [staging].[commtrip]
CREATE TABLE [staging].[commtrip] (
	[ORIG_TAZ] int NOT NULL,
    [DEST_TAZ] int NOT NULL,
	[TOD] nchar(2) NOT NULL,
	[TRIPS_COMMVEH] decimal(12, 6) NOT NULL,
	CONSTRAINT pk_staging_commtrip PRIMARY KEY([ORIG_TAZ], [DEST_TAZ], [TOD]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create crossBorderTours staging table'
IF OBJECT_ID('staging.crossBorderTours','U') IS NOT NULL
DROP TABLE [staging].[crossBorderTours]
CREATE TABLE [staging].[crossBorderTours] (
	[id] int NOT NULL,
    [purpose] tinyint NOT NULL,
    [sentri] nchar(5) NOT NULL,
	[poe] tinyint NOT NULL,
	[departTime] tinyint NOT NULL,
	[arriveTime] tinyint NOT NULL,
	[originMGRA] int NOT NULL,
    [destinationMGRA] int NOT NULL,
	[tourMode] tinyint NOT NULL,
	CONSTRAINT pk_staging_crossBorderTours PRIMARY KEY([id]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create crossBorderTrips staging table'
IF OBJECT_ID('staging.crossBorderTrips','U') IS NOT NULL
DROP TABLE [staging].[crossBorderTrips]
CREATE TABLE [staging].[crossBorderTrips] (
	[tourID] int NOT NULL,
    [tripID] tinyint NOT NULL,
	[originPurp] smallint NOT NULL,
	[destPurp] smallint NOT NULL,
	[originMGRA] int NOT NULL,
    [destinationMGRA] int NOT NULL,
	[inbound] nchar(5) NOT NULL,
	[period] tinyint NOT NULL,
	[tripMode] tinyint NOT NULL,
	[boardingTap] int NOT NULL,
	alightingTap int NOT NULL,
	CONSTRAINT pk_staging_crossBorderTrips PRIMARY KEY([tourID], [tripID]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create eetrip staging table'
IF OBJECT_ID('staging.eetrip','U') IS NOT NULL
DROP TABLE [staging].[eetrip]
CREATE TABLE [staging].[eetrip] (
	[ORIG_TAZ] int NOT NULL,
    [DEST_TAZ] int NOT NULL,
	[TRIPS_EE] decimal(12, 6) NOT NULL,
	CONSTRAINT pk_staging_eetrip PRIMARY KEY([ORIG_TAZ], [DEST_TAZ]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create eitrip staging table'
IF OBJECT_ID('staging.eitrip','U') IS NOT NULL
DROP TABLE [staging].[eitrip]
CREATE TABLE [staging].[eitrip] (
	[ORIG_TAZ] int NOT NULL,
    [DEST_TAZ] int NOT NULL,
    [TOD] nchar(2) NOT NULL,
    [PURPOSE] nchar(7) NOT NULL,
	[TRIPS_DAN] decimal(20, 16) NOT NULL,
	[TRIPS_S2N] decimal(20, 16) NOT NULL,
	[TRIPS_S3N] decimal(20, 16) NOT NULL,
	[TRIPS_DAT] decimal(20, 16) NOT NULL,
	[TRIPS_S2T] decimal(20, 16) NOT NULL,
	[TRIPS_S3T] decimal(20, 16) NOT NULL,
	CONSTRAINT pk_staging_eitrip PRIMARY KEY([ORIG_TAZ], [DEST_TAZ],
	    [TOD], [PURPOSE]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create householdData staging table'
IF OBJECT_ID('staging.householdData','U') IS NOT NULL
DROP TABLE [staging].[householdData]
CREATE TABLE [staging].[householdData] (
	[hh_id] int NOT NULL,
    [autos] tinyint NOT NULL,
    [transponder] bit NOT NULL,
	CONSTRAINT pk_staging_householdData PRIMARY KEY([hh_id]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create households staging table'
IF OBJECT_ID('staging.households','U') IS NOT NULL
DROP TABLE [staging].[households]
CREATE TABLE [staging].[households] (
	[hhid] int NOT NULL,
    [household_serial_no] bigint NOT NULL,
    [taz] int NOT NULL,
    [mgra] int NOT NULL,
    [hinccat1] tinyint NOT NULL,
    [hinc] int NOT NULL,
    [hworkers] tinyint NOT NULL,
    [veh] tinyint NOT NULL,
    [persons] tinyint NOT NULL,
    [hht] tinyint NOT NULL,
    [bldgsz] tinyint NOT NULL,
    [unittype] tinyint NOT NULL,
    [version] int NOT NULL,
    [poverty] decimal(7,4) NOT NULL,
	CONSTRAINT pk_staging_households PRIMARY KEY([hhid]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create indivTourData staging table'
IF OBJECT_ID('staging.indivTourData','U') IS NOT NULL
DROP TABLE [staging].[indivTourData]
CREATE TABLE [staging].[indivTourData] (
    [person_id] int NOT NULL,
    [tour_id]  tinyint NOT NULL,
    [tour_category] nchar(25) NOT NULL,
    [tour_purpose] nchar(15) NOT NULL,
    [orig_mgra] int NOT NULL,
    [dest_mgra] int NOT NULL,
    [start_period] tinyint NOT NULL,
    [end_period] tinyint NOT NULL,
    [tour_mode] tinyint NOT NULL,
	CONSTRAINT pk_staging_indivTourData PRIMARY KEY(
	[person_id], [tour_id], [tour_purpose]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create indivTripData staging table'
IF OBJECT_ID('staging.indivTripData','U') IS NOT NULL
DROP TABLE [staging].[indivTripData]
CREATE TABLE [staging].[indivTripData] (
    [person_id] int NOT NULL,
    [tour_id]  tinyint NOT NULL,
    [stop_id] smallint NOT NULL,
    [inbound] bit NOT NULL,
    [tour_purpose] nchar(15) NOT NULL,
    [orig_purpose] nchar(15) NOT NULL,
    [dest_purpose] nchar(15) NOT NULL,
    [orig_mgra] int NOT NULL,
    [dest_mgra] int NOT NULL,
    [parking_mgra] int NOT NULL,
    [stop_period] tinyint NOT NULL,
    [trip_mode] tinyint NOT NULL,
    [trip_board_tap] int NOT NULL,
    [trip_alight_tap] int NOT NULL,
	CONSTRAINT pk_staging_indivTripData PRIMARY KEY(
	    [person_id], [tour_id], [stop_id], [inbound], [tour_purpose]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create internalExternalTrips staging table'
IF OBJECT_ID('staging.internalExternalTrips','U') IS NOT NULL
DROP TABLE [staging].[internalExternalTrips]
CREATE TABLE [staging].[internalExternalTrips] (
    [id] int IDENTITY(1,1) NOT NULL,
    [tourID] int NOT NULL,
    [originMGRA] int NOT NULL,
    [destinationMGRA] int NOT NULL,
    [inbound] nchar(5) NOT NULL,
    [period] tinyint NOT NULL,
    [tripMode] tinyint NOT NULL,
    [boardingTap] int NOT NULL,
    [alightingTap] int NOT NULL,
	CONSTRAINT pk_staging_internalExternalTrips PRIMARY KEY([id]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create jointTourData staging table'
IF OBJECT_ID('staging.jointTourData','U') IS NOT NULL
DROP TABLE [staging].[jointTourData]
CREATE TABLE [staging].[jointTourData] (
    [hh_id] int NOT NULL,
    [tour_id]  tinyint NOT NULL,
    [tour_category] nchar(20) NOT NULL,
    [tour_purpose] nchar(15) NOT NULL,
    [tour_participants] nchar(20) NOT NULL,
    [orig_mgra] int NOT NULL,
    [dest_mgra] int NOT NULL,
    [start_period] tinyint NOT NULL,
    [end_period] tinyint NOT NULL,
    [tour_mode] tinyint NOT NULL,
	CONSTRAINT pk_staging_jointTourData PRIMARY KEY([hh_id], [tour_id]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create jointTripData staging table'
IF OBJECT_ID('staging.jointTripData','U') IS NOT NULL
DROP TABLE [staging].[jointTripData]
CREATE TABLE [staging].[jointTripData] (
    [hh_id] int NOT NULL,
    [tour_id]  tinyint NOT NULL,
    [stop_id] smallint NOT NULL,
    [inbound] bit NOT NULL,
    [orig_purpose] nchar(15) NOT NULL,
    [dest_purpose] nchar(15) NOT NULL,
    [orig_mgra] int NOT NULL,
    [dest_mgra] int NOT NULL,
    [parking_mgra] int NOT NULL,
    [stop_period] tinyint NOT NULL,
    [trip_mode] tinyint NOT NULL,
    [trip_board_tap] int NOT NULL,
    [trip_alight_tap] int NOT NULL,
	CONSTRAINT pk_staging_jointTripData PRIMARY KEY(
	[hh_id], [tour_id], [stop_id], [inbound]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create personData staging table'
IF OBJECT_ID('staging.personData','U') IS NOT NULL
DROP TABLE [staging].[personData]
CREATE TABLE [staging].[personData] (
    [hh_id] int NOT NULL,
    [person_id] int NOT NULL,
    [person_num] tinyint NOT NULL,
    [age] tinyint NOT NULL,
    [gender] nchar(1) NOT NULL,
    [type] nchar(30) NOT NULL,
    [value_of_time] float NOT NULL, /* determine data type */
    [activity_pattern] nchar(1) NOT NULL,
    [fp_choice] smallint NOT NULL,
    [reimb_pct] decimal(8,6) NOT NULL,
	CONSTRAINT pk_staging_personData PRIMARY KEY([person_id]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create persons staging table'
IF OBJECT_ID('staging.persons','U') IS NOT NULL
DROP TABLE [staging].[persons]
CREATE TABLE [staging].[persons] (
    [hhid] int NOT NULL,
    [perid] int NOT NULL,
    [household_serial_no] bigint NOT NULL,
    [pnum] tinyint NOT NULL,
    [age] tinyint NOT NULL,
    [sex] tinyint NOT NULL,
    [military] tinyint NOT NULL,
    [pemploy] tinyint NOT NULL,
    [pstudent] tinyint NOT NULL,
    [ptype] tinyint NOT NULL,
    [educ] tinyint NOT NULL,
    [grade] tinyint NOT NULL,
    [occen5] smallint NOT NULL,
    [occsoc5] nchar(15) NOT NULL,
    [indcen] smallint NOT NULL,
    [weeks] tinyint NOT NULL,
    [hours] tinyint NOT NULL,
    [rac1p] tinyint NOT NULL,
    [hisp] tinyint NOT NULL,
    [version] int NOT NULL,
	CONSTRAINT pk_staging_persons PRIMARY KEY([perid]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create tapskim staging table'
IF OBJECT_ID('staging.tapskim','U') IS NOT NULL
DROP TABLE [staging].[tapskim]
CREATE TABLE [staging].[tapskim] (
	[ORIG_TAP] int NOT NULL,
    [DEST_TAP] int NOT NULL,
    [TOD] nchar(2) NOT NULL,
    [TIME_INIT_WAIT_PREMIUM_TRANSIT] decimal(8,4) NOT NULL,
    [TIME_IVT_TIME_PREMIUM_TRANSIT] decimal(8,4) NOT NULL,
    [TIME_WALK_TIME_PREMIUM_TRANSIT] decimal(8,4) NOT NULL,
    [TIME_TRANSFER_TIME_PREMIUM_TRANSIT] decimal(8,4) NOT NULL,
    [FARE_PREMIUM_TRANSIT] decimal(4,2) NOT NULL,
	CONSTRAINT pk_staging_tapskim PRIMARY KEY([ORIG_TAP], [DEST_TAP], [TOD]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create tazskim staging table'
IF OBJECT_ID('staging.tazskim','U') IS NOT NULL
DROP TABLE [staging].[tazskim]
CREATE TABLE [staging].[tazskim] (
	[ORIG_TAZ] int NOT NULL,
    [DEST_TAZ] int NOT NULL,
    [TOD] nchar(2) NOT NULL,
    [DIST_DRIVE_ALONE_TOLL] decimal(12,6) NOT NULL,
    [TIME_DRIVE_ALONE_TOLL] decimal(12,6) NOT NULL,
    [COST_DRIVE_ALONE_TOLL] int NOT NULL,
    [DIST_DRIVE_ALONE_FREE] decimal(12,6) NOT NULL,
    [TIME_DRIVE_ALONE_FREE] decimal(12,6) NOT NULL,
    [DIST_HOV2_TOLL] decimal(12,6) NOT NULL,
    [TIME_HOV2_TOLL] decimal(12,6) NOT NULL,
    [COST_HOV2_TOLL] int NOT NULL,
    [DIST_HOV2_FREE] decimal(12,6) NOT NULL,
    [TIME_HOV2_FREE] decimal(12,6) NOT NULL,
    [DIST_HOV3_TOLL] decimal(12,6) NOT NULL,
    [TIME_HOV3_TOLL] decimal(12,6) NOT NULL,
    [COST_HOV3_TOLL] int NOT NULL,
    [DIST_HOV3_FREE] decimal(12,6) NOT NULL,
    [TIME_HOV3_FREE] decimal(12,6) NOT NULL,
    [DIST_TRUCK_HH_TOLL] decimal(12,6) NOT NULL,
    [TIME_TRUCK_HH_TOLL] decimal(12,6) NOT NULL,
    [COST_TRUCK_HH_TOLL] int NOT NULL,
    [DIST_TRUCK_HH_FREE] decimal(12,6) NOT NULL,
    [TIME_TRUCK_HH_FREE] decimal(12,6) NOT NULL,
	CONSTRAINT pk_staging_tazskim PRIMARY KEY([ORIG_TAZ], [DEST_TAZ], [TOD]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create visitorTours staging table'
IF OBJECT_ID('staging.visitorTours','U') IS NOT NULL
DROP TABLE [staging].[visitorTours]
CREATE TABLE [staging].[visitorTours] (
    [id] int NOT NULL,
    [segment] bit NOT NULL,
    [purpose] tinyint NOT NULL,
    [autoAvailable] bit NOT NULL,
    [partySize] tinyint NOT NULL,
    [income] tinyint NOT NULL,
    [departTime] tinyint NOT NULL,
    [arriveTime] tinyint NOT NULL,
    [originMGRA] int NOT NULL,
    [destinationMGRA] int NOT NULL,
    [tourMode] tinyint NOT NULL,
	CONSTRAINT pk_staging_visitorTours PRIMARY KEY([id]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create visitorTrips staging table'
IF OBJECT_ID('staging.visitorTrips','U') IS NOT NULL
DROP TABLE [staging].[visitorTrips]
CREATE TABLE [staging].[visitorTrips] (
	[tourID] int NOT NULL,
	[tripID] tinyint NOT NULL,
    [originPurp] smallint NOT NULL,
	[destPurp] smallint NOT NULL,
	[originMGRA] int NOT NULL,
    [destinationMGRA] int NOT NULL,
	[inbound] char(5) NOT NULL,
	[period] tinyint NOT NULL,
	[tripMode] tinyint NOT NULL,
	[boardingTap] int NOT NULL,
	[alightingTap] int NOT NULL,
	CONSTRAINT pk_staging_visitorTrips PRIMARY KEY([tourID], [tripID]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)



PRINT 'create walkMgraEquivMinutes staging table'
IF OBJECT_ID('staging.walkMgraEquivMinutes','U') IS NOT NULL
DROP TABLE [staging].[walkMgraEquivMinutes]
CREATE TABLE [staging].[walkMgraEquivMinutes] (
	[i] int NOT NULL,
	[j] int NOT NULL,
	[percieved] decimal(6,3) NOT NULL,
	[actual] decimal(6,3) NOT NULL,
	[gain] decimal(5,1) NOT NULL,
	CONSTRAINT pk_staging_walkMgraEquivMinutes PRIMARY KEY([i], [j]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create walkMgraTapEquivMinutes staging table'
IF OBJECT_ID('staging.walkMgraTapEquivMinutes','U') IS NOT NULL
DROP TABLE [staging].[walkMgraTapEquivMinutes]
CREATE TABLE [staging].[walkMgraTapEquivMinutes] (
	[mgra] int NOT NULL,
	[tap] int NOT NULL,
	[boardingPerceived] decimal(6,3) NOT NULL,
	[boardingActual] decimal(6,3) NOT NULL,
	[alightingPerceived] decimal(6,3) NOT NULL,
	[alightingActual] decimal(6,3) NOT NULL,
	[boardingGain] decimal(4,1) NOT NULL,
	[alightingGain] decimal(4,1) NOT NULL,
	CONSTRAINT pk_staging_walkMgraTapEquivMinutes PRIMARY KEY([mgra], [tap]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


PRINT 'create wsLocResults staging table'
IF OBJECT_ID('staging.wsLocResults','U') IS NOT NULL
DROP TABLE [staging].[wsLocResults]
CREATE TABLE [staging].[wsLocResults] (
	[PersonID] int NOT NULL,
	[EmploymentCategory] tinyint NOT NULL,
	[StudentCategory] tinyint NOT NULL,
    [WorkSegment] int NOT NULL,
    [SchoolSegment] int NOT NULL,
    [WorkLocation] int NOT NULL,
    [SchoolLocation] int NOT NULL,
	CONSTRAINT pk_staging_wsLocResults PRIMARY KEY([PersonID]))
ON staging_fg
WITH (DATA_COMPRESSION = PAGE)


COMMIT TRANSACTION
