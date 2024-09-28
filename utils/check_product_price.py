# import asyncio
# import aiohttp
# from bs4 import BeautifulSoup


# async def fetch_and_parse(session, kztin):
#     url = f"https://omarket.kz/search/?q={kztin}&send=Y&r=Y"
#     async with session.get(url) as response:
#         html = await response.text() 
#         soup = BeautifulSoup(html, "html.parser")

#         a_tag = soup.find('a', class_='name')
#         if a_tag:
#             href = a_tag.get("href") if a_tag else None
#             print({kztin: href})
#             return {kztin: href}
#         else:
#             return {kztin: "Не найдено"}

import re
from bs4 import BeautifulSoup
from .searching_payload_info import matching 

def fetch_and_parse(session, kztin):
    #direct url 
    url = f"https://omarket.kz/search/?q={kztin}&send=Y&r=Y"
    response = session.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    a_tag = soup.find('a', class_='name')
    if a_tag:
        href = a_tag.get("href")
        full_url = f"https://omarket.kz{href}"
        print({kztin: full_url})
        
        with open('links.txt', 'a', encoding='utf-8') as f:
            f.write(full_url + '\n')

        return {kztin: full_url}
    else:
        return {kztin: "Не найдено"}



def parse_price(session, url, ip_name):
    try:
        response = session.get(url)
        html = response.text
        main_url = "https://omarket.kz/catalog/ajax_load_offers.php"
        match = matching(html) 

        payload = {
            "PRODUCT_ID": match[1],
            "bitrix_sessid": match[0],
            "SHOW_TRACE": "",
            "FROM_CALC": "N"
        }

        resp = session.post(main_url, data=payload)
        
        html = resp.text
        
        soup = BeautifulSoup(html, "html.parser")

        first_tr = soup.find('tbody').find('tr')

        first_td = first_tr.find('td')
        name = first_td.find("a").text.strip()
        if name != ip_name:
            second_td = first_tr.find_all('td')[1]
            price_str = second_td.get_text(strip=True).replace('\xa0', '').replace(' ', '')  # Удаление &nbsp; и пробелов
            print(url, name)
            price_match = re.search(r'(\d+)', price_str)
            if price_match:
                price = int(price_match.group(1))
                return {"url": url, "name": name, "price": price}

    except Exception as e:
        #Добавить ошибку в логи 
        #print({url: f"Error: {str(e)}"})
        return {url: url, "error": f"Error: {str(e)}"}