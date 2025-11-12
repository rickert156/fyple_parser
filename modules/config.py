from SinCity.colors import RED, RESET, GREEN, BLUE, YELLOW

#директории/файл для хранения инфы
result_dir = 'Result'
result_file = 'result.csv'
categories_file = f'{result_dir}/categories.csv'
subcategories_file = f'{result_dir}/subcategories.csv'
result_file_path = f'{result_dir}/{result_file}'

data_dir = 'Data'
complite_categories_url = f'{data_dir}/complite_categories_url.txt'
companies_url_doc = f'{data_dir}/companies.csv'


#статусы
status_type_info = f"[{GREEN}INFO{RESET}]"
status_type_error = f"[{RED}ERROR{RESET}]"
status_type_warning = f"[{YELLOW}WARNING{RESET}]"
