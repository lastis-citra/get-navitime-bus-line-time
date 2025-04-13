import logging
import os

import navitime
import util
from model.input import BusLineData
from model.input import InputData

logger = logging.getLogger(__name__)


def create_diagram_stops_link_list(_diagram_stops_link_list: list[BusLineData], _input_data_list, no_alternative: bool):
    """
    すべてのバスのダイヤの停車バス停の時刻リストを作成する
    :param _diagram_stops_link_list:
    :param _input_data_list:
    :param no_alternative 入力された通りの方向のものを探す
    :return:
    """
    for input_data in _input_data_list:
        logging.info(input_data)
        _soup = util.download_html(input_data.url)

        div_id, dl_class = navitime.prepare_div_id_and_dl_class(_soup, input_data.day, input_data.direction)
        # print(f'div_id: {div_id}, dl_class: {dl_class}')

        # 各バスごとの停車時間表へのリンクを取得する
        diagram_stops_link_list_1 = navitime.get_diagram_stops_link_list(_soup, div_id, dl_class, no_alternative)

        if len(diagram_stops_link_list_1) > 0:
            print(f'diagram_stops_link_list_1: {diagram_stops_link_list_1}')
            bus_line_data_list = []
            for diagram_stops_link_1 in diagram_stops_link_list_1:
                # 同じURLが2回以上入らないようにチェックする
                _check = True
                for _diagram_stops_link in _diagram_stops_link_list:
                    if _diagram_stops_link.bus_url.split('?')[0] == diagram_stops_link_1.split('?')[0]:
                        _check = False
                        break
                if _check:
                    bus_line_data = BusLineData(diagram_stops_link_1, input_data.destination_list)
                    bus_line_data_list.append(bus_line_data)
            _diagram_stops_link_list.extend(bus_line_data_list)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_file_path = os.getenv("INPUT_FILE_PATH", 'input_url_list.conf')
    input_route_file_path = os.getenv("INPUT_ROUTE_FILE_PATH", 'input_route_url_list.conf')

    if not os.path.exists(input_file_path) and not os.path.exists(input_route_file_path):
        logging.error(f'There is no input file!!! input_file_path: {input_file_path}'
                      f'or input_route_file_path: {input_route_file_path}')
        exit(1)

    diagram_stops_link_list: list[BusLineData] = []
    input_route_data_list = []
    input_data_list = []

    # 先にinput_route_file_pathの方を読んで，得られるURLがある場合は路線リストの処理，ない場合は路線の処理を行う
    if os.path.exists(input_route_file_path):
        input_route_data_list = util.read_route_input(input_route_file_path)
        print(f'input_route_data_list: {input_route_data_list}')

    # 路線リストから得られるURLがあるかどうかチェック
    if len(input_route_data_list) > 0:
        for input_route_data in input_route_data_list:
            url_list = navitime.create_url_list(input_route_data.route_url)
            for url in url_list:
                input_data_list.append(InputData(url, input_route_data.day, 0, input_route_data.destination_list))
                input_data_list.append(InputData(url, input_route_data.day, 1, input_route_data.destination_list))
        create_diagram_stops_link_list(diagram_stops_link_list, input_data_list, True)
    else:
        input_data_list = util.read_input(input_file_path)
        create_diagram_stops_link_list(diagram_stops_link_list, input_data_list, False)

    print(f'input_data_list: {input_data_list}')
    print(f'diagram_stops_link_list: {diagram_stops_link_list}')

    # すべてのバスの発着時刻とバス停名のリスト
    bus_list = []
    for diagram_stops_link in diagram_stops_link_list:
        soup = util.download_html(diagram_stops_link.bus_url)
        diagram_stops = navitime.get_diagram_stops(soup)
        # print(f'diagram_stops: {diagram_stops}')
        check = False
        # 目的地リストが空の場合はチェックしない
        if len(diagram_stops_link.destination_list) == 0:
            check = True
        else:
            for stop in diagram_stops.stop_list:
                if stop.name in diagram_stops_link.destination_list:
                    # print(f'stop.name: {stop.name}')
                    check = True
                    break
        if check:
            bus_list.append(diagram_stops)
        else:
            print(f'diagram_stops_link.destination_list: {diagram_stops_link.destination_list} error!')

    print(f'bus_list: {bus_list}')

    # 最初に最もバス停数が多いバスのバス停名のリストを取得する
    name_list = navitime.get_max_length_name_list(bus_list)
    print(f'name_list: {name_list}')

    # すべてのバスのバス停名のリストを結合する
    for bus in bus_list:
        old_name_list = name_list
        check_name_list = bus.get_name_list()
        print(f'####################################################')
        print(f'old_name_list: {old_name_list}')
        print(f'check_name_list: {check_name_list}')
        name_list = navitime.create_name_list_compare_order(name_list, bus.get_name_list())

    print(f'name_list: {name_list}')
    # print(','.join(name_list))

    time_list_list = []
    for bus in bus_list:
        check_name_list = name_list.copy()
        # print(bus)
        # print(check_name_list)
        time_list = navitime.create_bus_time_table(check_name_list, bus.stop_list)
        # print(','.join(time_list))

        # ||を埋める作業
        # 最初に時刻が入っている箇所から最後に時刻が入っている箇所を調べる
        i = 0
        start_i = -1
        end_i = -1
        for time in time_list:
            if start_i < 0 and time != '':
                start_i = i
                end_i = i
            elif time != '':
                end_i = i
            i += 1

        # 時刻が入っている区間で空文字が入っていれば，通過文字に変更する
        i = 0
        changed_time_list = []
        for time in time_list:
            if start_i < i < end_i and time == '':
                changed_time_list.append('||')
            else:
                changed_time_list.append(time)
            i += 1

        time_list_list.append(changed_time_list)

    count_list = [0] * len(name_list)
    for time_list in time_list_list:
        i = 0
        for time in time_list:
            if time != '' and time != '||':
                count_list[i] += 1
            i += 1

    # for name_count in zip(name_list, count_list):
    #     print(name_count)

    # 最も時刻が存在する数の多いバス停を調べる
    max_i = count_list.index(max(count_list))


    def max_time(x):
        return x[max_i]


    # 最も時刻が存在する数の多いバス停の停車時刻で並び替える
    sorted_time_list_list = sorted(time_list_list, key=max_time)
    print(','.join(name_list))
    for time_list in sorted_time_list_list:
        print(','.join(time_list))
