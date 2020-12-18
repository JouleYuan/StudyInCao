from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app, supports_credentials=True)
app.register_blueprint(routes, url_prefix='/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
