import argparse
from distutils.log import debug

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *

from models import Website, Crawler

def main():
    
    set_env(title='Краулер и парсер веб-ресурсов')

    tstu_logo = open('static/tstu_logo.png', 'rb').read()  
    put_image(tstu_logo, height='100px')

    isizi_logo = open('static/isizi_logo.png', 'rb').read()  
    put_image(isizi_logo, height='150px')
    
    put_markdown("# Программный комплекс «Краулер и парсер веб-ресурсов» (версия 0.1)")
    put_markdown("Программный комплекс **«Краулер и парсер веб-ресурсов» (версия 0.1)** предоставляет возможность автоматического обхода страниц заданных разделов интернет-ресурсов (например, новостных) с возможностью парсинга их содержимого по заранее определённому шаблону веб-страниц.") 
    put_markdown("Проект выполнен на кафедре «Информационные системы и защита информации» Тамбовского государственного технического университета.")
    
    put_markdown("Для запуска процедуры поиска необходимо задать следующие парметры:")
    
    put_table([
    ['Параметр', 'Описание', 'Тип'],
    ['Имя набора параметров', put_markdown('Имя набора параметров, определямое пользователем'), put_markdown('`строка`')],
    ['Стартовый адрес', put_markdown('URL-адрес веб-ресурса, с которого осуществляется сбор данных'), put_markdown('`URL`')],
    ['Паттерн для поиска в разделах', put_markdown('Паттерн, наличие которого является обязательным в URL-адресе ресурса'), put_markdown('`регулярное выражение`')],  
    ['Тег для выделения заголовка', put_markdown('Синтаксическое правило HTML для выделения заголовка статьи по тегам разметки'), put_markdown('`синтаксическое правило HTML`')],
    ['Тег для выделения текста статьи', put_markdown('Синтаксическое правило HTML для выделения текста статьи по тегам разметки'), put_markdown('`синтаксическое правило HTML`')],
    ])
    
    put_markdown("**Примеры задания поисковых параметров**")

    put_table([
    ['Параметр', 'Значение'],
    ['Имя набора параметров', 'Новые известия'],
    ['Стартовый адрес', put_markdown('`https://newizv.ru`')],
    ['Паттерн для поиска в разделах', put_markdown('`^(/news/)`')],  
    ['Тег для выделения заголовка', put_markdown('`div.title`')],
    ['Тег для выделения текста статьи',put_markdown('`div.content-blocks`')],
    ])

    put_table([
    ['Параметр', 'Значение'],
    ['Имя набора параметров', 'The Insider'],
    ['Стартовый адрес', put_markdown('`https://theins.ru`')],
    ['Паттерн для поиска в разделах', put_markdown('`^(/news/)`')],  
    ['Тег для выделения заголовка', put_markdown('`h1`')],
    ['Тег для выделения текста статьи',put_markdown('`div.xzBG5`')],
    ])

    info = input_group("Параметры поиска", [
        input('Имя набора параметров', name='name', type=TEXT, help_text='Пример: Новые известия'),
        input('Стартовый адрес', name='url', type=URL, required=True, help_text='Пример: https://newizv.ru'),
        input('Паттерн для поиска в разделах', name='targetPattern', type=TEXT, required=True, help_text='Пример: ^(/news/)'),
        input('Правило выделения заголовка статьи',
              name='titleTag', type=TEXT, required=True, help_text='Пример: div.title'),
        input('Правило выделения текста статьи',
              name='bodyTag', type=TEXT, required=True, help_text='Пример: div.content-blocks')
    ])

    site = Website(info['name'], info['url'], info['targetPattern'],
                   False, info['titleTag'], info['bodyTag'])
    crawl(site)


def crawl(site):
    crawler = Crawler(site)
    with put_loading(shape='border', color='primary').style('width:2rem; height:2rem'):
        results = crawler.crawl()
    print_results(results)


def print_results(results):
    put_markdown('## Результаты поиска')
    if len(results) == 0:
        put_markdown('Результатов нет. Попробуйте задать другие параметры поиска.')
        put_button("Назад", onclick=lambda: eval_js("window.location.assign('/')"))
    else:
        for result in results:
            put_markdown(f'[{result.url}]({result.url})')
            put_markdown(f'**{result.title}**')
            put_text(result.body).style('paddin-bottom: 10px')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(main, port=args.port, websocket_ping_interval=30, debug=True)
