from sqlalchemy import CheckConstraint
from app import db

# Modelo que representa un club
class Club(db.Model):
  __tablename__ = "clubs"
  
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  owner_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "RESTRICT"), nullable = False)
  club_name = db.Column(db.String(50), unique = True, nullable = False)
  address = db.Column(db.String(100), nullable = False)
  open_hour = db.Column(db.Time, nullable = False)
  close_hour = db.Column(db.Time, nullable = False)
  game_duration = db.Column(db.Integer, nullable = False, default = 60)
  municipality = db.Column(db.String(50), nullable = False)
  photo = db.Column(db.String(255), nullable = False)
  active = db.Column(db.Boolean, nullable = True, default = True)
  
  # Restricción
  __table_args__ = (CheckConstraint("game_duration IN (60, 90)", name = "check_game_duration"), db.UniqueConstraint("owner_id", "club_name", name = "owner_id"))
  
  # Relación
  user = db.relationship("User", back_populates = "clubs")
  courts = db.relationship("Court", back_populates = "club")