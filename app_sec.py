from website_sec import create_app
from flask_session import Session
from flask_socketio import SocketIO
from datetime import timedelta
from website.socketio_functions import message, connect, disconnect

app = create_app() # create_app() in __init__.py
app.config['SECRET_KEY'] = b'*51_.2S7H2F\n\xec]/'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)

Session(app)
socketio = SocketIO(app)

@socketio.on("disconnect")
def disconnect_io():
    disconnect()

@socketio.on("connect")
def connect_io(auth):
    connect(auth)

@socketio.on("message")
def handle_message(data):
    message(data)

if __name__ == "__main__":
    socketio.run(app, debug=True)