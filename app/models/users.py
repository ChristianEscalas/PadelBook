from app import db
from sqlalchemy import CheckConstraint, func
from app.enums import UserRole

# Modelo que representa un usuario
class User(db.Model):
  __tablename__ = "users"
  
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  username = db.Column(db.String(50), unique = True, nullable = False)
  email = db.Column(db.String(50), unique = True, nullable = False)
  password_hash = db.Column(db.String(255), nullable = False)
  mobile = db.Column(db.String(15), nullable = False)
  address = db.Column(db.String(100), nullable = True)
  age = db.Column(db.Integer, nullable = False)
  firstname = db.Column(db.String(50), nullable = False)
  lastname = db.Column(db.String(50), nullable = True)
  category = db.Column(db.Integer, nullable = False, default = 6)
  rol = db.Column(db.Enum(UserRole), nullable = False, default = UserRole.player)
  points = db.Column(db.Float, nullable = False, default = 0)
  created_at = db.Column(db.DateTime, nullable = False, server_default = func.now())
  photo = db.Column(db.String(255), nullable = False)
  
  # Restricción
  __table_args__ = (CheckConstraint("category IN (1,2,3,4,5,6)", name = "check_category"),)
  
  # Relación
  clubs = db.relationship("Club", back_populates = "user")
  reservations = db.relationship("Reservation", back_populates = "creator_user")
  player_reservations = db.relationship("ReservationPlayer", back_populates="user")
  points_movements = db.relationship("PointMovement", back_populates = "user")
  following = db.relationship("Follower", foreign_keys="Follower.follower_id", back_populates="follower_user")
  followers = db.relationship("Follower", foreign_keys="Follower.following_id", back_populates="followed_user")