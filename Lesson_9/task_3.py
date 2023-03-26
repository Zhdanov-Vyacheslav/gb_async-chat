from tabulate import tabulate

from task_2 import host_range_ping


def host_range_ping_tab():
    while True:
        cidr = input('Введите диапазон адресов CIDR формата "<ip>/<mask>", или "exit"')
        if cidr.lower() == "exit":
            break
        cidr = cidr.split("/")
        if len(cidr) == 2:
            ping_dict = host_range_ping(*cidr)
            if ping_dict is not None:
                print(tabulate(ping_dict, headers='keys', stralign="center"))


if __name__ == "__main__":
    host_range_ping_tab()
