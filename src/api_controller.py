# Patient API Controller

from flask import Flask, jsonify, request
from flask_cors import CORS
from patient_db import PatientDB
from patient import Patient
from config import GENDERS, WARD_NUMBERS, ROOM_NUMBERS

class PatientAPIController:
    def __init__(self):
        self.app = Flask(__name__)
        self.patient_db = PatientDB()
        CORS(self.app)  # Enable CORS for all routes
        self.setup_routes()
        

    def setup_routes(self):

        # Sets up the routes for the API endpoints.

        self.app.route("/", methods=["GET"])(self.index)
        self.app.route("/patients", methods=["GET"])(self.get_patients)
        self.app.route("/patients/<id>", methods=["GET"])(self.get_patient)
        self.app.route("/patients", methods=["POST"])(self.create_patient)
        self.app.route("/patients/<id>", methods=["PUT"])(self.update_patient)
        self.app.route("/patients/<id>", methods=["DELETE"])(self.delete_patient)
        self.app.route("/patients/search", methods=["GET"])(
            self.search_patients_by_name
        )
        self.app.route("/patients/<id>/room", methods=["PUT"])(
            self.set_patient_room
        )
        self.app.route("/patients/<id>/checkout", methods=["PUT"])(
            self.checkout_patient_api
        )

    def index(self):
        """
        Provides a welcome message for the root endpoint.
        """
        return jsonify({"message": "Welcome to the Patient API!"}), 200

    def get_patients(self):
        """
        Retrieves a list of all patients.
        """
        patients = self.patient_db.select_all_patients()
        return jsonify(patients), 200

    def get_patient(self, id):
        """
        Retrieves a single patient by their ID.
        """
        patient = self.patient_db.select_patient(id)
        if patient:
            return jsonify(patient), 200
        else:
            return jsonify({"message": "Patient not found"}), 404

    def create_patient(self):
        """
        Creates a new patient.
        Expects a JSON body with 'name', 'gender', and 'age'.
        """
        request_body = request.get_json()
        if not request_body:
            return jsonify({"message": "Request body cannot be empty"}), 400

        required_fields = ["name", "gender", "age"]
        if not all(key in request_body for key in required_fields):
            return (
                jsonify(
                    {"message": f"Missing required fields: {', '.join(required_fields)}"}
                ),
                400,
            )

        name = request_body["name"]
        gender = request_body["gender"]
        age = request_body["age"]

        # --- Enhanced Validation ---
        if not isinstance(name, str) or not name.strip():
            return jsonify({"message": "Name must be a non-empty string"}), 400

        if gender not in GENDERS:
            return (
                jsonify(
                    {
                        "message": f"Invalid gender provided. Must be one of: {', '.join(GENDERS)}"
                    }
                ),
                400,
            )

        if not isinstance(age, int) or age <= 0:
            return jsonify({"message": "Age must be a positive integer"}), 400
        # --- End of Validation ---
        
        ward = request_body.get("ward")
        room = request_body.get("room")

        # Optional validation for ward and room if they are provided
        if ward is not None and room is not None:
            if ward not in WARD_NUMBERS or str(room) not in ROOM_NUMBERS.get(ward, []):
                return jsonify({"message": "Invalid ward or room number"}), 400
        elif ward is not None or room is not None:
            return jsonify({"message": "Both ward and room must be provided together"}), 400


        new_patient = Patient(name=name, gender=gender, age=age, ward=ward, room=room)
        patient_data = new_patient.to_dict()

        # Insert the patient data into the database
        result = self.patient_db.insert_patient(patient_data)

        if result:
            # Return the created patient object for better API practice
            return jsonify(patient_data), 201
        else:
            return jsonify({"message": "Failed to create patient"}), 500

    def update_patient(self, id):
        """
        Updates an existing patient.
        Expects a JSON body with fields to update (e.g., 'name', 'age', 'gender').
        """
        update_data = request.get_json()
        if not update_data:
            return jsonify({"message": "Request body cannot be empty"}), 400

        # --- Enhanced Validation ---
        if "name" in update_data and (
            not isinstance(update_data["name"], str) or not update_data["name"].strip()
        ):
            return jsonify({"message": "Name must be a non-empty string"}), 400

        if "gender" in update_data and update_data["gender"] not in GENDERS:
            return (
                jsonify(
                    {
                        "message": f"Invalid gender provided. Must be one of: {', '.join(GENDERS)}"
                    }
                ),
                400,
            )

        if "age" in update_data and (
            not isinstance(update_data["age"], int) or update_data["age"] <= 0
        ):
            return jsonify({"message": "Age must be a positive integer"}), 400
        # --- End of Validation ---

        allowed_updates = {
            k: v for k, v in update_data.items() if k in ["name", "age", "gender", "room", "ward"]
        }

        if not allowed_updates:
            return jsonify({"message": "No valid fields provided for update"}), 400

        rows_affected = self.patient_db.update_patient(id, allowed_updates)

        if rows_affected is not None and rows_affected > 0:
            # Fetch and return the updated patient object
            updated_patient = self.patient_db.select_patient(id)
            return jsonify(updated_patient), 200
        elif rows_affected == 0:
            # Check if patient exists to give a more accurate message
            if self.patient_db.select_patient(id):
                return jsonify({"message": "Patient data is the same, no update performed"}), 200
            else:
                return jsonify({"message": "Patient not found"}), 404
        else:
            return jsonify({"message": "Error updating patient"}), 500

    def delete_patient(self, id):
        try:
            rows_affected = self.patient_db.delete_patient(id)
            if rows_affected is not None and rows_affected > 0:
                return jsonify({"message": "Patient deleted successfully"}), 200
            else:
                return jsonify({"message": "Patient not found"}), 404
        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500

    def search_patients_by_name(self):
        """
        Searches for patients by name.
        """
        name = request.args.get("search_name")
        if not name:
            return jsonify({"message": "search_name parameter is required"}), 400

        patients = self.patient_db.search_patients_by_name(name)
        if patients:
            return jsonify(patients), 200
        else:
            return jsonify({"message": "No patients found with that name"}), 404

    def set_patient_room(self, id):
        """
        Assigns a patient to a ward and room.
        Expects a JSON body with 'ward' and 'room'.
        """
        request_body = request.get_json()
        if not request_body or not all(key in request_body for key in ["ward", "room"]):
            return (
                jsonify({"message": "Missing required fields: ward, room"}),
                400,
            )

        ward = request_body["ward"]
        room = request_body["room"]

        # Validate ward and room numbers based on config
        if ward not in WARD_NUMBERS or str(room) not in ROOM_NUMBERS.get(ward, []):
            return jsonify({"message": "Invalid ward or room number"}), 400

        update_data = {"ward": ward, "room": room}
        rows_affected = self.patient_db.update_patient(id, update_data)

        if rows_affected is not None and rows_affected > 0:
            updated_patient = self.patient_db.select_patient(id)
            return jsonify(updated_patient), 200
        elif rows_affected == 0:
            # Check if patient exists to give a more accurate message
            if self.patient_db.select_patient(id):
                return jsonify({"message": "Patient room is the same, no update performed"}), 200
            else:
                return jsonify({"message": "Patient not found"}), 404
        else:
            return jsonify({"message": "Error updating patient's room"}), 500

    def checkout_patient_api(self, id):
        """
        Sets the checkout time for a patient.
        """
        patient_data = self.patient_db.select_patient(id)
        if not patient_data:
            return jsonify({"message": "Patient not found"}), 404

        # Create a Patient object to use its checkout_patient method
        # Note: This re-initializes the patient, but we only need the method
        # A more robust solution might involve a dedicated DB method for checkout
        patient_obj = Patient(
            name=patient_data["name"],
            age=patient_data["age"],
            gender=patient_data["gender"],
            ward=patient_data["ward"],
            room=patient_data["room"]
        )
        patient_obj.checkout_patient() # This updates the object's checkout time

        rows_affected = self.patient_db.update_patient(id, {"checkout": patient_obj.checkout})
        if rows_affected is not None and rows_affected > 0:
            return jsonify({"message": "Patient checked out successfully", "checkout_time": patient_obj.checkout}), 200
        return jsonify({"message": "Failed to checkout patient"}), 500
    def run(self):
        """
        Runs the Flask application.
        """
        # WARNING: debug=True is not suitable for production environments.
        # In a production deployment, this should be set to False.
        self.app.run(host="0.0.0.0", port=5001, debug=True)


if __name__ == "__main__":
    app = PatientAPIController()
    app.run()
