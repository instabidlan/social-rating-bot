import psycopg2

from abc import ABC, abstractmethod


class DatabaseAccess(ABC):
    @abstractmethod
    def insert(self, values: tuple): pass

    @abstractmethod
    def update_table(self, to_set: str, cond: str, values: tuple): pass

    @abstractmethod
    def get(self, to_get: str, cond: str, values: tuple): pass

    @abstractmethod
    def is_in_table(self, item, column: str): pass


class DatabaseConnection:
    def __init__(self, uri):
        self.connection = psycopg2.connect(uri, sslmode='require')
        self.cursor = self.connection.cursor()

    def commit(self) -> None:
        self.connection.commit()

    def execute(self, query, values) -> None:
        self.cursor.execute(query, values)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()


class SRDatabaseAccess(DatabaseAccess):
    def __init__(self, db_obj: DatabaseConnection):
        self.db = db_obj

    def insert(self, values: tuple) -> None:
        query = f"INSERT INTO social_rating VALUES ({', '.join(len(values) * ['%s'])})"

        self.db.execute(query, values)
        self.db.commit()

    def update_table(self, to_set: str, cond: str, values: tuple) -> None:
        query = f"UPDATE social_rating SET {to_set} WHERE {cond}"

        self.db.execute(query, values)
        self.db.commit()

    def get(self, to_get: str, cond: str, values: tuple) -> dict:
        query = f"SELECT to_json(result) FROM (SELECT {to_get} FROM social_rating WHERE {cond}) result"

        self.db.execute(query, values)
        user_dict = self.db.fetchone()[0]
        return user_dict

    def is_in_table(self, item, column: str) -> bool:
        self.db.execute(f"SELECT {column} FROM social_rating", ())
        return (item,) in self.db.fetchall()


class BlacklistDatabaseAccess(DatabaseAccess):
    def __init__(self, db_obj: DatabaseConnection):
        self.db = db_obj

    def insert(self, values: tuple) -> None:
        query = f"INSERT INTO blacklist VALUES ({', '.join(len(values) * ['%s'])})"

        self.db.execute(query, values)
        self.db.commit()

    def update_table(self, to_set: str, cond: str, values: tuple) -> None:
        query = f"UPDATE blacklist SET {to_set} WHERE {cond}"

        self.db.execute(query, values)
        self.db.commit()

    def get(self, to_get: str, cond: str, values: tuple) -> dict:
        query = f"SELECT to_json(result) FROM (SELECT {to_get} FROM blacklist WHERE {cond}) result"

        self.db.execute(query, values)
        user_dict = self.db.fetchone()[0]
        return user_dict

    def get_all(self, to_get: str) -> list[dict]:
        query = f"SELECT to_json(result) FROM (SELECT {to_get} FROM blacklist) result"

        self.db.execute(query, ())
        blacklist_users = self.db.fetchall()
        return blacklist_users

    def is_in_table(self, item, column: str) -> bool:
        self.db.execute(f"SELECT {column} FROM blacklist", ())
        return (item,) in self.db.fetchall()
