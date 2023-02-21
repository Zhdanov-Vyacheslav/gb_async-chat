import csv
from datetime import datetime
import json
import re
import os

import chardet
import yaml

RE_MAIN = r'^([А-яA-z() ]*): *([A-zА-я 0-9\/,:;()+.-]*)'

DATA = {
    "Изготовитель системы": "os_prod_list",
    "Название ОС": "os_name_list",
    "Код продукта": "os_code_list",
    "Тип системы": "os_type_list"}


def get_data() -> dict:
    files = [file_path for file_path in os.listdir() if file_path.find(".txt") != -1]
    result = {"main_data": []}
    for k, v in DATA.items():
        result["main_data"].append(k)
        result[v] = []
    for file_path in files:
        with open(file_path, "rb") as f:
            byte_line = f.readline()
        encoding = chardet.detect(byte_line)["encoding"]
        with open(file_path, encoding=encoding) as file:
            for line in file:
                parse = re.match(RE_MAIN, line)
                if parse is not None and parse[1] in DATA.keys():
                    result[DATA[parse[1].strip()]].append(parse[2].strip())
    return result


def write_to_csv(csv_path: str):
    main_data = get_data()
    with open(csv_path, "w", encoding="windows-1251") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC, lineterminator="\n")
        writer.writerow(main_data.pop("main_data"))
        writer.writerows(zip(*(v for v in main_data.values())))


def write_order_to_json(*, item, quantity, price, buyer, date: datetime):
    file_path = "orders.json"
    with open(file_path, "rb") as f:
        byte_line = f.readline()
    encoding = chardet.detect(byte_line)["encoding"]
    with open(file_path, encoding=encoding) as f:
        orders = json.load(f)
    order = {
        "item": item,
        "quantity": quantity,
        "price": price,
        "buyer": buyer,
        "date": str(date)
    }

    orders["orders"].append(order)
    with open(file_path, "w", encoding=encoding) as f:
        json.dump(orders, f, indent=4)


def write_to_yaml(data: dict):
    with open("data.yaml", "w", encoding="utf-8") as f:
        # Если allow_unicode=True, работает только в случае если символ есть в кодировке, к примеру "¥" нет в 1251
        # из-за чего запись в файл будет прервана ошибкой
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)


#  Проверка созданного yaml
def check_yaml(data: dict):
    with open("data.yaml", encoding="utf-8") as f:
        f_data = yaml.load(f, yaml.FullLoader)
        print(data == f_data)


write_to_csv("main_data.csv")
write_order_to_json(item=1, quantity=2, price=3, buyer=4, date=datetime.now())
task_3_data = {
    1: ["1", "фывфыв"],
    2: 0,
    3: {
        4: "12€",
        5: "34¥",
        6: "41₽"
    }
}
write_to_yaml(task_3_data)
check_yaml(task_3_data)  # Проверка созданного yaml
