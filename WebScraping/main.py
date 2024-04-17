import requests
import selectorlib

URL = 'https://programmer100.pythonanywhere.com/tours/'

def scrape(url):
    response = requests.get(url)
    text = response.text
    return text


if __name__ == '__main__':
    print(scrape(URL))