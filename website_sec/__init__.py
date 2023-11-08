from flask import Flask
from .socketio_functions import socketio_functions

def create_app():
    app = Flask(__name__)

    # Import blueprints
    from .views import views
    from .auth  import auth
    from .database import setup_database
    
    from .databaseChat import setup_databaseChat
    from .databaseMessages import setup_databaseMessages

    setup_database()
    setup_databaseChat()
    setup_databaseMessages()
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth,  url_prefix='/')
    app.register_blueprint(socketio_functions, url_prefix='/')

    return app