
from memory.database import get_connection


class FeedbackMemory:
    """Stores and retrieves user feedback on investigations."""

    VALID_RATINGS = [
        "correct",
        "incorrect",
        "partially_correct"
    ]

    def save_feedback(self, investigation_id, rating, comment=""):
        """Save user feedback for an investigation."""

        if rating not in self.VALID_RATINGS:
            raise ValueError("Invalid feedback rating.")

        connection = get_connection()
        cursor = connection.cursor()

        try:
            # Check whether the investigation exists
            cursor.execute(
                "SELECT id FROM investigations WHERE id = ?",
                (investigation_id,)
            )

            if cursor.fetchone() is None:
                raise ValueError("Investigation not found.")

            # Save feedback
            cursor.execute(
                """
                INSERT INTO feedback
                (investigation_id, rating, comment)
                VALUES (?, ?, ?)
                """,
                (investigation_id, rating, comment)
            )

            feedback_id = cursor.lastrowid
            connection.commit()

            return feedback_id

        finally:
            connection.close()

    def get_feedback(self, investigation_id):
        """Retrieve feedback for a particular investigation."""

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM feedback
            WHERE investigation_id = ?
            ORDER BY created_at DESC
            """,
            (investigation_id,)
        )

        results = cursor.fetchall()
        connection.close()

        return [dict(row) for row in results]

    def get_all_feedback(self):
        """Retrieve all stored feedback."""

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT * FROM feedback
            ORDER BY created_at DESC
            """
        )

        results = cursor.fetchall()
        connection.close()

        return [dict(row) for row in results]
