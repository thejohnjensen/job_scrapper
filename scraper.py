import requests
from bs4 import BeautifulSoup

url = 'https://stackoverflow.com/jobs'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html)
posts = soup.find('div', attrs={'class': 'listResults'})

for div in posts.find_all('div', attrs={'class': '-job-item'}):
    for job in div.find_all('div', attrs={'class': '-job-summary'}):
        if job.find('a', attrs={'class': 'post-tag'}).string == 'python':
            print(job)