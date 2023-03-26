import socket
from socket import gaierror
from ipaddress import ip_address
from subprocess import Popen, PIPE
from sys import platform
import re

RE_IP = r"^(?:(?:[01]?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:[01]?\d\d?|2[0-4]\d|25[0-5])){3})$"


def host_ping(addresses: list, timeout: int = 600, count: int = 1):
    # В windows для указания кол-ва ping запросов используется ключ "-n", в системах linux и mac используется "-с"
    count = "-n {}".format(count) if "win" in platform else "-c {}".format(count)
    result = {
        "reachable": [],
        "unreachable": []
    }
    for address in addresses:
        code = None
        ip = re.match(RE_IP, str(address))
        if ip is None:
            try:
                ip = socket.gethostbyname(address)
            except gaierror:
                code = 1
        else:
            ip = ip[0]
        if code is None:
            ip = ip_address(ip)
            proc = Popen("ping {ip} -w {timeout} {count}".format(ip=ip, timeout=timeout, count=count), shell=False,
                         stdout=PIPE)
            proc.wait()
            code = proc.returncode
        if code == 0:
            if __name__ == "__main__":
                print("{} Узел доступен".format(address))
            result["reachable"].append(address)
        else:
            if __name__ == "__main__":
                print("{} Узел недоступен".format(address))
            result["unreachable"].append(address)
    return result


if __name__ == "__main__":
    host_ping(["5.255.255.242", "ya.ru", "10.0.0.0", "yssys.ru"])

