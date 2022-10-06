#sql statements

INSERT_LOCATION = ("INSERT INTO Locations(location_name, country_code, state_code, lon, lat) " 
                   "select * from (select %s as location_name, %s as country_code, %s as state_code, %s as lon, %s as lat)"
                   " as temp where not EXISTS (select location_name from Locations where location_name" 
                   " like temp.location_name collate 'utf8mb4_general_ci') limit 1;")


INSERT_LOCATION = ("INSERT INTO Weather_types(condition_code, name, desc, icon)" 
                   "select * from (select %s as condition_code, %s as name, %s desc, %s as icon)"
                   " as temp where not EXISTS (select condition_code from Weather_types where condition_code" 
                   " like temp.condition_code) limit 1;")
