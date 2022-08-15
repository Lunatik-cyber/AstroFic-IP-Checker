import datetime
import os

from ipaddress import *

import argparse
from rich.console import Console
from rich.live import Live
from rich.progress import Progress, TimeElapsedColumn, SpinnerColumn
from rich.rule import Rule
from rich.spinner import Spinner
from rich.text import Text

from addition import *

console = Console()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def nowTime():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    return current_time


def press_enter():
    with Live(
            Spinner('point', text=Text('Press Enter to continue', style='blink khaki1')),
            refresh_per_second=20,
    ) as live:
        while True:
            live.update(console.input())
            break


def write_ip_in_file(file, data):
    with open(file, 'a', encoding='utf-8') as work:
        work.write(f'{data}\n')


def checkPort(ip: str, port: int):
    try:
        check = R(ip, port, 60)
        if check.ping(1):
            return True
        else:
            return False
    except:
        return False


def checkPing(ip: str):
    import ping3
    result = ping3.ping(ip)
    if f'{result}'.replace('\n', '') == 'None':
        return False
    else:
        return True


def manual_write(method: str, ip_list=None, ping_check=None):
    clear()
    if method == 'cli':
        ip_list = ip_list.replace(' ', '').split(',')
    else:
        console.print('Инструкция по вводу рабочих подсетей:\n'
                      'Если вы хотите найти:\n'
                      '     [1.X.X.X], то введите 1.0.0.0/8\n'
                      '     [1.1.X.X], то введите 1.1.0.0/16\n'
                      '     [1.1.1.X], то введите 1.1.1.0/24\n'
                      'Разрешается вводить сразу нескольно через запятую. \n'
                      'А можно ввести просто IP нужные через запятую\n\n')
        ip_list = console.input('[blink]>>> ')
        ip_list = ip_list.replace(' ', '').split(',')
        ping_check = console.input('Проверить пинг? (Y/N) [blink]>>> ')
    if method == 'cli':
        work_file = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}_work.txt'
    else:
        work_file = 'work.txt'
        try:
            os.remove(f'work.txt')
        except FileNotFoundError:
            pass
    ips_number = 0
    total = 0
    for ip in ip_list:
        total += 1
        ipv4 = ip_network(ip)
        for _ in ipv4.hosts():
            ips_number += 1
    try:
        clear()
        with Progress(
                SpinnerColumn(),
                *Progress.get_default_columns(),
                TimeElapsedColumn(),
                console=console,
                transient=False, ) as progress:
            console.print(Rule(f'Всего подсетей/IP: {total} | Всего IP: {ips_number}'))
            for ip in ip_list:
                console.print(f'Подсеть/IP: {ip}')
            console.print(Rule(f'Проверка запущена'))
            task = progress.add_task("[orange1]Processing", total=ips_number)
            task3 = progress.add_task("[cyan1]Scanning", total=None)
            number_ip = 0
            for ip in ip_list:
                console.print(Rule(f'Проверяется подсеть/IP: {ip}'))
                ipv4 = ip_network(ip)
                for ip_net in ipv4.hosts():
                    if ping_check.lower() == 'y':
                        result = checkPing(str(ip_net))
                    else:
                        result = False
                    if result:
                        console.print(f'[cyan1]{nowTime()}[/cyan1]| IP: {str(ip_net)} | Пинг: [pale_turquoise1]ОК')
                        write_ip_in_file(file=work_file, data=str(f'{nowTime()}| IP: {str(ip_net)} | Ping: OK'))
                    else:
                        result = checkPort(str(ip_net), 22)
                        if result:
                            console.print(
                                f'[cyan1]{nowTime()}[/cyan1]| IP: {str(ip_net)} | Порт 22: [pale_turquoise1]ОК')
                            write_ip_in_file(file=work_file, data=str(f'{nowTime()}| IP: {str(ip_net)} | Port 22: OK'))
                        else:
                            result = checkPort(str(ip_net), 443)
                            if result:
                                console.print(
                                    f'[cyan1]{nowTime()}[/cyan1]| IP: {str(ip_net)} | Порт 443: [pale_turquoise1]ОК')
                                write_ip_in_file(file=work_file,
                                                 data=str(f'{nowTime()}| IP: {str(ip_net)} | Port 443: OK'))
                            else:
                                console.print(
                                    f'[cyan1]{nowTime()}[/cyan1]| IP: {str(ip_net)} | [blink medium_violet_red]Не рабочий!')
                    number_ip += 1
                    progress.update(task, advance=1)
                    progress.update(task3, description=f'[cyan1]Scanned {number_ip} of {ips_number}', advance=1)
        console.print(Rule(f'[dark_slate_gray2]Проверка завершена!'))
        press_enter()
        clear()
    except KeyboardInterrupt:
        console.print(Rule(f'[red]Отмена проверки!'))
        time.sleep(3)
        clear()
    lines = 0
    try:
        with open(work_file, 'r') as f:
            for _ in f.readlines():
                lines += 1
    except FileNotFoundError:
        pass

    console.print(Rule(f'Всего найдено: {lines}'))
    try:
        with open(work_file, 'r') as f:
            id_ip = 0
            for line in f.readlines():
                console.print(f'{id_ip} | ' + line.replace("\n", ""))
                id_ip += 1
            console.print(f'\n\n[blink dark_slate_gray2]Рабочие IP записаны в файл {work_file}')
            if method == 'cli':
                exit()
            press_enter()
            clear()
            start_scan()
    except FileNotFoundError:
        console.print(Rule(f'[blink red]Файл {work_file} не найден, т.к нет рабочих IP!'))
        if method == 'cli':
            exit()
        press_enter()
        clear()
        start_scan()


def manual_read(method: str, file=None, ping_check=None):
    clear()
    if method == 'cli':
        pass
    else:
        console.print('Чтобы использовать данный вариант, введите путь до файла с диапазоном.\n'
                      '     1 линия - 1 подсеть/IP.\n'
                      '         Пример:\n'
                      '             1.1.1.0/24\n'
                      '             1.1.2.0/24')
        file = console.input('[blink]>>> ')
        ping_check = console.input('Проверить пинг? (Y/N) [blink]>>> ')
    if method == 'cli':
        work_file = f'{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}_work.txt'
    else:
        work_file = 'work.txt'
        try:
            os.remove(f'work.txt')
        except FileNotFoundError:
            pass
    press_enter()
    clear()
    ips_number = 0
    total = 0
    with open(file, 'r') as f:
        for ip in f.readlines():
            total += 1
            ipv4 = ip_network(ip)
            for _ in ipv4.hosts():
                ips_number += 1
    try:
        clear()
        with Progress(
                SpinnerColumn(),
                *Progress.get_default_columns(),
                TimeElapsedColumn(),
                console=console,
                transient=False, ) as progress:
            console.print(Rule(f'Всего подсетей/IP: {total} | Всего IP: {ips_number}'))
            with open(file, 'r') as f:
                for ip in f.readlines():
                    console.print(f'Подсеть/IP: {ip}')
                console.print(Rule(f'Проверка запущена'))
                task = progress.add_task("[orange1]Processing", total=ips_number)
                task3 = progress.add_task("[cyan1]Scanning", total=None)
                number_ip = 0
                with open(file, 'r') as files:
                    for ip in files.readlines():
                        console.print(Rule(f'Проверяется подсеть/IP: {ip}'))
                        ipv4 = ip_network(ip)
                        for ip_net in ipv4.hosts():
                            if ping_check.lower() == 'y':
                                result = checkPing(str(ip_net))
                            else:
                                result = False
                            if result:
                                console.print(
                                    f'[cyan1]{nowTime()}[/cyan1]| IP: {str(ip_net)} | Пинг: [pale_turquoise1]ОК')
                                write_ip_in_file(file=work_file, data=str(f'{nowTime()}| IP: {str(ip_net)} | Ping: OK'))
                            else:
                                result = checkPort(str(ip_net), 22)
                                if result:
                                    console.print(
                                        f'[cyan1]{nowTime()}[/cyan1]| IP: {str(ip_net)} | Порт 22: [pale_turquoise1]ОК')
                                    write_ip_in_file(file=work_file,
                                                     data=str(f'{nowTime()}| IP: {str(ip_net)} | Port 22: OK'))
                                else:
                                    result = checkPort(str(ip_net), 443)
                                    if result:
                                        console.print(
                                            f'[cyan1]{nowTime()}[/cyan1]| IP: {str(ip_net)} | Порт 443: [pale_turquoise1]ОК')
                                        write_ip_in_file(file=work_file,
                                                         data=str(f'{nowTime()}| IP: {str(ip_net)} | Port 443: OK'))
                                    else:
                                        console.print(
                                            f'[cyan1]{nowTime()}[/cyan1]| IP: {str(ip_net)} | [blink medium_violet_red]Не рабочий!')
                            number_ip += 1
                            progress.update(task, advance=1)
                            progress.update(task3, description=f'[cyan1]Scanned {number_ip} of {ips_number}', advance=1)
        console.print(Rule(f'[dark_slate_gray2]Проверка завершена!'))
        if method == 'cli':
            exit()
        press_enter()
        clear()
    except KeyboardInterrupt:
        console.print(Rule(f'[red]Отмена проверки!'))
        time.sleep(3)
        clear()
    lines = 0
    try:
        with open(work_file, 'r') as f:
            for _ in f.readlines():
                lines += 1
    except FileNotFoundError:
        pass

    console.print(Rule(f'Всего найдено: {lines}'))
    try:
        with open(work_file, 'r') as f:
            id_ip = 0
            for line in f.readlines():
                console.print(f'{id_ip} | ' + line.replace("\n", ""))
                id_ip += 1
            console.print(f'\n\n[blink dark_slate_gray2]Рабочие IP записаны в файл {work_file}')
            if method == 'cli':
                exit()
            press_enter()
            clear()
            start_scan()
    except FileNotFoundError:
        console.print(Rule(f'[blink red]Файл {work_file} не найден, т.к нет рабочих IP!'))
        if method == 'cli':
            exit()
        press_enter()
        clear()
        start_scan()


def start_scan():
    clear()
    try:
        console.print('Автоматическая проверка пинга и порта от [blink cyan1]@ShellRok')
        console.print('Выберите формат ввода адреса:\n')
        console.print('1 => Ввод адреса вручную')
        console.print('2 => Ввод адреса из файла')
        console.print('3 => Выход\n')
        option = console.input('[blink]>>> ')
        if option == '1':
            clear()
            manual_write(method='ip')
        elif option == '2':
            clear()
            manual_read(method='ip')
        elif option == '3':
            clear()
            exit()
        else:
            console.print('Неверный ввод')
            start_scan()
    except KeyboardInterrupt:
        clear()
        exit()


if __name__ == '__main__':
    clear()
    parser = argparse.ArgumentParser(description='Проверка пинга и порта выбранных IP/IP диапазонов')
    parser.add_argument('-i', '--ip', help='Введите IP/ IP диапазон для проверки')
    parser.add_argument('-f', '--file', help='Введите путь к файлу с IP/ IP диапазонами для проверки')
    parser.add_argument('-p', '--ping', help='Введите y/n для проверки пинга [По умолчанию: y]', default='y')
    args = parser.parse_args()
    if args.ip:
        manual_write(method='cli', ip_list=args.ip, ping_check=args.ping)
    elif args.file:
        manual_read(method='cli', file=args.file, ping_check=args.ping)
    else:
        start_scan()
