import os.path
import subprocess


def launcher():
    processes = []
    env = os.environ.copy()
    env['PATH'] = r"C:\Python\gb_async-chat\venv\Scripts"
    action = input("Сколько клиентов запустить: ")
    try:
        action = int(action)
    except ValueError:
        action = None

    if action is not None:
        for i in range(action):
            start = [
                r"C:\Python\gb_async-chat\venv\Scripts\python.exe",
                r"C:\Python\gb_async-chat\gb_chat\client.py",
                "localhost"
            ]
            processes.append(subprocess.Popen(start, env=env, creationflags=subprocess.CREATE_NEW_CONSOLE))
    for process in processes:
        print(process.returncode)
        print(process.stdout)
    while True:
        action = input('Для закрытие клиентов введите "exit"')
        if action.lower() == 'exit':
            while processes:
                process = processes.pop()
                process.kill()


if __name__ == "__main__":
    launcher()
