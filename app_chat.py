from flask import Flask, render_template, request, redirect, current_app
from flask_sqlalchemy import SQLAlchemy
from form import ResistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
from flask_socketio import SocketIO, emit
import json


#setting up the app
app = Flask(__name__)

#configure security key for the app
app.config[ 'SECRET_KEY' ] = 'Thisisforchatserver!'
socketio = SocketIO( app )
#for SQLITE database setting the path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatHistory.db'
db=SQLAlchemy(app)


#Using Class from sqla1chemy to create table Chat in sqlite 
class Chat(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100))
	message = db.Column(db.String(500))
	date = db.Column(db.String(50))


db.create_all()
db.session.commit()


#routing to localhost:8000 after success on login screen 
@app.route( '/' )
def hello():
	#getting the cookie value from app.py
	value = request.cookies.get('cookie_name')
	#query table Chat from chathistory.db
	messages = Chat.query.all()
	# only works if user is logged in ie if cookie is store if not  it will redirect to localhost:8000 for login
	# blocking the user from going to chat screen without login in
	if value:
		return render_template( './app_chat.html', name=value, messages= messages)
	else:
		redirect_to_index = redirect("http://localhost:8000/")
		response = current_app.make_response(redirect_to_index )  
		return response

#to test if user is connected to server
def messageRecived():
  print( 'message was received!!!' )


#brotcasting the messsage recived from client side in json format
@socketio.on( 'my event' )
def handle_my_custom_event( json ):
	print( 'recived my event: ' + str( json ))
	chat_list=[]
	for i in json:
		chat_list.append(json[i])
	#storing each chat in the database
	if len(chat_list)>1:	
		#inserting all the chat history in chatdatabase
		chat_Storage=Chat(name=chat_list[0], message=chat_list[1], date=chat_list[2])
		db.session.add(chat_Storage)
		db.session.commit()
	print('----------------------------------')
	socketio.emit( 'my response', json, callback=messageRecived )

#calling the main funtion 
if __name__ == '__main__':
  socketio.run(app, debug=True, port=1111, host='0.0.0.0')