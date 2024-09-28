import io
import requests
from multiprocessing import Pool
from utils.published_count import pub_count
from utils.kztin_search import find_product
from utils.check_product_price import fetch_and_parse, parse_price
from cost_edit.launch import start 
import asyncio 
from config import user_login, user_password, ua, page_size, start_point, ip_name, admins 
from utils.login_handler import login 
from bot import bot, start_bot
import json
from aiogram.types.input_file import FSInputFile


# Функция для входа


def fetch_pages_with_kztin(session, page_num):
    url = f"https://omarket.kz/personal/trade/moffers/index.php?TYPE=&search%5Bstatus%5D=3&is_search=Y&PAGE_SIZE={page_size}&nav-more-news=page-{page_num}"
    response = session.get(url)
    return response.text

def read_urls_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f.readlines()]


def main():
    with requests.Session() as session:
        session.headers.update({'User-Agent': ua.random})

        logged_in_page_content = login(session)
        if logged_in_page_content:
            print("fetching Started")
            if not read_urls_from_file('links.txt'):
                first_page_content = fetch_pages_with_kztin(session, start_point)
                kztin_values = find_product(first_page_content)


                with Pool(processes=5) as pool:
                    print("pool Started")
                    results = pool.starmap(fetch_and_parse, [(session, kztin) for kztin in kztin_values])
                    print("pool Ended")

                for res in results:
                    print(res)

                pages = pub_count(first_page_content, page_size)

                tasks = []
                for i in range(2, pages + 1):
                    tasks.append(fetch_pages_with_kztin(session, i))


                for page_content in tasks:
                    kztin_values = find_product(page_content)
                    with Pool(processes=5) as pool:
                        results = pool.starmap(fetch_and_parse, [(session, kztin) for kztin in kztin_values])
                    for res in results:
                        print(res)
            asyncio.run(start_checking(session))



async def start_checking(session):
    urls = read_urls_from_file('links.txt')
    asyncio.create_task(start_bot())
    while True: 
        print("Начало искать")
        with Pool(processes=5) as pool:
            results = pool.starmap(parse_price, [(session, url, ip_name) for url in urls])
        results = [result for result in results if result is not None]
        # Convert each dictionary to a string
        results_as_strings = [json.dumps(result, ensure_ascii=False) + "\n" for result in results]

        with open("results.txt", "w", encoding="utf-8") as f:
            f.writelines(results_as_strings)
        
        document = FSInputFile('results.txt')
        if results:
            for i in admins:
                await bot.send_document(i, document)
            await start(results, session)   
        else:
            print("Пока не перебили")


# def main():
#     with requests.session() as session:
#         session.headers.update({'User-Agent': ua.random})

#         login(session)
#         testing(session)


if __name__ == '__main__':

    main()
    #asyncio.run(start_checking)