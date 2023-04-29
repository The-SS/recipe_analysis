from colorama import init, Fore, Back, Style


def print_colored(msg, color=''):
    if color == 'g':
        print(Fore.GREEN + msg + Style.RESET_ALL)
    elif color == 'r':
        print(Fore.RED + msg + Style.RESET_ALL)
    elif color == 'b':
        print(Fore.BLUE + msg + Style.RESET_ALL)
    elif color == 'y':
        print(Fore.YELLOW + msg + Style.RESET_ALL)
    elif color == 'm':
        print(Fore.MAGENTA + msg + Style.RESET_ALL)
    elif color == 'c':
        print(Fore.CYAN + msg + Style.RESET_ALL)
    else:
        print(Style.RESET_ALL + msg)
