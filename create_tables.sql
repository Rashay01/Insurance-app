Create Table users(
	ID varchar(50) Primary key,
	name varchar(50) NOT NULL,
	surname varchar(50) NOT NULL,
	email varchar(50) NOT NULL,
	cell_no varchar(15) NOT NULL,
	password varchar(200) NOT NULL,
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
	current_value Float,
	year_purchased Date,
	Foreign KEY (policy_number) REFERENCES  policy(policy_number),
	Foreign KEY (customer_id) REFERENCES users(ID)
)

Create Table car_quote(
vehicle_id varchar(50) NOT NULL Foreign KEY REFERENCES classic_cars(vehicle_id),
quote_id varchar(50) NOT NULL Foreign KEY REFERENCES quote(quote_id)
)

Create Table claim(
	claim_number varchar(50) Primary key,
	claim_date Date NOT NULL,
	date_incident_occurred Date NOT NULL,
	claim_description varchar(500) NOT NULL,
	police_claim_number varchar(15),
	claim_amount float,
	policy_number varchar(50) Not NULL Foreign KEY REFERENCES policy(policy_number)

)

Create Table claim_status(
	status_id varchar(50) Primary Key,
	status_name varchar (20) Not NULL,
	status_date Date Not NULL,
	claim_number varchar(50) Not NUll FOreign KEY REFERENCES claim(claim_number),
)

Insert into category(category_name,category_desc,premium_percentage) 
Values ('classic cars','antique/colletors cars more than 25 years old and in good condition',0.00225),
('jewelry','antique/colletors jewelry that is in good condition',0.0225)

Insert into users values('0101165410082','Rashay','Daya','rashay.jcdaya@gmail.com','0833331111','scrypt:32768:8:1$WOULdilOiIRJM0dw$eaed19ab61daa3c85421a5e22eea3d21b9c4d3c545d4281964f9d17a45652d073f61a3a23fe1fa98ca4056f947eddcd9f542f9c23658daea161a6889651d143e','121 Cape Town')

insert into classic_cars(vehicle_id,vehicle_make, model, year_model, vin, license_plate_number, odometer_reading, fuel_type, color, customer_id,current_value,year_purchased)
values ('as1234-12asd12','Alfa Romeo','Giulietta Spider', '1957','ZARBB32N0M6004488', 'JCD007GP', 246879,'Diesel', 'white', '0101165410082',8000000,'1997-06-16')

insert into classic_cars(vehicle_id,vehicle_make, model, year_model, vin, license_plate_number, odometer_reading, fuel_type, color, customer_id,current_value,year_purchased)
values ('as1234-12asd13','Mercedes Benz','M Class', '1999','4JGAB54E1XA094195', 'JCD008GP', 246890,'Petrol', 'black', '0101165410082',4500000,'2000-06-17')

insert into quote(quote_id,quote_date,quoted_premium,quote_decision_date,status,category_id) values('qt-001','2024-03-01',18000,'2024-03-05','Accepted',1)
,('qt-002','2024-04-02',11250,NULL,'Deciding',1)

insert into car_quote values('as1234-12asd12','qt-001'),('as1234-12asd13','qt-002')

insert into policy(policy_number,policy_date,monthly_premium,category_id) values('pol-001','2024-03-05',18000,1)

update classic_cars set policy_number = 'pol-001' where vehicle_id ='as1234-12asd12'


Insert into claim(claim_number, claim_date, date_incident_occurred, claim_description, police_claim_number, policy_number) 
Values('claim-001','2024-03-20','2024-03-19','There was theft of my car that was kept in the garage. It was stolen at 4 AM in the morning', 'CAS060435-01','pol-001')

Insert into claim_status values('csts-001','Received','2024-03-20','claim-001'), ('csts-002','Investigation','2024-03-21','claim-001'), ('csts-003','Declined','2024-03-28','claim-001')
