import requests
import time
import random
import uuid
import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()
Bearer_account = os.getenv('Bearer')
DEBUG = True

# Импортируем функции для получения заголовков
from headers import get_headers_opt, get_headers_post

configurations = [
    {'app_token': 'd28721be-fd2d-4b45-869e-9f253b554e50', 'promo_id': '43e35910-c168-4634-ad4f-52fd764a843f'},
    {'app_token': 'd1690a07-3780-4068-810f-9b5bbf2931b2', 'promo_id': 'b4170868-cef0-424f-8eb9-be0622e8e8e3'},
    {'app_token': '74ee0b5b-775e-4bee-974f-63e7f4d5bacb', 'promo_id': 'fe693b26-b342-4159-8808-15e3ff7f8767'},
    {'app_token': '82647f43-3f87-402d-88dd-09a90025313f', 'promo_id': 'c4480ac7-e178-4973-8061-9ed5b2e17954'}
]

def generate_client_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
    return f"{timestamp}-{random_numbers}"

def login_client(app_token):
    client_id = generate_client_id()
    try:
        response = requests.post('https://api.gamepromo.io/promo/login-client', json={
            'appToken': app_token,
            'clientId': client_id,
            'clientOrigin': 'deviceid'
        }, headers={
            'Content-Type': 'application/json; charset=utf-8',
        })
        response.raise_for_status()
        data = response.json()
        return data['clientToken']
    except Exception as error:
        print(f'Ошибка при входе клиента: {error}')
        time.sleep(5)
        return login_client(app_token)  # Рекурсивный вызов

def register_event(token, promo_id):
    event_id = str(uuid.uuid4())
    try:
        response = requests.post('https://api.gamepromo.io/promo/register-event', json={
            'promoId': promo_id,
            'eventId': event_id,
            'eventOrigin': 'undefined'
        }, headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json; charset=utf-8',
        })
        response.raise_for_status()
        data = response.json()
        if not data.get('hasCode', False):
            time.sleep(5)
            return register_event(token, promo_id)  # Рекурсивный вызов
        else:
            return True
    except Exception as error:
        time.sleep(5)
        return register_event(token, promo_id)  # Рекурсивный вызов в случае ошибки

def create_code(token, promo_id):
    response = None
    while not response or not response.get('promoCode'):
        try:
            resp = requests.post('https://api.gamepromo.io/promo/create-code', json={
                'promoId': promo_id
            }, headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json; charset=utf-8',
            })
            resp.raise_for_status()
            response = resp.json()
        except Exception as error:
            print(f'Ошибка при создании кода: {error}')
            time.sleep(1)
    return response['promoCode']





def gen(app_token, promo_id):
    token = login_client(app_token)
    print(f'Token for {app_token}: {token}')
    
    register_event(token, promo_id)
    code_data = create_code(token, promo_id)
    print(f'Сгенерированный код для {app_token} и {promo_id}: {code_data}')
    
    return code_data






def apply_promo(code_data):
#-----------------------------------------------###OPTIONS###-----------------------------------------------#  
        
        resp = requests.options('https://api.hamsterkombatgame.io/clicker/apply-promo', 
        headers={
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Content-Type': 'application/json; charset=utf-8',
            'priority': 'u=1, i',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36', 
            'referrer': 'https://hamsterkombatgame.io/',
        })
        print(f"Status Code: {resp.status_code}")
      
        time.sleep(1)
#-----------------------------------------------###POST###-----------------------------------------------#     
        data = {"promoCode": code_data}
        resp = requests.post('https://api.hamsterkombatgame.io/clicker/apply-promo', 
        headers={
            'accept': 'application/json',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            "Authorization": f"Bearer {Bearer_account}",
            'Content-Type': 'application/json; charset=utf-8',
            'priority': 'u=1, i',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36', 
            'referrer': 'https://hamsterkombatgame.io/',
        },json=data)
        
        print(f"Status Code: {resp.status_code}")
        if resp.content:
            try:
                response_json = resp.json()
                print('JSON = ', response_json)
                #return response_json.get('dailyKeysMiniGame', {}).get('isClaimed') TODO
            except json.JSONDecodeError as e:
                debug_print("JSON decode error: ", e)
        time.sleep(random.randint(300, 420))
        time.sleep(10)
        
        
        
        

def main():
    try:
        for config in configurations:
            for _ in range(4):  # Запуск каждой конфигурации 4 раза
                PromoCode = gen(config['app_token'], config['promo_id'])
                apply_promo(PromoCode)
    except Exception as error:
        print(f'Ошибка: {error}')

if __name__ == "__main__":
    main()
