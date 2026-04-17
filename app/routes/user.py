import os
import time

from werkzeug.security import generate_password_hash

from app import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.models.followers import Follower
from app.models.users import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/perfil', methods=['GET'])
def get_profile():
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()
  
  user_id = get_jwt_identity()
  user = User.query.get(user_id)
  
  if not user:
    return jsonify({"error": "No existe el usuario"}), 404
  
  return jsonify({
    "username": user.username,
    "email": user.email,
    "mobile": user.mobile,
    "address": user.address,
    "age": user.age,
    "firstname": user.firstname,
    "lastname": user.lastname,
    "category": user.category,
    "photo": user.photo,
    "rol": user.rol.value,
    "points": user.points
  })

@user_bp.route('/perfil', methods=['PUT'])
def update_profile():
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()
  
  user_id = get_jwt_identity()
  user = User.query.get(user_id)
  
  if not user:
    return jsonify({"error": "No existe el usuario"}), 404
  
  data = request.form
  photo = request.files.get("photo")
  
  # comprovamos que no existe un usuario con el mismo email o username que no sea el usuario logueado
  if data.get("email"):
    existing_email = User.query.filter(User.email == data.get("email"), User.id != user_id).first()

    if existing_email:
      return jsonify({"error": "Email ya en uso"}), 409

  if data.get("username"):
    existing_username = User.query.filter(User.username == data.get("username"), User.id != user_id).first()

    if existing_username:
      return jsonify({"error": "Username ya en uso"}), 409
  
  user.username = data.get("username", user.username)
  user.email = data.get("email", user.email)
  user.mobile = data.get("mobile", user.mobile)
  user.address = data.get("address", user.address)
  user.age = data.get("age", user.age)
  user.firstname = data.get("firstname", user.firstname)
  user.lastname = data.get("lastname", user.lastname)
  user.category = data.get("category", user.category)
  
  if photo and photo.filename:
    folder = "images/users"
    extension = photo.filename.split('.')[-1]
    
    username = data.get("username", user.username)
    filename = f"{username}_{int(time.time())}.{extension}"
    
    save_path = os.path.join('app', 'static', folder)
    
    if not os.path.exists(save_path):
      os.makedirs(save_path)

    file_path = os.path.join(save_path, filename)
    photo.save(file_path)
    
    user.photo = f"{folder}/{filename}"
  
  if data.get("password"):
    user.password_hash = generate_password_hash(data.get("password"))
    
  db.session.commit()

  return jsonify({"message": "Perfil actualizado"}), 200

@user_bp.route('/ranking', methods=['GET'])
def get_ranking():
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()
  
  category = request.args.get("category")
  query = User.query.filter(User.rol == "player")

  if category:
    query = query.filter(User.category == int(category))

  users = query.order_by(User.points.desc()).all()

  result = []
  for user in users:
    result.append({
      "id": user.id,
      "firstname": user.firstname,
      "photo": user.photo,
      "points": user.points
    })

  return jsonify(result), 200

@user_bp.route('/usuario/<int:id>', methods=['GET'])
def get_public_profile(id):
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()

  user = User.query.get(id)

  if not user:
    return jsonify({"error": "Usuario no encontrado"}), 404

  return jsonify({
    "id": user.id,
    "username": user.username,
    "mobile": user.mobile,
    "category": user.category,
    "firstname": user.firstname,
    "lastname": user.lastname,
    "points": user.points,
    "photo": user.photo,
  }), 200

@user_bp.route('/usuario/seguir/<int:id>', methods=['POST'])
def follow_user(id):
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()

  user_id = int(get_jwt_identity())
  
  user_to_follow = User.query.get(id)
  if not user_to_follow:
    return jsonify({"error": "El usuario que quieres seguir no existe"}), 404

  if user_id == id:
    return jsonify({"error": "No puedes seguirte a ti mismo"}), 400

  exists = Follower.query.filter_by(follower_id=user_id, following_id=id).first()

  if exists:
    return jsonify({"error": "Ya sigues a este usuario"}), 400

  follow = Follower(follower_id=user_id, following_id=id)
  db.session.add(follow)
  db.session.commit()

  return jsonify({"message": "Has empezado a seguir al usuario"}), 200

@user_bp.route('/usuario/dejar_de_seguir/<int:id>', methods=['DELETE'])
def unfollow_user(id):
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()

  user_id = get_jwt_identity()

  user_to_unfollow = User.query.get(id)
  if not user_to_unfollow:
    return jsonify({"error": "El usuario que quieres dejar de seguir no existe"}), 404
  
  follow = Follower.query.filter_by(follower_id=user_id, following_id=id).first()
  if not follow:
    return jsonify({"error": "No sigues a este usuario"}), 400

  db.session.delete(follow)
  db.session.commit()

  return jsonify({"message": "Has dejado de seguir al usuario"}), 200

@user_bp.route('/usuario/es_seguido/<int:id>', methods=['GET'])
def is_following(id):
  # comprobar si el usuario ha hecho login
  verify_jwt_in_request()

  user_id = get_jwt_identity()

  follow = Follower.query.filter_by(follower_id=user_id, following_id=id).first()

  return jsonify({
    "following": follow is not None
  }), 200