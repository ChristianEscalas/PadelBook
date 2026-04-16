from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.models.users import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/perfil', methods=['POST'])
def get_profile():
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()
  
  user_id = get_jwt_identity()
  user = User.query.get(user_id)
  
  if not user:
    return jsonify({"error": "No existe el usuario"})
  
  return jsonify({
    "username": user.username,
    "email": user.email,
    "password_hash": user.password_hash,
    "mobile": user.mobile,
    "address": user.address,
    "age": user.age,
    "firstname": user.firstname,
    "lastname": user.lastname,
    "category": user.category,
    "photo": user.photo
  })