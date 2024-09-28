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
    {'app_token': 'd02fc404-8985-4305-87d8-32bd4e66bb16', 'promo_id': '61308365-9d16-4040-8bb0-2f4a4c69074c','rnd1':'3','rnd2':'20'},       #Factory World
    {'app_token': 'daab8f83-8ea2-4ad0-8dd5-d33363129640', 'promo_id': 'd02fc404-8985-4305-87d8-32bd4e66bb16','rnd1':'400','rnd2':'800'},    #Among Water
    {'app_token': '4bdc17da-2601-449b-948e-f8c7bd376553', 'promo_id': '4bdc17da-2601-449b-948e-f8c7bd376553','rnd1':'310','rnd2':'720'},    #Count Masters
    {'app_token': 'd2378baf-d617-417a-9d99-d685824335f0', 'promo_id': 'c4480ac7-e178-4973-8061-9ed5b2e17954','rnd1':'720','rnd2':'900'},    #Pin Out Master
    {'app_token': '4bf4966c-4d22-439b-8ff2-dc5ebca1a600', 'promo_id': '4bf4966c-4d22-439b-8ff2-dc5ebca1a600','rnd1':'3720','rnd2':'7440'},  #Hide Ball
    {'app_token': 'bc72d3b9-8e91-4884-9c33-f72482f0db37', 'promo_id': 'bc72d3b9-8e91-4884-9c33-f72482f0db37','rnd1':'450','rnd2':'1220'},   #Bouncemasters
    {'app_token': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af', 'promo_id': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af','rnd1':'450','rnd2':'1220'},   #Stone Age
    {'app_token': '112887b0-a8af-4eb2-ac63-d82df78283d9', 'promo_id': '112887b0-a8af-4eb2-ac63-d82df78283d9','rnd1':'450','rnd2':'1220'},   #Fluff Crusade
    {'app_token': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b', 'promo_id': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b','rnd1':'450','rnd2':'1220'},   #Zoopolis
    {'app_token': 'e68b39d2-4880-4a31-b3aa-0393e7df10c7', 'promo_id': 'e68b39d2-4880-4a31-b3aa-0393e7df10c7','rnd1':'450','rnd2':'1220'},   #Tile Trio
    {'app_token': 'ef319a80-949a-492e-8ee0-424fb5fc20a6', 'promo_id': 'ef319a80-949a-492e-8ee0-424fb5fc20a6','rnd1':'450','rnd2':'1220'},   #Mow and Trim
    {'app_token': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71', 'promo_id': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71','rnd1':'450','rnd2':'1220'},   #Polysphere
    {'app_token': '61308365-9d16-4040-8bb0-2f4a4c69074c', 'promo_id': '61308365-9d16-4040-8bb0-2f4a4c69074c','rnd1':'450','rnd2':'1220'},   #Twerk Race
    {'app_token': '8d1cc2ad-e097-4b86-90ef-7a27e19fb833', 'promo_id': 'dc128d28-c45b-411c-98ff-ac7726fbaea4','rnd1':'450','rnd2':'1220'},   #Merge Away
    {'app_token': 'd1690a07-3780-4068-810f-9b5bbf2931b2', 'promo_id': 'b4170868-cef0-424f-8eb9-be0622e8e8e3','rnd1':'450','rnd2':'1220'},   #Chain Cube 2048
    {'app_token': '', 'promo_id': '','rnd1':'450','rnd2':'1220'},   #
    {'app_token': '', 'promo_id': '','rnd1':'450','rnd2':'1220'},   #
    {'app_token': '', 'promo_id': '','rnd1':'450','rnd2':'1220'},   #
    
    
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
            time.sleep(100)
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
