import re

from bs4 import BeautifulSoup

import util
from model.stop import StopData, BusData


def prepare_div_id_and_dl_class(soup: BeautifulSoup, day: str, direction: str) -> (str, str):
    """
    ページ内から曜日と方向が一致する時刻表のテーブルを特定するためのidとclassを用意する
    :param soup: ページ全体のsoup
    :param day: 曜日を表す数字
    :param direction: 方向
    :return: div_id, dl_class
    """
    div_tags = soup.select('.diagramTable')
    # print(div_tags)
    div_id_list = []
    for div_tag in div_tags:
        div_id_list.append(div_tag.attrs['id'])
    print(f'table_id_list: {div_id_list}')

    if len(div_id_list) == 0:
        print("No possible IDs")
        div_id = None
    elif len(div_id_list) == 1:
        div_id = div_id_list.pop()
    else:
        div_id = f'd_{direction}_{day}'

    dl_class = f'dl_{day}'

    return div_id, dl_class


def get_diagram_stops_link_list(soup: BeautifulSoup, div_id: str, dl_class: str, no_alternative: bool) -> list[str]:
    """
    各バスごとの停車時間表へのリンクを取得する
    :param soup: ページ全体のsoup
    :param div_id: 読み込むdivタグのid（d_0_0など）
    :param dl_class: 読み込むdlタグのclass（dl_0など）
    :param no_alternative: trueの場合，入力された通りの方向のものを探す
    :return: 各バスごとの停車時間表へのリンクのlist
    """
    print(f'get_diagram_stops_link: div_id: {div_id}, dl_class: {dl_class}')
    dl_tags = soup.select(f'#{div_id} dl.{dl_class}')
    div_tags = soup.select('div.diagramTable')
    if len(div_tags) > 0 and len(dl_tags) == 0:
        print(f'get_diagram_stops_link: div_id: {div_id}, dl_class: dl_date alternatively')
        dl_tags = soup.select(f'#{div_id} dl.dl_date')
    if len(div_tags) > 0 and len(dl_tags) == 0:
        div_id_tmp = div_id.split('_')
        div_id_alt = div_id_tmp[0] + '_' + div_id_tmp[1] + '_date'
        print(f'get_diagram_stops_link: div_id: {div_id_alt}, dl_class: dl_date alternatively')
        dl_tags = soup.select(f'#{div_id_alt} dl.dl_date')
    if not no_alternative:
        if len(div_tags) > 0 and len(dl_tags) == 0:
            div_id_tmp = div_id.split('_')
            if div_id_tmp[1] == '0':
                div_id_alt = div_id_tmp[0] + '_1_' + div_id_tmp[2]
            else:
                div_id_alt = div_id_tmp[0] + '_0_' + div_id_tmp[2]
            print(f'get_diagram_stops_link: div_id: {div_id_alt}, dl_class: {dl_class} alternatively')
            dl_tags = soup.select(f'#{div_id_alt} dl.{dl_class}')

    # print(f'dl_tags: {dl_tags}')
    diagram_stops_link_list = []
    for dl_tag in dl_tags:
        li_tags = dl_tag.select('li')
        dt_tag = dl_tag.select_one('dt')
        hour = dt_tag.text.replace('\n', '')
        print(f'HOUR: {hour}')
        for li_tag in li_tags:
            link = li_tag.select_one('a')['href']
            time = li_tag.select_one('a').text.replace('\n', '').replace(' ', '')
            diagram_stops_link: str = f'https://www.navitime.co.jp{link}'
            print(f'MIN: {time} {diagram_stops_link}')
            diagram_stops_link_list.append(diagram_stops_link)

    # リンクが1つも取れていない場合はおかしいのでエラーで強制終了する
    if len(diagram_stops_link_list) == 0:
        print(f'ERROR: diagram_stops_link_list is empty!')
        # sys.exit(1)

    return diagram_stops_link_list


def get_diagram_stops(soup: BeautifulSoup) -> BusData:
    """
    各バス停停車時刻のページをスクレイピングする
    :param soup: 各バス停停車時刻のページのsoup
    :return: BusData
    """
    ul_tag = soup.select_one('ul.stops-area')
    dl_tags = ul_tag.select('dl.stops')

    stop_list = []
    for dl_tag in dl_tags:
        # print(f'dl_tag: {dl_tag}')
        name = dl_tag.select_one('a.station-name-link').text
        # print(f'name: {name}')
        # バス停名の（福井県）などを削除する
        name = re.sub('（.*?）$', '', name)
        # バス停名の〔東福バス〕などを削除する
        name = re.sub('〔.*?〕$', '', name)
        # 着発表示のあるバス停の場合，着時刻は無視して発時刻のみを残す
        if len(dl_tag.select('dd.from-to-time')) > 0:
            time = dl_tag.select_one('dd.from-to-time').text.split('着')[1].replace('発', '').replace('\n', '').replace(
                ' ', '')
        else:
            time = dl_tag.select_one('dd.time').text.replace('着', '').replace('発', '')

        stop = StopData(name, time)
        stop_list.append(stop)

    bus = BusData('', stop_list)
    print(f'bus: {bus}')

    return bus


def get_max_length_name_list(bus_list: list[BusData]) -> list[str]:
    """
    最も停車バス停が多いバスの停車バス停名のリストを取得する
    :param bus_list: すべてのバスの発着時刻とバス停名のリスト
    :return: バス停名のリスト
    """
    max_length = 0
    max_bus = None
    for bus in bus_list:
        len(bus.stop_list)
        if len(bus.stop_list) > max_length:
            max_length = len(bus.stop_list)
            max_bus = bus

    return max_bus.get_name_list()


def create_name_list_compare_order(old_name_list: list[str], check_name_list: list[str]) -> list[str]:
    """
    create_name_listを逆順で適用した場合とどちらが短くなるかを比較して短い方を採用する
    :param old_name_list: 結合前のバス停名のリスト
    :param check_name_list: チェックしたいバス停名のリスト
    :return: バス停名のリスト
    """
    reverse_old_name_list = old_name_list.copy()
    reverse_old_name_list.reverse()
    reverse_check_name_list = check_name_list.copy()
    reverse_check_name_list.reverse()

    # print(f'---------')
    # print(f'old_name_list: {old_name_list}')
    # print(f'check_name_list: {check_name_list}')
    normal_order_list = create_name_list(old_name_list, check_name_list)
    # print(f'normal_order_list: {normal_order_list}')

    old_name_list.reverse()
    check_name_list.reverse()
    # print(f'---------')
    # print(f'reverse_old_name_list: {reverse_old_name_list}')
    # print(f'reverse_check_name_list: {reverse_check_name_list}')
    reverse_order_list = create_name_list(reverse_old_name_list, reverse_check_name_list)
    reverse_order_list.reverse()
    # print(f'reverse_order_list: {reverse_order_list}')

    if len(normal_order_list) <= len(reverse_order_list):
        return normal_order_list
    else:
        return reverse_order_list


def create_name_list(old_name_list: list[str], check_name_list: list[str]) -> list[str]:
    """
    すべてのバスのバス停名のリストを結合する
    :param old_name_list: 結合前のバス停名のリスト
    :param check_name_list: チェックしたいバス停名のリスト
    :return: バス停名のリスト
    """
    # print(f'---------')
    # print(f'old_name_list: {old_name_list}')
    # print(f'check_name_list: {check_name_list}')

    # old_name_listが空になっていれば，check_name_listの残りを出力して終了
    if len(old_name_list) == 0:
        return check_name_list
    # old_name_listの先頭を取り出す
    stop_name = old_name_list.pop(0)
    # print(f'name: {stop_name}')
    # もしcheck_name_listに名前が一致するバス停がなければ
    if stop_name not in check_name_list:
        # 取り出したのが最後のバス停なら，check_name_listの残りを出力して終了
        if len(old_name_list) == 0:
            return [stop_name] + check_name_list
        # そうでなければ，残りのlistをチェックする
        else:
            return [stop_name] + create_name_list(old_name_list, check_name_list)
    # もしcheck_name_listに名前が一致するバス停があれば
    else:
        # print(f'{stop_name} is in check_name_list')
        # 一致するバス停がある位置を取得
        i = check_name_list.index(stop_name)
        # print(f'i: {i}')
        # 一致するバス停までを（一致するバス停を含めて）check_name_listから取り出す
        another_list = check_name_list[:i + 1]
        # print(f'another_list: {another_list}')
        # print(f'old_name_list: {old_name_list}')
        # print(f'check_name_list: {check_name_list[i + 1:]}')
        # 残りのlistをチェックする
        return another_list + create_name_list(old_name_list, check_name_list[i + 1:])


def create_bus_time_table(name_list: list[str], stop_list: list[StopData]) -> list[str]:
    """
    対象のstop_list（バス1本の停車時刻情報）に，name_list（全バス停のリスト）のバス停のバス時刻が存在するか確認し，
    存在する場合はその時刻を入れ，存在しない場合は空の文字を入れたリストを返す
    :param name_list: バス1本の停車時刻情報
    :param stop_list: 全バス停のリスト
    :return: 時刻表の横1列分の時刻情報（バス停ごとの停車時刻のリスト）
    """
    # name_listが空になったら終了
    if len(name_list) == 0:
        return []
    # name_listの先頭のバス停名を取り出す
    stop_name = name_list.pop(0)
    # stop_listに存在しないバス停の場合は空文字を入れる
    if len(stop_list) == 0 or stop_list[0].name != stop_name:
        return [''] + create_bus_time_table(name_list, stop_list)
    # 存在するバス停の場合は，その時刻を入れ，stop_listからそのバス停を抜く
    else:
        stop = stop_list.pop(0)
        return [stop.time] + create_bus_time_table(name_list, stop_list)


def create_url_list(route_url: str) -> list[str]:
    """
    バス系統一覧ページのURLから時刻表URLのリストを取得する
    :param route_url: バス系統一覧ページのURL
    :return: 時刻表URLのリスト
    """
    url_list = []

    soup = util.download_html(route_url)
    li_tags = soup.select('ul.dest-list')
    for li_tag in li_tags:
        links = li_tag.select('a')
        for link in links:
            url = link.attrs['href']
            url_list.append(f'https:{url}')

    return url_list
