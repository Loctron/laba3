from database.database_manager import DatabaseManager


class AttributeRepository:

    def __init__(self):
        self.db = DatabaseManager()

    def add_attribute(self, project_id, name, value_type, fuzzy_type=None):
        self.db.execute(
            """
            INSERT INTO attributes(
                project_id,
                name,
                value_type,
                fuzzy_type
            )
            VALUES(?,?,?,?)
            """,
            (project_id, name, value_type, fuzzy_type)
        )

    def get_attribute(self, attribute_id):
        return self.db.fetch_one(
            """
            SELECT *
            FROM attributes
            WHERE id=?
            """,
            (attribute_id,)
        )

    def get_all_attributes(self, project_id):
        return self.db.fetch_all(
            """
            SELECT *
            FROM attributes
            WHERE project_id=?
            ORDER BY name
            """,
            (project_id,)
        )

    def search_attribute(self, text):
        return self.db.fetch_all(
            """
            SELECT *
            FROM attributes
            WHERE name LIKE ?
            """,
            (f"%{text}%",)
        )

    def rename_attribute(self, attribute_id, new_name):
        self.db.execute(
            """
            UPDATE attributes
            SET name=?
            WHERE id=?
            """,
            (new_name, attribute_id)
        )

    def delete_attribute(self, attribute_id):
        self.db.execute(
            """
            DELETE FROM attributes
            WHERE id=?
            """,
            (attribute_id,)
        )

    def copy_attribute(self, source_id, target_project_id):

        attr = self.db.fetch_one(
            """
            SELECT *
            FROM attributes
            WHERE id=?
            """,
            (source_id,)
        )

        if not attr:
            return

        self.add_attribute(
            target_project_id,
            attr["name"] + "_copy",
            attr["value_type"],
            attr["fuzzy_type"]
        )

    def get_attribute_values(self, attribute_id):
        return self.db.fetch_all(
            """
            SELECT *
            FROM attribute_values
            WHERE attribute_id=?
            ORDER BY value
            """,
            (attribute_id,)
        )

    def add_attribute_value(self, attribute_id, value):
        self.db.execute(
            """
            INSERT INTO attribute_values(attribute_id, value)
            VALUES(?, ?)
            """,
            (attribute_id, value)
        )