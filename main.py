import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
import os

PRODUCT_URL = 'https://www.amazon.com/Toshiba-Digital-Programmable-Uncooked-One-Touch/dp/B091TW6ND5?ref_=Oct_d_onr_d_678540011&pd_rd_w=SPJ2Z&pf_rd_p=f2b556d9-2905-446e-a142-cdce50e9497c&pf_rd_r=HSZD3389GR835CZ7R9QF&pd_rd_r=5465b42a-3583-436c-9236-e0364af0d8d9&pd_rd_wg=JA7aC&pd_rd_i=B091TW6ND5'
TARGET_PRICE = 85
MY_EMAIL = os.environ.get('MY_EMAIL')
PASSWORD = os.environ.get('PASSWORD')
headers = {
    'Accept-Language': 'en-US',
    'User-Agent': os.environ.get('USER_AGENT'),
}

response = requests.get(url=PRODUCT_URL, headers=headers)
response.raise_for_status()

website = response.text
soup = BeautifulSoup(website, 'lxml')
price = float(soup.find(id='priceblock_ourprice').getText().replace('$', ''))
product_name = soup.find(id='productTitle').getText().strip()

if price < TARGET_PRICE:
    message = f'Subject:Price Alert\n\n{product_name} is now ${price}\n{PRODUCT_URL}'
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=os.environ.get('TO_ADDRS'),
                            msg=message)
