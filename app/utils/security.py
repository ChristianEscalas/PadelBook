from werkzeug.security import generate_password_hash, check_password_hash

# Genera el hash de la contraseña
def new_password_hash(password: str) -> str:
  return generate_password_hash(password)

# Comprueba la contraseña con el hash
def check_password(password: str, password_hash: str) -> bool:
  return check_password_hash(password_hash, password)