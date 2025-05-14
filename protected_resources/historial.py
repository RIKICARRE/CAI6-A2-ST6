from flask import Blueprint, jsonify

historial_bp = Blueprint('historial', __name__)

@historial_bp.route('/historial')
def historial():
    return jsonify({
        "patient_id": "P123456",
        "history": [
            {"date": "2023-12-01", "diagnosis": "Gripe", "treatment": "Reposo y paracetamol"},
            {"date": "2022-07-15", "diagnosis": "Fractura de radio", "treatment": "Escayola 6 semanas"}
        ]
    })