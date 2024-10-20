import requests
import time
import random
import uuid
import os
from dotenv import load_dotenv
from datetime import datetime
import json 

# Загрузка переменных из .env файла
load_dotenv()
Bearer_account = os.getenv('Bearer')
DEBUG = True
LOG_ON = False

# Импортируем функции для получения заголовков
from headers import get_headers_opt, get_headers_post

configurations = [
    {'app_token': 'ed526e8c-e6c8-40fd-b72a-9e78ff6a2054', 'promo_id': 'ed526e8c-e6c8-40fd-b72a-9e78ff6a2054','rnd1':'100','rnd2':'122','game':'Cooking Stories'}, 
    {'app_token': '8d1cc2ad-e097-4b86-90ef-7a27e19fb833', 'promo_id': 'dc128d28-c45b-411c-98ff-ac7726fbaea4','rnd1':'80','rnd2':'100','game':'Merge Away'},
    {'app_token': 'c8e017e2-8817-4d02-bce6-b951e74bb18f', 'promo_id': 'c8e017e2-8817-4d02-bce6-b951e74bb18f','rnd1':'100','rnd2':'122','game':'Snake Run'}, 
    {'app_token': 'd02fc404-8985-4305-87d8-32bd4e66bb16', 'promo_id': 'd02fc404-8985-4305-87d8-32bd4e66bb16','rnd1':'80','rnd2':'120','game':'Factory World'},         
    {'app_token': '4bdc17da-2601-449b-948e-f8c7bd376553', 'promo_id': '4bdc17da-2601-449b-948e-f8c7bd376553','rnd1':'80','rnd2':'100','game':'Count Masters'},         
    #{'app_token': '4bf4966c-4d22-439b-8ff2-dc5ebca1a600', 'promo_id': '4bf4966c-4d22-439b-8ff2-dc5ebca1a600','rnd1':'80','rnd2':'100','game':'Hide Ball'},     
    {'app_token': 'bc72d3b9-8e91-4884-9c33-f72482f0db37', 'promo_id': 'bc72d3b9-8e91-4884-9c33-f72482f0db37','rnd1':'80','rnd2':'100','game':'Bouncemasters'},         
    {'app_token': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b', 'promo_id': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b','rnd1':'80','rnd2':'100','game':'Zoopolis'},     
    {'app_token': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71', 'promo_id': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71','rnd1':'80','rnd2':'100','game':'Polysphere'},     
    {'app_token': 'd1690a07-3780-4068-810f-9b5bbf2931b2', 'promo_id': 'b4170868-cef0-424f-8eb9-be0622e8e8e3','rnd1':'80','rnd2':'100','game':'Chain Cube 2048'},     
    {'app_token': '82647f43-3f87-402d-88dd-09a90025313f', 'promo_id': 'c4480ac7-e178-4973-8061-9ed5b2e17954','rnd1':'125','rnd2':'140','game':'Train Miner'},   
    {'app_token': 'eb518c4b-e448-4065-9d33-06f3039f0fcb', 'promo_id': 'eb518c4b-e448-4065-9d33-06f3039f0fcb','rnd1':'100','rnd2':'122','game':'Infected Frontier'},  
    {'app_token': '53bf823a-948c-48c4-8bd5-9c21903416df', 'promo_id': '53bf823a-948c-48c4-8bd5-9c21903416df','rnd1':'100','rnd2':'122','game':'Tower Defense'},    
    
]


def debug_print(*args):
    if DEBUG:
        # Печать в консоль
        print(*args)

            
            
def LOG(*args):
    if LOG_ON:
        # Формирование имени файла
        current_time = datetime.now()
        file_name = f"PlayGround_{current_time.strftime('%d.%m.%Y_%H-%M')}.txt"

        # Запись в файл с кодировкой utf-8
        try:
            with open(file_name, 'a', encoding='utf-8') as file:
                file.write(' '.join(map(str, args)) + '\n')
        except Exception as e:
            print(f"Error writing to file: {e}")            


def countdown_timer(seconds, text):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = text + " {:02d}:{:02d}".format(mins, secs)
        print(timer, end="\r")  # Перезаписываем строку
        time.sleep(1)
        seconds -= 1
    # Очищаем строку после завершения
    print(' ' * len(timer), end='\r')
    


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
            'clientOrigin': 'android',
            
        }, headers={
            'Content-Type': 'application/json; charset=utf-8',
        })
        response.raise_for_status()
        data = response.json()
        print('login-client [clientToken] = ',data['clientToken'])
        LOG('login-client [clientToken] = ',data['clientToken'])
        return data['clientToken']
    except Exception as error:
        print(f'Ошибка при входе клиента: {error}')
        LOG(f'Ошибка при входе клиента: {error}')
        countdown_timer(20, 'timer after login_client Error')
        return login_client(app_token)  # Рекурсивный вызов


def register_event(token, promo_id, delay):
    event_id = str(uuid.uuid4())
    print ("event_id"+event_id)
    LOG("event_id"+event_id)
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
            print (data)
            LOG(data)
            countdown_timer(random.randint(delay[0], delay[1]), 'next try register_event')
            return register_event(token, promo_id, delay)  # Рекурсивный вызов
        else:
            return True
    except Exception as error:
        print(f'Ошибка при register_event: {error}')
        LOG(f'Ошибка при register_event: {error}')
        countdown_timer(120, 'Задержка после ошибки register_event')
        return register_event(token, promo_id, delay)  # Рекурсивный вызов в случае ошибки




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
            LOG(f'Ошибка при создании кода: {error}')
            countdown_timer(120, 'Задержка после ошибки создании кода')
    return response['promoCode']




 
def gen(app_token, promo_id, delay, game):
    token = login_client(app_token)
    print(f'Token for {app_token}: {token} game = {game}')
    LOG(f'Token for {app_token}: {token} game = {game}')
    countdown_timer(random.randint(delay[0], delay[1]), 'wait for register_event')
    register_event(token, promo_id, delay)
    code_data = create_code(token, promo_id)
    print(f'Сгенерированный код для {app_token} и {promo_id}: {code_data}')
    LOG(f'Сгенерированный код для {app_token} и {promo_id}: {code_data}')
    return code_data








def get_promos():
#-----------------------------------------------###OPTIONS###-----------------------------------------------#  
        resp = requests.options('https://api.hamsterkombatgame.io/interlude/get-promos', 
        headers=get_headers_opt())
        print(f"get_promos [options] Status Code: {resp.status_code}")
        LOG(f"get_promos [options] Status Code: {resp.status_code}")
      
        time.sleep(3)
#-----------------------------------------------###POST###-----------------------------------------------#     
        resp = requests.post('https://api.hamsterkombatgame.io/interlude/get-promos', 
        headers=get_headers_post(Bearer_account))
        print(f"get_promos [post] Status Code: {resp.status_code}")
        LOG(f"get_promos [post] Status Code: {resp.status_code}")
        if resp.content:
            try:
                response_json = resp.json()
                debug_print('get_promos JSON = ', response_json)
                LOG('get_promos JSON = ', response_json)
                return response_json
            except json.JSONDecodeError as e:
                debug_print("JSON decode error: ", e)
                LOG("JSON decode error: ", e)
        countdown_timer(random.randint(10, 20)+10, 'Ждём после JSON decode error')





def apply_promo(code_data):
#-----------------------------------------------###OPTIONS###-----------------------------------------------#  
        
        resp = requests.options('https://api.hamsterkombatgame.io/interlude/apply-promo', 
        headers=get_headers_opt())
        print(f"Status Code: {resp.status_code}")
        LOG(f"Status Code: {resp.status_code}")
      
        time.sleep(3)
#-----------------------------------------------###POST###-----------------------------------------------#     
        data = {"promoCode": code_data}
        resp = requests.post('https://api.hamsterkombatgame.io/interlude/apply-promo', 
        headers=get_headers_post(Bearer_account),json=data)
        
        print(f"Status Code: {resp.status_code}")
        LOG(f"Status Code: {resp.status_code}")
        if resp.content:
            try:
                response_json = resp.json()
                print('apply_promo JSON = ', response_json)
                LOG('apply_promo JSON = ', response_json)
                #return response_json.get('dailyKeysMiniGame', {}).get('isClaimed') TODO
            except json.JSONDecodeError as e:
                debug_print("JSON decode error: ", e)
                LOG("JSON decode error: ", e)
        countdown_timer(random.randint(10, 20)+10, 'Ждём после ввода кода')
        
        
        
        
        

def main():
    promos = get_promos().get("states", None) 
    print('promos JSON = ', promos)
    LOG('promos JSON = ', promos)
    try:
        for config in configurations:
            for state in promos:
                if state.get("promoId") == config['promo_id']:     
                    receive_keys_today = state.get("receiveKeysToday", 0)
                    break
            keys_need = 4 - receive_keys_today        
            print ("Нужно ключей для ", config['game'],' = ',keys_need)
            LOG("Нужно ключей для ", config['game'],' = ',keys_need)
            # promos = get_promos().get("states", None) #Обновляем promos
            # print('promos JSON update = ', promos)
                
            if keys_need > 0:
                for _ in range(keys_need):  # Запуск каждой конфигурации keys_need раза
                    TimeWait = int(config['rnd1']), int(config['rnd2']) 
                    PromoCode = gen(config['app_token'], config['promo_id'], TimeWait, config['game'])
                    countdown_timer(random.randint(15, 45)+3, 'Ждём до ввода кода')
                    apply_promo(PromoCode)
                    countdown_timer(random.randint(60, 320)+3, 'Ждём до следующей иттерации '+config['game'])
            else:
                 print ("Ключей для ", config['game'],'больше не нужно :3')
                 LOG(data)
            
    except Exception as error:
        print(f'Ошибка: {error}')
        LOG(data)

if __name__ == "__main__":
    main()
