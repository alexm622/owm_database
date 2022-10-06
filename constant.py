#sql statements

INSERT_LOCATION = ("INSERT INTO Locations(location_name, country_code, state_code, lon, lat) " 
                   "select * from (select %s as location_name, %s as country_code, %s as state_code, %s as lon, %s as lat)"
                   " as temp where not EXISTS (select location_name from Locations where location_name" 
                   " like temp.location_name collate 'utf8mb4_general_ci') limit 1;")
