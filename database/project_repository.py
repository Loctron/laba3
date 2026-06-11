from database.database_manager import DatabaseManager


class ProjectRepository:

    def __init__(self):
        self.db = DatabaseManager()

    def add_project(self, name, parent_id=None):

        self.db.execute(
            """
            INSERT INTO projects(name, parent_id)
            VALUES(?, ?)
            """,
            (name, parent_id)
        )

    def get_all_projects(self):

        return self.db.fetch_all(
            """
             SELECT *
             FROM projects
            ORDER BY name
            """
        )
    
    def find_project(self, name):

        return self.db.fetch_all(
            """
            SELECT *
            FROM projects
            WHERE name LIKE ?
            """,
            (f"%{name}%",)
        )

    def rename_project(self, project_id, new_name):

        self.db.execute(
            """
            UPDATE projects
            SET name=?
            WHERE id=?
            """,
            (new_name, project_id)
        )
    
    def delete_project(self, project_id):

        self.db.execute(
            """
            DELETE FROM projects
            WHERE id=?
            """,
            (project_id,)
        )

    def copy_project(self, source_id, new_name):

        project = self.db.fetch_one(
            """
            SELECT *
            FROM projects
            WHERE id=?
            """,
            (source_id,)
        )

        if not project:
            return

        self.add_project(new_name, project["parent_id"])