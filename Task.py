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





def check_task(idTask):
    url = f"{BASE_URL}/interlude/check-task"
    perform_options_request(url)
    headers_post = get_headers_post(Bearer)  # Получаем заголовки POST запроса
    data={'taskId': idTask}
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
    # check_task()
    tasks = list_tasks()
    for task in tasks['tasks']:
        if not task['isCompleted']:
            task_id = task['id']
            check_task(task_id)
            time.sleep(5)
    time.sleep(60)

if __name__ == "__main__":
    main()
