# from bs4 import BeautifulSoup

# async def pub_count(html_content, page_size):
#     soup = BeautifulSoup(html_content, 'lxml')

#     published = soup.find(attrs={'id':'published'})

#     published = int((published.find('span').text).strip('()'))
#     if published % page_size == 0:
#         pages = published // page_size
#     else:
#         pages = (published // page_size) + 1 

#     return pages 

from bs4 import BeautifulSoup

def pub_count(html_content, page_size):
    soup = BeautifulSoup(html_content, 'lxml')
    published = soup.find(attrs={'id': 'published'})
    published = int((published.find('span').text).strip('()'))

    if published % page_size == 0:
        pages = published // page_size
    else:
        pages = (published // page_size) + 1 

    return pages
