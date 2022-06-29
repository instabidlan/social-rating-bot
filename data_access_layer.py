import psycopg2

from config import DB_URI
from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    social_rating: int


@dataclass
class BlacklistUser:
    username: str
    fio: str
    group: str
    status: str
    spec_signs: str


class DataBaseAccess:
    def __init__(self, uri: str) -> None:
        self.db_conn = psycopg2.connect(uri, sslmode='require')
        self.cursor = self.db_conn.cursor()
        
    def item_in_column(self, item, table: str, column: str) -> bool:
        self.cursor.execute(f"SELECT {column} FROM {table}")
        return (item,) in self.cursor.fetchall()

    def insert_into(self, table: str, values: tuple, columns=()) -> None:
        if columns:
            query = f"INSERT INTO {table} ({','.join(values)}) VALUES ({', '.join(len(columns) * ['%s'])})"
        else:
            query = f"INSERT INTO {table} VALUES ({', '.join(len(values) * ['%s'])})"
        self.cursor.execute(query, values)
        self.db_conn.commit()
    
    def update_table_where(self, table: str, set: str, cond: str, values: tuple) -> None:
        self.cursor.execute(f"UPDATE {table} SET {set} WHERE {cond}", values)
        self.db_conn.commit()

    def get_user(self, table: str, cond: str, values: tuple) -> User:
        self.cursor.execute(f"SELECT to_json(result) FROM (SELECT * FROM {table} WHERE {cond}) result", values)
        user_dict = self.cursor.fetchone()[0]
        return User(id=user_dict["id"], username=user_dict["username"], social_rating=user_dict["social_rating"])

    def get_blacklist(self) -> list[BlacklistUser]:
        self.cursor.execute(f"SELECT to_json(result) FROM (SELECT * FROM blacklist) result")
        blacklist = [BlacklistUser(
            username=user[0]["username"],
            fio=user[0]["fio"],
            group=user[0]["group"],
            status=user[0]["status"],
            spec_signs=user[0]["spec_signs"]) for user in self.cursor.fetchall()]

        return blacklist
