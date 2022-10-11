#sql statements

INSERT_LOCATION = ("INSERT INTO Locations(location_name, country_code, state_code, lon, lat) " 
                   "select * from (select %s as location_name, %s as country_code, %s as state_code, %s as lon, %s as lat)"
                   " as temp where not EXISTS (select location_name from Locations where location_name" 
                   " like temp.location_name collate 'utf8mb4_general_ci') limit 1;")


INSERT_WEATHER_TYPES = ("INSERT INTO Weather_types(condition_code, name, description, icon) " 
                   "select * from (select %s as condition_code, %s as name, %s as description, %s as icon)"
                   " as temp where not EXISTS (select condition_code from Weather_types where condition_code" 
                   " = temp.condition_code) limit 1;")

INSERT_TEMP = ("insert into temperature_data (location_id, temperature, feels_like, temp_min, temp_max, pressure, humidity, recorded_date)" 
               " select * from (select %s as location_id, %s as temperature, %s as feels_like,%s as temp_min, %s as temp_max," 
               "%s as pressure,%s as humidity, %s as recorded_date) as temp where not exists (select temperature_id from temperature_data where" 
               " location_id = temp.location_id AND DATE(recorded_date) = DATE(temp.recorded_date)) limit 1")

INSERT_WIND = ("INSERT INTO wind_data(location_id, speed, degrees, gust, recorded_date)" 
                   "SELECT * from (SELECT %s AS location_id, %s AS speed, %s as degrees, %s AS gust, %s as recorded_date)"
                   " AS temp WHERE NOT EXISTS (select wind_id FROM wind_data WHERE "
                   " location_id = temp.location_id AND DATE(temp.recorded_date) = DATE(recorded_date)) LIMIT 1;")

INSERT_PRECIP = ("INSERT INTO precipitation_data(location_id, one_hour, three_hour, is_snow, recorded_date)" 
                   "select * from (select %s as location_id, %s as one_hour, %s three_hour, %s as is_snow, %s as recorded_date)"
                   " as temp where not EXISTS (select precipitation_id from precipitation_data where location_id" 
                   " = temp.location_id AND DATE(recorded_date) = DATE(temp.recorded_date)) limit 1;")

INSERT_LOC_DATA = ("INSERT INTO day_data(location_id, sunrise, sunset, timezone)" 
                   "select * from (select %s as location_id, %s as sunrise, %s as sunset, %s as timezone)"
                   " as temp where not EXISTS (select day_data_id from day_data where location_id" 
                   " = temp.location_id and DATE(sunrise) = DATE(temp.sunrise) and"
                   " DATE(sunset) = DATE(temp.sunset) and timezone = temp.timezone) limit 1;")

INSERT_WEATHER = ("INSERT INTO weather_data(location_id, recorded_date, weather_type, temperature_id, precipitation_id"
                  ", wind_id, day_loc_id, clouds_percent, visibility) SELECT * from (SELECT %s as location_id,"
                  " %s as recorded_date, %s as weather_type, %s as temperature_id, %s as precipitation_id, %s as wind_id,"
                  " %s as day_loc_id, %s as clouds_percent, %s as visibility) as temp where not exists (select"
                  " unique_id from weather_data where location_id=temp.location_id and DATE(recorded_date) = DATE(temp.recorded_date))"
                  " limit 1;")
