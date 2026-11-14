
from memory.database import get_connection, initialize_database


class LongTermMemory:
    """Stores and retrieves previous job investigations."""

    def __init__(self):
        initialize_database()

    def save_investigation(self, job_offer, analysis, verification):
        """Save an investigation permanently."""

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO investigations
            (job_offer, analysis, verification)
            VALUES (?, ?, ?)
            """,
            (job_offer, analysis, verification)
        )

        investigation_id = cursor.lastrowid

        connection.commit()
        connection.close()

        return investigation_id

    def get_investigation(self, investigation_id):
        """Retrieve one investigation using its ID."""

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM investigations WHERE id = ?",
            (investigation_id,)
        )

        result = cursor.fetchone()
        connection.close()

        return dict(result) if result else None

    def get_all_investigations(self):
        """Retrieve all saved investigations."""

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM investigations ORDER BY created_at DESC"
        )

        results = cursor.fetchall()
        connection.close()

        return [dict(row) for row in results]
