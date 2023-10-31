from website import create_app
from flask_session import Session
from datetime import timedelta

app = create_app() # create_app() in __init__.py
app.config['SECRET_KEY'] = b'*51_.2S7H2F\n\xec]/'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)

Session(app)

if __name__ == "__main__":
    app.run(debug=True)