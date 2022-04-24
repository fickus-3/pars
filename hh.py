import requests
from bs4 import BeautifulSoup


URL = 'https://klin.hh.ru/search/vacancy?text=python&currency_code=RUR&items_on_page=100'

headers = {
    'Host': 'hh.ru',
    'User-Agent': 'Safari',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

def extract_max_page():

    hh = requests.get(URL, headers=headers)
    hh_soup = BeautifulSoup(hh.text, 'html.parser')

    pages = []

    paginator = hh_soup.find_all('span', {'class': 'pager-item-not-in-short-range'})

    for page in paginator:
        pages.append(int(page.find('a').text))

    return pages[-1]

def extract_job(html):
    title = html.find('a').text
    link = html.find('a')['href']
    company = html.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).find('a').text
    company = company.strip()
    location = html.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text
    location = location.partition(',')[0]
    return {'title': title, 'company': company, 'location': location, 'link': link}


def extract_hh_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f'страница номер {page}')
        result = requests.get(f'{URL}& page={page}', headers=headers)
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all('div', {'class': 'vacancy-serp-item'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    hh_max_page = extract_max_page()
    hh_jobs = extract_hh_jobs(hh_max_page)
    return hh_jobs
