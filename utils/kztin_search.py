# from bs4 import BeautifulSoup
# from .check_product_price import fetch_and_parse
# import asyncio

# async def find_product(html_content, session):
#     soup = BeautifulSoup(html_content, 'lxml')

    
#     header_row = soup.find('tr')

    
#     kztin_index = header_row.find_all('th').index(header_row.find('th', string='KZTIN'))

#     rows = soup.find_all('tr')[1:]

#     kztin_values = []
#     for row in rows:
#         cells = row.find_all('td')
#         if len(cells) > kztin_index:
#             kztin_value = cells[kztin_index].get_text(strip=True)
#             kztin_values.append(kztin_value)

#     if kztin_values:
#         kztin_values.pop()
#     tasks = []
#     for value in kztin_values:
#         print(value)
#         if value.isdigit():
#             tasks.append(fetch_and_parse(session, value))
#     print("runned")
#     results = await asyncio.gather(*tasks)
#     for res in results:
#         print(res)

from bs4 import BeautifulSoup

def find_product(html_content):
    soup = BeautifulSoup(html_content, 'lxml')

    header_row = soup.find('tr')
    kztin_index = header_row.find_all('th').index(header_row.find('th', string='KZTIN'))

    rows = soup.find_all('tr')[1:]

    kztin_values = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > kztin_index:
            kztin_value = cells[kztin_index].get_text(strip=True)
            if kztin_value.isdigit():
                kztin_values.append(kztin_value)

    return kztin_values
