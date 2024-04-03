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


Insert into users values('0101165410081','Rashay','Daya','rashay.jcdaya@gmail.com','0836681148','12345678','121 Rondebosch')


insert into category values('classic cars','antique/colletors cars more than 25 years old and in good condition',0.25)


insert into classic_cars(vehicle_id,vehicle_make, model, year_model, vin, license_plate_number, odometer_reading, fuel_type, color, customer_id,current_value,year_purchased)
values ('as1234-12asd12','Alfa Romeo','Giulietta Spider', '1957','ZARBB32N0M6004488', 'JCD007GP', 246879,'Diesel', 'white', '0101165410081',8000000,'1997-06-16')

insert into classic_cars(vehicle_id,vehicle_make, model, year_model, vin, license_plate_number, odometer_reading, fuel_type, color, customer_id,current_value,year_purchased)
values ('as1234-12asd13','Mercedes Benz','M Class', '1999','4JGAB54E1XA094195', 'JCD008GP', 246890,'Petrol', 'black', '0101165410081',4500000,'2000-06-17')

Select * from quote;
insert into quote(quote_id,quote_date,quoted_premium,quote_decision_date,status,category_id) values('qt-001','2024-03-01',18000,'2024-03-05','Accepted',1)
,('qt-002','2024-04-02',11250,NULL,'Deciding',1)


insert into car_quote values('as1234-12asd12','qt-001'),('as1234-12asd13','qt-002')


insert into policy(policy_number,policy_date,monthly_premium,category_id) values('pol-001','2024-03-05',18000,1)

update classic_cars set policy_number = 'pol-001' where vehicle_id ='as1234-12asd12'