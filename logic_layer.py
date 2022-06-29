from random import randint
from os import environ
from data_access_layer import *

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


def antispam(message, data):
    if 'sticker' in message.values.keys():
        print('yeah sticker')
        seq = message.values['sticker'].thumb['file_unique_id']
    elif 'animation' in message.values.keys():
        print('yeah gifka')
        seq = message.values['animation'].thumb['file_unique_id']
    else:
        seq = message.text

    if 'last_messages' not in data.keys():
        data['last_messages'] = [seq]
    else:
        if data['last_messages'][-1] == seq:
            data['last_messages'].append(seq)
        else:
            data['last_messages'] = [seq]
    print(data['last_messages'])
    return seq

