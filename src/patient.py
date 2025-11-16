import uuid
from datetime import datetime, timezone
from config import GENDERS, WARD_NUMBERS, ROOM_NUMBERS, API_CONTROLLER_URL
from doctor import Doctor
import requests

# TODO: Implement the Patient class.
# Please import and use the config and db config variables.
#
# The attributes for this class should be the same as the columns in the PATIENTS_TABLE.
#
# The Object Arguments should only be name , gender and age.
# Rest of the attributes should be set within the class.
#
# -> for id use uuid4 to generate a unique id for each patient.
# -> for checkin and checkout use the current date and time.
#
# There should be a method to update the patient's room and ward. validation should be used.(config is given)
#
# Validation should be done for all of the variables in config and db_config.
#
# There should be a method to commit that patient to the database using the api_controller.


class Patient:
    """A class to represent a patient."""

    def __init__(self, name: str, age: int, gender: str, ward: int | None = None, room: int | None = None, doctor_name: str | None = None):
        """
        Initialize the Patient object.
        Args:
            name (str): The name of the patient.
            age (int): The age of the patient.
            gender (str): The gender of the patient.
            doctor_name (str, optional): The name of the assigned doctor. Defaults to None.
        """
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be a positive integer.")
        if gender not in GENDERS:
            raise ValueError(f"Gender must be one of {GENDERS}.")

        self.id = str(uuid.uuid4())
        self.checkin = datetime.now(timezone.utc).strftime("%d-%m-%Y %H:%M:%S")
        self.checkout = None
        self.name = name
        self.age = age
        self.gender = gender
        self.ward: int | None = None  # Initialize to None
        self.room: int | None = None  # Initialize to None
        self.doctor_name: str | None = None # Initialize to None

        if ward is not None and room is not None:
            self.setroom_andward(ward, room)
        
        if doctor_name:
            self.assign_doctor(doctor_name)

    def assign_doctor(self, doctor_name: str) -> None:
        """
        Assigns a doctor to the patient with validation.
        Args:
            doctor_name (str): The name of the doctor.
        Raises:
            ValueError: If the doctor's name is not recognized.
        """
        validated_doctor = Doctor(doctor_name) # This will raise ValueError if invalid
        self.doctor_name = validated_doctor.name

    def setroom_andward(self, ward: int, room: int) -> None:
        """
        Sets the room and ward for the patient with validation.
        Args:
            ward (int): The ward number.
            room (int): The room number.
        """
        if ward in WARD_NUMBERS and str(room) in ROOM_NUMBERS.get(ward, []):
            self.ward = ward
            self.room = room
        else:
            self.ward = None
            self.room = None
            raise ValueError("Invalid ward or room number.")

    def checkout_patient(self) -> None:
        """Sets the checkout time for the patient."""
        self.checkout = datetime.now(timezone.utc).strftime("%d-%m-%Y %H:%M:%S")

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the patient.
        Returns:
            dict: A dictionary containing patient data.
        """
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "checkin": self.checkin,
            "checkout": self.checkout,
            "ward": self.ward,
            "room": self.room,
            "doctor_name": self.doctor_name,
        }

    def commit_to_db(self) -> requests.Response:
        """
        Commits the patient to the database using the API.
        Returns:
            requests.Response: The response from the API.
        """
        url = f"{API_CONTROLLER_URL}:5001/patients"
        payload = {"name": self.name, "age": self.age, "gender": self.gender}
        response = requests.post(url, json=payload)
        return response
