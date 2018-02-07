SET NOCOUNT ON;
BEGIN TRANSACTION household_dimension

-- insert not applicable record for the scenario
INSERT INTO [dimension].[household]
([scenario_id], [household_id], [household_income], [household_income_category],
 [household_size], [household_unit_type], [household_autos],
 [household_transponder], [household_poverty], [geography_household_location_id])
SELECT
	1 AS [scenario_id] -- need to parameterize
	,0 AS [household_id] -- indexing begins at 1
	,NULL AS [household_income]
	,'Not Applicable' AS [household_income_category]
	,'Not Applicable' AS [household_size]
	,'Not Applicable' AS [household_unit_type]
	,'Not Applicable' AS [household_autos]
	,'Not Applicable' AS [household_transponder]
	,NULL AS [household_poverty]
	,(SELECT [geography_household_location_id] 
	  FROM [dimension].[geography_household_location] 
	  WHERE	[household_location_mgra_13] = 'Not Applicable' 
			AND [household_location_taz_13] = 'Not Applicable' 
			AND [household_location_luz_13] = 'Not Applicable'
			AND [household_location_region_2004] = 'Not Applicable') -- subquery for the null record


-- insert household data into dimension table
INSERT INTO [dimension].[household]
([scenario_id], [household_id], [household_income], [household_income_category],
 [household_size], [household_unit_type], [household_autos],
 [household_transponder], [household_poverty], [geography_household_location_id])
SELECT --1175038
	1 AS [scenario_id]  -- need to parameterize
	,[householdData].[hh_id] AS [household_id]
	,CASE	WHEN [households].[unittype] IN (1,2) THEN NULL
			WHEN [households].[unittype] = 0 THEN [households].[hinc] 
			ELSE NULL
			END AS [household_income]
	,CASE	WHEN [households].[unittype] IN (1,2) THEN 'Not Applicable'
			WHEN [households].[unittype] = 0 AND [households].[hinccat1] = 1 THEN 'Less than 30k'
			WHEN [households].[unittype] = 0 AND [households].[hinccat1] = 2 THEN '30k-60k'
			WHEN [households].[unittype] = 0 AND [households].[hinccat1] = 3 THEN '60k-100k'
			WHEN [households].[unittype] = 0 AND [households].[hinccat1] = 4 THEN '100k-150k'
			WHEN [households].[unittype] = 0 AND [households].[hinccat1] = 5 THEN '150k+'
			ELSE NULL -- throws insert error on unexpected value since column is not nullable
			END AS [household_income]
	,[households].[persons] AS [household_size]
	,CASE	WHEN [households].[unittype] = 0 THEN 'Household'
			WHEN [households].[unittype] = 1 THEN 'Non-Institutional Group Quarters'
			WHEN [households].[unittype] = 2 THEN 'Institutional Group Quarters'
			ELSE NULL -- throws insert error on unexpected value since column is not nullable
			END AS [household_unit_type]
	,CASE	WHEN [householdData].[autos] = 4 THEN '4+' -- auto ownership model value of 4 is really 4 or more
			ELSE CONVERT(nchar, [householdData].[autos])
			END AS [household_autos]
	,CASE	WHEN [householdData].[transponder] = 0 THEN 'No Transponder Owned'
			WHEN [householdData].[transponder] = 1 THEN 'Transponder Owned'
			ELSE NULL -- throws insert error on unexpected value since column is not nullable
			END AS [household_transponder]
	,CASE	WHEN [households].[unittype] IN (1,2) THEN NULL
			WHEN [households].[unittype] = 0 THEN [households].[poverty] 
			ELSE NULL
			END AS [household_poverty]
	,[geography_household_location].[geography_household_location_id]
FROM
	[staging].[householdData] -- sampled households in ABM model
INNER JOIN -- inner join keeps only sampled households in ABM model
	[staging].[households] -- input synthetic households
ON
	[householdData].[hh_id] = [households].[hhid]
INNER JOIN
	[dimension].[geography_household_location]
ON
	CONVERT(nchar, [households].[mgra]) = [geography_household_location].[household_location_mgra_13] -- household location is mgra_13 based

COMMIT TRANSACTION household_dimension