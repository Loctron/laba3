from database.database_manager import DatabaseManager


class FuzzyRepository:

    def __init__(self):
        self.db = DatabaseManager()

    def create_fuzzy_variable(
            self,
            attribute_id,
            scale_name,
            min_value,
            max_value,
            step
    ):

        cursor = self.db.execute(
            """
            INSERT INTO fuzzy_variables(
                attribute_id,
                scale_name,
                min_value,
                max_value,
                step
            )
            VALUES(?,?,?,?,?)
            """,
            (
                attribute_id,
                scale_name,
                min_value,
                max_value,
                step
            )
        )
        
        return cursor.lastrowid

    def get_fuzzy_variable(self, attribute_id):

        return self.db.fetch_one(
            """
            SELECT *
            FROM fuzzy_variables
            WHERE attribute_id=?
            """,
            (attribute_id,)
        )

    def add_term(self, fuzzy_variable_id, name):

        cursor = self.db.execute(
            """
            INSERT INTO terms(
                fuzzy_variable_id,
                name
            )
            VALUES(?,?)
            """,
            (fuzzy_variable_id, name)
        )

        return cursor.lastrowid

    def get_terms(self, fuzzy_variable_id):

        return self.db.fetch_all(
            """
            SELECT *
            FROM terms
            WHERE fuzzy_variable_id=?
            ORDER BY id
            """,
            (fuzzy_variable_id,)
        )

    def save_membership_function(self, term_id, a, b, c, d):

        existing = self.db.fetch_one(
            """
            SELECT id FROM membership_functions
            WHERE term_id=?
            """,
            (term_id,)
        )

        if existing:

            self.db.execute(
                """
                UPDATE membership_functions
                SET a=?, b=?, c=?, d=?
                WHERE term_id=?
                """,
                (a, b, c, d, term_id)
            )

        else:

            self.db.execute(
                """
                INSERT INTO membership_functions(
                    term_id, a, b, c, d
                )
                VALUES(?,?,?,?,?)
                """,
                (term_id, a, b, c, d)
            )

    def get_fuzzy_variable_by_attribute(self, attribute_id):

        return self.db.fetch_one(
            """
            SELECT *
            FROM fuzzy_variables
            WHERE attribute_id=?
            """,
            (attribute_id,)
        )