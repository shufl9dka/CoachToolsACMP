from utils import acmp_funcs, users as db, tools, captcha_solving


def registrator():
    print('Введите количество аккаунтов для регистрации и формат логинов (латиница и цифры)')
    print('Пример: "5 minreg-nyasvizh-{i}", вместо i будет подставлен индекс аккаунта')
    n = ''
    while True:
        fmt = input("Ввод (q для выхода): ")
        if fmt.strip().lower() == 'q':
            return
        if len(fmt.split()) < 2:
            print('Неверный формат ввода')
            continue
        n, fmt = fmt.strip().split(maxsplit=1)
        fmt = fmt.strip()
        if not n.isdigit() or ' ' in fmt or int(n) < 1 or (int(n) > 1 and '{i}' not in fmt):
            print('Неверный формат ввода')
            continue
        if '{i}' not in fmt and db.check_user(fmt):
            print('Аккаунт с таким логином уже существует в Вашей базе')
            continue
        n = int(n)
        break
    names = []
    for i in range(1, n + 1):
        names.append(input(f'Имя {i}-го участника: '))
    print('Пытаемся зарегистрировать аккаунты. Пожалуйста, подождите...')

    current_idx = 0
    successes = 0
    occupied_usernames = set([user['username'] for user in db.load_users()])
    captcha_solver = captcha_solving.tkinter_solver.TkinterSolver()

    def good_captcha(_captcha: str):
        return len(_captcha) == 6 and _captcha.isdigit()

    for name in names:
        current_idx += 1
        while fmt.format(**{'i': current_idx}) in occupied_usernames:
            current_idx += 1
        username = fmt.format(**{'i': current_idx})
        session, data = None, None
        captcha = ''
        password = tools.gen_password()
        while not good_captcha(captcha) or not acmp_funcs.reg_success(session, name, username, password, captcha):
            password = tools.gen_password()
            session, data = acmp_funcs.get_registration_captcha()
            if data is None:
                print('Произошла ошибка получения капчи. Возможно, проблемы с соединением или аккаунт с таким логином уже существует.')
                break
            captcha = captcha_solver.solve(data)
            if captcha == '!EXIT':
                break
        else:
            db.append_user({'name': name, 'username': username, 'password': password})
            successes += 1
    if successes == 0:
        print('Нет успешных попыток регистрации.')
    else:
        print(f'{successes} участник{"ов" if successes > 1 else ""} был{"о" if successes > 1 else ""} зарегистрирован{"о" if successes > 1 else ""} успешно.')
