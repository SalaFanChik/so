from datetime import datetime 
import base64 
from config import user_login, user_password

def login(session):
    login_url = 'https://omarket.kz/auth/?backurl=/'
    date_time_str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    base64_encoded = base64.b64encode(date_time_str.encode('utf-8')).decode('utf-8')

    login_data = {
        'tab': 'main',
        'signature': '', 
        'signature_text_raw': base64_encoded,
        'AUTH_FORM': 'Y',
        'TYPE': 'AUTH',
        'backurl': '/auth/?backurl=%2F',
        'USER_LOGIN': user_login,
        'USER_PASSWORD': user_password
    }

    response = session.post(login_url, data=login_data)
    if response.status_code == 200:
        print('Успешный вход!')
        return session.cookies.get_dict()
    else:
        print(f'Ошибка входа: {response.status_code}')
        return None