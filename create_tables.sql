CREATE TABLE category (
    category_id int NOT NULL IDENTITY(1,1),
    category_name varchar(50) NOT NULL,
    category_desc varchar(500),
	premium_percentage float NOT NULL,
    PRIMARY KEY (category_id),
);

insert into category values('Jewelry','Wearable items',0.01)

select * from category;

CREATE TABLE policy (
    policy_id varchar(50) NOT NULL PRIMARY KEY,
    policy_date Date Not NUll,
    monthly_premium float Not Null,
	policy_end_date Date,
	active bit default 1,
	customer_id varchar(50) Not Null FOREIGN KEY REFERENCES users(ID)
    
);


CREATE TABLE quote (
    quote_id varchar(50) NOT NULL PRIMARY KEY,
    quote_date Date Not NUll,
    quoted_premium float Not Null,
	quote_decision_date Date,
	status varchar(30),
	customer_id varchar(50) Not Null FOREIGN KEY REFERENCES users(ID)
    
);

CREATE TABLE items (
    item_id varchar(50) NOT NULL PRIMARY KEY,
	category_id int NOT NULL FOREIGN KEY REFERENCES category(category_id),
    item_name varchar(50) NOT NUll,
	item_desc varchar(500),
	item_value float Not NULL,
	policy_id varchar(50) FOREIGN KEY REFERENCES policy(policy_id),
	quote_id varchar(50) NOT NULL FOREIGN KEY REFERENCES quote(quote_id)
    
);