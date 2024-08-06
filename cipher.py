import requests
import json
import base64
import time

Bearer = ''
DEBUG = True

BASE_URL = "https://api.hamsterkombatgame.io/clicker"
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

def process_string(encoded_str):
    # Удаляем четвертый символ с начала строки
    modified_str = encoded_str[:3] + encoded_str[4:]
    # Декодируем строку из base64
    decoded_bytes = base64.b64decode(modified_str)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str

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

def fetch_config():
    url = f"{BASE_URL}/config"
    perform_options_request(url)
    response = requests.post(url, headers=HEADERS_POST)
    print(response.headers)
    debug_print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            response_json = response.json()
            debug_print('JSON = ', response_json)
            return response_json.get('dailyCipher', {}).get('cipher'),response_json.get('dailyCipher', {}).get('isClaimed')
        except json.JSONDecodeError as e:
            debug_print("JSON decode error: ", e)
            return None
    return None

def claim_daily_cipher(cipher):
    url = f"{BASE_URL}/claim-daily-cipher"
    perform_options_request(url)
    data = {"cipher": cipher}
    response = requests.post(url, headers=HEADERS_POST, json=data)
    debug_print('claim-daily-cipher = ', response.text)

def main():
    cipher_base64 = fetch_config()
    if cipher_base64[0]:
        debug_print('cipher Base64 = ', cipher_base64[0])
        cipher = process_string(cipher_base64[0])
        debug_print('cipher = ', cipher)
        if not cipher_base64[1]:
            time.sleep(15)
            claim_daily_cipher(cipher) 
        else:
            debug_print("cipher is Claimed")
    else:
        debug_print("Failed to fetch daily cipher.")
    time.sleep(60)

if __name__ == "__main__":
    main()
