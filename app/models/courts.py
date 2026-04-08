from app import db
from app.enums import CourtType, WallType, SurfaceType

# Modelo que representa una pista
class Court(db.Model):
  __tablename__ = "courts"
  
  id = db.Column(db.Integer, primary_key = True, autoincrement = True)
  club_id = db.Column(db.Integer, db.ForeignKey("clubs.id", ondelete = "CASCADE"), nullable = False)
  number_court = db.Column(db.Integer, nullable = False)
  court_type = db.Column(db.Enum(CourtType), default = CourtType.double, nullable = False)
  covered = db.Column(db.Boolean, default = False, nullable = False)
  wall = db.Column(db.Enum(WallType), default = WallType.glass, nullable = False)
  surface = db.Column(db.Enum(SurfaceType), default = SurfaceType.grass, nullable = False)
  active = db.Column(db.Boolean, nullable = True, default = True)
  
  # Restricción
  __table_args__ = (db.UniqueConstraint("club_id", "number_court", name = "unique_court_per_club"),)
  
  # Relación
  club = db.relationship("Club", back_populates = "courts")
  reservations = db.relationship("Reservation", back_populates = "court")