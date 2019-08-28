from flask import Flask, render_template, request, redirect,url_for, session
import psycopg2, json

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
con = psycopg2.connect("dbname='airlines' user='postgres' host='localhost' password=''")
cur=con.cursor()
cur.execute("SELECT iata_code,name,location from airports ")
airports=cur.fetchall()


@app.route('/',methods = ['POST', 'GET'])
@app.route('/aviair/home',methods = ['POST', 'GET'])
def home():
	if request.method=="POST":
		return redirect(url_for('searchFlights',data=request.form))
	else:
		return render_template('home.html',home='active',airports=airports)


@app.route('/aviair/search',methods = ['POST', 'GET'])
def searchFlights():
	print(request.args['data'])
	return render_template('tickets.html',)


@app.route('/aviair/contact',methods = ['POST', 'GET'])
def contact():
	return render_template('contact.html',contact='active')


@app.route('/aviair/register',methods = ['POST', 'GET'])
@app.route('/aviair/login',methods = ['POST', 'GET'])
def login():
	con = psycopg2.connect("dbname='airlines' user='postgres' host='localhost' password='Saurabh@12'")
	cur=con.cursor()
	cur.execute("SELECT u_name FROM users")
	usernames=cur.fetchall()
	usernames=[u[0] for u in usernames]
	if request.method=="POST":
		if 'login' in request.form:
			uname=request.form['username']
			password=request.form['password']
			cur.execute("SELECT * FROM (SELECT u_name, name, wallet FROM users WHERE u_name='"+uname+"' AND password=crypt('"+password+"',password)) AS s NATURAL JOIN regusers;")
			data=cur.fetchone()
			con.commit()
			cur.close()
			con.close()
			print(data)
			if data:
				return render_template('home.html',home='active',airports=airports,userdata=data)
			else:
				return render_template('login.html',login='active',usernames=usernames)
		
		elif 'register' in request.form:
			uname=request.form['username']
			fname=request.form['fullname']
			email=request.form['email']
			password=request.form['password']
			print(request.form)
			cur.execute("INSERT INTO Users(u_name,name,password,email) VALUES('"+uname+"','"+fname+"',crypt('"+password+"',gen_salt('bf')),'"+email+"');")
			con.commit()
			cur.close()
			con.close()
			return render_template('login.html',login='active',usernames=usernames)
	con.commit()
	cur.close()
	con.close()
	return render_template('login.html',login='active',usernames=usernames)


@app.route('/aviair/logout',methods = ['POST', 'GET'])
def logout():
	return redirect(url_for('home'))


if __name__ == '__main__':
   app.run(debug=True)
