import requests
import json
import base64
import time
import random

Bearer = '' #Base
#Bearer = '1722341526688PS1wwJRwa2YmJAjcXNu6fnDvIhdm8RbEtkArmFnPXGaCuqa4WjpQfFX5skd51t8B7341791862' #Luda
#Bearer = "1722342928555Zr3o0M3nUgtLzjMhRzRuXpfEWPDjTzl4l5sM72iznagJRm9dtQNfoq56yeK2ehBE7453211883"
DEBUG = True

BASE_URL = "https://api.hamsterkombatgame.io"
HEADERS_OPT = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.1",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Access-Control-Request-Method": "POST",
    "Access-Control-Request-Headers": "authorization,content-type",
    "Referer": "https://hamsterkombatgame.io/",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Priority": "u=4"
}

HEADERS_POST = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.1",
    "Accept": "application/json",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://hamsterkombatgame.io/",
    "Authorization": f"Bearer {Bearer}",
    "Content-Type": "application/json",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Priority": "u=1"
}

def debug_print(*args):
    if DEBUG:
        print(*args)



def perform_options_request(url):
    response = requests.options(url, headers=HEADERS_OPT)
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
    response = requests.post(url, headers=HEADERS_POST)
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
    response = requests.post(url, headers=HEADERS_POST)
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
    response = requests.post(url, headers=HEADERS_POST)
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
    response = requests.post(url, headers=HEADERS_POST, json=data)
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
    print("user id: ",user_id)
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
        print("isClaimed: ", game_config()," STOP")
    time.sleep(60)

if __name__ == "__main__":
    main()
