from flask import Flask, jsonify
from protected_resources.historial import historial_bp
from protected_resources.recetas import recetas_bp
from protected_resources.citas import citas_bp
from protected_resources.informes import informes_bp

app = Flask(__name__)

app.register_blueprint(historial_bp)
app.register_blueprint(recetas_bp)
app.register_blueprint(citas_bp)
app.register_blueprint(informes_bp)

@app.route('/resource')
def resource():
    # Recurso protegido (general)
    return jsonify({
        "patient_id": "P123456",
        "name": "John Doe",
        "age": 45,
        "medical_record": {
            "blood_type": "A+",
            "allergies": ["penicillin", "pollen"],
            "chronic_conditions": ["hypertension"],
            "current_medications": [
                {
                    "name": "Lisinopril",
                    "dosage": "10mg",
                    "frequency": "daily"
                }
            ],
            "last_visit": "2024-03-15",
            "vital_signs": {
                "blood_pressure": "120/80",
                "heart_rate": 72,
                "temperature": 36.6
            }
        },
        "lab_results": {
            "glucose": "95 mg/dL",
            "cholesterol": "180 mg/dL",
            "white_blood_cells": "7.5 K/uL"
        }
    })

if __name__ == '__main__':
    app.run(port=5001)