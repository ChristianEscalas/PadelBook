from sqlalchemy import func
from app import db

class Follower(db.Model):
  __tablename__ = "followers"
  
  following_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "CASCADE"), primary_key = True)
  follower_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete = "CASCADE"), primary_key = True)
  follow_date = db.Column(db.DateTime, nullable = False, server_default = func.now())
  
  # Relación
  followed_user = db.relationship("User", foreign_keys=[following_id], back_populates="followers")
  follower_user = db.relationship("User", foreign_keys=[follower_id], back_populates="following")