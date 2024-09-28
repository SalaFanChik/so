from utils.login_handler import login
from config import ua
import requests
from utils.searching_payload_info import matching


def main():
    with requests.Session() as session:
        session.headers.update({'User-Agent': ua.random})

        login(session)

        # Предполагается, что эта функция уже реализована
        resp = session.get("https://omarket.kz/personal/trade/moffers/edit.php?ID=18117033")
        match = matching(resp.text)

        payload = {
            "PRODUCT_ID": 18117033,
            "bitrix_sessid": match[0],
            "SHOW_TRACE": "",
            "FROM_CALC": "N",
            "price_no_nds_all": "333299"
        }


        resp = session.post("https://omarket.kz/personal/trade/moffers/save_form.php?ID=18117033", data=payload)
        print(resp.status_code)
        # with open("a.html", "w", encoding="utf-8") as f:
        #     f.write(resp.text)

        


main()