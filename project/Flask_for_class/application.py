#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import datetime
from datetime import timedelta
import  time

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='project_4',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('project_index.html')

#Define route for login
@app.route('/cuslogin')
def cuslogin():
	try:
		session.pop('email')
	except:
		print(1)
	return render_template('login_1.html')

@app.route('/forgot')
def forgot():
	return render_template('forgot.html')

@app.route('/balogin')
def balogin():
	return render_template('login_2.html')

@app.route('/stafflogin')
def stafflogin():
	return render_template('login_3.html')

#Define route for register
@app.route('/cusregister')
def cusregister():
	return render_template('cusregister.html')
    
@app.route('/baregister')
def baregister():
	return render_template('baregister.html')

@app.route('/staffregister')
def staffregister():
	return render_template('staffregister.html')


#############login design
@app.route('/cusloginAuth', methods=['GET', 'POST'])
def cusloginAuth():
	#grabs information from the forms
	try:
		session.pop('email')
	except:
		print(1)
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s and password = %s'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['email'] = email
		return redirect(url_for('cushome'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or email'
		return render_template('login_1.html', error=error)

@app.route('/forgotAuth', methods=['GET', 'POST'])
def forgotAuth():
	try:
		session.pop('email')
	except:
		print(0)
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	answer = request.form['answer']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		cursor = conn.cursor();
		query = "select answer from question where customer_email = %s"
		cursor.execute(query,(email))
		data = cursor.fetchall()
		if(data):
			right = data[0]['answer']
			if answer == right:
				cursor = conn.cursor();
				query = '''UPDATE customer
				SET password = %s 
				WHERE email = %s  '''
				cursor.execute(query, (password, email))
				cursor.close()
				error = "change success"
				return render_template('login_1.html', error=error)
			else:
				error = 'wrong answer'
				return render_template('forgot.html', error=error)
		else:
			if answer == "S":
				cursor = conn.cursor();
				query = '''UPDATE customer
				SET password = %s 
				WHERE email = %s  '''
				cursor.execute(query, (password, email))
				cursor.close()
				error = "change success"
				return render_template('login_1.html', error=error)
			else:
				error = 'wrong answer'
				return render_template('forgot.html', error=error)

		session['email'] = email
		return redirect(url_for('cushome'))
	else:
		#returns an error message to the html page
		error = 'Invalid email'
		return render_template('forgot.html', error=error)
	
@app.route('/baloginAuth', methods=['GET', 'POST'])
def baloginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM booking_agent WHERE email = %s and password = %s and booking_agent_id = %s'
	cursor.execute(query, (email, password, booking_agent_id))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['email'] = email
		session['booking_agent_id'] = booking_agent_id
		return redirect(url_for('bahome'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or email'
		return render_template('login_2.html', error=error)

@app.route('/staffloginAuth', methods=['GET', 'POST'])
def staffloginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s and password = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('staffhome'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or email'
		return render_template('login_3.html', error=error)

##############register design
@app.route('/cusregisterAuth', methods=['GET', 'POST'])
def cusregisterAuth():
	#grabs information from the forms
	email = request.form['email']
	name = request.form['name'] 
	password = request.form['password']
	building_number = request.form['building_number']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	phone_number = request.form['phone_number']
	passport_number = request.form['passport_number']
	passport_expiration = request.form['passport_expiration']
	passport_country = request.form['passport_country']
	date_of_birth = request.form['date_of_birth']
	answer = request.form['answer']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute(query, (email))
	
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This customer already exists"
		return render_template('cusregister.html', error = error)
	else:
		ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (email, name, password, building_number, street, city, state, phone_number, passport_number, passport_expiration, passport_country, date_of_birth))
		if answer == '':
			query = 'INSERT INTO question VALUES(%s, %s)'
			cursor.execute(query,(email,'S'))
		else:
			query = 'INSERT INTO question VALUES(%s, %s)'
			cursor.execute(query,(email,answer))
		conn.commit()
		cursor.close()
		return render_template('project_index.html')



@app.route('/baregisterAuth', methods=['GET', 'POST'])
def baregisterAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	booking_agent_id = request.form['booking_agent_id']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM booking_agent WHERE email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This booking_agent already exists"
		return render_template('baregister.html', error = error)
	else:
		ins = 'INSERT INTO booking_agent VALUES(%s, %s, %s)'
		cursor.execute(ins, (email, password, booking_agent_id))
		conn.commit()
		cursor.close()
		return render_template('project_index.html')

@app.route('/staffregisterAuth', methods=['GET', 'POST'])
def staffregisterAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']
	first_name = request.form['first_name']
	last_name = request.form['last_name']
	date_of_birth = request.form['date_of_birth']
	airline_name = request.form['airline_name']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This staff already exists"
		return render_template('staffregister.html', error = error)
	else:
		ins = 'INSERT INTO airline_staff VALUES(%s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (username, password, first_name, last_name, date_of_birth, airline_name))
		conn.commit()
		cursor.close()
		return render_template('project_index.html')

############staff home design
@app.route('/staffhome')
def staffhome():
	username = session['username']
	cursor = conn.cursor();
	status = 'upcoming'
	today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	str=today.replace("-","")
	str2date=datetime.datetime.strptime(str,"%Y%m%d")
	start = str2date-timedelta(30)
	
	sy = start.year
	sm = start.month
	sd = start.day
	
	ey = datetime.datetime.now().year
	em = datetime.datetime.now().month
	ed = datetime.datetime.now().day
	query = '''SELECT * 
	FROM flight, airline_staff
	WHERE username = %s and status = %s and airline_staff.airline_name = flight.airline_name
	and departure_time >= %s'''
	cursor.execute(query, (username, status, datetime.datetime(sy,sm,sd,0,0,0)))
	data1 = cursor.fetchall() 
	print(data1)
	session['username'] = username
	for each in data1:
		print(each)
	cursor.close()

	cursor = conn.cursor();
	query = '''select * from airline_staff where username = %s'''
	cursor.execute(query, (username))
	data = cursor.fetchall() 
	airline = data[0]['airline_name']
	username = session['username']
	session['airline_name'] = airline
	cursor.close()

	
	return render_template('staffhome.html', username=username, posts=data1, result = [])

@app.route('/staffsee_flight', methods=['GET', 'POST'])
def staffsee_flight():
	username = session['username']
	dcity = request.form['departure_city']
	acity = request.form['arrival_city']
	start = request.form['startday']
	end = request.form['endday']

	sy = int(start[0:4])
	sm = int(start[5:7])
	sd = int(start[8:10])
	
	ey = int(end[0:4])
	em = int(end[5:7])
	ed = int(end[8:10])

	cursor = conn.cursor();
	#SELECT flight.flight_num as flight_num, flight.status as status, flight.airline_name as airline_name, departure_city, arrival_city, flight.departure_airport as departure_airport, flight.arrival_airport as arrival_airport
	#query = '''select distinct flight.flight_num as flight_num, flight.status as status, flight.airline_name as airline_name, departure_city, arrival_city, flight.departure_airport as departure_airport, flight.arrival_airport as arrival_airport, departure_time, arrival_time
	#FROM flight, airline_staff, flight_search
	#WHERE username = %s and airline_staff.airline_name = flight.airline_name and airline_staff.airline_name = flight_search.airline_name
	#and date >= %s
	#and date <= %s
	#and departure_city = %s
	#and arrival_city = %s'''
	query = '''select *
	from flight
	where flight_num in (select flight_search.flight_num
	from flight_search, airline_staff
	where username = %s and airline_staff.airline_name = flight_search.airline_name
	and date >= %s
	and date <= %s
	and departure_city = %s
	and arrival_city = %s)
	'''
	cursor.execute(query, (username, datetime.datetime(sy,sm,sd,0,0,0),datetime.datetime(ey,em,ed,0,0,0),dcity,acity))
	data1 = cursor.fetchall() 
	print(data1)
	cursor.close()

	return render_template('staffhome.html', username=username, posts=data1, result = [])


@app.route('/cus_flight', methods=['GET', 'POST'])
def cus_flight():
	username = session['username']
	cursor = conn.cursor();
	status = 'upcoming'
	today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	str=today.replace("-","")
	str2date=datetime.datetime.strptime(str,"%Y%m%d")
	start = str2date-timedelta(30)
	
	sy = start.year
	sm = start.month
	sd = start.day
	
	ey = datetime.datetime.now().year
	em = datetime.datetime.now().month
	ed = datetime.datetime.now().day
	query = '''SELECT * 
	FROM flight, airline_staff
	WHERE username = %s and status = %s and airline_staff.airline_name = flight.airline_name
	and departure_time >= %s'''
	cursor.execute(query, (username, status, datetime.datetime(sy,sm,sd,0,0,0)))
	data1 = cursor.fetchall() 
	print(data1)
	session['username'] = username
	cursor.close()


	flight_num = request.form['flight']
	cursor = conn.cursor()
	query = '''SELECT distinct customer_email, flight_num
	FROM ba_flight, airline_staff
	WHERE username = %s and airline_staff.airline_name = ba_flight.airline_name and flight_num = %s'''
	cursor.execute(query, (username, flight_num))
	cus_list = cursor.fetchall()
	cursor.close()
	return render_template('staffhome.html', username=username, posts=data1, cus_list = cus_list, result = [])

@app.route('/operation', methods=['GET', 'POST'])
def operation():
	username = session['username']
	cursor = conn.cursor();
	status = 'upcoming'
	today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	str=today.replace("-","")
	str2date=datetime.datetime.strptime(str,"%Y%m%d")
	start = str2date-timedelta(30)
	
	sy = start.year
	sm = start.month
	sd = start.day
	
	ey = datetime.datetime.now().year
	em = datetime.datetime.now().month
	ed = datetime.datetime.now().day
	query = '''SELECT * 
	FROM flight, airline_staff
	WHERE username = %s and status = %s and airline_staff.airline_name = flight.airline_name
	and departure_time >= %s'''
	cursor.execute(query, (username, status, datetime.datetime(sy,sm,sd,0,0,0)))
	data1 = cursor.fetchall() 
	print(data1)
	session['username'] = username
	cursor.close()

	cursor = conn.cursor()
	query = '''select * from airplane where airline_name = %s'''
	cursor.execute(query, (session['airline_name']))
	airplane = cursor.fetchall() 
	print(airplane)
	cursor.close()

	cursor = conn.cursor()
	query = '''select * from airport'''
	cursor.execute(query)
	airport = cursor.fetchall() 
	print(airplane)
	cursor.close()
	

	return render_template('operation.html', username=username, posts=data1, airplane = airplane, airport = airport)

@app.route('/add_ticket', methods=['GET', 'POST'])
def add_ticket():
	username = session['username']
	cursor = conn.cursor();
	status = 'upcoming'
	today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	str=today.replace("-","")
	str2date=datetime.datetime.strptime(str,"%Y%m%d")
	start = str2date-timedelta(30)
	
	sy = start.year
	sm = start.month
	sd = start.day
	
	ey = datetime.datetime.now().year
	em = datetime.datetime.now().month
	ed = datetime.datetime.now().day
	query = '''SELECT * 
	FROM flight, airline_staff
	WHERE username = %s and status = %s and airline_staff.airline_name = flight.airline_name
	and departure_time >= %s'''
	cursor.execute(query, (username, status, datetime.datetime(sy,sm,sd,0,0,0)))
	data1 = cursor.fetchall() 
	print(data1)
	session['username'] = username
	cursor.close()

	cursor = conn.cursor()
	flight_num = request.form['flight_num']
	ticket_id = request.form['ticket_id']
	query = '''insert into ticket values (%s,%s,%s)'''
	cursor.execute(query, (ticket_id, session['airline_name'], flight_num))
	conn.commit()
	error_2 = 'success'
	cursor.close()

	cursor = conn.cursor()
	query = '''select * from airplane where airline_name = %s'''
	cursor.execute(query, (session['airline_name']))
	airplane = cursor.fetchall() 
	print(airplane)
	cursor.close()
	

	return render_template('operation.html', username=username, posts=data1, airplane = airplane, error2 = error_2)

@app.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
	username = session['username']
	cursor = conn.cursor();
	status = 'upcoming'
	today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	str=today.replace("-","")
	str2date=datetime.datetime.strptime(str,"%Y%m%d")
	start = str2date-timedelta(30)
	
	sy = start.year
	sm = start.month
	sd = start.day
	
	ey = datetime.datetime.now().year
	em = datetime.datetime.now().month
	ed = datetime.datetime.now().day
	query = '''SELECT * 
	FROM flight, airline_staff
	WHERE username = %s and status = %s and airline_staff.airline_name = flight.airline_name
	and departure_time >= %s'''
	cursor.execute(query, (username, status, datetime.datetime(sy,sm,sd,0,0,0)))
	data1 = cursor.fetchall() 
	print(data1)
	session['username'] = username
	cursor.close()

	cursor = conn.cursor()
	airplane_id = request.form['airplane_id']
	seats = request.form['seats']
	query = '''insert into airplane values (%s,%s,%s)'''
	cursor.execute(query, (session['airline_name'], airplane_id, seats))
	conn.commit()
	error_2 = 'success'
	cursor.close()

	cursor = conn.cursor()
	query = '''select * from airplane where airline_name = %s'''
	cursor.execute(query, (session['airline_name']))
	airplane = cursor.fetchall() 
	print(airplane)
	cursor.close()
	

	return render_template('operation.html', username=username, posts=data1, airplane = airplane, error2 = error_2)

@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
	username = session['username']
	
	cursor = conn.cursor()
	airline_name = session['airline_name']
	flight_num = request.form['flight_num']
	departure_airport = request.form['departure_airport']
	start = request.form['departure_time']
	arrival_airport = request.form['arrival_airport']
	end = request.form['arrival_time']
	price = request.form['price']
	status = request.form['status']
	airplane_id = request.form['airplane_id']

	sy = int(start[0:4])
	sm = int(start[5:7])
	sd = int(start[8:10])
	s1 = int(start[11:13])
	s2 = int(start[14:16])
	s3 = int(start[17:19])
	
	ey = int(end[0:4])
	em = int(end[5:7])
	ed = int(end[8:10])
	e1 = int(start[11:13])
	e2 = int(start[14:16])
	e3 = int(start[17:19])

	query = '''insert into flight values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
	cursor.execute(query, (airline_name, flight_num, departure_airport, datetime.datetime(sy,sm,sd,s1,s2,s3), arrival_airport, datetime.datetime(ey,em,ed,e1,e2,e3), price, status, airplane_id))
	conn.commit()
	error_2 = 'success'
	cursor.close()

	cursor = conn.cursor()
	query = '''select * from airplane where airline_name = %s'''
	cursor.execute(query, (session['airline_name']))
	airplane = cursor.fetchall() 
	print(airplane)
	cursor.close()

	cursor = conn.cursor();
	status = 'upcoming'
	today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	str=today.replace("-","")
	str2date=datetime.datetime.strptime(str,"%Y%m%d")
	start = str2date-timedelta(30)
	
	sy = start.year
	sm = start.month
	sd = start.day
	
	ey = datetime.datetime.now().year
	em = datetime.datetime.now().month
	ed = datetime.datetime.now().day
	query = '''SELECT * 
	FROM flight, airline_staff
	WHERE username = %s and status = %s and airline_staff.airline_name = flight.airline_name
	and departure_time >= %s'''
	cursor.execute(query, (username, status, datetime.datetime(sy,sm,sd,0,0,0)))
	data1 = cursor.fetchall() 
	print(data1)
	session['username'] = username
	cursor.close()

	error = "add_success"

	

	return render_template('operation.html', username=username, error = error, posts=data1, airplane = airplane, error2 = error_2)

@app.route('/add_airport', methods=['GET', 'POST'])
def add_airport():
	username = session['username']
	cursor = conn.cursor();
	status = 'upcoming'
	today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	str=today.replace("-","")
	str2date=datetime.datetime.strptime(str,"%Y%m%d")
	start = str2date-timedelta(30)
	
	sy = start.year
	sm = start.month
	sd = start.day
	
	ey = datetime.datetime.now().year
	em = datetime.datetime.now().month
	ed = datetime.datetime.now().day
	query = '''SELECT * 
	FROM flight, airline_staff
	WHERE username = %s and status = %s and airline_staff.airline_name = flight.airline_name
	and departure_time >= %s'''
	cursor.execute(query, (username, status, datetime.datetime(sy,sm,sd,0,0,0)))
	data1 = cursor.fetchall() 
	print(data1)
	session['username'] = username
	cursor.close()

	cursor = conn.cursor()
	airplane_id = request.form['airport_name']
	seats = request.form['airport_city']
	query = '''insert into airport values (%s,%s)'''
	cursor.execute(query, (airplane_id, seats))
	conn.commit()
	error_3 = 'success'
	cursor.close()

	cursor = conn.cursor()
	query = '''select * from airplane where airline_name = %s'''
	cursor.execute(query, (session['airline_name']))
	airplane = cursor.fetchall() 
	print(airplane)
	cursor.close()

	cursor = conn.cursor()
	query = '''select * from airport'''
	cursor.execute(query)
	airport = cursor.fetchall() 
	print(airplane)
	cursor.close()
	

	return render_template('operation.html', username=username, posts=data1, airplane = airplane, airport = airport, error3 = error_3)


@app.route('/update_status', methods=['GET', 'POST'])
def update_status():
	username = session['username']
	

	flight = request.form['flight']
	status = request.form['status']
	
	cursor = conn.cursor();
	query = '''select * from airline_staff where username = %s'''
	cursor.execute(query, (username))
	data = cursor.fetchall() 
	airline = data[0]['airline_name']
	query = '''select * from flight where flight.airline_name = %s AND flight.flight_num = %s'''
	cursor.execute(query, (airline, flight))
	data = cursor.fetchall() 
	if (data):
		error = "change_success"
	else:
		error = 'no such flight'
	query = '''UPDATE flight 
	SET status = %s 
	WHERE flight.airline_name = %s AND flight.flight_num = %s '''
	cursor.execute(query, (status, airline, flight))
	conn.commit()
	cursor.close()

	cursor = conn.cursor();
	status = 'upcoming'
	today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	str=today.replace("-","")
	str2date=datetime.datetime.strptime(str,"%Y%m%d")
	start = str2date-timedelta(30)
	
	sy = start.year
	sm = start.month
	sd = start.day
	
	ey = datetime.datetime.now().year
	em = datetime.datetime.now().month
	ed = datetime.datetime.now().day
	query = '''SELECT * 
	FROM flight, airline_staff
	WHERE username = %s and status = %s and airline_staff.airline_name = flight.airline_name
	and departure_time >= %s'''
	cursor.execute(query, (username, status, datetime.datetime(sy,sm,sd,0,0,0)))
	data1 = cursor.fetchall() 
	print(data1)
	session['username'] = username
	cursor.close()
	return render_template('operation.html', username=username, posts=data1, error = error)


@app.route('/reports', methods=['GET', 'POST'])
def reports():
	username = session['username']
	airline = session['airline_name']

	year = datetime.datetime.now().year
	month = datetime.datetime.now().month
	month += 1
	if month > 12:
		month = 1
		year += 1
	sy = year
	sm = month
	ey = sy
	em = sm
	month -= 12
	if month <= 0:
		month += 12
		year -= 1
	sm -= 1
	if sm <= 0:
		sm += 12
		sy -= 1
	cursor = conn.cursor();
	query = '''select booking_agent_id, count(ticket_id) as amount
				from ba_flight
				where airline_name = %s
				and purchase_date >= %s
				and purchase_date < %s
				and booking_agent_id is not null
				group by booking_agent_id
				order by amount desc
				limit 0,5 '''
	cursor.execute(query, (airline, datetime.date(year,month,1),datetime.date(ey,em,1)))
	data = cursor.fetchall()
	cursor.close()

	cursor = conn.cursor();
	query = '''select booking_agent_id, count(ticket_id) as amount
				from ba_flight
				where airline_name = %s
				and purchase_date >= %s
				and purchase_date < %s
				and booking_agent_id is not null
				group by booking_agent_id
				order by amount desc
				limit 0,5 '''
	cursor.execute(query, (airline, datetime.date(sy,sm,1),datetime.date(ey,em,1)))
	data1 = cursor.fetchall()
	cursor.close()

	cursor = conn.cursor();
	query = '''select booking_agent_id, sum(price)*0.1 as total, avg(price)*0.1 as average, count(price) as amount
				from ba_flight,flight
  				where ba_flight.flight_num = flight.flight_num 
				and booking_agent_id >= 0
				and ba_flight.airline_name = flight.airline_name 
				and ba_flight.airline_name = %s
				and purchase_date >= %s
				and purchase_date < %s
   				group by booking_agent_id
				order by total desc
				limit 0,5 '''
	cursor.execute(query, (airline, datetime.date(year,month,1),datetime.date(ey,em,1)))
	data2 = cursor.fetchall()
	cursor.close()

	cursor = conn.cursor()
	query = '''select * from airport'''
	cursor.execute(query)
	airport = cursor.fetchall() 
	cursor.close()

	cursor = conn.cursor();
	query = '''select customer_email, count(purchases.ticket_id) as amount
				from purchases, ticket
				where ticket.airline_name = %s
				and purchases.ticket_id = ticket.ticket_id
				and purchase_date >= %s
				and purchase_date < %s
   				group by customer_email
				order by amount desc
				limit 0,1 '''
	cursor.execute(query, (airline, datetime.date(year,month,1),datetime.date(ey,em,1)))
	cus = cursor.fetchall()
	cursor.close()

	cursor = conn.cursor();
	query = '''select airport_city, count(ticket_id) as amount
				from ba_flight, airport
				where ba_flight.airline_name = %s
				and purchase_date >= %s
				and purchase_date < %s
				and airport_name = departure_airport
   				group by airport_city
				order by amount desc
				limit 0,3 '''
	cursor.execute(query, (airline, datetime.date(year,month,1),datetime.date(ey,em,1)))
	destination = cursor.fetchall()
	cursor.close()

	cursor = conn.cursor();
	query = '''select airport_city, count(ticket_id) as amount
				from ba_flight, airport
				where ba_flight.airline_name = %s
				and purchase_date >= %s
				and purchase_date < %s
				and airport_name = departure_airport
   				group by airport_city
				order by amount desc
				limit 0,3 '''
	cursor.execute(query, (airline, datetime.date(sy,sm,1),datetime.date(ey,em,1)))
	destination1 = cursor.fetchall()
	cursor.close()

	cursor = conn.cursor()
	query = '''select * from airport'''
	cursor.execute(query)
	airport = cursor.fetchall() 
	cursor.close()
	

	return render_template('reports.html', username=username, ba = data, ba1 = data1, ba2 = data2, cus = cus, destination = destination, destination1 = destination1)

@app.route('/staff_see_cus', methods=['GET', 'POST'])
def staff_see_cus():
	username = session['username']
	airline = session['airline_name']

	year = datetime.datetime.now().year
	month = datetime.datetime.now().month
	month += 1
	if month > 12:
		month = 1
		year += 1
	sy = year
	sm = month
	ey = sy
	em = sm
	month -= 12
	if month <= 0:
		month += 12
		year -= 1
	sm -= 1
	if sm <= 0:
		sm += 12
		sy -= 1
	cursor = conn.cursor();
	query = '''select booking_agent_id, count(ticket_id) as amount
				from ba_flight
				where airline_name = %s
				and purchase_date >= %s
				and purchase_date < %s
				and booking_agent_id is not null
				group by booking_agent_id
				order by amount desc
				limit 0,5 '''
	cursor.execute(query, (airline, datetime.date(year,month,1),datetime.date(ey,em,1)))
	data = cursor.fetchall()
	cursor.close()

	cursor = conn.cursor();
	query = '''select booking_agent_id, count(ticket_id) as amount
				from ba_flight
				where airline_name = %s
				and purchase_date >= %s
				and purchase_date < %s
				and booking_agent_id is not null
				group by booking_agent_id
				order by amount desc
				limit 0,5 '''
	cursor.execute(query, (airline, datetime.date(sy,sm,1),datetime.date(ey,em,1)))
	data1 = cursor.fetchall()
	cursor.close()

	cursor = conn.cursor();
	query = '''select booking_agent_id, sum(price)*0.1 as total, avg(price)*0.1 as average, count(price) as amount
				from ba_flight,flight
  				where ba_flight.flight_num = flight.flight_num 
				and ba_flight.airline_name = flight.airline_name 
				and ba_flight.airline_name = %s
				and purchase_date >= %s
				and purchase_date < %s
   				group by booking_agent_id
				order by total desc
				limit 0,5 '''
	cursor.execute(query, (airline, datetime.date(year,month,1),datetime.date(ey,em,1)))
	data2 = cursor.fetchall()
	cursor.close()

	cursor = conn.cursor();
	query = '''select customer_email, count(ticket_id) as amount
				from ba_flight
				where ba_flight.airline_name = %s
				and purchase_date >= %s
				and purchase_date < %s
   				group by booking_agent_id
				order by amount desc
				limit 0,1 '''
	cursor.execute(query, (airline, datetime.date(year,month,1),datetime.date(ey,em,1)))
	cus = cursor.fetchall()
	cursor.close()

	cursor = conn.cursor();
	query = '''select airport_city, count(ticket_id) as amount
				from ba_flight, airport
				where ba_flight.airline_name = %s
				and airport_name = departure_airport
   				group by airport_city
				order by amount desc
				limit 0,3 '''
	cursor.execute(query, (airline))
	destination = cursor.fetchall()
	cursor.close()
	
	cursor = conn.cursor();
	query = '''select airport_city, count(ticket_id) as amount
				from ba_flight, airport
				where ba_flight.airline_name = %s
				and purchase_date >= %s
				and purchase_date < %s
				and airport_name = departure_airport
   				group by airport_city
				order by amount desc
				limit 0,3 '''
	cursor.execute(query, (airline, datetime.date(sy,sm,1),datetime.date(ey,em,1)))
	destination1 = cursor.fetchall()
	cursor.close()

	cus_email = request.form['customer_email']
	cursor = conn.cursor();
	query = '''select distinct flight_num, customer_email
				from ba_flight
				where ba_flight.airline_name = %s
				and customer_email = %s'''
	cursor.execute(query, (airline, cus_email))
	lis = cursor.fetchall()
	cursor.close()
	return render_template('reports.html', username=username, ba = data, ba1 = data1, ba2 = data2, cus = cus, lis = lis, destination = destination, destination1 = destination1)

@app.route('/financial_report', methods=['GET', 'POST'])
def financial_report():
	airline = session['airline_name']
	year = datetime.datetime.now().year
	month = datetime.datetime.now().month
	month += 1
	if month > 12:
		month = 1
		year += 1
	ym = []
	ym_1 = []
	for i in range(12):
		ym_1.append([year,month])
		month -= 1
		if month <= 0:
			year -= 1
			month += 12
		ym.append([year,month])
	print(ym)
	amount = []
	for j in range(len(ym)):
		cursor = conn.cursor();
		query = '''select airline_name, count(ticket_id) as amount
					from ba_flight
					where airline_name = %s
						and purchase_date >= %s
						and purchase_date < %s
					group by airline_name '''
		cursor.execute(query, (airline, datetime.date(ym[j][0],ym[j][1],1),datetime.date(ym_1[j][0],ym_1[j][1],1)))
		data = cursor.fetchall()
		if (data):
			amount.append(int(data[0]['amount']))
		else:
			amount.append(0)
		cursor.close()
	total = sum(amount)
	print(amount)
	return render_template('financial_report.html', ym = ym, amount = amount, total = total)

@app.route('/see_sold', methods=['GET', 'POST'])
def see_sold():
	airline = session['airline_name']
	start = request.form['start']
	end = request.form['end']
	sy = int(start[0:4])
	sm = int(start[5:7])
	sd = int(start[8:10])
	ey = int(end[0:4])
	em = int(end[5:7])
	ed = int(end[8:10])


	em += 1
	if em > 12:
		em = 1
		ey += 1
	ym = []
	ym_1 = []
	while (em != sm) and (ey != em):
		ym.append([sy,sm])
		sm += 1
		if sm >= 13:
			sy += 1
			sm = 1
		ym_1.append([sy,sm])
	print(ym)
	amount = []
	for j in range(len(ym)):
		cursor = conn.cursor();
		query = '''select airline_name, count(ticket_id) as amount
					from ba_flight
					where airline_name = %s
						and purchase_date >= %s
						and purchase_date < %s
					group by airline_name '''
		cursor.execute(query, (airline, datetime.date(ym[j][0],ym[j][1],1),datetime.date(ym_1[j][0],ym_1[j][1],1)))
		data = cursor.fetchall()
		if (data):
			amount.append(int(data[0]['amount']))
		else:
			amount.append(0)
		cursor.close()
	print(amount)
	total = sum(amount)
	return render_template('financial_report.html', ym = ym, amount = amount, total = total)

@app.route('/piechart', methods=['GET', 'POST'])
def piechart():
	username = session['username']
	airline = session['airline_name']

	year = datetime.datetime.now().year
	month = datetime.datetime.now().month
	month += 1
	if month > 12:
		month = 1
		year += 1
	sy = year
	sm = month
	ey = sy
	em = sm
	month -= 12
	if month <= 0:
		month += 12
		year -= 1
	sm -= 1
	if sm <= 0:
		sm += 12
		sy -= 1

	cursor = conn.cursor();
	query = '''select ba_flight.airline_name, sum(price) as total
		from ba_flight, flight
		where (booking_agent_id is not null and  booking_agent_id> 0)
		and ba_flight.flight_num = flight.flight_num 
		and ba_flight.airline_name = flight.airline_name
		and ba_flight.airline_name = %s
		and purchase_date >= %s
		and purchase_date < %s '''
	cursor.execute(query, (airline, datetime.date(sy,sm,1),datetime.date(ey,em,1)))
	data = cursor.fetchall()
	if data[0]['total']:
		ba = int(data[0]['total'])
	else:
		ba = 1
	cursor.close()

	cursor = conn.cursor();
	query = '''select ba_flight.airline_name, sum(price) as total
		from ba_flight, flight
		where (booking_agent_id is null or booking_agent_id = 0)
		and ba_flight.flight_num = flight.flight_num 
		and ba_flight.airline_name = flight.airline_name
		and ba_flight.airline_name = %s
		and purchase_date >= %s
		and purchase_date < %s '''
	cursor.execute(query, (airline, datetime.date(sy,sm,1),datetime.date(ey,em,1)))
	data = cursor.fetchall()
	#print(data)
	if data[0]['total']:
		cus = int(data[0]['total'])
	else:
		cus = 1
	cursor.close()

	cursor = conn.cursor();
	query = '''select ba_flight.airline_name, sum(price) as total
		from ba_flight, flight
		where (booking_agent_id is not null and  booking_agent_id> 0) 
		and ba_flight.flight_num = flight.flight_num 
		and ba_flight.airline_name = flight.airline_name
		and ba_flight.airline_name = %s
		and purchase_date >= %s
		and purchase_date < %s '''
	cursor.execute(query, (airline, datetime.date(year,month,1),datetime.date(ey,em,1)))
	data = cursor.fetchall()
	if data[0]['total']:
		print('aaaaaaaaaa')
		ba1 = int(data[0]['total'])
	else:
		ba1 = 1
	cursor.close()

	cursor = conn.cursor();
	query = '''select ba_flight.airline_name, sum(price) as total
		from ba_flight, flight
		where (booking_agent_id is null or booking_agent_id = 0)
		and ba_flight.flight_num = flight.flight_num 
		and ba_flight.airline_name = flight.airline_name
		and ba_flight.airline_name = %s
		and purchase_date >= %s
		and purchase_date < %s '''
	cursor.execute(query, (airline, datetime.date(year,month,1),datetime.date(ey,em,1)))
	data = cursor.fetchall()
	if data[0]['total']:
		cus1 = int(data[0]['total'])
	else:
		cus1 = 1
	cursor.close()

	ratio = [int(cus*100/(cus+ba))/100,int(ba*100/(cus+ba))/100+0.01]
	print([cus,ba])
	print([cus1,ba1])
	ratio1 = [int(cus1*100/(cus1+ba1))/100,int(ba1*100/(cus1+ba1))/100+0.01]
	print(ratio)
	print(ratio1)
	print(1111111111111)
	print(airline)
	return render_template('test.html', ratio = ratio, ratio1 = ratio1)

@app.route('/staffback', methods=['GET', 'POST'])
def staffback():
	return redirect(url_for('staffhome'))

@app.route('/stafflogout')
def stafflogout():
	session.pop('username')
	session.pop('airline_name')
	return redirect('/')


############ba home design
@app.route('/bashome')
def bahome():
	booking_agent_id = session['booking_agent_id']
	email = session['email']
	cursor = conn.cursor();
	status = 'upcoming'
	query = 'SELECT * FROM ba_flight WHERE booking_agent_id = %s and status = %s'
	cursor.execute(query, (booking_agent_id,status))
	data1 = cursor.fetchall() 
	for each in data1:
		print(each)
	# deal with commission
	today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	str=today.replace("-","")
	str2date=datetime.datetime.strptime(str,"%Y%m%d")
	start = str2date-timedelta(30)

	sy = start.year
	sm = start.month
	sd = start.day
	
	ey = datetime.datetime.now().year
	em = datetime.datetime.now().month
	ed = datetime.datetime.now().day

	cursor1 = conn.cursor();
	query = '''select ba_flight.booking_agent_id, sum(price)*0.1 as total, avg(price)*0.1 as average, count(price) as amount
		from ba_flight,flight, purchases
   		where ba_flight.flight_num = flight.flight_num 
  		 and ba_flight.airline_name = flight.airline_name
   		and ba_flight.ticket_id = purchases.ticket_id
		and purchases.booking_agent_id = %s
   		and purchases.purchase_date >= %s
   		and purchases.purchase_date <= %s
   		group by booking_agent_id'''
	cursor1.execute(query, (booking_agent_id,datetime.date(sy,sm,sd),datetime.date(ey,em,ed)))
	commission = cursor1.fetchall()
	if not (commission):
		commission = [{'booking_agent_id': booking_agent_id, 'total': 0, 'average': 0, 'amount': 0}]

	cursor1.close()


	cursor.close()
	return render_template('bahome.html', email=email, posts=data1, result = [], commission = commission)

@app.route('/basee_flight', methods=['GET', 'POST'])
def basee_flight():
	booking_agent_id = session['booking_agent_id']
	email = session['email']    
	cursor = conn.cursor();
	status = request.form['status']
	query = 'SELECT * FROM ba_flight WHERE booking_agent_id = %s and status = %s '
	cursor.execute(query, (booking_agent_id,status))
	data1 = cursor.fetchall() 
	for each in data1:
		print(each)
	cursor.close()

	today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	str=today.replace("-","")
	str2date=datetime.datetime.strptime(str,"%Y%m%d")
	start = str2date-timedelta(30)

	sy = start.year
	sm = start.month
	sd = start.day
	
	ey = datetime.datetime.now().year
	em = datetime.datetime.now().month
	ed = datetime.datetime.now().day

	cursor1 = conn.cursor();
	query = '''select ba_flight.booking_agent_id, sum(price)*0.1 as total, avg(price)*0.1 as average, count(price) as amount
		from ba_flight,flight, purchases
   		where ba_flight.flight_num = flight.flight_num 
  		 and ba_flight.airline_name = flight.airline_name
   		and ba_flight.ticket_id = purchases.ticket_id
		and purchases.booking_agent_id = %s
   		and purchases.purchase_date >= %s
   		and purchases.purchase_date < %s
   		group by booking_agent_id'''
	cursor1.execute(query, (booking_agent_id, datetime.date(sy,sm,sd),datetime.date(ey,em,ed)))
	commission = cursor1.fetchall()
	if not (commission):
		commission = [{'booking_agent_id': booking_agent_id, 'total': 0, 'average': 0, 'amount': 0}]
	cursor1.close()

	return render_template('bahome.html', email=email, posts=data1, result = [], commission = commission)

@app.route('/basearch_flight', methods=['GET', 'POST'])
def basearch_flight():
	booking_agent_id = session['booking_agent_id']
	email = session['email']
	cursor = conn.cursor();
	status = 'upcoming'
	query = 'SELECT * FROM ba_flight WHERE booking_agent_id = %s and status = %s'
	cursor.execute(query, (booking_agent_id,status))
	data1 = cursor.fetchall()
	cursor = conn.cursor();
	departure_city = request.form['departure_city']
	departure_airport = request.form['departure_airport']
	print(departure_city == "")
	arrival_city = request.form['arrival_city']
	arrival_airport = request.form['arrival_airport']
	date = request.form['date']
	query = '''select *
    from flight
    where status = "upcoming" and (flight_num,airline_name) in (
    SELECT flight_num, airline_name FROM flight_search
    WHERE departure_city = (case when %s = '' then departure_city else %s end)
    and departure_airport = (case when %s = '' then departure_airport else %s end)
    and arrival_city = (case when %s = '' then arrival_city else %s end)
    and arrival_airport = (case when %s = '' then arrival_airport else %s end)
    and date = (case when %s = '' then date else %s end))

    '''
	cursor.execute(query, (departure_city,departure_city,departure_airport,departure_airport,arrival_city,arrival_city,arrival_airport,arrival_airport,date,date))
	result = cursor.fetchall()
	cursor.close()
	
	today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	str=today.replace("-","")
	str2date=datetime.datetime.strptime(str,"%Y%m%d")
	start = str2date-timedelta(30)

	sy = start.year
	sm = start.month
	sd = start.day
	
	ey = datetime.datetime.now().year
	em = datetime.datetime.now().month
	ed = datetime.datetime.now().day

	cursor1 = conn.cursor();
	query = '''select ba_flight.booking_agent_id, sum(price)*0.1 as total, avg(price)*0.1 as average, count(price) as amount
		from ba_flight,flight, purchases
   		where ba_flight.flight_num = flight.flight_num 
  		 and ba_flight.airline_name = flight.airline_name
   		and ba_flight.ticket_id = purchases.ticket_id
		and purchases.booking_agent_id = %s
   		and purchases.purchase_date >= %s
   		and purchases.purchase_date < %s
   		group by booking_agent_id'''
	cursor1.execute(query, (booking_agent_id, datetime.date(sy,sm,sd),datetime.date(ey,em,ed)))
	commission = cursor1.fetchall()
	if not (commission):
		commission = [{'booking_agent_id': booking_agent_id, 'total': 0, 'average': 0, 'amount': 0}]
	cursor1.close()

	return render_template('bahome.html', email=email, posts=data1, result = result, commission = commission)

@app.route('/bapurchase', methods=['GET', 'POST'])
def bapurchase():
	email = session['email']
	booking_agent_id = session['booking_agent_id']
	cursor = conn.cursor();
	flight = request.form['flight']
	airline = request.form['airline']
	cusemail = request.form['customer_email']
	query = '''select ticket_id 
			from ticket
			where airline_name = %s and flight_num = %s
				and ticket_id not in (select ticket_id from purchases)'''
	cursor.execute(query, (airline, flight))
	ticket = cursor.fetchall()
	print(ticket)
	error = None
	today=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	str=today.replace("-","")
	str2date=datetime.datetime.strptime(str,"%Y%m%d")
	start = str2date-timedelta(30)

	sy = start.year
	sm = start.month
	sd = start.day
	
	ey = datetime.datetime.now().year
	em = datetime.datetime.now().month
	ed = datetime.datetime.now().day

	cursor1 = conn.cursor();
	query = '''select ba_flight.booking_agent_id, sum(price)*0.1 as total, avg(price)*0.1 as average, count(price) as amount
		from ba_flight,flight, purchases
   		where ba_flight.flight_num = flight.flight_num 
  		 and ba_flight.airline_name = flight.airline_name
   		and ba_flight.ticket_id = purchases.ticket_id
		and purchases.booking_agent_id = %s
   		and purchases.purchase_date >= %s
   		and purchases.purchase_date < %s
   		group by booking_agent_id'''
	cursor1.execute(query, (booking_agent_id, datetime.date(sy,sm,sd),datetime.date(ey,em,ed)))
	commission = cursor1.fetchall()
	if not (commission):
		commission = [{'booking_agent_id': booking_agent_id, 'total': 0, 'average': 0, 'amount': 0}]
	cursor1.close()
	
	try:
		cursor1 = conn.cursor();
		query = 'SELECT count(ticket_id) as maxi FROM ticket WHERE airline_name = %s and flight_num = %s group by flight_num '
		cursor1.execute(query, (airline, flight))
		res = cursor1.fetchall()
		num = int(res[0]['maxi'])
		cursor1.close()

		cursor1 = conn.cursor();
		query = 'SELECT seats FROM airplane, flight WHERE flight.airline_name = %s and flight.flight_num = %s and flight.airplane_id =airplane.airplane_id '
		cursor1.execute(query, (airline, flight))
		res = cursor1.fetchall()
		num1 = int(res[0]['seats'])
		cursor1.close()
	
		if num1 == num:
			print(996)
			cursor = conn.cursor();
			query = 'SELECT * FROM ba_flight WHERE booking_agent_id = %s and status = "upcoming" '
			cursor.execute(query, (booking_agent_id))
			data1 = cursor.fetchall()
			cursor.close()
			error = "flight full"
			return ender_template('bahome.html', email=email, posts=data1, success=error, commission = commission)
	except:
		print(996)
		cursor = conn.cursor();
		query = 'SELECT * FROM ba_flight WHERE booking_agent_id = %s and status = "upcoming" '
		cursor.execute(query, (booking_agent_id))
		data1 = cursor.fetchall()
		cursor.close()
		error = 'Invalid flight (use search to check flight) or no ticket'
		return render_template('bahome.html', email=email, posts=data1, error=error, commission = commission)


	if(ticket):
		query = 'INSERT INTO purchases VALUES(%s, %s, %s, %s)'
		cursor.execute(query, (ticket[0]["ticket_id"], cusemail, booking_agent_id, datetime.date.today()))
		conn.commit()
		error = "purchase success"
		session['email'] = email
		query = 'SELECT * FROM ba_flight WHERE booking_agent_id = %s and status = "upcoming" '
		cursor.execute(query, (booking_agent_id))
		data1 = cursor.fetchall()
		conn.commit()
		cursor.close()
		return render_template('bahome.html', email=email, posts=data1, success=error, commission = commission)
	else:
		cursor = conn.cursor();
		query = '''select max(ticket_id) as maxi
			from ticket'''
		cursor.execute(query)
		res = cursor.fetchall()
		num = int(res[0]['maxi']) + 1
		try:
			query = 'INSERT INTO ticket VALUES(%s, %s, %s)'
			cursor.execute(query, (num, airline, flight))
		except:
			query = 'SELECT * FROM ba_flight WHERE booking_agent_id = %s and status = "upcoming" '
			cursor.execute(query, (booking_agent_id))
			data1 = cursor.fetchall()
			cursor.close()
			error = 'Invalid flight (use search to check flight) or no ticket'
			return render_template('bahome.html', email=email, posts=data1, error=error, commission = commission)
		try:
			query = 'INSERT INTO purchases VALUES(%s, %s, %s, %s)'
			cursor.execute(query, (num, cusemail, booking_agent_id, datetime.date.today()))
		except:
			query = 'SELECT * FROM ba_flight WHERE booking_agent_id = %s and status = "upcoming" '
			cursor.execute(query, (booking_agent_id))
			data1 = cursor.fetchall()
			cursor.close()
			error = 'Invalid user'
			return render_template('bahome.html', email=email, posts=data1, error=error, commission = commission)
		error = "purchase success"
		#error = 'Invalid flight (use search to check flight) or no ticket'
		query = 'SELECT * FROM ba_flight WHERE booking_agent_id = %s and status = "upcoming" '
		cursor.execute(query, (booking_agent_id))
		data1 = cursor.fetchall()
		conn.commit()
		cursor.close()

		#error = 'Invalid flight (use search to check flight) or no ticket'
	
		return render_template('bahome.html', email=email, posts=data1, error=error, commission = commission)
	

	return render_template('bahome.html', email=email, posts=data1, result = result, commission = commission)

@app.route('/commission', methods=['GET', 'POST'])
def commission():
	booking_agent_id = session['booking_agent_id']
	email = session['email']
	start = request.form['start']
	end = request.form['end']

	sy = int(start[0:4])
	sm = int(start[5:7])
	sd = int(start[8:10])
	
	ey = int(end[0:4])
	em = int(end[5:7])
	ed = int(end[8:10])

	cursor1 = conn.cursor();
	query = '''select ba_flight.booking_agent_id, sum(price)*0.1 as total, avg(price)*0.1 as average, count(price) as amount
		from ba_flight,flight, purchases
   		where ba_flight.flight_num = flight.flight_num 
  		 and ba_flight.airline_name = flight.airline_name
   		and ba_flight.ticket_id = purchases.ticket_id
		and purchases.booking_agent_id = %s
   		and purchases.purchase_date >= %s
   		and purchases.purchase_date < %s
   		group by booking_agent_id'''
	cursor1.execute(query, (booking_agent_id, datetime.date(sy,sm,sd),datetime.date(ey,em,ed)))
	commission = cursor1.fetchall()
	print(commission)
	if not (commission):
		commission = [{'booking_agent_id': booking_agent_id, 'total': 0, 'average': 0, 'amount': 0}]
	cursor1.close()

	cursor = conn.cursor();
	status = 'upcoming'
	query = 'SELECT * FROM ba_flight WHERE booking_agent_id = %s and status = %s'
	cursor.execute(query, (booking_agent_id,status))
	data1 = cursor.fetchall() 
	cursor.close()

	return render_template('bahome.html', email=email, posts=data1, result = [], commission = commission)

@app.route('/view_customers', methods=['GET', 'POST'])
def view_customers():
	email = session['email']
	booking_agent_id = session['booking_agent_id']

	year = datetime.datetime.now().year
	month = datetime.datetime.now().month
	month += 1
	if month > 12:
		month = 1
		year += 1
	sy = year
	sm = month
	month -= 6
	if month <= 0:
		month += 12
		year -= 1
	name = []
	amount = []
	cursor = conn.cursor();
	query = '''select customer_email, count(ticket_id) as amount
				from ba_flight
				where booking_agent_id = %s
				and purchase_date >= %s
				and purchase_date < %s
				group by customer_email
				order by amount desc
				limit 0,5 '''
	cursor.execute(query, (booking_agent_id, datetime.date(year,month,1),datetime.date(sy,sm,1)))
	data = cursor.fetchall()
	print(data)
	for i in data:
		name.append(i['customer_email'])
		amount.append(i['amount'])
	cursor.close()

	month -= 6
	if month <= 0:
		month += 12
		year -= 1
	name1 = []
	amount1 = []
	cursor = conn.cursor();
	query = '''select customer_email, count(ticket_id) as amount
				from ba_flight
				where booking_agent_id = %s
				and purchase_date >= %s
				and purchase_date < %s
				group by customer_email
				order by amount desc
				limit 0,5 '''
	cursor.execute(query, (booking_agent_id, datetime.date(year,month,1),datetime.date(sy,sm,1)))
	data = cursor.fetchall()
	print(data)
	for i in data:
		name1.append(i['customer_email'])
		amount1.append(i['amount'])
	cursor.close()
	print(amount1)
	session['email'] = email
	return render_template('view_customers.html', name = name, amount = amount, name1= name1, amount1 = amount1)

@app.route('/baback', methods=['GET', 'POST'])
def baback():
	email = session['email']
	session['email'] = email
	return redirect(url_for('bahome'))

@app.route('/balogout')
def balogout():
	session.pop('email')
	session.pop('booking_agent_id')
	return redirect('/')

############cus home design
@app.route('/cushome')
def cushome():
	email = session['email']
	cursor = conn.cursor();
	status = 'upcoming'
	query = 'SELECT * FROM view_flight WHERE customer_email = %s and status = %s '
	cursor.execute(query, (email,status))
	data1 = cursor.fetchall() 

	cursor = conn.cursor();
	status = 'upcoming'
	query = 'SELECT count(ticket_id) as count FROM view_flight WHERE customer_email = %s'
	cursor.execute(query, (email))
	count = cursor.fetchall() 
	#for each in data1:
		#print(each)
	num = int(count[0]['count'])
	cursor.close()
	yes = False
	if num >= 3 and num < 10:
		email = 'VIP Customer_' + email
		away = str(10 - num)
	elif num >= 10:
		email = 'Super VIP_' + email
	else:
		away = str(10 - num)
		yes = True
	return render_template('cushome.html', email=email, posts=data1, result = [], away = away, yes = yes)

@app.route('/cuslogout')
def cuslogout():
	session.pop('email')
	return redirect('/')

@app.route('/public_search', methods=['GET', 'POST'])
def public_search():
	cursor = conn.cursor();
	departure_city = request.form['departure_city']
	departure_airport = request.form['departure_airport']
	arrival_city = request.form['arrival_city']
	flight_num = request.form['flight_num']
	arrival_airport = request.form['arrival_airport']
	date = request.form['date']
	query = '''select *
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
	cursor.execute(query, (departure_city,departure_city,departure_airport,departure_airport,arrival_city,arrival_city,arrival_airport,arrival_airport,date,date,flight_num,flight_num))
	result = cursor.fetchall()
	cursor.close()
	return render_template('project_index.html', result=result)

@app.route('/search_flight', methods=['GET', 'POST'])
def search_flight():
    email = session['email']

    cursor = conn.cursor();
    status = 'upcoming'
    query = 'SELECT * FROM view_flight WHERE customer_email = %s and status = %s '
    cursor.execute(query, (email,status))
    data1 = cursor.fetchall() 
    cursor.close()
    
    cursor = conn.cursor();
    departure_city = request.form['departure_city']
   
    departure_airport = request.form['departure_airport']
    print(departure_city == "")
    arrival_city = request.form['arrival_city']
    arrival_airport = request.form['arrival_airport']
    date = request.form['date']
    
    query = '''select *
    from flight
    where status = "upcoming" and (flight_num,airline_name) in (
    SELECT flight_num, airline_name FROM flight_search
    WHERE departure_city = (case when %s = '' then departure_city else %s end)
    and departure_airport = (case when %s = '' then departure_airport else %s end)
    and arrival_city = (case when %s = '' then arrival_city else %s end)
    and arrival_airport = (case when %s = '' then arrival_airport else %s end)
    and date = (case when %s = '' then date else %s end))

    '''
    cursor.execute(query, (departure_city,departure_city,departure_airport,departure_airport,arrival_city,arrival_city,arrival_airport,arrival_airport,date,date))
    result = cursor.fetchall()
    for each in result:
        print(each)
    cursor.close()
    return render_template('cushome.html', email=email, posts=data1, result=result)

@app.route('/see_flight', methods=['GET', 'POST'])
def see_flight():
    email = session['email']
    cursor = conn.cursor();
    status = request.form['status']
    query = 'SELECT * FROM view_flight WHERE customer_email = %s and status = %s '
    cursor.execute(query, (email,status))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each)
    cursor.close()
    return render_template('cushome.html', email=email, posts=data1, result = [])

@app.route('/extra_search', methods=['GET', 'POST'])
def extr_search():
	email = session['email']
	dcity = request.form['departure_city']
	acity = request.form['arrival_city']
	start = request.form['startday']
	end = request.form['endday']

	sy = int(start[0:4])
	sm = int(start[5:7])
	sd = int(start[8:10])
	
	ey = int(end[0:4])
	em = int(end[5:7])
	ed = int(end[8:10])

	cursor = conn.cursor();
	#SELECT flight.flight_num as flight_num, flight.status as status, flight.airline_name as airline_name, departure_city, arrival_city, flight.departure_airport as departure_airport, flight.arrival_airport as arrival_airport
	#query = '''select distinct flight.flight_num as flight_num, flight.status as status, flight.airline_name as airline_name, departure_city, arrival_city, flight.departure_airport as departure_airport, flight.arrival_airport as arrival_airport, departure_time, arrival_time
	#FROM flight, airline_staff, flight_search
	#WHERE username = %s and airline_staff.airline_name = flight.airline_name and airline_staff.airline_name = flight_search.airline_name
	#and date >= %s
	#and date <= %s
	#and departure_city = %s
	#and arrival_city = %s'''
	query = '''select distinct *
	from view_flight
	where flight_num in (select distinct view_flight.flight_num
	from view_flight, flight_search
	where view_flight.flight_num = flight_search.flight_num
	and customer_email = %s 
	and date >= %s
	and date <= %s
	and departure_city = (case when %s = '' then departure_city else %s end)
	and arrival_city = (case when %s = '' then arrival_city else %s end))
	order by flight_num
	'''
	cursor.execute(query, (email, datetime.datetime(sy,sm,sd,0,0,0),datetime.datetime(ey,em,ed,0,0,0),dcity,dcity,acity,acity))
	extra = cursor.fetchall() 
	cursor.close()
	
	cursor = conn.cursor();
	status = 'upcoming'
	query = 'SELECT * FROM view_flight WHERE customer_email = %s and status = %s '
	cursor.execute(query, (email,status))
	data1 = cursor.fetchall()
	cursor.close()
	return render_template('cushome.html', email=email, extra = extra, posts=data1, result = [])

@app.route('/cuspurchase', methods=['GET', 'POST'])
def cuspurchase():
	email = session['email']
	cursor = conn.cursor();
	flight = request.form['flight']
	airline = request.form['airline']
	query = '''select ticket_id 
			from ticket
			where airline_name = %s and flight_num = %s
				and ticket_id not in (select ticket_id from purchases)'''
	cursor.execute(query, (airline, flight))
	ticket = cursor.fetchall()
	print(ticket)
	error = None
	cursor.close()

	try:
		cursor1 = conn.cursor();
		query = 'SELECT count(ticket_id) as maxi FROM ticket WHERE airline_name = %s and flight_num = %s group by flight_num '
		cursor1.execute(query, (airline, flight))
		res = cursor1.fetchall()
		num = int(res[0]['maxi'])
		cursor1.close()

		cursor1 = conn.cursor();
		query = 'SELECT seats FROM airplane, flight WHERE flight.airline_name = %s and flight.flight_num = %s and flight.airplane_id =airplane.airplane_id '
		cursor1.execute(query, (airline, flight))
		res = cursor1.fetchall()
		num1 = int(res[0]['seats'])
		cursor1.close()
	
		if num1 == num:
			print(996)
			cursor = conn.cursor();
			query = 'SELECT * FROM view_flight WHERE customer_email = %s and status = "upcoming" '
			cursor.execute(query, (email))
			data1 = cursor.fetchall()
			cursor.close()
			error = "flight full"
			return ender_template('cushome.html', email=email, posts=data1, success=error, commission = commission)
	except:
		print(996)
		cursor = conn.cursor();
		query = 'SELECT * FROM view_flight WHERE customer_email = %s and status = "upcoming" '
		cursor.execute(query, (email))
		data1 = cursor.fetchall()
		cursor.close()
		error = 'Invalid flight (use search to check flight) or no ticket'
		return render_template('cushome.html', email=email, posts=data1, error=error, commission = commission)

	if(ticket):
		cursor = conn.cursor();
		query = 'INSERT INTO purchases VALUES(%s, %s, %s, %s)'
		cursor.execute(query, (ticket[0]["ticket_id"], email, 'null', datetime.date.today()))
		conn.commit()
		error = "purchase success"
		session['email'] = email
		query = 'SELECT * FROM view_flight WHERE customer_email = %s and status = "upcoming" '
		cursor.execute(query, (email))
		
		data1 = cursor.fetchall()
		conn.commit()
		cursor.close()
		return render_template('cushome.html',email=email, posts=data1, success=error)
	else:
		cursor = conn.cursor();
		query = '''select max(ticket_id) as maxi
			from ticket'''
		cursor.execute(query)
		res = cursor.fetchall()
		num = int(res[0]['maxi']) + 1
		cursor.close()
		

		try:
			cursor = conn.cursor();
			query = 'INSERT INTO ticket VALUES(%s, %s, %s)'
			cursor.execute(query, (num, airline, flight))
			conn.commit()
			cursor.close()
		except:
			cursor = conn.cursor();
			query = 'SELECT * FROM view_flight WHERE customer_email = %s and status = "upcoming" '
			cursor.execute(query, (email))
			data1 = cursor.fetchall()
			cursor.close()
			error = 'Invalid flight (use search to check flight) or no ticket'
			return render_template('bahome.html', email=email, posts=data1, error=error, commission = commission)
		cursor = conn.cursor();
		query = 'INSERT INTO purchases VALUES(%s, %s, %s, %s)'
		cursor.execute(query, (num, email, 'null', datetime.date.today()))
		print('success')
		conn.commit()
		cursor.close()
		cursor = conn.cursor();
		error = "purchase success"
		#error = 'Invalid flight (use search to check flight) or no ticket'
		query = 'SELECT * FROM view_flight WHERE customer_email = %s and status = "upcoming" '
		cursor.execute(query, (email))
		
		data1 = cursor.fetchall()
		conn.commit()
		cursor.close()
		return render_template('cushome.html',email = email, posts=data1, error=error)
	
	return redirect(url_for('cushome'))

@app.route('/cusspending', methods=['GET', 'POST'])
def cusspending():
	email = session['email']
	year = datetime.datetime.now().year
	month = datetime.datetime.now().month
	month += 1
	if month > 12:
		month = 1
		year += 1
	ym = []
	ym_1 = []
	for i in range(6):
		ym_1.append([year,month])
		month -= 1
		if month <= 0:
			year -= 1
			month += 12
		ym.append([year,month])
	print(ym)
	amount = []
	for j in range(len(ym)):
		cursor = conn.cursor();
		query = '''select view_flight.customer_email, sum(price) as total
					from view_flight, flight, purchases
					where view_flight.flight_num = flight.flight_num 
						and purchases.customer_email = %s
						and view_flight.airline_name = flight.airline_name
						and view_flight.ticket_id = purchases.ticket_id
						and purchases.purchase_date >= %s
						and purchases.purchase_date < %s
					group by customer_email '''
		cursor.execute(query, (email, datetime.date(ym[j][0],ym[j][1],1),datetime.date(ym_1[j][0],ym_1[j][1],1)))
		data = cursor.fetchall()
		if (data):
			amount.append(int(data[0]['total']))
		else:
			amount.append(0)
		cursor.close()
	total = sum(amount)
	print(amount)
	session['email'] = email
	return render_template('cusspending.html', ym = ym, amount = amount, total = total)

@app.route('/see_spending', methods=['GET', 'POST'])
def see_spending():
	email = session['email']
	start = request.form['start']
	end = request.form['end']
	sy = int(start[0:4])
	sm = int(start[5:7])
	sd = int(start[8:10])
	ey = int(end[0:4])
	em = int(end[5:7])
	ed = int(end[8:10])

	cursor = conn.cursor();
	query = '''select view_flight.customer_email, sum(price) as total
					from view_flight, flight, purchases
					where view_flight.flight_num = flight.flight_num 
						and purchases.customer_email = %s
						and view_flight.airline_name = flight.airline_name
						and view_flight.ticket_id = purchases.ticket_id
						and purchases.purchase_date >= %s
						and purchases.purchase_date < %s
					group by customer_email '''
	cursor.execute(query, (email, datetime.date(sy,sm,sd),datetime.date(ey,em,ed)))
	data = cursor.fetchall()
	if (data):
		total = int(data[0]['total'])
	else:
		total = 0
	cursor.close()

	em += 1
	if em > 12:
		em = 1
		ey += 1
	ym = []
	ym_1 = []
	while (em != sm) and (ey != em):
		ym.append([sy,sm])
		sm += 1
		if sm >= 13:
			sy += 1
			sm = 1
		ym_1.append([sy,sm])
	print(ym)
	amount = []
	for j in range(len(ym)):
		cursor = conn.cursor();
		query = '''select view_flight.customer_email, sum(price) as total
					from view_flight, flight, purchases
					where view_flight.flight_num = flight.flight_num 
						and purchases.customer_email = %s
						and view_flight.airline_name = flight.airline_name
						and view_flight.ticket_id = purchases.ticket_id
						and purchases.purchase_date >= %s
						and purchases.purchase_date < %s
					group by customer_email '''
		cursor.execute(query, (email, datetime.date(ym[j][0],ym[j][1],1),datetime.date(ym_1[j][0],ym_1[j][1],1)))
		data = cursor.fetchall()
		print(data)
		if (data):
			amount.append(int(data[0]['total']))
		else:
			amount.append(0)
		cursor.close()
	print(amount)
	total = sum(amount)
	session['email'] = email
	return render_template('cusspending.html', ym = ym, amount = amount, total = total)

@app.route('/cusback', methods=['GET', 'POST'])
def cusback():
	email = session['email']
	session['email'] = email
	return redirect(url_for('cushome'))




		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
