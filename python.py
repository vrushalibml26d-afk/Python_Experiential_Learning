import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

from flask import Flask, jsonify, request, send_from_directory


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = Path(os.environ.get("CONTACTS_DB", BASE_DIR / "contacts.db"))
FIELDS = ("name", "mobile", "email", "organization")

app = Flask(__name__)


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                mobile TEXT NOT NULL DEFAULT '',
                email TEXT NOT NULL DEFAULT '',
                organization TEXT NOT NULL DEFAULT ''
            )
            """
        )


def read_contact_payload() -> dict[str, str]:
    payload: Any = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object.")

    return {
        field: str(payload.get(field, "")).strip()
        for field in FIELDS
    }


@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/api/contacts")
def list_contacts():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, name, mobile, email, organization "
            "FROM contacts ORDER BY name COLLATE NOCASE, id"
        ).fetchall()
    return jsonify([dict(row) for row in rows])


@app.post("/api/contacts")
def create_contact():
    try:
        contact = read_contact_payload()
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    if not contact["name"]:
        return jsonify({"error": "Name is required."}), 400

    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO contacts (name, mobile, email, organization) "
            "VALUES (?, ?, ?, ?)",
            tuple(contact[field] for field in FIELDS),
        )
        row = connection.execute(
            "SELECT id, name, mobile, email, organization "
            "FROM contacts WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return jsonify(dict(row)), 201


@app.put("/api/contacts/<int:contact_id>")
def update_contact(contact_id: int):
    try:
        contact = read_contact_payload()
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    if not contact["name"]:
        return jsonify({"error": "Name is required."}), 400

    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE contacts SET name = ?, mobile = ?, email = ?, "
            "organization = ? WHERE id = ?",
            (*[contact[field] for field in FIELDS], contact_id),
        )
        if cursor.rowcount == 0:
            return jsonify({"error": "Contact not found."}), 404
        row = connection.execute(
            "SELECT id, name, mobile, email, organization "
            "FROM contacts WHERE id = ?",
            (contact_id,),
        ).fetchone()
    return jsonify(dict(row))


@app.delete("/api/contacts/<int:contact_id>")
def delete_contact(contact_id: int):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM contacts WHERE id = ?", (contact_id,)
        )
        if cursor.rowcount == 0:
            return jsonify({"error": "Contact not found."}), 404
    return jsonify({"message": "Contact deleted."})


initialize_database()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000")),
        debug=False,
    )