from typing import Any, Dict, List, Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import operators
from sqlalchemy import select, insert, update, delete
from patient_db_config import PATIENTS_TABLE, ENGINE


class PatientDB:
    """
    A class for interacting with the patient database.
    Provides methods for CRUD operations on patient records.
    """

    @staticmethod
    def _row_to_dict(row: Any) -> Dict[str, Any]:
        """Converts a database row to a dictionary."""
        return dict(row._mapping)

    def insert_patient(self, patient_data: Dict[str, Any]) -> Optional[str]:
        """
        Inserts a new patient record into the database.
        Args:
            patient_data: A dictionary containing the patient's information.
        Returns:
            The primary key of the inserted patient, or None if an error occurs.
        """
        try:
            with ENGINE.connect() as conn:
                stmt = insert(PATIENTS_TABLE).values(**patient_data)
                result = conn.execute(stmt)
                conn.commit()
                if result.inserted_primary_key:
                    return str(result.inserted_primary_key[0])
                return None
        except SQLAlchemyError as e:
            print(f"Error inserting patient: {e}")
            return None

    def select_all_patients(self) -> Optional[List[Dict[str, Any]]]:
        """
        Retrieves all patient records from the database.
        Returns:
            A list of dictionaries representing patient records, or None on error.
        """
        try:
            with ENGINE.connect() as conn:
                stmt = select(PATIENTS_TABLE)
                result = conn.execute(stmt)
                return [self._row_to_dict(row) for row in result]
        except SQLAlchemyError as e:
            print(f"Error selecting all patients: {e}")
            return None

    def search_patients_by_name(self, name: str) -> Optional[List[Dict[str, Any]]]:
        """
        Searches for patients by name (case-insensitive).
        Args:
            name: The name to search for.
        Returns:
            A list of matching patient records, or None on error.
        """
        try:
            with ENGINE.connect() as conn:
                stmt = select(PATIENTS_TABLE).where(
                    PATIENTS_TABLE.c.name.ilike(f"%{name}%")
                )
                result = conn.execute(stmt)
                return [self._row_to_dict(row) for row in result]
        except SQLAlchemyError as e:
            print(f"Error searching for patients by name: {e}")
            return None

    def select_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a specific patient record by their ID.
        Args:
            patient_id: The ID of the patient to retrieve.
        Returns:
            A dictionary representing the patient, or None if not found or on error.
        """
        try:
            with ENGINE.connect() as conn:
                stmt = select(PATIENTS_TABLE).where(PATIENTS_TABLE.c.id == patient_id)
                row = conn.execute(stmt).first()
                return self._row_to_dict(row) if row else None
        except SQLAlchemyError as e:
            print(f"Error selecting patient: {e}")
            return None

    def update_patient(
        self, patient_id: str, update_data: Dict[str, Any]
    ) -> Optional[int]:
        """
        Updates a patient record in the database.
        Args:
            patient_id: The ID of the patient to update.
            update_data: A dictionary with the fields to update.
        Returns:
            The number of rows affected, or None on error.
        """
        try:
            with ENGINE.connect() as conn:
                stmt = (
                    update(PATIENTS_TABLE)
                    .where(PATIENTS_TABLE.c.id == patient_id)
                    .values(**update_data)
                )
                result = conn.execute(stmt)
                conn.commit()
                return result.rowcount
        except SQLAlchemyError as e:
            print(f"Error updating patient: {e}")
            return None

    def delete_patient(self, patient_id: str) -> Optional[int]:
        """
        Deletes a patient record from the database.
        Args:
            patient_id: The ID of the patient to delete.
        Returns:
            The number of rows affected, or None on error.
        """
        try:
            with ENGINE.connect() as conn:
                stmt = delete(PATIENTS_TABLE).where(PATIENTS_TABLE.c.id == patient_id)
                result = conn.execute(stmt)
                conn.commit()
                return result.rowcount
        except SQLAlchemyError as e:
            print(f"Error deleting patient: {e}")
            return None
