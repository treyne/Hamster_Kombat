import requests
import json
import base64
import time
import random
import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()
Bearer = os.getenv('Bearer')
DEBUG = True

# Импортируем функции для получения заголовков
from headers import get_headers_opt, get_headers_post

BASE_URL = "https://api.hamsterkombatgame.io"

def debug_print(*args):
    if DEBUG:
        print(*args)

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

def account_info():
    url = f"{BASE_URL}/auth/account-info"
    perform_options_request(url)
    headers_post = get_headers_post(Bearer)  # Получаем заголовки POST запроса с актуальным Bearer токеном
    response = requests.post(url, headers=headers_post)
    debug_print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            response_json = response.json()
            debug_print('JSON = ', response_json)
            return response_json.get('accountInfo', {}).get('id')
        except json.JSONDecodeError as e:
            debug_print("JSON decode error: ", e)
            return None
    return None

def game_config():
    url = f"{BASE_URL}/clicker/config"
    perform_options_request(url)
    headers_post = get_headers_post(Bearer)  # Получаем заголовки POST запроса
    response = requests.post(url, headers=headers_post)
    debug_print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            response_json = response.json()
            debug_print('JSON = ', response_json)
            return response_json.get('dailyKeysMiniGame', {}).get('isClaimed')
        except json.JSONDecodeError as e:
            debug_print("JSON decode error: ", e)
            return None
    return None

def start_keys_minigame():
    url = f"{BASE_URL}/clicker/start-keys-minigame"
    perform_options_request(url)
    headers_post = get_headers_post(Bearer)  # Получаем заголовки POST запроса
    response = requests.post(url, headers=headers_post)
    debug_print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            response_json = response.json()
            debug_print('JSON = ', response_json)
            return response_json.get('clickerUser', {}).get('id'),response_json.get('dailyCipher', {}).get('isClaimed')
        except json.JSONDecodeError as e:
            debug_print("JSON decode error: ", e)
            return None
    return None

def claim_daily_keys_minigame(cipher):
    url = f"{BASE_URL}/clicker/claim-daily-keys-minigame"
    perform_options_request(url)
    data = {"cipher": cipher}
    headers_post = get_headers_post(Bearer)  # Получаем заголовки POST запроса
    response = requests.post(url, headers=headers_post, json=data)
    debug_print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            response_json = response.json()
            debug_print('JSON = ', response_json)
            return response_json.get('dailyKeysMiniGame', {}).get('isClaimed')
        except json.JSONDecodeError as e:
            debug_print("JSON decode error: ", e)
            return None
    return None

def main():
    user_id = account_info()
    print("user id: ", user_id)
    if not game_config():
        debug_print("isClaimed: ", game_config())
        start_keys_minigame()
        game_sleep_time = random.randint(12, 26)
        time.sleep(game_sleep_time)
        cipher_prepare = f"0{game_sleep_time}{random.randint(10000000000, 99999999999)}"[:10]
        cipher_prepare = f"{cipher_prepare}|{user_id}"
        cipher = base64.b64encode(cipher_prepare.encode()).decode()
        print("cipher =  ", cipher)
        status = claim_daily_keys_minigame(cipher)
        print("MiniGame =  ", status)
    else:
        print("isClaimed: ", game_config(), " STOP")
    time.sleep(60)

if __name__ == "__main__":
    main()
