#use cases and queries


##############################
##Explanation
##############################

## This file lists the use cases follow the order of project_3.pdf
## all values are written in the form %s which follows Python String Format function
## I tried my best to make application.py neat and in order, if you have furthur question you can check application.py by search
## eg. you want to see how search function work you search with key word "search" and you can see functions: 'publics_search', 'cussearch'......
## More questions please just contact me cz1682@nyu,edu


##############################
##login and register
##############################
#customer login
	'SELECT * FROM customer WHERE email = %s and password = %s'
#ba login
	 'SELECT * FROM booking_agent WHERE email = %s and password = %s and booking_agent_id = %s'
#staff login
	'SELECT * FROM airline_staff WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))'
#cus register
	'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
#ba register
	'INSERT INTO booking_agent VALUES(%s, %s, %s)'
#staff register
	'INSERT INTO airline_staff VALUES(%s, %s, %s, %s, %s, %s)'

##############################
##forget password implementation (additional use case)
##############################
#set answer to question
	'INSERT INTO question VALUES(%s, %s)'
#check answer
	"select answer from question where customer_email = %s"
#change password
	'''UPDATE customer
		SET password = %s 
		WHERE email = %s  '''
###############################
##public search
###############################
'''select *
    from flight
    where status = "upcoming" and (flight_num,airline_name) in (
    SELECT flight_num, airline_name FROM flight_search
    WHERE departure_city = (case when %s = '' then departure_city else %s end)
    and departure_airport = (case when %s = '' then departure_airport else %s end)
    and arrival_city = (case when %s = '' then arrival_city else %s end)
    and arrival_airport = (case when %s = '' then arrival_airport else %s end)
    and date = (case when %s = '' then date else %s end)
	and flight_num = (case when %s = '' then flight_num else %s end))

    '''
###############################
##customer use cases
###############################

#view my flights
	'SELECT * FROM view_flight WHERE customer_email = %s and status = %s '
#purchases tickets
	#check information correctness:
		#use python try except
	#see ticket left:
			'''select ticket_id 
			from ticket
			where airline_name = %s and flight_num = %s
				and ticket_id not in (select ticket_id from purchases)'''
	#check if flight full:
		'SELECT seats FROM airplane, flight WHERE flight.airline_name = %s and flight.flight_num = %s and flight.airplane_id =airplane.airplane_id '
		'SELECT count(ticket_id) as maxi FROM ticket WHERE airline_name = %s and flight_num = %s group by flight_num '
	#if not full:
		'INSERT INTO purchases VALUES(%s, %s, %s, %s)'
		'INSERT INTO ticket VALUES(%s, %s, %s)'
#search flight
   	'''select *
    	from flight
    	where status = "upcoming" and (flight_num,airline_name) in (
    	SELECT flight_num, airline_name FROM flight_search
    	WHERE departure_city = (case when %s = '' then departure_city else %s end)
    	and departure_airport = (case when %s = '' then departure_airport else %s end)
    	and arrival_city = (case when %s = '' then arrival_city else %s end)
  	and arrival_airport = (case when %s = '' then arrival_airport else %s end)
    	and date = (case when %s = '' then date else %s end))

    '''
#track spending:
	'''select view_flight.customer_email, sum(price) as total
					from view_flight, flight, purchases
					where view_flight.flight_num = flight.flight_num 
						and purchases.customer_email = %s
						and view_flight.airline_name = flight.airline_name
						and view_flight.ticket_id = purchases.ticket_id
						and purchases.purchase_date >= %s
						and purchases.purchase_date < %s
					group by customer_email '''
#logout
	session.pop('email')

###################################
##Booking agent use cases
###################################

#view my flight
	'SELECT * FROM ba_flight WHERE booking_agent_id = %s and status = %s '
#Purchase ticket
	#check information correctness:
		#use python try except
	#see ticket left:
			'''select ticket_id 
			from ticket
			where airline_name = %s and flight_num = %s
				and ticket_id not in (select ticket_id from purchases)'''
	#check if flight full:
		'SELECT seats FROM airplane, flight WHERE flight.airline_name = %s and flight.flight_num = %s and flight.airplane_id =airplane.airplane_id '
		'SELECT count(ticket_id) as maxi FROM ticket WHERE airline_name = %s and flight_num = %s group by flight_num '
	#if not full:
		'INSERT INTO ticket VALUES(%s, %s, %s)'
		'INSERT INTO purchases VALUES(%s, %s, %s, %s)'
#Search for flights:
	'''select *
    	from flight
   	where status = "upcoming" and (flight_num,airline_name) in (
    	SELECT flight_num, airline_name FROM flight_search
    	WHERE departure_city = (case when %s = '' then departure_city else %s end)
    	and departure_airport = (case when %s = '' then departure_airport else %s end)
    	and arrival_city = (case when %s = '' then arrival_city else %s end)
   	and arrival_airport = (case when %s = '' then arrival_airport else %s end)
   	and date = (case when %s = '' then date else %s end))

    '''
#view commission
	'''select ba_flight.booking_agent_id, sum(price)*0.1 as total, avg(price)*0.1 as average, count(price) as amount
		from ba_flight,flight, purchases
   		where ba_flight.flight_num = flight.flight_num 
  		 and ba_flight.airline_name = flight.airline_name
   		and ba_flight.ticket_id = purchases.ticket_id
		and purchases.booking_agent_id = %s
   		and purchases.purchase_date >= %s
   		and purchases.purchase_date < %s
   		group by booking_agent_id'''
#view top customers
	'''select customer_email, count(ticket_id) as amount
				from ba_flight
				where booking_agent_id = %s
				and purchase_date >= %s
				and purchase_date < %s
				group by customer_email
				order by amount desc
				limit 0,5 '''
#log out
	session.pop('email')
	session.pop('booking_agent_id')

###################################
##staff use cases
###################################
#View My flights
	'''select *
	from flight
	where flight_num in (select flight_search.flight_num
	from flight_search, airline_staff
	where username = %s and airline_staff.airline_name = flight_search.airline_name
	and date >= %s
	and date <= %s
	and departure_city = %s
	and arrival_city = %s)
	'''
#create new flights
	'''insert into flight values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
#change flight status
	'''UPDATE flight 
	SET status = %s 
	WHERE flight.airline_name = %s AND flight.flight_num = %s '''
#add airplane
	'''insert into airplane values (%s,%s,%s)'''
#add airport
	'''insert into airport values (%s,%s)'''
#view booking agents
	'''select booking_agent_id, count(ticket_id) as amount
				from ba_flight
				where airline_name = %s
				and purchase_date >= %s
				and purchase_date < %s
				and booking_agent_id is not null
				group by booking_agent_id
				order by amount desc
				limit 0,5 '''
#view frequent customers
	'''select customer_email, count(purchases.ticket_id) as amount
				from purchases, ticket
				where ticket.airline_name = %s
				and purchases.ticket_id = ticket.ticket_id
				and purchase_date >= %s
				and purchase_date < %s
   				group by customer_email
				order by amount desc
				limit 0,1 '''


	####see record of one customer:
	'''select distinct flight_num, customer_email
				from ba_flight
				where ba_flight.airline_name = %s
				and customer_email = %s'''

#view reports
	'''select airline_name, count(ticket_id) as amount
					from ba_flight
					where airline_name = %s
						and purchase_date >= %s
						and purchase_date < %s
					group by airline_name '''
#comparison of Revenue earned
       
  #######with ba:

	 '''select ba_flight.airline_name, sum(price) as total
		from ba_flight, flight
		where booking_agent_id is not null 
		and ba_flight.flight_num = flight.flight_num 
		and ba_flight.airline_name = flight.airline_name
		and ba_flight.airline_name = %s
		and purchase_date >= %s
		and purchase_date < %s '''

         ########without ba:

	'''select ba_flight.airline_name, sum(price) as total
		from ba_flight, flight
		where booking_agent_id is null 
		and ba_flight.flight_num = flight.flight_num 
		and ba_flight.airline_name = flight.airline_name
		and ba_flight.airline_name = %s
		and purchase_date >= %s
		and purchase_date < %s '''	

#View Top destinations	
	 '''select airport_city, count(ticket_id) as amount
				from ba_flight, airport
				where ba_flight.airline_name = %s
				and airport_name = departure_airport
				and purchase_date >= %s
				and purchase_date < %s
   				group by airport_city
				order by amount desc
				limit 0,3 '''