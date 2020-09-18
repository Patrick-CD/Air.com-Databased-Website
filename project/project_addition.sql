CREATE TABLE `question` (
  `customer_email` varchar(50) NOT NULL,
  `answer` varchar(50) NOT NULL,
  PRIMARY KEY(`customer_email`)
) ;

create view view_flight as 
	select customer_email, ticket.ticket_id, flight.airline_name, flight.flight_num, status, departure_airport, departure_time, arrival_airport, arrival_time
   from purchases, ticket, flight
   where purchases.ticket_id = ticket.ticket_id and ticket.flight_num = flight.flight_num and ticket.airline_name = flight.airline_name
   group by customer_email, ticket.ticket_id;

create view flight_arrive as
select flight_num, arrival_airport, airport_city, cast(arrival_time as date) as date, airline_name
from flight, airport
where arrival_airport = airport_name;

create view flight_departure as
select flight_num, departure_airport, airport_city, cast(departure_time as date) as date
from flight, airport
where departure_airport = airport_name;

create view flight_search as
select flight_departure.flight_num, arrival_airport, flight_arrive.airport_city as arrival_city, departure_airport, airline_name, flight_departure.airport_city as departure_city, flight_departure.date as date
from flight_departure, flight_arrive
where flight_departure.flight_num = flight_arrive.flight_num;

create view ba_flight as 
	select booking_agent_id, customer_email, purchase_date, ticket.ticket_id, flight.airline_name, flight.flight_num, status, departure_airport, departure_time, arrival_airport, arrival_time
   from purchases, ticket, flight
   where purchases.ticket_id = ticket.ticket_id and ticket.flight_num = flight.flight_num and ticket.airline_name = flight.airline_name
   group by booking_agent_id, ticket.ticket_id;

create view commission as
	select booking_agent_id, sum(price)*0.1 as total, avg(price)*0.1 as average, count(price) as amount
	from ba_flight,flight
   where ba_flight.flight_num = flight.flight_num and ba_flight.airline_name = flight.airline_name
   group by booking_agent_id;