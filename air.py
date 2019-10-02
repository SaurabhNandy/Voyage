from flask import Flask, render_template, request, redirect,url_for, session,flash
import psycopg2, json

app = Flask(__name__,static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
con = psycopg2.connect("dbname='airlines' user='postgres' host='localhost' password='Saurabh@12'")
cur=con.cursor()
cur.execute("SELECT iata_code,name,location from airports ")
airports=cur.fetchall()


@app.route('/',methods = ['POST', 'GET'])
@app.route('/aviair/home',methods = ['POST', 'GET'])
def home():
	if "username" in session:
		data=[session["username"],session["fullname"],session["wallet"],session["vcoins"]]
		if request.method=="POST":
			return redirect(url_for('searchFlights',data=request.form))
		else:
			return render_template('home.html',home='active',airports=airports,userdata=data)
	else:
		if request.method=="POST":
			return redirect(url_for('searchFlights',data=request.form))
		else:
			return render_template('home.html',home='active',airports=airports)


@app.route('/aviair/contact',methods = ['POST', 'GET'])
def contact():
	return render_template('contact.html',contact='active')


@app.route('/aviair/profile',methods = ['POST', 'GET'])
def profile():
	if "username" in session:
		cur.execute("SELECT u_name,name,email,wallet,phone,address,city,state,country,profilepic from Users where u_name=%s;",(session["username"],))
		userdata=cur.fetchone()
		print(userdata)
		return render_template('profile.html',profile='active',userdata=userdata)
	else:
		flash('Please login to continue.. ','info')
		return redirect(url_for('login'))


@app.route('/aviair/register',methods = ['POST', 'GET'])
@app.route('/aviair/login',methods = ['POST', 'GET'])
def login():
	if "username" in session:
		data=[session["username"],session["fullname"],session["wallet"],session["vcoins"]]
		return redirect(url_for('home'))
	elif request.method=="POST":
		if 'login' in request.form:
			uname=request.form['username']
			password=request.form['password']
			cur.execute("SELECT * FROM (SELECT u_name, name, wallet FROM users WHERE u_name=%s AND password=crypt(%s,password)) AS s NATURAL JOIN regusers;",(uname,password,))
			data=cur.fetchone()
			#cur.close()
			#con.close()
			print(data)
			if data:
				session["username"]=data[0]
				session["fullname"]=data[1]
				session["wallet"]=data[2]
				session["vcoins"]=data[3]
				flash('Logged in successfully! Welcome '+session["fullname"],'success')
				return redirect(url_for('home'))
			else:
				flash('Invalid username or password. Please try again ','warning')
				return render_template('login.html',login='active')
		
		elif 'register' in request.form:
			uname=request.form['username']
			fname=request.form['fullname']
			email=request.form['email']
			password=request.form['password']
			print(request.form)
			cur.execute("INSERT INTO Users(u_name,name,password,email) VALUES(%s,%s,crypt(%s,gen_salt('bf')),%s);",(uname,fname,password,email,))
			con.commit()
			cur.execute("INSERT INTO regusers VALUES(%s,0);",(uname,))
			con.commit()
			#cur.close()
			#con.close()
			flash('Registration successful! Please login to continue','success')
			return render_template('login.html',login='active')
	#con.commit()
	#cur.close()
	#con.close()
	return render_template('login.html',login='active')


@app.route('/aviair/logout',methods = ['POST', 'GET'])
def logout():
	session.pop("username")
	session.pop("fullname")
	session.pop("wallet")
	session.pop("vcoins")
	flash('Logged out successfully','success')
	return redirect(url_for('home'))



@app.route('/aviair/search',methods = ['POST', 'GET'])
def searchFlights():
	print(request.args['data'])
	return render_template('tickets.html',)


@app.route('/aviair/getusernames',methods = ['POST', 'GET'])
def getUsernames():
	cur.execute("SELECT u_name FROM users")
	usernames=cur.fetchall()
	usernames=[u[0] for u in usernames]
	return json.dumps(usernames)


if __name__ == '__main__':
	app.secret_key = 'the random string'
	app.run(debug=True)
