from app import db
from app.enums import StatusGame, WinnerTeam

# Modelo que representa una reserva
class Reservation(db.Model):
  __tablename__ = "reservations"
  
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  court_id = db.Column(db.Integer, db.ForeignKey("courts.id", ondelete = "RESTRICT"), nullable = False)
  creator_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "RESTRICT"), nullable = False)
  start_date = db.Column(db.DateTime, nullable = False)
  end_date = db.Column(db.DateTime, nullable = False)
  status_game = db.Column(db.Enum(StatusGame), default = StatusGame.open, nullable = False)
  result = db.Column(db.String(20), nullable = True)
  closed_at = db.Column(db.DateTime, nullable = True)
  winner_team = db.Column(db.Enum(WinnerTeam), nullable = True)
  confirmed_by_creator = db.Column(db.Boolean, default=False)
  confirmed_by_team_b = db.Column(db.Boolean, default=False)
  
  # Restricción
  __table_args__ = (db.UniqueConstraint("court_id", "start_date", name = "court_id"),)
  
  # Relación
  court = db.relationship("Court", back_populates = "reservations")
  creator_user = db.relationship("User", back_populates = "reservations")
  players = db.relationship("ReservationPlayer", back_populates="reservation")
  points_movements = db.relationship("PointMovement", back_populates = "reservation")