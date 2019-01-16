from flask import Flask, render_template, flash, redirect, url_for, current_app
from flask_sqlalchemy import SQLAlchemy
from form import ResistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
#to render a templet we need a secret key
app.config['SECRET_KEY'] = 'ThisissecreteKey!'
#for SQLITE database setting the path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db=SQLAlchemy(app)
#using login_mnamager from Login_form for validation  of the form
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
socketio = SocketIO(app)

#creating a user table in database.db
class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50))
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(80))

#geting login data from user
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

db.create_all()
db.session.commit()


#creating a route after loging so it redirect to chathomepage
@app.route('/chat')
@login_required
def hello():
    redirect_to_index = redirect("http://localhost:1111/")
    response = current_app.make_response(redirect_to_index )  
    response.set_cookie('cookie_name', current_user.username)
    return response



#creating a route for home or login screen 
@app.route('/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	#validating form  on submit button
	if form.validate_on_submit():
		# query from database and using it on login page
		user_info = User.query.filter_by(email=form.email.data).first()
		if user_info:
			#mathing the password from user input and hassed password
			if check_password_hash(user_info.password, form.password.data):
				login_user(user_info, remember=form.remember.data)
				#return '<h1>' + form.email.data + ' ' + form.password.data + '</h1>'
				flash(f'Account created for {user_info.username}!', 'success')
				return redirect(url_for('hello'))
			else:
				return '<h1>' + 'invalid email or password' + '<h1>'
		else:
			return '<h1>' + 'invalid email or password' + '<h1>'
	#or else it will render the registration page	
			#flash('Login Unsuccesful. Please check username and password', 'danger')
	return render_template('login.html', title='Register', form=form)


# creating a route for resistration page
@app.route('/resistrationpage', methods=['GET', 'POST'])
def resistration():
	form = ResistrationForm()
	#validate on submit
	if form.validate_on_submit():
		#storing into database
		#hasing password
		hashed_password = generate_password_hash(form.password.data, method='sha256')
		#updating to User table 
		new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(new_user)
		db.session.commit()

		#return '<h1>' + form.email.data + ' ' + form.password.data + '</h1>'

		flash(f'Account created for {form.username.data}!', 'success')
		return redirect(url_for('login'))
	return render_template('resistration.html', title='Register', form=form)

#calling the main function
if __name__ == "__main__":
	socketio.run(app, debug=True, port=8000, host='0.0.0.0')