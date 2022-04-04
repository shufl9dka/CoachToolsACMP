import pyperclip
from utils import users as db


def print_list():
    users = db.load_users()
    if not users:
        print('В вашей базе нет ни одного аккаунта.')
    else:
        for i, user in enumerate(users):
            print(f"[{i + 1}] {user['name']}: {user['username']}")


def copy_list():
    data = '\n'.join([f"{user['name']}: {user['username']} {user['password']}" for user in db.load_users()])
    try:
        pyperclip.copy(data)
    except pyperclip.PyperclipException:
        ans = input('Не удалось скопировать данные аккаунтов. Вывести их на экран? (д/н): ')
        if ans.strip().lower() in 'yд':
            print(data)
    else:
        print('Данные успешно скопированы в буфер обмена.')
