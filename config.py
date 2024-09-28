import os
from dotenv import load_dotenv
from fake_useragent import UserAgent


ua = UserAgent()


os.environ.pop('USER_LOGIN', None)
os.environ.pop('USER_PASSWORD', None)


# Загрузка переменных окружения
load_dotenv()
user_login = os.getenv('USER_LOGIN')
user_password = os.getenv('USER_PASSWORD')
page_size = int(os.getenv('PAGE_SIZE'))
start_point = int(os.getenv('START_POINT'))
ip_name = os.getenv('IP_NAME')
token = os.getenv('TOKEN')

admins = ["1639491822"]