import time
from datetime import datetime

import requests
import selectorlib
from WebScraping.send_mail import send_email
import db

URL = 'https://programmer100.pythonanywhere.com/tours/'
conn = db.connect()


def parse_string(string):
    data = tuple(st.strip() for st in string.split(', '))
    return tuple((*data[:2], datetime.strptime(data[2], '%d.%m.%Y').date()))


def scrape(url):
    response = requests.get(url)
    text = response.text
    return text


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(source)['tours']
    return value


def store(extracted):
    if conn:
        db.insert(conn, extracted)


def read_all():
    if conn:
        return db.fetch_all(conn)


def read_by_date(date):
    if conn:
        return db.query_by_date(conn, date)


if __name__ == '__main__':
    while True:
        s = scrape(URL)
        e = extract(s)

        if e != 'No upcoming tours':
            e = parse_string(e)
            a = read_all()
            if e not in a:
                store([tuple((*e[:2], e[2].strftime('%Y-%m-%d')))])

        time.sleep(2)
