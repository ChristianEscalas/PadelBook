from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect
import os

# Carga de variables de entorno
from dotenv import load_dotenv
load_dotenv()

# Instancia y configuración de la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Instancia de protección CSRF
csrf = CSRFProtect(app)

# Configuración y conexión a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Importación y registro de blueprints
from app.routes.auth import auth_bp
from app.routes.contact import contact_bp
from app.routes.views import views_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(contact_bp)
app.register_blueprint(views_bp)

csrf.exempt(auth_bp)
csrf.exempt(contact_bp)

# Importación de los orm
from app.models.users import User
from app.models.clubs import Club
from app.models.courts import Court
from app.models.reservations import Reservation
from app.models.followers import Follower
from app.models.pointsMovements import PointMovement
from app.models.reservationPlayers import ReservationPlayer