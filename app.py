import argparse

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *

from models import Website, Crawler

set_env(title='Краулер и парсер веб-ресурсов')

def main():

    put_markdown(
        "# Краулер и парсер веб-ресурсов\nСервис предоставляет возможность обхода страниц разделов новостных веб-ресурсов с возможностью парсинга их содержимого.")

    info = input_group("Параметры поиска", [
        input('Имя набора параметров', name='name', type=TEXT, help_text='Пример: Новые известия'),
        input('Стартовый адрес', name='url', type=URL, required=True, help_text='Пример: https://newizv.ru'),
        input('Паттерн для поиска в разделах', name='targetPattern', type=TEXT, required=True, help_text='Пример: ^(/news/)'),
        input('Тег для выделения заголовка',
              name='titleTag', type=TEXT, required=True, help_text='Пример: div.title'),
        input('Тег для выделения текста статьи',
              name='bodyTag', type=TEXT, required=True, help_text='Пример: div.content-blocks')
    ])

    site = Website(info['name'], info['url'], info['targetPattern'],
                   False, info['titleTag'], info['bodyTag'])
    crawl(site)


def crawl(site):
    crawler = Crawler(site)
    with put_loading(shape='border', color='info').style('width:2rem; height:2rem'):
        results = crawler.crawl()
    print_results(results)


def print_results(results):
    put_markdown('## Результаты поиска')
    for result in results:
        put_markdown(f'[{result.url}]({result.url})')
        put_markdown(f'**{result.title}**')
        put_text(result.body).style('paddin-bottom: 10px')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(main, port=args.port, websocket_ping_interval=30)
