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
    # print("Введите формат для вывода аккаунта (одна строка для одного аккаунта).")
    # print("Можно использовать переменные:\n"
    #       "{name} - ФИО участника\n"
    #       "{login} - Логин участника\n"
    #       "{pass} - Пароль участника. Ниже можно увидеть пример:")
    # print("{name}: {login} {pass} // Joe Doe: joedoe42 passw000rd")
    fmt = "{name}: {login} {pass}"
    data = '\n'.join([fmt.format(**{'name': user['name'],
                                    'login': user['username'],
                                    'pass': user['password']}) for user in db.load_users()])
    try:
        pyperclip.copy(data)
    except pyperclip.PyperclipException:
        ans = input('Не удалось скопировать данные аккаунтов. Вывести их на экран? (д/н): ')
        if ans.strip().lower() in 'yYдД':
            print(data)
    else:
        print('Данные успешно скопированы в буфер обмена.')
