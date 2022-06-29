from random import randint
from data_access_layer import *
from config import DB_URI


db = DataBaseAccess(DB_URI)


def get_social_rating(user_id: int, username: str) -> int:
    if not db.item_in_column(item=user_id, table="social_rating", column="id"):
        db.insert_into(table="social_rating", values=(user_id, username, 0))

    user_obj = db.get_user(table="social_rating", cond="id=%s", values=(user_id,))
    _social_rating = user_obj.social_rating

    return _social_rating


def stats_func_output(user_id: int, username: str) -> str:
    _social_rating = get_social_rating(user_id, username)

    party_op = "*ПАРТИЯ ВАМИ НЕДОВОЛЬНА*" if _social_rating <= 0 else "*ПАРТИЯ ВАМИ ДОВОЛЬНА*"
    out_str = f"```@{username}```, твой социальный рейтинг: \{_social_rating}\n\n" \
              f"{party_op}"
    return out_str

#
# def get_blacklist_output():
#     blacklist = db.get_blacklist()
#     out_str = f"BLACKLIST FB-11:\n" \
#               "{}"


def change_social_rating(user_id: int, username: str, delta: int) -> str:
    _social_rating = get_social_rating(user_id, username) + delta

    db.update_table_where(table="social_rating",
                          set="social_rating=%s, username=%s",
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
