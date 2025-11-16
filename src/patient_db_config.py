# All sqlalchemy related config goes here, including the database schema definition.

import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData

DB_FILE_PATH = "patient.db"

CONN = sqlite3.connect(DB_FILE_PATH)
ENGINE = create_engine("sqlite:///" + DB_FILE_PATH, echo=True)
METADATA = MetaData()

PATIENTS_TABLE_NAME = "patients"
ID_COLUMN = "id"
NAME_COLUMN = "name"
AGE_COLUMN = "age"
GENDER_COLUMN = "gender"
CHECKIN_COLUMN = "checkin"
CHECKOUT_COLUMN = "checkout"
WARD_COLUMN = "ward"
ROOM_COLUMN = "room"

PATIENT_COLUMN_NAMES = [
    ID_COLUMN,
    NAME_COLUMN,
    AGE_COLUMN,
    GENDER_COLUMN,
    ROOM_COLUMN,
    WARD_COLUMN,
    CHECKOUT_COLUMN,
    CHECKIN_COLUMN,
]

PATIENTS_TABLE = Table(
    PATIENTS_TABLE_NAME,
    METADATA,
    Column(ID_COLUMN, String, primary_key=True),
    Column(NAME_COLUMN, String),
    Column(AGE_COLUMN, Integer),
    Column(GENDER_COLUMN, String),
    Column(CHECKIN_COLUMN, String),
    Column(CHECKOUT_COLUMN, String),
    Column(WARD_COLUMN, Integer),
    Column(ROOM_COLUMN, Integer),
    Column("doctor_name", String),
)

METADATA.create_all(ENGINE)
