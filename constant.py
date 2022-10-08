#sql statements

INSERT_LOCATION = ("INSERT INTO Locations(location_name, country_code, state_code, lon, lat) " 
                   "select * from (select %s as location_name, %s as country_code, %s as state_code, %s as lon, %s as lat)"
                   " as temp where not EXISTS (select location_name from Locations where location_name" 
                   " like temp.location_name collate 'utf8mb4_general_ci') limit 1;")


INSERT_LOCATION = ("INSERT INTO Weather_types(condition_code, name, desc, icon)" 
                   "select * from (select %s as condition_code, %s as name, %s as desc, %s as icon)"
                   " as temp where not EXISTS (select condition_code from Weather_types where condition_code" 
                   " = temp.condition_code) limit 1;")

INSERT_TEMP = ("INSERT INTO temperature_data "
                   "(location_id, temperature, feels_like, temp_min, temp_max, pressure, humidity)" 
                   "select * from (select %s as location_id, %s as temperature, %s as feels_like,"
                   "%s as temp_min, %s as temp_max, %s as pressure, %s as humidity)"
                   " as temp where not EXISTS (select location_id temperature_data" 
                   " where location_id = temp.location_id and"
                   " temp_min = temp.temp_min and temperature = temp.temperature and humidity = temp.humidity and"
                   " pressure = temp.pressure"
                   " ) limit 1;")

INSERT_WIND = ("INSERT INTO Wind_data(location_id, speed, degrees, gust)" 
                   "SELECT * from (SELECT %s AS location_id, %s AS speed, %s as degrees, %s AS gust)"
                   " AS temp WHERE NOT EXISTS (select location_id FROM Wind_data WHERE "
                   " location_id = temp.location_id AND speed = temp.speed AND degrees = temp.degrees" 
                   " AND gust = temp.gust) LIMIT 1;")

INSERT_PRECIP = ("INSERT INTO precipitation_data(location_id, one_hour, three_hour, is_snow)" 
                   "select * from (select %s as location_id, %s as one_hour, %s three_hour, %s as is_snow)"
                   " as temp where not EXISTS (select precipitation_id from precipitation_data where location_id" 
                   " = temp.location_id AND one_hour = temp.one_hour AND three_hour = temp.three_hour"
                   " and is_snow = temp.is_snow) limit 1;")
INSERT_LOC_DATA = ("INSERT INTO day_data(location_id, sunrise, sunset, timezone)" 
                   "select * from (select %s as location_id, %s as sunrise, %s as sunset, %s as timezone)"
                   " as temp where not EXISTS (select day_data_id from day_data where location_id" 
                   " = temp.location_id and sunrise = temp.sunrise and"
                   " sunset = temp.sunset and timezone = temp.timezone) limit 1;")

