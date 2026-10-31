import pandas as pd
from bs4 import BeautifulSoup as bs
import requests

urls = [
    'https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-acting/top-grossing-leading-stars',
    'https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-acting/top-grossing-leading-stars/101',
    'https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-acting/top-grossing-leading-stars/201',
    'https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-acting/top-grossing-leading-stars/301',
    'https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-acting/top-grossing-leading-stars/401',
    'https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-acting/top-grossing-leading-stars/501',
    'https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-acting/top-grossing-leading-stars/601',
    'https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-acting/top-grossing-leading-stars/701',
    'https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-acting/top-grossing-leading-stars/801',
    'https://www.the-numbers.com/box-office-star-records/worldwide/lifetime-acting/top-grossing-leading-stars/901'
]

fake_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}

scraped_dfs = []

for url in urls:
    req = requests.get(url, headers=fake_header)
    soup = bs(req.text, 'html.parser')

    table = soup.find('tbody')
    tr = table.find_all('tr')

    columns = []
    for row in tr:
        row_data = row.find_all('td')
        individual_row_data = [data.text.strip() for data in row_data]
        columns.append(individual_row_data)

    thead = soup.find('thead')
    th = thead.find_all('th')
    headers = []
    for head in th:
        headers.append(head.text.strip())

    df_dict = {}

    for header in headers:
        df_dict[header] = []

    for column in columns:
        for data, header in zip(column, headers):
            df_dict[header].append(data)

    df = pd.DataFrame(df_dict)

    scraped_dfs.append(df)

total_df = pd.concat(scraped_dfs, ignore_index='True').reset_index(drop=True)
total_df.to_csv('top_1000_grossing_actors.csv', index=False)
