from flask import Blueprint, jsonify

recetas_bp = Blueprint('recetas', __name__)

@recetas_bp.route('/recetas')
def recetas():
    return jsonify({
        "patient_id": "P123456",
        "prescriptions": [
            {"date": "2024-03-01", "medication": "Ibuprofeno 600mg", "duration": "7 días", "instructions": "Cada 8 horas tras las comidas"},
            {"date": "2023-12-01", "medication": "Paracetamol 1g", "duration": "5 días", "instructions": "Cada 6 horas si fiebre"}
        ]
    })