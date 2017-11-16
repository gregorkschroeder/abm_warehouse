USE [ws]


BEGIN TRANSACTION


PRINT 'create airport_trips staging table'
IF OBJECT_ID('staging.airport_trips','U') IS NOT NULL
DROP TABLE [staging].[airport_trips]

CREATE TABLE
	[staging].[airport_trips] (
		[id] int NOT NULL,
		[direction] bit NOT NULL,
    	[purpose] tinyint NOT NULL,
        [size] tinyint NOT NULL,
        [income] tinyint NOT NULL,
        [nights] tinyint NOT NULL,
        [departTime] smallint NOT NULL,
        [originMGRA] int NOT NULL,
        [destinationMGRA] int NOT NULL,
        [tripMode] smallint NOT NULL,
        [boardingTAP] tinyint NOT NULL,
		[alightingTAP] int NOT NULL,
		CONSTRAINT pk_airport_trips PRIMARY KEY([id])
	)
WITH
	(DATA_COMPRESSION = PAGE)


PRINT 'create crossborder_tours staging table'
IF OBJECT_ID('staging.crossborder_tours','U') IS NOT NULL
DROP TABLE [staging].[crossborder_tours]

CREATE TABLE
	[staging].[crossborder_tours] (
		[id] int NOT NULL,
    	[purpose] tinyint NOT NULL,
    	[sentri] nchar(5) NOT NULL,
		[poe] tinyint NOT NULL,
		[departTime] smallint NOT NULL,
		[arriveTime] smallint NOT NULL,
		[originMGRA] int NOT NULL,
        [destinationMGRA] int NOT NULL,
		[originTAZ] int NOT NULL,
        [destinationTAZ] int NOT NULL,
		[tourMode] tinyint NOT NULL,
		CONSTRAINT pk_crossborder_tours PRIMARY KEY([id])
	)
WITH
	(DATA_COMPRESSION = PAGE)


PRINT 'create crossborder_trips staging table'
IF OBJECT_ID('staging.crossborder_trips','U') IS NOT NULL
DROP TABLE [staging].[crossborder_trips]

CREATE TABLE
	[staging].[crossborder_trips] (
		[tourID] int NOT NULL,
    	[tripID] int NOT NULL,
		[originPurp] tinyint NOT NULL,
		[destPurp] tinyint NOT NULL,
		[originMGRA] int NOT NULL,
        [destinationMGRA] int NOT NULL,
		[originTAZ] int NOT NULL,
        [destinationTAZ] int NOT NULL,
		[inbound] nchar(5) NOT NULL,
		[originIsTourDestination] nchar(5) NOT NULL,
		[destinationIsTourDestination] nchar(5) NOT NULL,
		[period] smallint NOT NULL,
		[tripMode] smallint NOT NULL,
		[boardingTap] int NOT NULL,
		alightingTap int NOT NULL,
		CONSTRAINT pk_crossborder_trips PRIMARY KEY([tourID], [tripID])
	)
WITH
	(DATA_COMPRESSION = PAGE)


PRINT 'create internalexternal_trips staging table'
IF OBJECT_ID('staging.internalexternal_trips','U') IS NOT NULL
DROP TABLE [staging].[internalexternal_trips]

CREATE TABLE
	[staging].[internalexternal_trips] (
		[id] int IDENTITY(1,1) NOT NULL,
		[hhID] int NOT NULL,
    	[pnum] int NOT NULL,
		[personID] int NOT NULL,
		[tourID] int NOT NULL,
		[originMGRA] int NOT NULL,
        [destinationMGRA] int NOT NULL,
		[originTAZ] int NOT NULL,
        [destinationTAZ] int NOT NULL,
		[inbound] nchar(5) NOT NULL,
		[originIsTourDestination] nchar(5) NOT NULL,
		[destinationIsTourDestination] nchar(5) NOT NULL,
		[period] smallint NOT NULL,
		[tripMode] smallint NOT NULL,
		[boardingTap] int NOT NULL,
		[alightingTap] int NOT NULL,
		CONSTRAINT pk_internalexternal_trips PRIMARY KEY([id])
	)
WITH
	(DATA_COMPRESSION = PAGE)


PRINT 'create visitor_tours staging table'
IF OBJECT_ID('staging.visitor_tours','U') IS NOT NULL
DROP TABLE [staging].[visitor_tours]

CREATE TABLE
	[staging].[visitor_tours] (
		[id] int NOT NULL,
		[segment] bit NOT NULL,
    	[purpose] tinyint NOT NULL,
		[autoAvailable] bit NOT NULL,
		[partySize] tinyint NOT NULL,
		[income] tinyint NOT NULL,
		[departTime] smallint NOT NULL,
		[arriveTime] smallint NOT NULL,
		[originMGRA] int NOT NULL,
        [destinationMGRA] int NOT NULL,
		[tourMode] smallint NOT NULL,
		[outboundStops] int NOT NULL,
        [inboundStops] int NOT NULL
		CONSTRAINT pk_visitor_tours PRIMARY KEY([id])
	)
WITH
	(DATA_COMPRESSION = PAGE)


PRINT 'create visitor_trips staging table'
IF OBJECT_ID('staging.visitor_trips','U') IS NOT NULL
DROP TABLE [staging].[visitor_trips]

CREATE TABLE
	[staging].[visitor_trips] (
		[tourID] int NOT NULL,
		[tripID] int NOT NULL,
    	[originPurp] tinyint NOT NULL,
		[destPurp] tinyint NOT NULL,
		[originMGRA] int NOT NULL,
        [destinationMGRA] int NOT NULL,
		[inbound] char(5) NOT NULL,
		[originIsTourDestination] char(5) NOT NULL,
		[destinationIsTourDestination] char(5) NOT NULL,
		[period] smallint NOT NULL,
		[tripMode] smallint NOT NULL,
		[boardingTap] int NOT NULL,
		[alightingTap] int NOT NULL,
		CONSTRAINT pk_visitor_trips PRIMARY KEY([tourID], [tripID])
	)
WITH
	(DATA_COMPRESSION = PAGE)


COMMIT TRANSACTION
