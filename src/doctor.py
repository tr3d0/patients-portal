from config import DOCTORS


class Doctor:
    """A class to represent a doctor."""

    def __init__(self, name: str) -> None:
        """
        Initializes a new instance of the Doctor class.
        Args:
            name (str): The name of the doctor.
        """
        self.name = name

    @property
    def name(self) -> str:
        """
        Gets the name of the doctor.
        Returns:
            str: The name of the doctor.
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        Sets the name of the doctor with validation.
        Args:
            name (str): The name of the doctor.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string.")
        if name not in DOCTORS:
            raise ValueError(f"Doctor '{name}' is not recognized.")
        self._name = name
