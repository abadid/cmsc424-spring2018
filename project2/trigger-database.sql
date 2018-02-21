alter role vagrant with password 'vagrant';

create table airports (airportid char(3) primary key, city char(20), name char(100), total2011 int, total2012 int);

insert into airports(name, city, airportid, total2011, total2012) values
('Metropolitan Oakland International','Oakland','OAK',10040864,9266570), 
('Fort Lauderdale Hollywood International','Fort Lauderdale','FLL',23569103,23349835),
('General Edward Lawrence Logan International','Boston','BOS',29349759,28932808),
('Los Angeles International','Los Angeles','LAX',63688121,61862052),
('Hartsfield Jackson Atlanta International','Atlanta','ATL',95513828,92389023),
('Chicago O''Hare International','Chicago','ORD',66633503,66701241);

create table airlines (airlineid char(2) primary key, name char(20), hub char(3) references airports(airportid));
create table customers (customerid char(10) primary key, name char(30), birthdate date, frequentflieron char(2) references airlines(airlineid));
create table flights (flightid char(6) primary key, source char(3) references airports(airportid), dest char(3) references airports(airportid), airlineid char(2) references airlines(airlineid), local_departing_time time, local_arrival_time time);
create table ticketsales (ticketid char(6) primary key, flightid char(6) references flights(flightid), customerid char(10) references customers, salesdate date);

insert into airlines values 
('SW', 'Southwest Airlines', 'OAK'), 
('AA', 'American Airlines', 'FLL'), 
('DL', 'Delta Airlines', 'ATL'), 
('UA', 'United Airlines', 'ORD');

insert into customers values ('cust0', 'Anthony Allen', to_date('1985-05-14', 'yyyy-mm-dd'), 'AA');
insert into customers values ('cust1', 'Anthony Edwards', to_date('1986-10-18', 'yyyy-mm-dd'), 'SW');
insert into customers values ('cust2', 'Anthony Evans', to_date('1987-02-08', 'yyyy-mm-dd'), 'SW');
insert into customers values ('cust3', 'Anthony Garcia', to_date('1994-08-23', 'yyyy-mm-dd'), 'DL');
insert into customers values ('cust4', 'Anthony Gonzalez', to_date('1977-10-06', 'yyyy-mm-dd'), 'AA');
insert into customers values ('cust5', 'Anthony Harris', to_date('1991-03-15', 'yyyy-mm-dd'), 'UA');


insert into flights values 
('AA101', 'OAK', 'FLL', 'AA', time '00:00' + interval '522 minutes', time '00:00' + interval '760 minutes'), 
('SW102', 'OAK', 'FLL', 'SW', time '00:00' + interval '145 minutes', time '00:00' + interval '235 minutes'),
('UA101', 'BOS', 'FLL', 'UA', time '00:00' + interval '60 minutes', time '00:00' + interval '189 minutes'),
('DL119', 'LAX', 'OAK', 'DL', time '00:00' + interval '380 minutes', time '00:00' + interval '642 minutes');


insert into ticketsales values 
('T1', 'AA101', 'cust0', to_date('2016-08-09', 'YYYY-MM-DD')), 
('T2', 'AA101', 'cust0', to_date('2016-08-10', 'YYYY-MM-DD')), 
('T3', 'UA101', 'cust2', to_date('2016-08-08', 'YYYY-MM-DD')), 
('T4', 'SW102', 'cust1', to_date('2016-08-08', 'YYYY-MM-DD')), 
('T5', 'UA101', 'cust1', to_date('2016-08-09', 'YYYY-MM-DD'));

create table airlinesales as
select substring(flightid from 1 for 2) as airlineid, count(*) as total_ticket_sales
from ticketsales
group by airlineid;

create table reportmin (airlineid char(2), salesdate date);

insert into reportmin values
('AA', to_date('2016-08-09', 'YYYY-MM-DD')),
('UA', to_date('2016-08-08', 'YYYY-MM-DD')),
('SW', to_date('2016-08-08', 'YYYY-MM-DD'));
