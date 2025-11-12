import csv
import requests
import os
from bs4 import BeautifulSoup
from modules.miniTools import log_time
from modules.config import (
        result_dir, 
        result_file_path, 
        categories_file,
        subcategories_file,
        status_type_info,
        status_type_warning,
        status_type_error
        )
from SinCity.colors import RED, RESET, GREEN, BLUE
from SinCity.Agent.header import header

#######################################
#           Пишем результат           #
#######################################
def recording_categories(categories:list[dict]) -> None:
    with open(categories_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'category', 'url'])

    with open(categories_file, 'a') as file:
        writer = csv.writer(file)
        for id_, category_info in enumerate(categories, start=1):
            category = category_info.get('category')
            url = category_info.get('url')
            writer.writerow([id_, category, url])

        print(f'{log_time()} {status_type_info} Категории записаны:\t\t{categories_file}')

def recording_subcategories(subcategories_list:list[dict]) -> None:
    with open(subcategories_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'category', 'subcategory', 'url'])

    with open(subcategories_file, 'a') as file:
        writer = csv.writer(file)
        for id_, subcategory in enumerate(subcategories_list, start=1):
            subcategory_name = subcategory.get('subcategory')
            category_name = subcategory.get('category')
            subcategory_url = subcategory.get('url')
            writer.writerow([id_, category_name, subcategory_name, subcategory_url])

        print(f'{log_time()} {status_type_info} Подкатегории записаны:\t{subcategories_file}')


def get_categories():
    head = header()
    categories_url = 'https://www.fyple.com/categories/'

    response = requests.get(categories_url, headers=head)
    status_code = response.status_code
    if status_code == 200:
        print(
                f'[{log_time()}] {status_type_info} '
                f'Доступ к URL {categories_url} разрешен'
                )
        bs = BeautifulSoup(response.text, 'lxml')
        full_list_url = bs.find_all(class_='one_row')
        if full_list_url:
            number_link = 0

            categories_list = []
            subcategories_list = []
            categories_check_list = set()
            
            for link in full_list_url:
                subcategory = link.get_text()
                link = link.get('href')
                if link:
                    number_link+=1
                    category = link.split('/category/')[1].split('/')[0]
                    category_url = f'https://www.fyple.com/category/{category}/'
                    if '-' in category:category = category.replace('-', ' ')
                    category = category.title()
                    if category not in categories_check_list:
                        categories_check_list.add(category)
                        categories_list.append({'category':category, 'url':category_url})
                    link = f'https://www.fyple.com{link}'
                    
                    subcategory_info = {
                            'subcategory':subcategory, 
                            'category':category, 
                            'url':link
                            }
                    subcategories_list.append(subcategory_info)

                    print(
                            f'[{number_link}] {GREEN}{category}{RESET} '
                            f'{BLUE}{subcategory}{RESET} {link}'
                            )
            recording_categories(categories=categories_list)
            recording_subcategories(subcategories_list=subcategories_list)
        else:
            print(f'[{log_time()}] {status_type_warning} Категории не найдены')
    else:
        print(
                f'[{log_time()}] {status_type_error} Доступ не разрешен\n'
                f'[HEADERS] {response.headers}\n'
                f'[CONTENT] {response.content}'
                )

if __name__ == '__main__':
    print(f'{log_time()} {status_type_info} get categories...')
    categories = get_categories()
    
