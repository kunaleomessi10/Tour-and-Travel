CREATE TABLE customer
(
    customer_id INTEGER PRIMARY KEY,
    name        text,
    phone       integer,
    email       text,
    gender      text,
    dob         date,
    passport_no integer,
    address     text,
    postal_code integer,
    user_name   text,
    password    text
);
CREATE INDEX customer_index01 ON customer (customer_id);

CREATE TABLE payment
(
    payment_id     INTEGER PRIMARY KEY,
    customer_id    Integer,
    booking_id     Integer,
    payment_date   date,
    payable_amount Integer,
    payment_method text,
    payment_status text
);
CREATE INDEX payment_index01 ON payment (payment_id);

CREATE TABLE travel_agency
(
    agency_id   INTEGER PRIMARY KEY,
    agency_name text,
    phone       Integer,
    email       text,
    city        text,
    country     text,
    address     text,
    postal_code Integer
);
CREATE INDEX travel_agency_index01 ON travel_agency (agency_id);

CREATE TABLE booking
(
    booking_id     INTEGER PRIMARY KEY,
    customer_id    Integer,
    package_id     Integer,
    booking_date   date,
    package_name   text,
    members        text,
    total_amount   Integer,
    booking_status text
);
CREATE INDEX booking_index01 ON booking (booking_id);

CREATE TABLE package
(
    package_id             INTEGER PRIMARY KEY,
    agency_id              Integer,
    travel_class_id        Integer,
    transportation_type_id Integer,
    from_city              text,
    to_city                text,
    package_days           Integer,
    package_amount         Integer,
    description            text
);
CREATE INDEX package_index01 ON package (package_id);

CREATE TABLE travel_class
(
    travel_class_id INTEGER PRIMARY KEY,
    class_name      text,
    description     text
);
CREATE INDEX travel_class_index01 ON travel_class (travel_class_id);

CREATE TABLE transportation_type
(
    transportation_type_id   Integer PRIMARY KEY,
    transportation_type_name text,
    description              text
);
CREATE INDEX transportation_type_index01 ON transportation_type (transportation_type_id);
