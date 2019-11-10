from flask import Flask, render_template, request, redirect,url_for, session,flash
from werkzeug.utils import secure_filename
import psycopg2, json, os


app = Flask(__name__,static_url_path='/static')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['UPLOAD_FOLDER'] ='static/media/profilepics'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

con = psycopg2.connect("dbname='airlines' user='postgres' host='localhost' password='Saurabh@12'")
cur=con.cursor()
cur.execute("SELECT iata_code,name,location from airports ")
airports=cur.fetchall()


@app.route('/',methods = ['POST', 'GET'])
@app.route('/aviair/home',methods = ['POST', 'GET'])
def home():
	if "username" in session:
		data=[session["username"],session["fullname"],session["wallet"],session["vcoins"]]
		return render_template('home.html',home='active-link',airports=airports,userdata=data)
	else:
		return render_template('home.html',home='active-link',airports=airports)


@app.route('/aviair/contact',methods = ['POST', 'GET'])
def contact():
	if "username" in session:
		data=[session["username"],session["fullname"],session["wallet"],session["vcoins"]]
		return render_template('contact.html',contact='active-link',userdata=data)
	return render_template('contact.html',contact='active-link')

@app.route('/aviair/profile',methods = ['POST', 'GET'])
def profile():
	if "username" in session:
		cur.execute("SELECT u_name,name,email,wallet,phone,address,city,state,country,profilepic from Users where u_name=%s;",(session["username"],))
		userdata=cur.fetchone()
		cur.execute("SELECT pnr,from_airport,to_airport,date_,transaction_amount,flight_id,transaction_id,arr_time,dept_time,adults,children,status FROM (SELECT * FROM Bookings where u_name=%s) B JOIN Flights F ON B.f_id=F.id ORDER BY date_ DESC;",(session["username"],))
		book=cur.fetchall()
		print(book)
		return render_template('profile.html',profile='active-link',userdata=userdata,bookingdetails=book)
	else:
		flash('Please login to continue.. ','info')
		return redirect(url_for('login'))


@app.route('/aviair/update-profile/<username>',methods = ['POST'])
def UpdateProfile(username):
	if request.form['password']:		
		cur.execute("UPDATE Users SET name=%s,password=crypt(%s,gen_salt('bf')),email=%s,phone=%s,address=%s,city=%s,state=%s,country=%s WHERE u_name=%s;",(request.form['fname'],request.form['password'],request.form['email'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['country'],username,))
		con.commit()
	else:
		cur.execute("UPDATE Users SET name=%s,email=%s,phone=%s,address=%s,city=%s,state=%s,country=%s WHERE u_name=%s;",(request.form['fname'],request.form['email'],request.form['phone'],request.form['address'],request.form['city'],request.form['state'],request.form['country'],username,))
		con.commit()
	return redirect(url_for('profile'))


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadprofilepic/<name>', methods=['POST'])
def uploadProfilePic(name):
	file = request.files['profile-filename']
	if allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		cur.execute("UPDATE Users SET profilepic=%s WHERE u_name=%s;",(filename,name,))
		return redirect(url_for('profile'))


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
				return render_template('login.html',login='active-link')
		
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
			return render_template('login.html',login='active-link')
	#con.commit()
	#cur.close()
	#con.close()
	return render_template('login.html',login='active-link')


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
	print(request.form)
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
