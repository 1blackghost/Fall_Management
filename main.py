from flask import *

app=Flask(__name__)
app.config['SECRET_KEY']="thisisasecretkey"

@app.route("/logout")
def logout():
	if 'user' in session and 'role' in session:
		session.pop('user',None)
		session.pop('role',None) 
		return redirect(url_for('home'))
@app.route('/home',methods=['GET','POST'])
def root():
	if 'user' in session and 'role' in session:
		if session['step']=="False":
			if request.method=='POST':
				history=request.form['history']
				medicines=request.form['medicines']
				doctor=request.form["doctor"]
				r1=request.form['r1']
				r2=request.form['r2']
				with open("add.txt",'r') as f:
					d=eval(f.read())
				main=[]
				main.append(session['user'])
				main.append(history)
				main.append(medicines)
				main.append(doctor)
				main.append(r1)
				main.append(r2)
				d.append(main)
				with open("add.txt",'w') as f:
					f.write(str(d))
				with open("data.txt",'r') as f:
					d=eval(f.read())
				for i in d:
					if i[0]==session['user']:
						i[5]="True"
				with open('data.txt','w') as f:
					f.write(str(d))
				session['step']="True"
				return redirect(url_for('root'))

			return render_template('step2.html')
		
		if session['role']=="Ambulance Driver":
			with open("data.txt",'r') as f:
				d=eval(f.read())
			for i in d:
				if i[0]==session['user']:
					try:
						param=i[4]
						param=param.split(":")
						lat=param[4]
						lng=param[6]
					except:
						return render_template("ambulance.html",username=session['user'],error="Oops! Maps Could Not Be Loaded With Location Off!")

			if request.method=="POST":
				return render_template('map.html',lat=lat,lng=lng,name="Your Location: ",error="")
			return render_template("ambulance.html",username=session['user'])
		with open("add.txt",'r') as f:
			d=eval(f.read())
		for i in d:
			if i[0]==session['user']:
				history=i[1]
				medicines=i[2]
				doctor=i[3]
				r1=i[4]
				r2=i[5]
		return render_template('root.html',username=session['user'],history=history,medicines=medicines,doctor=doctor,r1=r1,r2=r2)
	else:
		return redirect(url_for('login'))
@app.errorhandler(404)
def page_not_found(e):
	print(e)
	return render_template('404.html')
@app.route("/")
def home():
	return render_template("home.html")
@app.route("/signup",methods=["GET","POST"])
def signup():
	if request.method=="POST":
		username=request.form['name']
		email=request.form['email']
		password=request.form['password']
		conf_password=request.form['conf']
		loc=request.form["demo"]
		print(password,conf_password)
		error="Something went wrong!"

		try:
			role=request.form['options']
		except:
			return render_template("signup.html",error=error)
		if username=="":
			return render_template("signup.html",error=error)
		if password=="":
			return render_template("signup.html",error=error)
		if email=="":
			return render_template("signup.html",error=error)
		if conf_password=="":
			return render_template("signup.html",error=error)
		if role=="":
			return render_template("signup.html",error="Role Error")
		if str(password)!=str(conf_password):
			return render_template("signup.html",error="Passwords Don't Match!")
		data_list=[]
		data_list.append(username)
		data_list.append(email)
		data_list.append(password)
		data_list.append(role)
		data_list.append(loc)
		if role=="User":
			data_list.append("False")
		else:
			data_list.append("None")


		with open("data.txt",'r') as f:
			d=eval(f.read())
		d.append(data_list)
		with open('data.txt','w') as f:
			f.write(str(d))
		session['user']=str(username)
		session['role']=str(role)
		if role=="User":
			session['step']=str("False")
		else:
			session['step']=str("True")

		return redirect(url_for("root"))


	return render_template("signup.html")
@app.route("/login",methods=['GET','POST'])
def login():

	if request.method=="POST":
		username=request.form['name']
		password=request.form['password']
		loc=request.form["demo"]
		with open("data.txt","r") as f:
			d=eval(f.read())
		In=False
		for i in d:
			if i[0]==username or i[1]==username:
				if i[2]==password:
					session['user']=username
					session['role']=str(i[3])
					session['step']=i[5]
					In=True
					return redirect(url_for('root'))
		if not In:
			return render_template("login.html",error="No Match Or User Not Found!")

	return render_template("login.html")
if __name__=="__main__":
	app.run(debug=True)