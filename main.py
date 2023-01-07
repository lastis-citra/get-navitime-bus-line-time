import logging
import os

import navitime
import util

logger = logging.getLogger(__name__)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    input_file_path = os.getenv("INPUT_FILE_PATH", 'input_url_list.conf')

    if not os.path.exists(input_file_path):
        logging.error(f'There is no input file!!! input_file_path: {input_file_path}')
        exit(1)

    input_data_list = util.read_input(input_file_path)
    print(f'input_data_list: {input_data_list}')

    diagram_stops_link_list = []
    for input_data in input_data_list:
        logging.info(input_data)
        soup = util.download_html(input_data.url)

        div_id, dl_class = navitime.prepare_div_id_and_dl_class(soup, input_data.day, input_data.direction)
        print(f'div_id: {div_id}, dl_class: {dl_class}')

        # 各バスごとの停車時間表へのリンクを取得する
        diagram_stops_link_list.extend(navitime.get_diagram_stops_link(soup, div_id, dl_class))

    print(f'diagram_stops_link_list: {diagram_stops_link_list}')

    # すべてのバスの発着時刻とバス停名のリスト
    bus_list = []
    for diagram_stops_link in diagram_stops_link_list:
        soup = util.download_html(diagram_stops_link)
        bus_list.append(navitime.get_diagram_stops(soup))

    print(f'bus_list: {bus_list}')

    # 最初に最もバス停数が多いバスのバス停名のリストを取得する
    name_list = navitime.get_max_length_name_list(bus_list)
    print(f'name_list: {name_list}')

    # すべてのバスのバス停名のリストを結合する
    for bus in bus_list:
        old_name_list = name_list
        check_name_list = bus.get_name_list()
        # print(f'####################################################')
        # print(f'old_name_list: {old_name_list}')
        # print(f'check_name_list: {check_name_list}')
        name_list = navitime.create_name_list(name_list, bus.get_name_list())

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
