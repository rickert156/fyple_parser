import csv
import sys
from SinCity.colors import RED, RESET, GREEN, BLUE
from SinCity.Agent.header import header
from modules.miniTools import log_time 
from modules.config import (
        categories_file,
        companies_url_doc,
        result_dir, 
        result_file_path, 
        status_type_info,
        status_type_warning,
        status_type_error
        )
from modules.parser_page import get_page_info
from modules.get_companies import parser_categories

if __name__ == '__main__':
    try:
        params = sys.argv
        if '--company' in params:
            with open(companies_url_doc, 'r') as file:
                number_url = 0
                for row in csv.DictReader(file):
                    number_url+=1
                    url = row.get('URL')
                    category = row.get('Category')
                    print(f'{log_time()} {status_type_info} [{number_url}] {url}')
                    get_page_info(url=url, category=category)
        elif '--category' in params:
            max_count_categories = 0
            with open(categories_file, 'r') as file:
                for row in csv.DictReader(file):
                    max_count_categories+=1
            with open(categories_file, 'r') as file:
                number_category = 0
                for row in csv.DictReader(file):
                    number_category+=1
                    category = row.get('category')
                    url = row.get('url')
                    print(
                            f'{log_time()} {status_type_info} '
                            f'[ {number_category} / {max_count_categories} ] '
                            f'{category} | {url} '
                            )
                    parser_categories(url=url, category=category)
        else:
            print(
                    f'--company\t - сбор инфы о команиях\n'
                    f'--category\t - сбор компаний'
                    )

    except KeyboardInterrupt:
        print(f'\n{log_time()} {status_type_info} Exit...')
