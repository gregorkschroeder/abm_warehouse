SET NOCOUNT ON;
BEGIN TRANSACTION person_dimension

-- insert not applicable record for the scenario
INSERT INTO [dimension].[person]
([scenario_id], [person_id], [household_id], [person_age], [person_sex],
 [person_employ_status], [person_student_status], [person_military_status],
 [person_abm_person_type], [person_hispanic], [person_race],
 [person_work_from_home], [person_home_schooled], [geography_work_location_id],
 [geography_school_location_id])
SELECT
	1 AS [scenario_id] -- need to parameterize
	,0 AS [person_id] -- indexing begins at 1
	,0 AS [household_id] -- indexing begins at 1
	,NULL AS [person_age]
	,'Not Applicable' AS [person_sex]
	,'Not Applicable' AS [person_employ_status]
	,'Not Applicable' AS [person_student_status]
	,'Not Applicable' AS [person_military_status]
	,'Not Applicable' AS [person_abm_person_type]
	,'Not Applicable' AS [person_hispanic]
	,'Not Applicable' AS [person_race]
	,'Not Applicable' AS [person_work_from_home]
	,'Not Applicable' AS [person_home_schooled]
	,(SELECT [geography_work_location_id] 
	  FROM [dimension].[geography_work_location] 
	  WHERE	[work_location_mgra_13] = 'Not Applicable' 
			AND [work_location_taz_13] = 'Not Applicable' 
			AND [work_location_luz_13] = 'Not Applicable'
			AND [work_location_region_2004] = 'Not Applicable') -- subquery for the null record
	,(SELECT [geography_school_location_id] 
	  FROM [dimension].[geography_school_location] 
	  WHERE	[school_location_mgra_13] = 'Not Applicable' 
			AND [school_location_taz_13] = 'Not Applicable' 
			AND [school_location_luz_13] = 'Not Applicable'
			AND [school_location_region_2004] = 'Not Applicable') -- subquery for the null record

-- insert person data into dimension table
INSERT INTO [dimension].[person]
([scenario_id], [person_id], [household_id], [person_age], [person_sex],
 [person_employ_status], [person_student_status], [person_military_status],
 [person_abm_person_type], [person_hispanic], [person_race],
 [person_work_from_home], [person_home_schooled], [geography_work_location_id],
 [geography_school_location_id])
SELECT
	1 AS [scenario_id]  -- need to parameterize
	,[personData].[person_id]
	,[personData].[hh_id] AS [household_id]
	,[personData].[age] AS [person_age]
	,CASE	WHEN [personData].[gender] = 'm' THEN 'Male'
			WHEN [personData].[gender] = 'f' THEN 'Female'
			ELSE NULL -- throws insert error on unexpected value since column is not nullable
			END AS [person_sex]
	,CASE	WHEN [persons].[pemploy] = 1 THEN 'Employed Full-Time'
			WHEN [persons].[pemploy] = 2 THEN 'Employed Part-Time'
			WHEN [persons].[pemploy] = 3 THEN 'Unemployed or Not in Labor Force'
			WHEN [persons].[pemploy] = 4 THEN 'Less than 16 Years Old'
			ELSE NULL -- throws insert error on unexpected value since column is not nullable
			END AS [person_employ_status]
	,CASE	WHEN [persons].[pstudent] = 1 THEN 'Pre K-12'
			WHEN [persons].[pstudent] = 2 THEN 'College Undergrad+Grad and Prof. School'
			WHEN [persons].[pstudent] = 3 THEN 'Not Attending School'
			ELSE NULL -- throws insert error on unexpected value since column is not nullable
			END AS [person_student_status]
	,CASE	WHEN [persons].[military] = 0 THEN 'N/A Less than 17 Years Old'
			WHEN [persons].[military] = 1 THEN 'Yes, Now on Active Duty'
			WHEN [persons].[military] = 2 THEN 'Yes, on Active Duty in Past, but Not Now'
			WHEN [persons].[military] = 3 THEN 'No, Training for Reserves/National Guard Only'
			WHEN [persons].[military] = 4 THEN 'No, Never Served in the Military'
			ELSE NULL -- throws insert error on unexpected value since column is not nullable
			END AS [person_military_status]
	,[personData].[type] AS [person_abm_person_type]
	,CASE	WHEN [persons].[hisp] = 1 THEN 'Non-Hispanic'
			WHEN [persons].[hisp] BETWEEN 2 AND 24 THEN 'Hispanic'
			ELSE NULL -- throws insert error on unexpected value since column is not nullable
			END AS [person_hispanic]
    ,CASE	WHEN [persons].[rac1p] = 1 THEN 'White Alone'
			WHEN [persons].[rac1p] = 2 THEN 'Black or African American Alone'
			WHEN [persons].[rac1p] = 3 THEN 'American Indian Alone'
			WHEN [persons].[rac1p] = 4 THEN 'Alaska Native Alone'
			WHEN [persons].[rac1p] = 5 THEN 'American Indian and Alaska Native Tribes specified; or American Indian or Alaska Native, not specified and no other races'
			WHEN [persons].[rac1p] = 6 THEN 'Asian Alone'
			WHEN [persons].[rac1p] = 7 THEN 'Native Hawaiian and Other Pacific Islander Alone'
			WHEN [persons].[rac1p] = 8 THEN 'Some Other Race Alone'
			WHEN [persons].[rac1p] = 9 THEN 'Two or More Major Race Groups'
			ELSE NULL -- throws insert error on unexpected value since column is not nullable
			END AS [person_race]
    ,CASE	WHEN [wsLocResults].[WorkSegment] = 99999 AND [wsLocResults].[WorkLocation] = 99999 THEN 'Work from Home'
			WHEN [wsLocResults].[WorkSegment] = -1 AND [wsLocResults].[WorkLocation] = 0 THEN 'Non-Worker'
			WHEN [wsLocResults].[WorkSegment] > -1 AND [wsLocResults].[WorkSegment] < 99999 THEN 'Does not Work from Home'  
			ELSE NULL -- throws insert error on unexpected value since column is not nullable
			END AS [person_work_from_home]
	,CASE	WHEN [wsLocResults].[SchoolSegment] = 88888 AND [wsLocResults].[SchoolLocation] = 88888 THEN 'Home-Schooled'
			WHEN [wsLocResults].[SchoolSegment] = -1 AND [wsLocResults].[SchoolLocation] = 0 THEN 'Non-Student'
			WHEN [wsLocResults].[SchoolSegment] > -1 AND [wsLocResults].[SchoolSegment] < 88888 THEN 'Not Home-Schooled'  
			ELSE NULL -- throws insert error on unexpected value since column is not nullable
			END AS [person_home_schooled]
    ,CASE	WHEN [geography_work_location_id] IS NULL THEN (SELECT [geography_work_location_id] 
															FROM [dimension].[geography_work_location] 
															WHERE [work_location_mgra_13] = 'Not Applicable' 
																  AND [work_location_taz_13] = 'Not Applicable' 
																  AND [work_location_luz_13] = 'Not Applicable'
																  AND [work_location_region_2004] = 'Not Applicable') -- subquery for the null record
			ELSE [geography_work_location_id]
			END AS [geography_work_location_id]
	,CASE	WHEN [geography_school_location_id] IS NULL THEN (SELECT [geography_school_location_id] 
															  FROM [dimension].[geography_school_location] 
															  WHERE [school_location_mgra_13] = 'Not Applicable' 
																    AND [school_location_taz_13] = 'Not Applicable' 
																    AND [school_location_luz_13] = 'Not Applicable'
																    AND [school_location_region_2004] = 'Not Applicable') -- subquery for the null record
			ELSE [geography_school_location_id]
			END AS [geography_school_location_id]
FROM
	[staging].[personData] -- sampled persons in ABM model
INNER JOIN -- inner join keeps only sampled persons in ABM model
	[staging].[persons] -- input synthetic persons
ON
	[personData].[person_id] = [persons].[perid]
INNER JOIN -- inner join keeps only sampled persons in ABM model
	[staging].[wsLocResults] -- work school location results only for sampled persons in ABM model
ON
	[personData].[person_id] = [wsLocResults].[PersonID]
INNER JOIN -- need to get the home mgra for work from home and home schooled locations
	[staging].[households]
ON
	[personData].[hh_id] = [households].[hhid]
LEFT OUTER JOIN -- not all persons have a valid work location
	[dimension].[geography_work_location]
ON
	CASE	WHEN [wsLocResults].[WorkSegment] = 99999 AND [wsLocResults].[WorkLocation] = 99999 THEN CONVERT(nchar, [households].[mgra]) -- work from home
			WHEN [wsLocResults].[WorkSegment] > -1 AND [wsLocResults].[WorkSegment] < 99999 THEN CONVERT(nchar, [wsLocResults].[WorkLocation])
			ELSE NULL -- keep as null instead of Not Applicable to not introduce a multiple match issue
			END = [geography_work_location].[work_location_mgra_13] -- work location is mgra_13 based
LEFT OUTER JOIN -- not all persons have a valid school location
	[dimension].[geography_school_location]
ON
	CASE	WHEN [wsLocResults].[SchoolSegment] = 88888 AND [wsLocResults].[SchoolLocation] = 88888 THEN CONVERT(nchar, [households].[mgra]) -- home-schooled
			WHEN [wsLocResults].[SchoolSegment] > -1 AND [wsLocResults].[SchoolSegment] < 88888 THEN CONVERT(nchar, [wsLocResults].[SchoolLocation])
			ELSE NULL -- keep as null instead of Not Applicable to not introduce a multiple match issue
			END = [geography_school_location].[school_location_mgra_13] -- school location is mgra_13 based

COMMIT TRANSACTION person_dimension
