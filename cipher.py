import requests
import json
import base64
import time
import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()
Bearer = os.getenv('Bearer')
DEBUG = False

# Импортируем функции для получения заголовков
from headers import get_headers_opt, get_headers_post

BASE_URL = "https://api.hamsterkombatgame.io/clicker"

def debug_print(*args):
    if DEBUG:
        print(*args)

def process_string(encoded_str):
    # Удаляем четвертый символ с начала строки
    modified_str = encoded_str[:3] + encoded_str[4:]
    # Декодируем строку из base64
    decoded_bytes = base64.b64decode(modified_str)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

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

def fetch_config():
    url = f"{BASE_URL}/config"
    perform_options_request(url)
    headers_post = get_headers_post(Bearer)  # Получаем заголовки POST запроса с актуальным Bearer токеном
    response = requests.post(url, headers=headers_post)
    debug_print(response.headers)
    debug_print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            response_json = response.json()
            debug_print('JSON = ', response_json)
            return response_json.get('dailyCipher', {}).get('cipher'), response_json.get('dailyCipher', {}).get('isClaimed')
        except json.JSONDecodeError as e:
            debug_print("JSON decode error: ", e)
            return None
    return None

def claim_daily_cipher(cipher):
    url = f"{BASE_URL}/claim-daily-cipher"
    perform_options_request(url)
    data = {"cipher": cipher}
    headers_post = get_headers_post(Bearer)  # Используем актуальный Bearer токен
    response = requests.post(url, headers=headers_post, json=data)
    debug_print('claim-daily-cipher JSON = ', response.text)
    print('dailyCipher = ', response.json().get('dailyCipher', {}).get('isClaimed'))

def main():
    cipher_base64 = fetch_config()
    if cipher_base64 and cipher_base64[0]:
        debug_print('cipher Base64 = ', cipher_base64[0])
        cipher = process_string(cipher_base64[0])
        print('cipher = ', cipher)
        if not cipher_base64[1]:
            time.sleep(15)
            claim_daily_cipher(cipher) 
        else:
            print("cipher is Claimed")
    else:
        debug_print("Failed to fetch daily cipher.")
    time.sleep(60)

if __name__ == "__main__":
    main()
