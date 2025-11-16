# Patient Portal API

The Patient Portal is a comprehensive RESTful API for managing patient records within a hospital setting. It provides a complete set of endpoints for creating, retrieving, updating, and deleting patient information, as well as specialized actions like searching, room assignment, and patient checkout.

The system is built with Python using the Flask framework for the API, SQLAlchemy for database interaction, and a SQLite database for data persistence.

## Features

- **Full CRUD Operations:** Create, Read, Update, and Delete patient records.
- **Doctor Assignment:** Assign a validated doctor to a patient.
- **Patient Search:** Search for patients by name.
- **Room Management:** Assign patients to specific wards and rooms with validation.
- **Checkout System:** Mark a patient as checked out, timestamping the event.
- **Data Validation:** Robust server-side validation for all incoming data to ensure integrity.
- **Structured Project:** Clear separation of concerns between the API controller, database logic, and data models.

## Project Structure

The project is organized into several key modules within the `src/` directory:

- `api_controller.py`: The main Flask application file that defines all API routes and handles HTTP requests and responses.
- `patient.py`: Contains the `Patient` class, which models a patient's data and includes methods for data manipulation.
- `patient_db.py`: Manages all database interactions using SQLAlchemy, abstracting the database logic from the API controller.
- `doctor.py`: A simple class to represent a `Doctor`.
- `config.py`: Stores shared configuration variables like available genders, ward/room numbers, and doctor names.
- `patient_db_config.py`: Defines the database schema using SQLAlchemy and initializes the database engine.
- `patient.db`: The SQLite database file where all patient data is stored.

## Prerequisites

- Python (version >= 3.10 is recommended)
- Git

## Installation and Setup

Follow these steps to get the application running on your local machine.

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/tr3d0/patients-portal/
    cd patients-portal
    ```

2.  **Create and Activate a Virtual Environment**

    - On macOS and Linux (using bash):
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

    - On Windows (using Command Prompt or PowerShell):
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```

3.  **Install Dependencies**
    Install all the required Python packages from the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Start the Flask Server**
    Navigate to the `src` directory and run the API controller. This will start the development server, typically on `http://127.0.0.1:5001`.
    ```bash
    cd src
    python api_controller.py
    ```
    Keep this terminal window open and running.

2.  **Interact with the API**
    Open a **new terminal** to run the provided shell scripts for testing the API endpoints. These scripts are located in the `testing-api-templates` directory.

    - **Create a Patient:**
      *(This script reads a payload from `payloads/create_patients.json`. Ensure the payload contains all required fields: `name`, `age`, `gender`, `ward`, `room`, and `doctor_name`)*
      ```bash
      ./testing-api-templates/create_patient.sh
      ```

    - **List All Patients:**
      ```bash
      curl -X GET http://127.0.0.1:5001/patients
      ```

    - **Search for a Patient by Name:**
      ```bash
      ./testing-api-templates/list_patient_by_name.sh "John"
      ```

    - **Get a Specific Patient by ID:**
      *(Replace `<patient-id>` with an actual ID from the creation or list response)*
      ```bash
      curl -X GET http://127.0.0.1:5001/patients/<patient-id>
      ```

    - **Update a Patient:**
      *(This script reads a payload from `payloads/update_patient.json`)*
      ```bash
      ./testing-api-templates/update_patient.sh <patient-id>
      ```

    - **Checkout a Patient:**
      *(Replace `<patient-id>` with an actual ID)*
      ```bash
      ./testing-api-templates/checkout_patient.sh <patient-id>
      ```

    - **Delete a Patient:**
      ```bash
      curl -X DELETE http://127.0.0.1:5001/patients/<patient-id>
      ```

## API Endpoints

| Method | Endpoint                       | Description                                         |
|--------|--------------------------------|-----------------------------------------------------|
| `GET`  | `/`                            | Displays a welcome message.                         |
| `GET`  | `/patients`                    | Retrieves a list of all patients.                   |
| `POST` | `/patients`                    | Creates a new patient.                              |
| `GET`  | `/doctors`                     | Retrieves the list of available doctors.            |
| `GET`  | `/patients/<id>`               | Retrieves a single patient by their ID.             |
| `PUT`  | `/patients/<id>`               | Updates a patient's information (name, age, etc.).  |
| `DELETE`| `/patients/<id>`              | Deletes a patient by their ID.                      |
| `GET`  | `/patients/search`             | Searches for patients by name (`?search_name=...`). |
| `PUT`  | `/patients/<id>/room`          | Assigns or updates a patient's ward and room.       |
| `PUT`  | `/patients/<id>/doctor`        | Assigns a doctor to the patient.                    |
| `PUT`  | `/patients/<id>/checkout`      | Sets the patient's checkout time.                   |

---

## Feedback and Bug Reports

Feedback, bug reports, and contributions are welcome!

If you encounter any issues or have ideas for improvements, please [open an issue](https://github.com/tr3d0/patients-portal/issues) on the project's GitHub repository.

*This project was developed based on an initial assignment structure. The implementation of all features, including the API logic, database interactions, and data models, represents the completed work.*