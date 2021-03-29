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

class DeviceModel(db.Model):
    '''
    기기 모델 Table
    ext: 내선번호
    name: 기기모델명
    ip: 기기 IP주소
    mac: 기기 MAC주소
    '''
    id = db.Column(db.Integer, primary_key=True)
    ext = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=True)
    ip = db.Column(db.String(28), unique=True, nullable=True)
    mac = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"Device(ext = {ext}, name = {name}, ip = {ip}, mac = {mac})"

class CallLogModel(db.Model):
    '''
    통화 로그 Table
    ext: 내선번호
    direct: 수신:1, 발신:0
    status: 통화상태 (0:종료, 1:연결, 2:벨울림, 3:부재중)
    '''
    id = db.Column(db.Integer, primary_key=True)
    ext = db.Column(db.String(20), nullable=True)
    direct = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"CallLog(ext = {ext}, direct = {direct}, status = {status}, ip = {ip}, mac = {mac})"

class IoLogModel(db.Model):
    '''
    출입 로그 Table
    ext: 내선번호
    direct: 출:0, 입:1
    '''
    id = db.Column(db.Interger, primary_key=True)
    ext = db.Column(db.String(20), nullable=True)
    direct = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"IoLog(ext = {ext}, direct = {direct}, ip = {ip}, mac = {mac})"

class DeviceLogModel(db.Model):
    '''
    기기 상태 로그 Table
    ext: 내선번호
    status: 기기 상태 (0:)
    '''
    id = db.Column(db.Interger, primary_key=True)
    ext = db.Column(db.String(20), nullable=True)
    status = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"DeviceLog(ext = {ext}, direct = {direct}, ip = {ip}, mac = {mac})"


# Register
class Register(Resource):
    def get(self, ext,  ip, model):
        print('mac: {0}, ip: {1}, model: {2}'.format(mac, ip, model))
        return mac

# Call is made
class Call(Resource):
    def get(self, ext):
        print('mac: {0}, ip: {1}, model: {2}'.format(mac, ip, model))
        return mac

# Device Status changed ( Setup Completed, DND On/Off, Mute On/Off,  )
class Device(Resource):
    def get(self, mac, ip, model):
        print('mac: {0}, ip: {1}, model: {2}'.format(mac, ip, model))
        return mac



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

api.add_resource(Reg0, '/reg0/<string:mac>&<string:ip>&<string:model>')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80)