import requests
import json
import base64
import time
import random
import os
import hashlib
import datetime
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
    url = f"{BASE_URL}/interlude/config"
    perform_options_request(url)
    headers_post = get_headers_post(Bearer)  # Получаем заголовки POST запроса
    response = requests.post(url, headers=headers_post)
    debug_print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            response_json = response.json()
            debug_print('game_config JSON = ', response_json) 
            return response_json.get('dailyKeysMiniGames', {}).get('Tiles', {}).get('isClaimed'), response_json.get('dailyKeysMiniGames', {}).get('Tiles', {}).get('startDate')
        except json.JSONDecodeError as e:
            debug_print("JSON decode error: ", e)
            return None
    return None

def start_keys_minigame():
    url = f"{BASE_URL}/interlude/start-keys-minigame"
    perform_options_request(url)
    headers_post = get_headers_post(Bearer)  # Получаем заголовки POST запроса
    data={'miniGameId': 'Tiles'}
    response = requests.post(url, headers=headers_post, json=data)
    debug_print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            response_json = response.json()
            debug_print('JSON = ', response_json)
            return response_json.get('clickerUser', {}).get('id')
        except json.JSONDecodeError as e:
            debug_print("JSON decode error: ", e)
            return None
    return None

def claim_daily_keys_minigame(cipher):
    url = f"{BASE_URL}/interlude/claim-daily-keys-minigame"
    perform_options_request(url)
    data = {"cipher": cipher, "miniGameId": "Tiles"}
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
    
    
    
    
    
def get_game_cipher(start_number: str):
    magic_index = int(start_number % (len(str(start_number)) - 2))
    res = ""
    for i in range(len(str(start_number))):
        res += '0' if i == magic_index else str(int(random.random() * 10))
    return res    
    
    
    
def get_mini_game_cipher(user_id: int,
                               start_date: str,
                               mini_game_id: str,
                               score: int):
    secret1 = "R1cHard_AnA1"
    secret2 = "G1ve_Me_y0u7_Pa55w0rD"

    start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    start_number = int(start_dt.replace(tzinfo=datetime.timezone.utc).timestamp())
    cipher_score = (start_number + score) * 2

    combined_string = f'{secret1}{cipher_score}{secret2}'

    sig = hashlib.sha256(combined_string.encode()).digest()
    sig = base64.b64encode(sig).decode()

    game_cipher = get_game_cipher(start_number=start_number)

    data = f'{game_cipher}|{user_id}|{mini_game_id}|{cipher_score}|{sig}'

    encoded_data = base64.b64encode(data.encode()).decode()

    return encoded_data    
    
    
    
    


def main():
    user_id = account_info()
    isClaimed,startDate = game_config()
    print("user id: ", user_id)
    if not isClaimed:
        debug_print("isClaimed: ", isClaimed)
        start_keys_minigame()
        game_sleep_time = random.randint(120, 300)
        time.sleep(game_sleep_time)
        cipher = get_mini_game_cipher(user_id=user_id,
                                   start_date=startDate,
                                   mini_game_id='Tiles',
                                   score=random.randint(300, 500))



        print("cipher =  ", cipher)
        status = claim_daily_keys_minigame(cipher)
        print("MiniGame =  ", status)
    else:
        print("isClaimed: ", game_config(), " STOP")
    time.sleep(60)

if __name__ == "__main__":
    main()
