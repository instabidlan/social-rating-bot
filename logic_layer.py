from random import randint
from os import environ
from data_access_layer import *

print(environ)
db = DatabaseConnection(environ["DB_URI"])

sr_table = SRDatabaseAccess(db)
bl_table = BlacklistDatabaseAccess(db)


def get_social_rating(user_id: int, username: str) -> int:
    if not sr_table.is_in_table(item=user_id, column="id"):
        sr_table.insert(values=(user_id, username, 0))

    user_obj = sr_table.get(cond="id=%s", values=(user_id,), to_get="*")
    _social_rating = user_obj["social_rating"]

    return _social_rating


def stats_func_output(user_id: int, username: str) -> str:
    _social_rating = get_social_rating(user_id, username)

    party_op = "*ПАРТИЯ ВАМИ НЕДОВОЛЬНА*" if _social_rating <= 0 else "*ПАРТИЯ ВАМИ ДОВОЛЬНА*"
    out_str = f"```@{username}```, твой социальный рейтинг: \{_social_rating}\n\n" \
              f"{party_op}"
    return out_str


def change_social_rating(user_id: int, username: str, delta: int) -> str:
    _social_rating = get_social_rating(user_id, username) + delta

    sr_table.update_table(to_set="social_rating=%s, username=%s",
                          cond="id=%s", values=(_social_rating, username, user_id))
    if delta < 0:
        return f"Партия тобой недовольна! {delta} social credits"
    return f"Так держать! +{delta} social credits"


def make_decision(user_id: int, username: str) -> str:
    if randint(0, 100) >= 70:
        _delta = randint(-200, 200)
        if _delta != 0:
            return change_social_rating(user_id, username, _delta)
    return ""
