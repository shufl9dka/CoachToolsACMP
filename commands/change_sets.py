import string
import random
from utils import users as db, acmp_funcs


def _gen_password(length: int = 12):
    return ''.join(random.choices(string.digits + string.ascii_letters, k=length))


def shuffle_passwords():
    users = db.load_users()
    for user in users:
        session = acmp_funcs.log_in(user['username'], user['password'])
        new_password = _gen_password()
        acmp_funcs.change_password(session, user['password'], new_password)
        user['password'] = new_password
    db.save_users(users)
    print('Все пароли были изменены.')
