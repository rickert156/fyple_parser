# parser Fyple 

## Установка
```sh
git clone https://github.com/rickert156/fyple_parser && cd fyple_parser && python3 -m venv venv && ./venv/bin/pip install -r requirements.txt
```

### Режим отладки
Для отладки можно парсить по одной странице, указывая параметр --test-url с url
```sh
python3 -m modules.test_requests --test-url=https://github.com
```
## Получить список категорий/подкатегорий
```sh
python3 -m modules.get_categories
```

## Парсинг одной страницы
Необходимо передать первым параметром URL. Bторым параметром можно добавить категорию, опционально
```sh
python3 -m modules.parser_page https://www.fyple.com/company/al-muhajreen-o88zgx3/ 'test category'
```

## Парсинг категорий
Параметром указываем url
```sh
python3 -m modules.get_companies https://www.fyple.com/category/construction-contractor
```

## Запуск парсера
собираем категории
```sh
python3 -m modules.get_categories
```
Парсим компании по категориям
```sh
python3 __main__.py --category
```
Парсим сами компании
```sh
python3 __main__.py --company
```
