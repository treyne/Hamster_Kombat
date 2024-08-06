import os
import requests
import time
import json

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
