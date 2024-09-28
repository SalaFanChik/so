import re 

def matching(content):
    match = re.search(r"bitrix_sessid':'(.*?)'", content)
    if match:
        bitrix_sessid_value = match.group(1)
    
    match = re.search(r'PRODUCT_ID=(\d+)', content)
    if match:
        product_id = match.group(1)
    return bitrix_sessid_value, product_id
