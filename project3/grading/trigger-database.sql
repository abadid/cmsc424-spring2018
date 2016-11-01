alter role vagrant with password 'vagrant';

create table airports (airportid char(3) primary key, city char(20), name char(100), total2011 int, total2012 int);
insert into airports(name, city, airportid, total2011, total2012) values('Metropolitan Oakland International','Oakland','OAK',10040864,9266570), ('Fort Lauderdale Hollywood International','Fort Lauderdale','FLL',23569103,23349835);

create table airlines (airlineid char(2) primary key, name char(20), hub char(3) references airports(airportid));
create table customers (customerid char(10) primary key, name char(30), birthdate date, frequentflieron char(2) references airlines(airlineid));
create table flights (flightid char(6) primary key, source char(3) references airports(airportid), dest char(3) references airports(airportid), airlineid char(2) references airlines(airlineid), local_departing_time time, local_arrival_time time);
create table flewon (flightid char(6) references flights(flightid), customerid char(10) references customers, flightdate date);

insert into airlines values ('SW', 'Southwest Airlines', 'OAK'), ('AA', 'American Airlines', 'FLL');

insert into customers values ('cust0', 'Anthony Allen', to_date('1979-01-11', 'yyyy-mm-dd'), 'SW'), ('cust1', 'Anthony Edwards', to_date('1991-01-04', 'yyyy-mm-dd'), 'AA'), ('cust2', 'Anthony Evans', to_date('1994-01-04', 'yyyy-mm-dd'), 'SW'), ('cust3', 'Anthony Garcia', to_date('1971-01-13', 'yyyy-mm-dd'), 'AA');

insert into flights values('AA101', 'OAK', 'FLL', 'AA', time '00:00' + interval '522 minutes', time '00:00' + interval '760 minutes'), ('SW102', 'OAK', 'FLL', 'SW', time '00:00' + interval '145 minutes', time '00:00' + interval '235 minutes');

insert into flewon values ('AA101', 'cust0', to_date('2016-08-09', 'YYYY-MM-DD')), ('AA101', 'cust0', to_date('2016-08-10', 'YYYY-MM-DD')), ('AA101', 'cust0', to_date('2016-08-11', 'YYYY-MM-DD')), ('SW102', 'cust1', to_date('2016-08-08', 'YYYY-MM-DD')), ('AA101', 'cust1', to_date('2016-08-09', 'YYYY-MM-DD'));

create table NumberOfFlightsTaken as select c.customerid, c.name as customername, count(*) as numflights from customers c join flewon fo on c.customerid = fo.customerid group by c.customerid, c.name;
