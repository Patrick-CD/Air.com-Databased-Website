delete from purchases;
delete from ticket;
delete from booking_agent;
delete from flight;
delete from airplane;
delete from customer;
delete from airline_staff;
delete from airline;
delete from airport;

#a. airline
insert into airline values ("China Eastern");

#b. At least Two airports named "JFK" in NYC and "PVG" in Shanghai.
insert into airport values ("JFK", "NYC");
insert into airport values ("PVG", "Shanghai");

#c. Insert at least two customers with appropriate names and other attributes.
insert into customer values ("cz1682@nyu.edu", "Canyu Zhu", "123456", "3680", "Zhangyang Road", "Shanghai", "China", "18980001218", "2544519254", 2022-11-12,"China", 2000-03-18);
insert into customer values ("sl1027@nyu.edu", "Sang Li", "123456", "1", "Sanlitun", "Beijing", "China", "18600001111", "9497494", 2022-3-18,"China", 1995-10-27);

#Insert one booking agent with appropriate name and other attributes.
insert into booking_agent values ("xiaoyu@nyu.edu", "123456", "233");

#d. Insert at least two airplanes.
insert into airplane values ("China Eastern", "4396", 443);
insert into airplane values ("China Eastern", "2800", 2200);

#e. Insert At least One airline Staff working for China Eastern.
insert into airline_staff values("PDD","777777","Benwei","Lu", 1999-06-02, "China Eastern");

#f. Insert several flights with upcoming, in-progress, delayed statuses.
insert into flight values("China Eastern", "370",  "JFK", '2012-12-21 00:00:00', "PVG", '2013-01-01 00:01:00', 4444, "upcoming", 4396);
insert into flight values("China Eastern", "380",  "JFK", '2012-12-21 00:00:00', "PVG",  '2013-01-01 00:01:00', 8888, "in-progress", 2800);
insert into flight values("China Eastern", "390",  "JFK", '2020-01-01 00:00:00', "PVG",  '2022-01-01 00:01:00', 6666, "delayed", 4396);

#g. Insert some tickets for corresponding flights. One customer buy ticket directly and one customer buy ticket using a booking agent
insert into ticket values("47","China Eastern", "370");
insert into ticket values("46","China Eastern", "370");
insert into ticket values("45","China Eastern", "370");
insert into ticket values("48","China Eastern", "380");
insert into ticket values("49","China Eastern", "390");

insert into purchases values("47","cz1682@nyu.edu", 233, 2020-3-18);
insert into purchases values("46","cz1682@nyu.edu", null, 2020-3-18);
insert into purchases values("48","sl1027@nyu.edu", null, 2020-3-18);
