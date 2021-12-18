import commands
from utils import tools


def show_menu():
    tools.clear_window()
    print("[1] Вывести список аккаунтов (только логины)")
    print("[2] Скопировать список участников с паролями")
    print("[3] Сменить пароли всем аккаунтам")
    print("[4] Добавить существующий аккаунт")
    print("[5] Удалить аккаунт(ы)")
    print("[6] Зарегистрировать новые аккаунты")


def main():
    cmd_dict = {'1': commands.account_list.print_list,
                '2': commands.account_list.copy_list,
                '3': commands.change_sets.shuffle_passwords,
                '4': commands.account_add.add_single,
                '5': commands.account_add.detach_accounts,
                '6': commands.account_reg.registrator}
    while True:
        show_menu()
        cmd = ''
        while cmd not in cmd_dict:
            cmd = input("Введите номер (q для выхода): ").strip().lower()
            if cmd == 'q':
                return
            if cmd not in cmd_dict:
                print("Невалидная команда, попробуйте ещё раз")
        cmd_dict[cmd]()
        input('Для продолжения нажмите Enter...: ')


if __name__ == '__main__':
    main()
