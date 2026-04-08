from sqlalchemy import func
from app import db
from app.enums import ReasonType

# Modelo que representa un movimiento de puntos
class PointMovement(db.Model):
  __tablename__ = "points_movements"
  
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "CASCADE"), nullable = False)
  reservation_id = db.Column(db.Integer, db.ForeignKey("reservations.id", ondelete = "RESTRICT"), nullable = False)
  reason = db.Column(db.Enum(ReasonType), nullable = False)
  delta = db.Column(db.Integer, nullable = False)
  created_at = db.Column(db.DateTime, nullable = False, server_default = func.now())
  
  # Restricción
  __table_args__ = (db.UniqueConstraint("user_id", "reservation_id", name = "user_id"),)
  
  # Relacion
  user = db.relationship("User", back_populates = "points_movements")
  reservation = db.relationship("Reservation", back_populates = "points_movements")