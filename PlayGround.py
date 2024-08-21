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
    {'app_token': 'd28721be-fd2d-4b45-869e-9f253b554e50', 'promo_id': '43e35910-c168-4634-ad4f-52fd764a843f','rnd1':'360','rnd2':'720'},    #Bike Ride 3D
    {'app_token': 'd1690a07-3780-4068-810f-9b5bbf2931b2', 'promo_id': 'b4170868-cef0-424f-8eb9-be0622e8e8e3','rnd1':'400','rnd2':'800'},    #Chain Cube 2048
    {'app_token': '74ee0b5b-775e-4bee-974f-63e7f4d5bacb', 'promo_id': 'fe693b26-b342-4159-8808-15e3ff7f8767','rnd1':'310','rnd2':'720'},    #My Clone Army
    {'app_token': '82647f43-3f87-402d-88dd-09a90025313f', 'promo_id': 'c4480ac7-e178-4973-8061-9ed5b2e17954','rnd1':'720','rnd2':'900'},    #Train Miner
    {'app_token': '8d1cc2ad-e097-4b86-90ef-7a27e19fb833', 'promo_id': 'dc128d28-c45b-411c-98ff-ac7726fbaea4','rnd1':'3720','rnd2':'7440'},  #Merge Away
    {'app_token': '61308365-9d16-4040-8bb0-2f4a4c69074c', 'promo_id': '61308365-9d16-4040-8bb0-2f4a4c69074c','rnd1':'450','rnd2':'1220'},   #Twerk Race
    {'app_token': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71', 'promo_id': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71','rnd1':'450','rnd2':'1220'},   #Polysphere
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
            time.sleep(20)
            return register_event(token, promo_id)  # Рекурсивный вызов
        else:
            return True
    except Exception as error:
        time.sleep(20)
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
            time.sleep(20)
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
      
        time.sleep(3)
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
        
        TimeWait = random.randint(10, 20)+10
        print('Ждём ', TimeWait,'c','задержка после ввода кода')
        time.sleep(TimeWait)
        
        
        
        
        

def main():
    try:
        for config in configurations:
            for _ in range(3):  # Запуск каждой конфигурации 4 раза
                PromoCode = gen(config['app_token'], config['promo_id'])
                TimeWait = random.randint(15, 45)+3
                print('Ждём ', TimeWait,'c','до ввода кода')
                time.sleep(TimeWait)
                apply_promo(PromoCode)
                TimeWait = random.randint(int(config['rnd1']), int (config['rnd2']))+3
                print('Ждём ', TimeWait,'c','до генерации следующего кода')
                time.sleep(TimeWait)
    except Exception as error:
        print(f'Ошибка: {error}')

if __name__ == "__main__":
    main()
