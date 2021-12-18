from utils import users as db, acmp_funcs


def detach_accounts():
    accounts = input("Введите через пробел логины аккаунтов для удаления из базы: ")
    accounts = set([account.strip() for account in accounts.split() if accounts.strip()])
    db.save_users([user for user in db.load_users() if user['username'] not in accounts])
    print("Введённые аккаунты были удалены из вашей базы аккаунтов.")


def add_single():
    print("Введите данные от аккаунта в формате [логин] [пароль] (без скобок)")
    while True:
        data = input("Ввод (q для выхода): ").strip()
        if data.lower() == 'q':
            return
        if len(data.split(' ')) < 2:
            print('Неверный формат ввода')
            continue
        username, password = data.split(' ', maxsplit=1)
        if db.check_user(username):
            print(f"Пользователь '{username}' уже существует.")
            return
        session = acmp_funcs.log_in(username, password.strip())
        name = acmp_funcs.get_name(session)
        if name is None:
            print("Не удалось авторизоваться. Возможно, данные неверны.")
            continue
        db.append_user({'name': name, 'username': username, 'password': password})
        print(f"Пользователь {name} был успешно добавлен!")
        break
