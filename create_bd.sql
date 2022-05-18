DROP TABLE IF EXISTS Crime;
		
CREATE TABLE Crime (
  id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  crime_id VARCHAR(9),
  original_crime_type_name VARCHAR
);

DROP TABLE IF EXISTS Date;
		
CREATE TABLE Date (
  id INTEGER NOT NULL PRIMARY KEY,
  report_date DATETIME NULL DEFAULT NULL,
  call_date DATETIME NULL DEFAULT NULL,
  offense_date DATETIME NULL DEFAULT NULL,
  call_time VARCHAR(5) NULL DEFAULT NULL,
  call_date_time DATETIME NULL DEFAULT NULL,
  crime_id INTEGER NOT NULL,
  FOREIGN KEY (crime_id) REFERENCES Crime (id)
);

DROP TABLE IF EXISTS Location;
		
CREATE TABLE Location (
  id INTEGER NOT NULL PRIMARY KEY,
  disposition VARCHAR NULL DEFAULT NULL,
  address VARCHAR NULL DEFAULT NULL,
  city VARCHAR NULL DEFAULT NULL,
  state VARCHAR NULL DEFAULT NULL,
  agency_id VARCHAR NULL DEFAULT NULL,
  address_type VARCHAR NULL DEFAULT NULL,
  common_location VARCHAR NULL DEFAULT NULL,
  crime_id INTEGER NOT NULL,
  FOREIGN KEY (crime_id) REFERENCES Crime (id)
);
