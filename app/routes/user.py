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

@user_bp.route('/perfil', methods=['PUT'])
def update_profile():
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()
  
  user_id = get_jwt_identity()
  user = User.query.get(user_id)
  
  if not user:
    return jsonify({"error": "No existe el usuario"})
  
  data = request.get_json()
  
  # comprovamos que no existe un usuario con el mismo email o username
  user_email = User.query.filter_by(email  = data.get("email")).first()
  user_username = User.query.filter_by(username = data.get("username")).first()
  if user_email or user_username:
    return jsonify({"error": "usuario ya registrado"}), 409
  
  user.username = data.get("username")
  user.email = data.get("email")
  user.password_hash = data.get("password_hash")
  user.mobile = data.get("mobile")
  user.address = data.get("address")
  user.age = data.get("age")
  user.firstname = data.get("firstname")
  user.lastname = data.get("lastname")
  user.category = data.get("category")
  user.photo = data.get("photo")
  
  return jsonify({"message": "Perfil actualizado"})