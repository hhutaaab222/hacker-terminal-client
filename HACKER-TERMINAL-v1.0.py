import random
import json
import os
import time
import requests

SERVER_URL = "http://127.0.0.1:5000"

def server_request(endpoint, payload):
    response = requests.post(
        SERVER_URL + endpoint,
        json=payload,
        timeout=5
    )
    response.raise_for_status()
    return response.json()

os.system("")
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
RESET = "\033[0m"
def type_text(text, delay=0.025):
    for char in text:
        print(char,end="", flush=True)
        time.sleep(delay)
    print()
def boot_sequence():
    os.system("cls")

    print(GREEN + r"""
 _   _    _    ____ _  _______ ____  
| | | |  / \  / ___| |/ / ____|  _ \ 
| |_| | / _ \| |   | ' /|  _| | |_) |
|  _  |/ ___ \ |___| . \| |___|  _ < 
|_| |_/_/   \_\____|_|\_\_____|_| \_\
""" + RESET)

    steps = [
        "Initializing system...",
        "Loading player modules...",
        "Loading save data...",
        "Preparing terminal..."
    ]

    for step in steps:
        type_text(CYAN + "[ .... ] " + step + RESET, 0.025)
        time.sleep(0.4)

    print(GREEN + "\n[  OK  ] SYSTEM READY" + RESET)
    time.sleep(0.8)


SERVER_URL = "https://hacker-terminal.onrender.com"

authorized = False
os.system("cls")

while not authorized:
    print(GREEN + "\n╔══════════════════════════════╗" + RESET)
    print(GREEN + "║     HACKER TERMINAL v1.0     ║" + RESET)
    print(GREEN + "╚══════════════════════════════╝" + RESET)

    print("\n1. Войти")
    print("2. Зарегистрироваться")
    print("3. Выход")

    choice = input("\nВыбери действие: ").strip()

    if choice == "3":
        print("Выход из игры...")
        exit()

    elif choice in ("1", "2"):
        login = input("Введите логин: ").strip()
        user_passwd = input("Введите пароль: ")

        if choice == "2":
            endpoint = "/register"
        else:
            endpoint = "/login"

        try:
            response = requests.post(
                SERVER_URL + endpoint,
                json={
                    "username": login,
                    "password": user_passwd
                },
                timeout=5
            )

            data = response.json()

            if response.ok:
                print(GREEN + data.get("message", "Успешно!") + RESET)
                authorized = True
            else:
                print(RED + data.get("error", "Ошибка входа") + RESET)

        except requests.RequestException:
            print(RED + "Не удалось подключиться к серверу!" + RESET)

    else:
        print(RED + "Выбери 1, 2 или 3." + RESET)

if not authorized:
    exit()



boss_wins = 0
exp = 0
exp_to_next_level = 200
balance = 500
bonus_reward = False
level = 1

save_file = f"save_{login}.json"

if os.path.exists(save_file):
    print("Найдено сохранение игрока!")
else:
    print("Новый игрок! Создаём новое сохранение.")

def save_game():
    data = {
        "balance": balance,
        "level": level,
        "exp": exp,
        "boss_wins": boss_wins,
        "bonus_reward": bonus_reward
    }

    try:
        result = server_request("/save", {
            "username": login,
            "password": user_passwd,
            "game_data": data
        })

        print(GREEN + result["message"] + RESET)

    except requests.RequestException:
        print(RED + "Не удалось сохранить прогресс на сервере!" + RESET)

def load_game():
    global balance, level, exp, boss_wins, bonus_reward

    if   os.path.exists(save_file):
        with open(save_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        balance = data.get("balance", balance)
        level = data.get("level", level)
        exp = data.get("exp", exp)
        boss_wins = data.get("boss_wins", boss_wins)
        bonus_reward = data.get("bonus_reward", bonus_reward)

        print("Прогресс загружен!")
def check_level_up():
    global exp,level

    while exp >= exp_to_next_level:
        exp -= exp_to_next_level
        level += 1
        print(f"Вы достигли {level} уровня!")
boot_sequence()

print(WHITE + "\nДобро пожаловать в HACKER TERMINAL!" + RESET)
print(CYAN + "Введти help, чтоб увидеть команды." + RESET)

try:
    game_data = server_request("/load", {
        "username": login,
        "password": user_passwd
    })

    balance = game_data["balance"]
    level = game_data["level"]
    exp = game_data["exp"]
    boss_wins = game_data["boss_wins"]
    bonus_reward = game_data["bonus_reward"]

    print(GREEN + "Прогресс загружен с сервера!" + RESET)

except requests.RequestException:
    print(RED + "Не удалось загрузить прогресс с сервера!" + RESET)
    exit()

while True:
    command = input(RED + f"\nroot@{login}:~$ " + RESET).lower()
    if command == "help":
        print(CYAN + "\n╔════════════ COMMANDS ════════════╗" + RESET)
        print(GREEN + "  help     " + WHITE + "- Список команд")
        print(GREEN + "  profile  " + WHITE + "- Профиль игрока")
        print(GREEN + "  missions " + WHITE + "- Выполнение миссий")
        print(GREEN + "  boss     " + WHITE + "- Бой с BLACK ICE")
        print(GREEN + "  shop     " + WHITE + "- Магазин")
        print(GREEN + "  clear    " + WHITE + "- Очистить терминал")
        print(GREEN + "  exit     " + WHITE + "- Выход")
        print(CYAN + "╚═════════════════════════════════╝" + RESET)
    elif command == "":
        print(RED + "Вы нечего не ввели" + RESET)
    elif command == "clear":
        os.system("cls")
        continue
    elif command == "profile":
        filled = int((exp / exp_to_next_level) * 20)
        empty = 20 - filled
        exp_bar = "█" * filled + "░" * empty

        print(CYAN + "\n╔══════════ PLAYER PROFILE ══════════╗" + RESET)
        print(f"{GREEN}  USERNAME: {login}{RESET}")
        print(f"{YELLOW}  LEVEL:    {level}{RESET}")
        print(f"{GREEN}  BALANCE:  {balance} coins{RESET}")
        print(f"{CYAN}  BOSSES DEFEATED: {boss_wins}{RESET}")
        print(f"{WHITE}  EXP: [{exp_bar}] {exp}/{exp_to_next_level}{RESET}")
        print(CYAN + "╚════════════════════════════════════╝" + RESET)

    elif command == "exit":
        print("Завершение работы...")
        break
    
        
    elif command == "missions":
        
        secret_number = random.randint(1, 10)
        print("=== МИССИЯ: УГАДАЙ ЧИСЛО ===\n(За каждую выигранную игру ты получаешь по 25 exp)")
        print("Я загадал число от 1 до 10")
        won = False
        attempt = 0
        while attempt < 3:
            try:
                user = int(input("Введи свое число: "))
            except ValueError:
                print("Нужно вводить цифры")
                continue
            attempt += 1
            if user == secret_number:
                if bonus_reward:
                    balance += 150
                    bonus_reward = False
                    exp += 25
                    check_level_up()
                    print("Молодец! Ты получил 150 коинов с бонусом!")
                else:
                    balance += 100
                    exp += 25
                    check_level_up()
                    print("Молодец! ты получил 100 коинов!")
                won = True
                break
            elif user < secret_number:

                print("Больше!")
            elif user > secret_number:
                print("Меньше!")
        if not won:
            print("\nЗакончились попытки!")
            print(f"Загаданное число было: {secret_number}")

    elif command == "shop":
        print(CYAN + f"\n=== ХАКАРСКИЙ МАГАЗИН ===\n* 1.Уровень хакера - 300 коинов\n* 2.Доп.Награда - 200 коинов\n\nТвой баланс: {balance}" + RESET)
        item = input(GREEN + "Что покупаем? (1/2 или back): ").lower()
        if item == "back":
            print("Возвращаемся назад...")
            continue
        elif item == "1":
            if balance >= 300:
                balance -= 300
                level += 1
                print(f"Вы купили уровень\nТеперь ваш уровен {level}")
            else:
                print(RED + "Недостаточно средств!" + RESET)

        elif item == "2":
            if bonus_reward:
                print("Бонус активен!")
            elif balance >= 200:
                balance -= 200
                print("Ты купил Дополнительную награду!")
                bonus_reward = True
            else:
                print(RED + "Недостаточно средств!")
        else:
            print("Такого выбора нет!")
    elif command == "boss":
        player_hp = 120
        boss_hp = 150
        player_damage = 30
        boss_damage = 20
        while player_hp > 0 and boss_hp > 0:
            print(f"Здаровье игрока: {player_hp}")
            print(f"Здаровье босса: {boss_hp}")
            action = input(RED + "Твой ход: attack - атаковать: " + RESET).lower()
            if action != "attack":
                print(RED + "Вы промахнулись!" + RESET)
                continue
            boss_hp -= player_damage
            print(GREEN + f"Ты нанес BLACK ICE {player_damage} урона!" + RESET)
            if boss_hp <= 0:
                balance += 500
                exp += 100
                boss_wins += 1
                check_level_up()
                print(CYAN + "\nБосс повержен!\nНаграда: 500 коинов!\nТы получил 100 EXP за убийство босса!" + RESET)
                break
            crit_chance = random.randint(1, 100)
            if crit_chance <= 45:
                player_hp -= 35
                print(RED + "Босс нанес критический удар!" + RESET)
            else:
                player_hp -= boss_damage
                print("Босс атаковал! -20 HP")
        if player_hp <= 0:
            print("Ты проиграл! BLACK ICE победил.")

            
    else:
        print("Неизвестная команда. Введи help")
save_game()
