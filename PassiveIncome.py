import requests
import json
import base64
import time
import random
import os
import hashlib
import datetime
from dotenv import load_dotenv
import re
from datetime import datetime


# Загрузка переменных из .env файла
load_dotenv()
Bearer = os.getenv('Bearer')
DEBUG = True

# Импортируем функции для получения заголовков
from headers import get_headers_opt, get_headers_post

BASE_URL = "https://api.hamsterkombatgame.io"



def countdown_timer(seconds, text):
    while seconds:
        mins, secs = divmod(seconds, 60)
        timer = text + " {:02d}:{:02d}".format(mins, secs)
        print(timer, end="\r")  # Перезаписываем строку
        time.sleep(1)
        seconds -= 1
    # Очищаем строку после завершения
    print(' ' * len(timer), end='\r')



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
            return response_json.get('dailyKeysMiniGames', {}).get('Candles', {}).get('isClaimed'), response_json.get('dailyKeysMiniGames', {}).get('Candles', {}).get('startDate')
        except json.JSONDecodeError as e:
            debug_print("JSON decode error: ", e)
            return None
    return None



    
def sync():
    url = f"{BASE_URL}/interlude/sync"
    perform_options_request(url)
    headers_post = get_headers_post(Bearer)  # Получаем заголовки POST запроса
    response = requests.post(url, headers=headers_post)
    debug_print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            response_json = response.json()
            debug_print('sync JSON = ', response_json) 
            return response_json
        except json.JSONDecodeError as e:
            debug_print("JSON decode error: ", e)
            return None
    return None    
    
    
    
 
def IP():
    url = f"{BASE_URL}/ip"
    perform_options_request(url)
    headers_post = get_headers_post(Bearer)  # Получаем заголовки POST запроса
    response = requests.get(url, headers=headers_post)
    debug_print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            response_json = response.json()
            debug_print('IP JSON = ', response_json) 
            return response_json
        except json.JSONDecodeError as e:
            debug_print("JSON decode error: ", e)
            return None
    return None        
    
    

def nuxt():
    url = "https://hamsterkombatgame.io/_nuxt/entry.BlVsFSc5.js"
    headers_opt = get_headers_opt()  # Получаем заголовки запроса
  
    try:
        response = requests.get(url, headers=headers_opt)
        debug_print(f"Status Code: {response.status_code}")
        # Проверяем, успешен ли запрос (200 OK)
        if response.status_code == 200 and response.content:
            # Ответ в формате текста, поскольку это JavaScript
            response_nuxt = response.text  
            #print('nuxt JS = ', response_nuxt) 
        else:
            debug_print(f"Request failed with status code: {response.status_code}")  
    except requests.RequestException as e:
        debug_print(f"Request error: {e}")
        return None
        
    pattern = r'buildId\s*:\s*"([a-f0-9\-]+)"'
    match = re.search(pattern, response_nuxt)
    
    if match:
        URL_NoName_JSON = "https://hamsterkombatgame.io/_nuxt/builds/meta/"+match.group(1)+".json"
        print ("URL_NoName_JSON = ",URL_NoName_JSON) 
    else:
        print ("# В entry.BlVsFSc5.js ничего не найдено!")  
        return None
    
    try:
        response = requests.get(URL_NoName_JSON, headers=headers_opt)
        debug_print(f"Status Code: {response.status_code}")
        # Проверяем, успешен ли запрос (200 OK)
        if response.status_code == 200 and response.content:
            # Ответ в формате текста, поскольку это JavaScript
            response_nuxt_json = response.text  
            print(f"{match.group(1)}.json file = ", response_nuxt_json) 
        else:
            debug_print(f"Request failed with status code: {response.status_code}")  
    except requests.RequestException as e:
        debug_print(f"Request error: {e}")
        return None
        
        
        
def get_promos():
#-----------------------------------------------###OPTIONS###-----------------------------------------------#  
        resp = requests.options('https://api.hamsterkombatgame.io/interlude/get-promos', 
        headers=get_headers_opt())
        print(f"get_promos [options] Status Code: {resp.status_code}")
        
        time.sleep(3)
#-----------------------------------------------###POST###-----------------------------------------------#     
        resp = requests.post('https://api.hamsterkombatgame.io/interlude/get-promos', 
        headers=get_headers_post(Bearer))
        print(f"get_promos [post] Status Code: {resp.status_code}")
        if resp.content:
            try:
                response_json = resp.json()
                debug_print('get_promos JSON = ', response_json)
                return response_json
            except json.JSONDecodeError as e:
                debug_print("JSON decode error: ", e)
                
                
                
                
                
def list_tasks():
    url = f"{BASE_URL}/interlude/list-tasks"
    perform_options_request(url)
    headers_post = get_headers_post(Bearer)  # Получаем заголовки POST запроса
    data={'taskId': 'invite_friends_3'}
    response = requests.post(url, headers=headers_post, json=data)
    debug_print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            response_json = response.json()
            debug_print('JSON = ', response_json)
            return response_json
        except json.JSONDecodeError as e:
            debug_print("JSON decode error: ", e)
            return None
    return None





           
        
        

    

def main():
    while True:
        nuxt()
        IP()
        account_info()
        sync()
        get_promos()
        game_config()
        countdown_timer(random.randint(1800, 11000),'До следующего логина: ')
        time.sleep(5)
if __name__ == "__main__":
    main()
