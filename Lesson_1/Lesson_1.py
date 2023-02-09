import os.path
import subprocess

import chardet

# Задание 1:
str_word = "разработка"
print(type(str_word))
uni_word = "\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430"
print(type(uni_word), uni_word)
str_word = "сокет"
print(type(str_word))
uni_word = "\u0441\u043e\u043a\u0435\u0442"
print(type(uni_word), uni_word)
str_word = "декоратор"
print(type(str_word))
uni_word = "\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440"
print(type(uni_word), uni_word)

# Задание 2:
byte_word = b"class"
print(type(byte_word), byte_word, len(byte_word))
byte_word = b"function"
print(type(byte_word), byte_word, len(byte_word))
byte_word = b"method"
print(type(byte_word), byte_word, len(byte_word))

# Задание 3:
# В байтовом типе невозможно записать слова состоящие не из ASCII символов в нашем случае "класс" и "функция"

# Задание 4:
byte_word = "разработка".encode("UTF-8")
print(byte_word)
print(byte_word.decode("UTF-8"))
byte_word = "администрирование".encode("UTF-8")
print(byte_word)
print(byte_word.decode("UTF-8"))
byte_word = "protocol".encode("UTF-8")
print(byte_word)
print(byte_word.decode("UTF-8"))
byte_word = "standard".encode("UTF-8")
print(byte_word)
print(byte_word.decode("UTF-8"))

# Задание 5:
yandex_ping = subprocess.Popen(("ping", "yandex.ru"), stdout=subprocess.PIPE)
youtube_ping = subprocess.Popen(("ping", "youtube.com"), stdout=subprocess.PIPE)

for line in yandex_ping.stdout:
    print(line.decode("cp866"))

for line in youtube_ping.stdout:
    print(line.decode("cp866"))

# Задание 6:
path = os.path.join("Lesson_1", "test_file.txt")
with open(path) as f:
    print(f.encoding)  # По умолчанию python устанавливает кодировку "cp1251"

# Способ узнать кодировку файла с помощью библиотеки chardet
with open(path, "rb") as f:
    byte_line = f.read()
print(chardet.detect(byte_line)["encoding"])

with open(path, "r", encoding="UTF-8") as f:
    for line in f:
        print(line)
