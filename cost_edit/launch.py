import asyncio
from playwright.async_api import async_playwright

async def run_playwright(url, cookies, headers):
    if url:
        if url.get('price'):
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                print("Browser launched")

                context = await browser.new_context(
                    user_agent=headers['User-Agent'],
                    extra_http_headers=headers
                )

                for name, value in cookies.items():
                    await context.add_cookies([{
                        'name': name,
                        'value': value,
                        'domain': '.omarket.kz',
                        'path': '/',
                        'secure': False,
                        'httpOnly': False
                    }])

                print("Started", url['url'])
                print()

                page = await context.new_page()
                try:
                    await page.goto(url['url'], wait_until="domcontentloaded", timeout=120000)

                    await page.wait_for_selector('a.btn.btn-primary.btn-sm', timeout=30000)
                    await page.click('a.btn.btn-primary.btn-sm')
                    new_page = await context.wait_for_event('page')
                    await new_page.wait_for_load_state('networkidle')
        
                    await new_page.evaluate("window.scrollBy(0, 400);")
                    
                    #await new_page.wait_for_selector('#price_no_nds_all', timeout=120000)
                    # Передаем цену напрямую через evaluate
                    price_value = int(url['price']) - 1
                    await new_page.evaluate(f"document.getElementById('price_no_nds_all').value = '{price_value}';")


                    await new_page.wait_for_timeout(5000) 
                    filled_value = await new_page.evaluate('document.getElementById("price_no_nds_all").value')
                    if filled_value == str(price_value):
                        print(url["url"], "Form is filled correctly.")
                        print()
                    else:
                        await browser.close()
                        print(url["url"], "Form is not filled correctly.")
                        print()

                    await new_page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                    
                    await new_page.wait_for_timeout(5000)
                    # Кликаем по элементу через JavaScript
                    #await new_page.evaluate("document.querySelector('#save-form-offer').click();")
                    # Максимальное количество попыток
                    max_attempts = 3

                    for attempt in range(max_attempts):
                        # Нажмите на кнопку
                        await new_page.evaluate("document.querySelector('#save-form-offer').click();")

                        # Получите textContent кнопки
                        text_content = await new_page.evaluate("document.querySelector('#save-form-offer').textContent")

                        # Проверяем, если textContent равен "Идет проверка..."
                        if text_content.strip() == "Идет проверка...":
                            print("Кнопка нажата, и текст изменился на 'Идет проверка...'")
                            break

                        # Подождите немного, прежде чем попробовать снова
                        await page.wait_for_timeout(1000)  # Задержка в 1 секунду

                    for _ in range(60):  # 60 попыток по 1 секунде
                        result_text = await new_page.evaluate("document.querySelector('#ajax_result').textContent")

                        if "Данные сохранены" in result_text:
                            break
                        # Ждем 1 секунду перед следующей проверкой
                        await new_page.wait_for_timeout(1000) #Данные сохранены; текст  # Ожидание до 30 секунд
                    # await new_page.wait_for_selector('#save-form-offer', timeout=120000)
                    # await new_page.click('#save-form-offer')
                    print(url, "Changed, Check, done")
                    print()
                    await browser.close()
                


                except Exception as e:
                    print(url["url"], e)
                    print()

                await browser.close()
        else:
            print("Invalid URL or price:", url)


async def process_result(url, cookies, semaphore, headers):
    async with semaphore:
        return await run_playwright(url, cookies, headers)

async def start(results, session):
    headers = {
        'User-Agent': session.headers.get('User-Agent'),
        'Accept-Language': session.headers.get('Accept-Language', 'en-US,en;q=0.9'),
        'Referer': 'https://omarket.kz/'
    }

    semaphore = asyncio.Semaphore(3)
    print("Active")
    tasks = [
        process_result(url, session.cookies.get_dict(), semaphore, headers) for url in results
    ]
    await asyncio.gather(*tasks)
    
