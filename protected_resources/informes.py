from flask import Blueprint, jsonify

informes_bp = Blueprint('informes', __name__)

@informes_bp.route('/informes')
def informes():
    return jsonify({
        "patient_id": "P123456",
        "reports": [
            {"date": "2024-02-20", "type": "Radiografía", "result": "Sin fracturas ni anomalías"},
            {"date": "2023-11-10", "type": "Análisis de sangre", "result": "Valores dentro de la normalidad"}
        ]
    })