import requests
import sys
import shutil
from bs4 import BeautifulSoup
from modules.config import (
        result_dir, 
        result_file_path, 
        status_type_info,
        status_type_warning,
        status_type_error
        )
from modules.logger import log_print
from modules.miniTools import log_time, init_parser, recording_company_info
from SinCity.colors import RED, RESET, GREEN
from SinCity.Agent.header import header

terminal_size = int(shutil.get_terminal_size().columns)
divine_line = '-'*(terminal_size-3)


def get_company_info(response:str, category:str=None) -> None:
    bs = BeautifulSoup(response, 'lxml')
    main_block = bs.find(class_='col-md-5')
    
    company_name = None
    country = None
    phone = None
    mobile = None
    site = None
    
    company_name = bs.find('h1')
    if company_name:company_name = company_name.get_text()

    address = bs.find(attrs={'itemprop':'address'})
    if address:
        country = address.find(attrs={'itemprop':'addressCountry'})
        if country:country = country.get_text()
        
    for block in main_block.find_all(class_='row'):
        if 'Phone number:' in block.get_text():
            phone = block.find(class_='col-xs-12 col-sm-7')
            if phone:phone = phone.get_text().strip()
        if 'WebSite' in block.get_text():
            link = block.find(class_='col-xs-12 col-sm-7').find('a')
            site = link.get('href')

    print(
            f'| Company:\t{company_name}\n'
            f'| Country:\t{country}\n'
            f'| Phone:\t{phone}\n'
            f'| Site:\t\t{site}\n'
            f'| Category:\t{category}\n'
            f'|{divine_line}\n'
            )
    recording_company_info(
            company=company_name, 
            country=country, 
            site=site, 
            phone=phone,
            category=category
            )


def get_page_info(url:str, category:str=None) -> None:
    head = header()
    response = requests.get(url, headers=head)
    status_code = response.status_code
    if status_code == 200:
        print(
                f'|{divine_line}\n'
                f'| {log_time()} {status_type_info} url: {url}\n'
                f'| {GREEN}Status code: {status_code}{RESET}'
                )
        get_company_info(response=response.text, category=category)
    else:
        print(
                f'{log_time()} {status_type_error} status code: {status_code}\n'
                f'[HEADERS] {response.headers}\n'
                f'[CONTENT] {response.content}'
                )


if __name__ == '__main__':
    init_parser()
    params = sys.argv
    if len(params) > 1:
        if 'https://www.fyple.com/' in params[1]:
            url = params[1]
            category = None
            if len(params) > 2:
                category = params[2]
            print(f'{log_time()} {status_type_info} processing...')
            get_page_info(url=url, category=category)
        else:
            sys.exit(
                    f'{log_time()} {status_type_warning} Передай страницу компании, пример\n'
                    f'https://www.fyple.com/company/al-muhajreen-o88zgx3/'
                    )
    else:
        sys.exit(
                f'{log_time()} {status_type_warning} Пример использования\n'
                f'python3 -m modules.parser_page '
                f'https://www.fyple.com/company/al-muhajreen-o88zgx3/'
                )
