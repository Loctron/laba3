from database.database_manager import DatabaseManager


class RuleRepository:

    def __init__(self):
        self.db = DatabaseManager()

    def add_rule(self, project_id, name):

        cursor = self.db.execute(
            """
            INSERT INTO rules(
                project_id,
                name
            )
            VALUES(?,?)
            """,
            (project_id, name)
    )

        return cursor.lastrowid

    def get_rules(self, project_id):
        return self.db.fetch_all(
            "SELECT * FROM rules WHERE project_id=? ORDER BY id",
            (project_id,)
        )

    def add_condition(self, rule_id, attribute_id, value, condition_type):
        self.db.execute(
            """INSERT INTO conditions(rule_id, attribute_id, value, condition_type)
               VALUES(?,?,?,?)""",
            (rule_id, attribute_id, value, condition_type)
        )

    def add_explanation(self, rule_id, text):

        existing = self.db.fetch_one(
            "SELECT id FROM explanations WHERE rule_id=?",
            (rule_id,)
        )

        if existing:
            self.db.execute(
                "UPDATE explanations SET explanation_text=? WHERE rule_id=?",
                (text, rule_id)
            )
        else:
            self.db.execute(
                "INSERT INTO explanations(rule_id, explanation_text) VALUES(?,?)",
                (rule_id, text)
            )

    def get_explanation(self, rule_id):

        return self.db.fetch_one(
            """
            SELECT *
            FROM explanations
            WHERE rule_id=?
            """,
            (rule_id,)
        )
    
    def get_all_rules(self):
        return self.db.fetch_all("""
            SELECT * FROM rules
            ORDER BY id
        """)