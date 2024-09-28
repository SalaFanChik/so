from playwright.async_api import async_playwright
import asyncio
import requests
from config import ua, user_login, user_password
import base64
from datetime import datetime
from time import sleep
from utils.login_handler import login

# Функция для авторизации с использованием requests.Session
# def login(session):
#     login_url = 'https://omarket.kz/auth/?backurl=/'
#     date_time_str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
#     base64_encoded = base64.b64encode(date_time_str.encode('utf-8')).decode('utf-8')

#     login_data = {
#         'tab': 'main',
#         'signature': '', 
#         'signature_text_raw': base64_encoded,
#         'AUTH_FORM': 'Y',
#         'TYPE': 'AUTH',
#         'backurl': '/auth/?backurl=%2F',
#         'USER_LOGIN': user_login,
#         'USER_PASSWORD': user_password
#     }

#     response = session.post(login_url, data=login_data)
#     if response.status_code == 200:
#         print('Успешный вход!')
#         return session.cookies.get_dict()  # Возвращаем куки как словарь
#     else:
#         print(f'Ошибка входа: {response.status_code}')
#         return None


# Функция для запуска Playwright с передачей куков и заголовков
async def run_playwright(url, cookies, headers):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        
        context = await browser.new_context(
            user_agent=headers['User-Agent'],  # Передаем User-Agent
            extra_http_headers=headers  # Передаем другие заголовки
        )
        for name, value in cookies.items():
            await context.add_cookies([{
                'name': name,  # Имя куки
                'value': value,  # Значение куки
                'domain': '.omarket.kz',  # Домен для куков
                'path': '/',  # Путь по умолчанию
                'secure': False,  # Установите True, если сайт использует HTTPS
                'httpOnly': False  # Если куки HttpOnly
            }])

        # Открываем страницу
        page = await context.new_page()
        await page.goto(url)
        
        # Ждем полной загрузки страницы
        await page.wait_for_load_state("load")
        sleep(1000)
        content = await page.content()  # Получаем контент страницы
        await browser.close()
        return content


async def ss(session):
    session.headers.update({'User-Agent': ua.random}) 
    
    cookies = session.cookies.get_dict()
    print(cookies)

    if cookies:
        headers = {
            'User-Agent': session.headers.get('User-Agent'),
            'Accept-Language': session.headers.get('Accept-Language', 'en-US,en;q=0.9'),
            'Referer': 'https://omarket.kz/'
        }

        url = 'https://omarket.kz/'  
        await run_playwright(url, cookies, headers)
    else:
        print("Ошибка авторизации, куки не были получены.")
