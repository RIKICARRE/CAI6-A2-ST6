from flask import Blueprint, jsonify

citas_bp = Blueprint('citas', __name__)

@citas_bp.route('/citas')
def citas():
    return jsonify({
        "patient_id": "P123456",
        "appointments": [
            {"date": "2024-04-10", "time": "09:30", "doctor": "Dra. García", "department": "Medicina General", "status": "confirmada"},
            {"date": "2024-05-22", "time": "11:00", "doctor": "Dr. López", "department": "Traumatología", "status": "pendiente"}
        ]
    })