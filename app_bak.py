from flask import Flask, render_template, request
from flask_restful import Api, Resource, reqparse
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secretkey'
# app.config['DEBUG'] = True
api = Api(app)
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	views = db.Column(db.Integer, nullable=False)
	likes = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Video(name = {name}, views = {views}, likes = {likes})"


users = []

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def connect():
    print('SessionID "{}" is connected.'.format(request.sid))

@socketio.on('disconnect')
def disconnect():
    print('SessionID "{}" is disconnected.'.format(request.sid))

@socketio.on('message')
def receive_message(message):
    message = 'USER({}) MESSAGE: {}'.format(request.sid, message)
    print(message)
    # emit('result', message, namespace='/msg')
    send(message)

@socketio.on('chat message')
def receive_chat_message(message):
    print('chat message: {}'.format(message))


if __name__ == '__main__':
    socketio.run(app)
