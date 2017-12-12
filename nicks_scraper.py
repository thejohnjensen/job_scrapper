"""Scrape jobs from stack overflow."""
from bs4 import BeautifulSoup as Soup
import requests
from datetime import datetime


DOMAIN = 'https://www.stackoverflow.com'
JOBS = []


def get_webpage(url):
    """Get the webpage."""
    response = requests.get(url)
    html = Soup(response.content, 'html.parser')
    return html


def retrieve_job_items(html):
    """Retrieve a job item and turn it into a dict."""
    items = html.find_all('div', {'class': '-job-item'})
    for item in items:
        tags_div = item.find('div', {'class': '-tags'})
        if tags_div:
            tags = tags_div.text
            if "python" in tags:
                JOBS.append(parse_item_into_dict(item))


def parse_item_into_dict(item):
    """Turn an item found from Stackoverflow into a dict."""
    title_tag = item.find('a', {'class': 'job-link'})
    title = title_tag.text
    posted_date = item.find('p', {'class': '-posted-date'}).text
    link = title_tag.attrs['href']
    company_name = item.find('div', {'class': '-company'}).find('div', {'class': '-name'}).text
    location = item.find('div', {'class': '-company'}).find('div', {'class': '-location'}).text
    return {
        "title": title.strip().replace(',', '&comma;'),
        "posted_date": posted_date.strip(),
        "link": DOMAIN + link,
        "company_name": company_name.strip().replace(',', '&comma;'),
        "location": location.strip()[2:].replace('\r\n', '').replace(',', '&comma;')
    }


def compile_to_csv():
    """Build CSV file out of scraping results."""
    today = datetime.now().strftime('%b-%d-%Y').lower()
    with open('results/{}.csv'.format(today), 'w') as f:
        lines = []
        for item in JOBS:
            lines.append('{},{},{},{},{}\n'.format(
                item['title'],
                item['posted_date'],
                item['company_name'],
                item['location'],
                item['link']
            ))
        f.writelines(lines)


if __name__ == '__main__':
    for i in range(1, 11):
        print('Gathering page {}...'.format(i))
        url = 'https://www.stackoverflow.com/jobs?pg={}'.format(i)
        html = get_webpage(url)
        retrieve_job_items(html)

    print('Writing to file...')
    compile_to_csv()