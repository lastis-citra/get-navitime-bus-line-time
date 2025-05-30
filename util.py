import cloudscraper
from bs4 import BeautifulSoup

from model.input import InputData
from model.input import InputRouteData


def download_html(url: str) -> BeautifulSoup:
    """
    HTMLをダウンロードしてsoupを返す
    :param url: ダウンロードしたいURL
    :return: 取得したsoup
    """
    print(f'download_url: {url}')
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    res = scraper.get(url)

    soup = BeautifulSoup(res.content, 'html.parser')
    return soup


def read_input(file_path: str) -> list[InputData]:
    """
    指定されたファイルパスのURLリストを読み込み，InputDataのリストを返す
    :param file_path: 読み込むファイルのパス
    :return: InputDataのリスト
    """
    input_data_list = []
    with open(file_path, 'r', errors='replace', encoding="utf_8") as file:
        line_list = file.read().splitlines()

    for line in line_list:
        if line.startswith('#') or line.startswith(';'):
            continue
        split_line = line.split(',')
        input_data = InputData(split_line[0], split_line[1], split_line[2], [], [])
        input_data_list.append(input_data)

    return input_data_list


def read_route_input(file_path: str) -> list[InputRouteData]:
    """
    指定されたファイルパスのURLリストを読み込み，InputRouteDataのリストを返す
    :param file_path: 読み込むファイルのパス
    :return: InputRouteDataのリスト
    """
    input_route_data_list = []
    with open(file_path, 'r', errors='replace', encoding="utf_8") as file:
        line_list = file.read().splitlines()

    for line in line_list:
        if line.startswith('#') or line.startswith(';'):
            continue
        split_line = line.split(',')

        destination_list = []
        destinations = split_line[3]

        for destination in destinations.split('|'):
            destination_list.append(destination)

        input_route_data = InputRouteData(split_line[0], split_line[1], split_line[2], destination_list)
        input_route_data_list.append(input_route_data)

    return input_route_data_list
