from flask import Blueprint, jsonify, request
import resend
import os
from dotenv import load_dotenv

contact_bp = Blueprint("contacto", __name__)

load_dotenv()
resend.api_key = os.getenv('RESEND_API_KEY')

@contact_bp.route("/api/contacto", methods=['POST'])
def contact():
  data = request.get_json()
  
  if not data or 'name' not in data or 'email' not in data or 'message' not in data:
    return jsonify({"error": "Faltan datos obligatorios"}), 400
  
  try:
    resend.Emails.send({
      "from": "onboarding@resend.dev",
      "to": "escalasnavarro@gmail.com",
      "subject": "Nuevo mensaje desde PadelBook",
      "html": f"""
        <h3>Nuevo mensaje</h3>
        <p><strong>Nombre:</strong> {data["name"]}</p>
        <p><strong>Email:</strong> {data["email"]}</p>
        <p><strong>Mensaje:</strong> {data["message"]}</p>
      """
    })
    
    return jsonify({"message": "Mensaje enviado"}), 200
  
  except Exception as e:
        return jsonify({"error": str(e)}), 500