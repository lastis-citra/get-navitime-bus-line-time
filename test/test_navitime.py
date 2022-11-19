from navitime import create_name_list


# 通常の結合
def test_create_name_list1():
    old_name_list = ['A', 'B', 'C', 'D', 'E']
    check_name_list = ['A', 'F', 'G', 'D', 'E']
    expected1 = ['A', 'F', 'G', 'B', 'C', 'D', 'E']
    expected2 = ['A', 'B', 'C', 'F', 'G', 'D', 'E']
    actual = create_name_list(old_name_list, check_name_list)

    assert actual in [expected1, expected2]


# 完全に吸収されるパターン
def test_create_name_list2():
    old_name_list = ['A', 'B', 'C', 'D', 'E']
    check_name_list = ['A', 'B', 'C']
    expected = ['A', 'B', 'C', 'D', 'E']
    assert create_name_list(old_name_list, check_name_list) == expected


# old_name_listに同じ名前があるパターン
def test_create_name_list3():
    old_name_list = ['A', 'B', 'C', 'B', 'D', 'E']
    check_name_list = ['A', 'F', 'G', 'D', 'E']
    expected1 = ['A', 'F', 'G', 'B', 'C', 'B', 'D', 'E']
    expected2 = ['A', 'B', 'C', 'B', 'F', 'G', 'D', 'E']
    actual = create_name_list(old_name_list, check_name_list)

    assert actual in [expected1, expected2]


# check_name_listに同じ名前があるパターン
def test_create_name_list3():
    old_name_list = ['A', 'B', 'C', 'D', 'E']
    check_name_list = ['C', 'A', 'B', 'C', 'D', 'E']
    expected = ['C', 'A', 'B', 'C', 'D', 'E']
    assert create_name_list(old_name_list, check_name_list) == expected


# old_name_listとcheck_name_listの両方に同じ名前があるパターン
def test_create_name_list4():
    old_name_list = ['A', 'B', 'C', 'B', 'D', 'E']
    check_name_list = ['C', 'A', 'B', 'C', 'D', 'E']
    expected = ['C', 'A', 'B', 'C', 'B', 'D', 'E']
    assert create_name_list(old_name_list, check_name_list) == expected


# バグチェック
def test_create_name_list5():
    old_name_list = ['伊豆海洋公園', '蓮着寺', '城ヶ崎オレンジ村', 'ルネッサ城ヶ崎', '蓮着寺口', '伊東高校城ヶ崎分校',
                     '対島中学校正門', '対島中学校', '伊豆高原駅', '平松', '伊豆高原駅やまも口', '八幡野コミュニティセンター',
                     '八幡野', '平松', '伊豆高原駅', '平松', '伊豆高原駅やまも口', '八幡野コミュニティセンター', '八幡野', '平松',
                     'ファミリーガーデン', '対島中学校', '四辻', '池入口', '先原', '光の村', '東大室', 'ぐらんぱる公園', '理想郷',
                     '理想郷東口', '大室高原二丁目', '大室山東', 'ファミリーガーデン', '瀬戸山', '高原中央', '株尻',
                     '南大室台入口', '池下林', '坂の下', '南原', '片倉', '池', '登山口', 'ふれあい広場', '池中野', '室の腰',
                     'ろう人形美術館', '桜の里', 'シャボテン公園']
    check_name_list = ['伊豆高原駅', '平松', '伊豆高原駅やまも口', '八幡野コミュニティセンター', '八幡野', '平松', 'ファミリーガーデン',
                       '瀬戸山', '高原中央', '株尻', '南大室台入口', '池下林', '坂の下', '南原', '片倉', '池', '登山口',
                       'ふれあい広場', '池中野']
    expected = ['伊豆海洋公園', '蓮着寺', '城ヶ崎オレンジ村', 'ルネッサ城ヶ崎', '蓮着寺口', '伊東高校城ヶ崎分校',
                '対島中学校正門', '対島中学校', '伊豆高原駅', '平松', '伊豆高原駅やまも口', '八幡野コミュニティセンター',
                '八幡野', '平松', '伊豆高原駅', '平松', '伊豆高原駅やまも口', '八幡野コミュニティセンター', '八幡野', '平松',
                'ファミリーガーデン', '対島中学校', '四辻', '池入口', '先原', '光の村', '東大室', 'ぐらんぱる公園', '理想郷',
                '理想郷東口', '大室高原二丁目', '大室山東', 'ファミリーガーデン', '瀬戸山', '高原中央', '株尻',
                '南大室台入口', '池下林', '坂の下', '南原', '片倉', '池', '登山口', 'ふれあい広場', '池中野', '室の腰',
                'ろう人形美術館', '桜の里', 'シャボテン公園']
    assert create_name_list(old_name_list, check_name_list) == expected


# old_name_listとcheck_name_listの両方に同じ名前があってcheck_name_listの方が途中で終わるパターン
def test_create_name_list6():
    old_name_list = ['A', 'B', 'C', 'B', 'D', 'E']
    check_name_list = ['C', 'A', 'B', 'C', 'D']
    expected = ['C', 'A', 'B', 'C', 'B', 'D', 'E']
    assert create_name_list(old_name_list, check_name_list) == expected
