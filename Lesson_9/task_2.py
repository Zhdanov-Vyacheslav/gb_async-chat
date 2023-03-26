import ipaddress
import re

from task_1 import host_ping

RE_IP = r"^(?:(?:[01]?\d\d?|2[0-4]\d|25[0-5])(?:\.(?:[01]?\d\d?|2[0-4]\d|25[0-5])){3})$"


def host_range_ping(ip: str, mask=24):
    try:
        mask = int(mask)
        if not isinstance(mask, int) or not 0 <= mask <= 32:
            raise ValueError
    except ValueError:
        print('mask: "{}" incorrect'.format(mask))
        return None
    address = re.match(RE_IP, ip)
    if address is None:
        print('ip: "{}" incorrect'.format(ip))
        return None
    try:
        net = ipaddress.ip_network("{ip}/{mask}".format(ip=address[0], mask=mask))
    except ValueError:
        print('Cannot create a range with ip: "{ip}" and mask: "{mask}"'.format(ip=address[0], mask=mask))
        return None
    return host_ping(addresses=net.hosts())


if __name__ == "__main__":
    host_range_ping(ip="80.0.0.0", mask=24)
    host_range_ping(ip="80.0.0.6", mask=31)
    host_range_ping(ip="80.0.0.0", mask=29)
