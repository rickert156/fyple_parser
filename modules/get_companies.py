import csv
import requests
import os
import sys
import time
from bs4 import BeautifulSoup
from SinCity.colors import RED, RESET, GREEN, BLUE
from SinCity.Agent.header import header
from modules.miniTools import log_time, recording_company_info
from modules.config import (
        data_dir,
        complite_categories_url,
        companies_url_doc,
        result_dir, 
        result_file_path, 
        status_type_info,
        status_type_warning,
        status_type_error
        )

def recording_company_links(links:list[str], category:str=None):
    if not os.path.exists(companies_url_doc):
        with open(companies_url_doc, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(['URL', 'Category'])
    
    with open(companies_url_doc, 'a') as file:
        writer = csv.writer(file)
        for link in links:
            writer.writerow([link, category])

def recording_complite_url(url:str) -> None:
    if not os.path.exists(data_dir):os.makedirs(data_dir)
    with open(complite_categories_url, 'a') as file:
        file.write(f'{url}\n')

def get_complite_categories_url() -> list[str]:
    list_complite_url = set()
    if os.path.exists(complite_categories_url):
        with open(complite_categories_url, 'r') as file:
            for line in file.readlines():
                list_complite_url.add(line.strip())

    return list_complite_url
    

def get_max_page(bs) -> int:
    max_page = 0
    list_nav = bs.find_all(class_='page')
    if list_nav:
        max_page = int(list_nav[-1].get_text().strip())
    return max_page

def get_company_link(bs) -> list[str]:
    list_url = set()
    list_a_comp_title = bs.find_all(class_='comp_title')
    if list_a_comp_title:
        for link in list_a_comp_title:
            link = link.get('href')
            if link:
                list_url.add(f'https://www.fyple.com{link}')

    return list_url


def parser_categories(url:str, category:str=None) -> None:
    try:
        max_page = 0
        count_requests = 0
        list_complite_url = get_complite_categories_url()
        while True:
            count_requests+=1
            head = header()
            full_url = f'{url}page/{count_requests}/'
            if full_url not in list_complite_url:
                response = requests.get(full_url, headers=head)
                status_code = response.status_code
                if status_code == 200:
                    bs = BeautifulSoup(response.text, 'lxml')
                    max_page = get_max_page(bs)
                
                    print(
                            f'{log_time()} {status_type_info} '
                            f'page [ {count_requests} / {max_page} ]\n'
                            f'{full_url}'
                            )
                    list_link = get_company_link(bs)
                    if len(list_link) > 0:
                        for id_, link in enumerate(list_link, start=1):
                            print(f'[{id_}] {BLUE}{link}{RESET}')
                        #запишем список ссылок
                        recording_company_links(links=list_link, category=category)
                    #записшем пройденный URL
                    recording_complite_url(url=full_url)
                        
                else:
                    print(f'{log_time()} {status_type_error} status code: {status_code}')
                
                if count_requests == max_page:
                    break

    except KeyboardInterrupt:
        sys.exit(f'\n{log_time()} {status_type_info} Exit...')

if __name__ == '__main__':
    params = sys.argv
    if len(params) > 1 and 'https://www.fyple.com/category/' in params[1]:
        category = None
        url = params[1]
        if len(params) > 2:
            category = params[2]
        parser_categories(url=url, category=category)
    else:
        print(
                f'{log_time()} {status_type_warning} Пример использования\n'
                f'python3 -m modules.get_companies '
                f'https://www.fyple.com/category/construction-contractor'
                )
