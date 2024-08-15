import os
import requests
import time


# Импортируем функции для получения заголовков
from headers import get_headers_opt, get_headers_post

BASE_URL = "https://api.hamsterkombatgame.io"


def debug_print(*args):
    if DEBUG:
        print(*args)


url = f"{BASE_URL}/clicker/buy-upgrade"
def perform_options_request(url):
    headers_opt = get_headers_opt()  # Получаем заголовки OPTIONS запроса
    response = requests.options(url, headers=headers_opt)
    debug_print(f"Status Code: {response.status_code}")
    debug_print("Headers:")
    for header, value in response.headers.items():
        debug_print(f"{header}: {value}")
    if response.content:
        debug_print("\nResponse Body:")
        debug_print(response.content.decode('utf-8'))
        debug_print("\n\n\n")
        
        
def upgrades_for_buy(cardID):
    url = f"{BASE_URL}/clicker/upgrades-for-buy "
    perform_options_request(url)
    headers_post = get_headers_post(Bearer)  # Получаем заголовки POST запроса с актуальным Bearer токеном
    response = requests.post(url, headers=headers_post)
    debug_print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            response_json = response.json()
            debug_print('JSON = ', response_json)
            # Поиск объекта с id "hamster_green_energy"
            for item in response_json["upgradesForBuy"]:
                if item["id"] == cardID:
                    total_cooldown_seconds = item.get("totalCooldownSeconds")
                    print(f"Total Cooldown Seconds for '{cardID}':' {total_cooldown_seconds}")
                    break
            return total_cooldown_seconds
        except json.JSONDecodeError as e:
            debug_print("JSON decode error: ", e)
            return None
    return None        




def make_request():
    url = "https://api.hamsterkombat.io/clicker/buy-upgrade"

    headersOPT = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.1",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "authorization,content-type",
        "Referer": "https://hamsterkombat.io/",
        "Origin": "https://hamsterkombat.io",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=4"
    }

    # Выполнение OPTIONS запроса
    response = requests.options(url, headers=headersOPT)

    # Вывод статуса и заголовков ответа
    print(f"Status Code: {response.status_code}")
    print("Headers:")
    for header, value in response.headers.items():
        print(f"{header}: {value}")

    # Вывод тела ответа, если оно есть
    if response.content:
        print("\nResponse Body:")
        print(response.content.decode('utf-8'))  # декодируем тело ответа как utf-8, если это текстовый формат
        print("\n\n\n")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.1",
        "Accept": "application/json",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://hamsterkombat.io/",
        "Authorization": "Bearer ",
        "Content-Type": "application/json",
        "Origin": "https://hamsterkombat.io",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Priority": "u=1"
    }

    while True:
        # Получаем текущее время в миллисекундах
        current_timestamp = int(time.time() * 1000)

        data = {
            "upgradeId": "sports_integration_0907",
            "timestamp": current_timestamp
        }

        # Преобразуем данные в JSON и выполним POST запрос
        response = requests.post(url, headers=headers, json=data)  # Запрос который может вернуть ошибку

        # Вывод статуса и заголовков ответа
        print(f"Status Code: {response.status_code}")
        print("Headers:")
        for header, value in response.headers.items():
            print(f"{header}: {value}")

        # Вывод тела ответа, если оно есть
        if response.content:
            response_content = response.content.decode('utf-8')
            print("\nResponse Body:")
            print(response_content)  # декодируем тело ответа как utf-8, если это текстовый формат

            # Проверка на наличие ошибки UPGRADE_COOLDOWN
            response_json = json.loads(response_content)
            if response_json.get("error_code") == "UPGRADE_COOLDOWN":
                cooldown_seconds = response_json.get("cooldownSeconds", 0) + 30
                print(f"Cooldown for {cooldown_seconds} seconds. Waiting...")
                time.sleep(cooldown_seconds)
            else:
                print("Request successful or different error received.")
                time.sleep(60)
                
                

        time.sleep(3)

make_request()