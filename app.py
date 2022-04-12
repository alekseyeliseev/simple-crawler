import argparse
from distutils.log import debug
from unicodedata import name

from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
from pywebio.pin import *

from models import Website, Crawler
from utils import preproc_line


def main():

    set_env(title='Краулер и парсер веб-ресурсов')

    tstu_logo = open('static/tstu_logo.png', 'rb').read()
    style(put_image(tstu_logo, height='100px'), 'float:left')

    iait_logo = open('static/iait_logo.png', 'rb').read()
    style(put_image(iait_logo, height='100px'), 'float:right')

    put_html('<div style="clear: left"></div>')

    put_markdown(
        "# Программный комплекс «Краулер и парсер веб-ресурсов» (версия 0.2)")
    put_markdown("Программный комплекс **«Краулер и парсер веб-ресурсов» (версия 0.2)** предоставляет возможность автоматического обхода страниц заданных разделов интернет-ресурсов (например, новостных) с возможностью парсинга их содержимого по заранее определённому шаблону веб-страниц и фильтрации по ключевым словам.")
    put_markdown("Проект выполнен на кафедре «Информационные системы и защита информации» Тамбовского государственного технического университета.")

    put_markdown(
        "Для запуска процедуры поиска необходимо задать следующие параметры:")

    put_table([
        ['Параметр', 'Описание', 'Тип'],
        ['Имя набора параметров', put_markdown(
            'Имя набора параметров, определямое пользователем'), put_markdown('`строка`')],
        ['Стартовый адрес', put_markdown(
            'URL-адрес веб-ресурса, с которого осуществляется сбор данных'), put_markdown('`URL`')],
        ['Паттерн для поиска в разделах', put_markdown(
            'Паттерн, наличие которого является обязательным в URL-адресе ресурса'), put_markdown('`регулярное выражение`')],
        ['Тег для выделения заголовка', put_markdown(
            'Синтаксическое правило HTML для выделения заголовка статьи по тегам разметки'), put_markdown('`синтаксическое правило HTML`')],
        ['Тег для выделения текста статьи', put_markdown(
            'Синтаксическое правило HTML для выделения текста статьи по тегам разметки'), put_markdown('`синтаксическое правило HTML`')],
    ])

    put_markdown("**Примеры задания поисковых параметров**")

    put_table([
        ['Параметр', 'Значение'],
        ['Имя набора параметров', 'Новые известия'],
        ['Стартовый адрес', put_markdown('`https://newizv.ru`')],
        ['Паттерн для поиска в разделах', put_markdown('`^(/news/)`')],
        ['Тег для выделения заголовка', put_markdown('`div.title`')],
        ['Тег для выделения текста статьи',
            put_markdown('`div.content-blocks`')],
    ])

    put_table([
        ['Параметр', 'Значение'],
        ['Имя набора параметров', 'The Insider'],
        ['Стартовый адрес', put_markdown('`https://theins.ru`')],
        ['Паттерн для поиска в разделах', put_markdown('`^(/news/)`')],
        ['Тег для выделения заголовка', put_markdown('`h1`')],
        ['Тег для выделения текста статьи', put_markdown('`div.xzBG5`')],
    ])

    name = eval_js("localStorage.name")
    url = eval_js("localStorage.url")
    targetPattern = eval_js("localStorage.targetPattern")
    titleTag = eval_js("localStorage.titleTag")
    bodyTag = eval_js("localStorage.bodyTag")
    keywords = eval_js("localStorage.keywords")

    info = input_group("Параметры поиска", [
        input('Имя набора параметров', name='name', type=TEXT,
              help_text='Пример: Новые известия', value=name),
        input('Стартовый адрес', name='url', type=URL, required=True,
              help_text='Пример: https://newizv.ru', value=url),
        input('Паттерн для поиска в разделах', name='targetPattern', type=TEXT,
              required=True, help_text='Пример: ^(/news/)', value=targetPattern),
        input('Правило выделения заголовка статьи',
              name='titleTag', type=TEXT, required=True, help_text='Пример: div.title', value=titleTag),
        input('Правило выделения текста статьи',
              name='bodyTag', type=TEXT, required=True, help_text='Пример: div.content-blocks', value=bodyTag),
        input('Ключевые слова',
              name='keywords', type=TEXT, help_text='Пример: война агрессия пропаганда', value=keywords)
    ])

    eval_js("localStorage.name=name", name=info['name'])
    eval_js("localStorage.url=url", url=info['url'])
    eval_js("localStorage.targetPattern=targetPattern",
            targetPattern=info['targetPattern'])
    eval_js("localStorage.titleTag=titleTag", titleTag=info['titleTag'])
    eval_js("localStorage.bodyTag=bodyTag", bodyTag=info['bodyTag'])
    eval_js("localStorage.keywords=keywords", keywords=info['keywords'])

    site = Website(info['name'], info['url'], info['targetPattern'],
                   False, info['titleTag'], info['bodyTag'])
    results = crawl(site)
    filtered_results = filtering_results(results, info['keywords'])
    print_results(filtered_results)


def crawl(site):
    crawler = Crawler(site)
    with put_loading(shape='border', color='primary').style('width:2rem; height:2rem'):
        results = crawler.crawl()
    return(results)


def filtering_results(results, keywords):
    if keywords:
        filtered_results = []
        keywords_list = preproc_line(keywords)
        for result in results:
            count_keywords = 0
            for keyword in keywords_list:
                count_keywords += (keyword in result.body_processed)
            if count_keywords:
                filtered_results.append(result)
        return(filtered_results)
    else:
        return(results)


def print_results(results):
    put_markdown('## Результаты поиска')
    if len(results) == 0:
        put_markdown(
            'Результатов нет. Попробуйте задать другие параметры поиска.')
        put_button("Назад", onclick=lambda: eval_js(
            "window.location.assign('/')"))
    else:
        for result in results:
            put_markdown(f'[{result.url}]({result.url})')
            put_markdown(f'**{result.title}**')
            put_text(result.body).style('paddin-bottom: 10px')
        put_button("Новый поиск", onclick=lambda: eval_js(
            "window.location.assign('/')"))
        #put_text(result.body_processed).style('paddin-bottom: 10px')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(main, port=args.port, websocket_ping_interval=30, debug=True)
