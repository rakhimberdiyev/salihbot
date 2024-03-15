import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id int AUTO_INCREMENT PRIMARY KEY,
            user_id BIGINT UNIQUE NOT NULL
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, user_id: int):
        # SQL_EXAMPLE = "INSERT INTO Users(id) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Users (user_id) VALUES(?);
        """
        self.execute(sql, parameters=(user_id,), commit=True)

    def select_all_users(self):
        sql = """
        SELECT user_id FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    # def update_user_email(self, email, id):
    #     # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"
    #
    #     sql = f"""
    #     UPDATE Users SET email=? WHERE id=?
    #     """
    #     return self.execute(sql, parameters=(email, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)


    def create_table_answers(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Answers (
            id int AUTO_INCREMENT PRIMARY KEY,
            user_id BIGINT NOT NULL,
            user_name VARCHAR(255) NOT NULL,
            username VARCHAR(255) NOT NULL,
            answer_number INT NOT NULL,
            answer TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
"""
        self.execute(sql, commit=True)

    def add_answer(self, user_id: int, user_name:str, username: str, answer_number: int, answer: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO Answers (user_id, user_name, username, answer_number, answer) VALUES(?, ?, ?, ?, ?);
        """
        self.execute(sql, parameters=(user_id, user_name, username, answer_number, answer), commit=True)

    def select_all_answers(self, answer_number:int):
        sql = """
        SELECT user_name, username, answer_number, answer, created_at FROM Answers WHERE answer_number=?
        """
        return self.execute(sql, parameters=(answer_number,), fetchall=True)
    

    def count_answers(self):
        return self.execute("SELECT COUNT(*) FROM Answers;", fetchone=True)

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
