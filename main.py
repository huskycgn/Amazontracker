from cred import *
from bs4 import BeautifulSoup
import requests
import smtplib


def sendmail(addr, text):
    my_email = MY_MAIL
    my_password = PASSWORD
    connection = smtplib.SMTP('smtp.office365.com', 587)
    connection.starttls()
    connection.login(user=my_email, password=my_password)
    connection.ehlo()
    connection.sendmail(from_addr=my_email,
                        to_addrs=addr,
                        msg=f'Subject: Price Alert!\n\n\n{text}'
                        )


header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/108.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,de-DE;q=0.7,de;q=0.6"
}

response = requests.get(f'https://www.amazon.de/-/en/DS920-Synology-Hard-Drives/dp/B08BG6WM3K/', headers=header)
ap = response.text

# print(ap)

bs = BeautifulSoup(ap, 'html.parser')

spans = bs.findAll(name='span', class_="a-color-price a-text-bold")
desired_price = int(600)
current_price = float(spans[ 0 ].getText().split('€')[ 1 ])

if current_price <= desired_price:
    sendmail(addr='joachim.lehmann@googlemail.com', text=f'Price reached - {current_price}')
