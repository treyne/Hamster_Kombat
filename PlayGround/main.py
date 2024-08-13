import asyncio
import aiohttp
import time
import random
import uuid

configurations = [
    {'app_token': 'd28721be-fd2d-4b45-869e-9f253b554e50', 'promo_id': '43e35910-c168-4634-ad4f-52fd764a843f'},
    {'app_token': 'd1690a07-3780-4068-810f-9b5bbf2931b2', 'promo_id': 'b4170868-cef0-424f-8eb9-be0622e8e8e3'},
    {'app_token': '74ee0b5b-775e-4bee-974f-63e7f4d5bacb', 'promo_id': 'fe693b26-b342-4159-8808-15e3ff7f8767'},
    {'app_token': '82647f43-3f87-402d-88dd-09a90025313f', 'promo_id': 'c4480ac7-e178-4973-8061-9ed5b2e17954'}
]

async def generate_client_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(19))
    return f"{timestamp}-{random_numbers}"

async def login_client(app_token):
    client_id = await generate_client_id()
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post('https://api.gamepromo.io/promo/login-client', json={
                'appToken': app_token,
                'clientId': client_id,
                'clientOrigin': 'deviceid'
            }, headers={
                'Content-Type': 'application/json; charset=utf-8',
            }) as response:
                data = await response.json()
                return data['clientToken']
        except Exception as error:
            print(f'Ошибка при входе клиента: {error}')
            await asyncio.sleep(5)
            return await login_client(app_token)  # Recursive call

async def register_event(token, promo_id):
    event_id = str(uuid.uuid4())
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post('https://api.gamepromo.io/promo/register-event', json={
                'promoId': promo_id,
                'eventId': event_id,
                'eventOrigin': 'undefined'
            }, headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json; charset=utf-8',
            }) as response:
                data = await response.json()
                if not data.get('hasCode', False):
                    await asyncio.sleep(5)
                    return await register_event(token, promo_id)  # Recursive call
                else:
                    return True
        except Exception as error:
            await asyncio.sleep(5)
            return await register_event(token, promo_id)  # Recursive call in case of error

async def create_code(token, promo_id):
    async with aiohttp.ClientSession() as session:
        response = None
        while not response or not response.get('promoCode'):
            try:
                async with session.post('https://api.gamepromo.io/promo/create-code', json={
                    'promoId': promo_id
                }, headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': 'application/json; charset=utf-8',
                }) as resp:
                    response = await resp.json()
            except Exception as error:
                print(f'Ошибка при создании кода: {error}')
                await asyncio.sleep(1)
        return response['promoCode']

async def gen(app_token, promo_id):
    token = await login_client(app_token)
    print(f'Token for {app_token}: {token}')
    
    await register_event(token, promo_id)
    code_data = await create_code(token, promo_id)
    print(f'Сгенерированный код для {app_token} и {promo_id}: {code_data}')
    with open ("codoe.txt", "a")
        file.write(code_data)

async def main():
    try:
        tasks = []
        for config in configurations:
            for _ in range(4):  # Запуск каждой конфигурации 4 раза
                tasks.append(gen(config['app_token'], config['promo_id']))
        await asyncio.gather(*tasks)
    except Exception as error:
        print(f'Ошибка: {error}')

asyncio.run(main())
