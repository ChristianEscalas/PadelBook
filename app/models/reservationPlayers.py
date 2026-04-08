from app import db
from app.enums import Team

# Modelo que representa la reserva de un jugador
class ReservationPlayer(db.Model):
  __tablename__ = "reservation_players"
  
  user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "RESTRICT"), primary_key = True)
  reservation_id = db.Column(db.Integer, db.ForeignKey("reservations.id", ondelete = "RESTRICT"), primary_key = True)
  team = db.Column(db.Enum(Team), nullable = False)
  is_creator = db.Column(db.Boolean, default = False, nullable = False)
  
  # Relación
  user = db.relationship("User", back_populates="player_reservations")
  reservation = db.relationship("Reservation", back_populates="players")