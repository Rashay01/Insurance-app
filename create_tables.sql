CReate Table users(
	ID varchar(50) Primary key,
	name varchar(50) NOT NULL,
	surname varchar(50) NOT NULL,
	email varchar(50) NOT NULL,
	cell_no varchar(15) NOT NULL,
	password varchar(100) NOT NULL,
	address varchar(200)
)

CREATE TABLE category (
    category_id int NOT NULL IDENTITY(1,1),
    category_name varchar(50) NOT NULL,
    category_desc varchar(500),
	premium_percentage float NOT NULL,
    PRIMARY KEY (category_id)
);

CREATE TABLE policy (
    policy_number varchar(50) NOT NULL PRIMARY KEY,
    policy_date Date Not NUll,
    monthly_premium float Not Null,
	policy_end_date Date,
	active bit NOT NULL default 1,
	category_id Integer Foreign Key REFERENCES category(category_id)
);

ALTER TABLE quote
add category_id Integer Foreign Key REFERENCES category(category_id)

CREATE TABLE quote (
    quote_id varchar(50) NOT NULL PRIMARY KEY,
    quote_date Date Not NUll,
    quoted_premium float Not Null,
	quote_decision_date Date,
	status varchar(30) NOT NULL,
	category_id Integer Foreign Key REFERENCES category(category_id)
);

Create Table classic_cars(
	vehicle_id varchar(50) Primary KEY,
	vehicle_make varchar(20) NOT NULL,
	model varchar(20) NOT NULL,
	year_model Date NOT NULL,
	vin varchar(20) NOT NULL,
	license_plate_number varchar(10) NOT NULL,
	odometer_reading  Integer NOT NULL,
	fuel_type varchar(10),
	color varchar(20),
	policy_number varchar(50),
	customer_id varchar(50) NOT NULL,
	Foreign KEY (policy_number) REFERENCES  policy(policy_number),
	Foreign KEY (customer_id) REFERENCES users(ID)
)

CReate Table car_quote(
vehicle_id varchar(50) NOT NULL Foreign KEY REFERENCES classic_cars(vehicle_id),
quote_id varchar(50) NOT NULL Foreign KEY REFERENCES quote(quote_id)
)