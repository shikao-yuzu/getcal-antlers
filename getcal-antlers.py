import os
import csv
import re
import datetime
from bs4 import BeautifulSoup
import requests
import jaconv


# 取得対象のWebサイト
URL_ANTLERS_CAL = 'http://www.so-net.ne.jp/antlers/games'

# 出力ファイル名
OUTPUT_PATH = 'antlers.csv'

# 年
YEAR_NOW = '2019'


def output_game_schedule(soup: BeautifulSoup, competitions: list, idx_comp: int) -> None:
    """
    @brief:
      試合情報(HTML)をパースしてGoogleカレンダー用のCSVに出力
    """
    # テーブルの取得
    tables = soup.findAll(name='table')

    # 大会名
    comp = competitions[idx_comp]

    # 試合リスト
    game_lists = tables[idx_comp].findAll(name='tr')

    # 出力ファイルの再オープン
    csvFile = open(OUTPUT_PATH, 'at', newline = '', encoding = 'shift_jis')
    writer = csv.writer(csvFile)

    # パース＆出力
    try:
        for idx_game, game in enumerate(game_lists):
            # 表ラベルは不要
            if idx_game == 0:
                continue

            parsed_game = []
            for idx_cell, cell in enumerate(game.findAll(name=['td', 'th'])):
                s = cell.get_text().strip().replace('\n','')

                # 中継以降の列は飛ばす
                if idx_cell > 3:
                    continue

                # 全角英数字を半角に変換
                s_z2h = jaconv.z2h(s, kana=False, digit=True, ascii=True)

                parsed_game.append(s_z2h)

            # 節
            sec = parsed_game[0]

            # 日時
            date_time = re.split('[or +)(※]', parsed_game[1])
            day       = date_time[0]
            s_time    = date_time[-1]

            # 終日イベントフラグと終了時刻の設定
            if s_time == '未定':
                all_day_flag = 'TRUE'
                s_time       = ''
                e_time       = ''
            else:
                all_day_flag = ''
                s_time_dt    = datetime.datetime.strptime(s_time, '%H:%M')
                e_time_dt    = s_time_dt + datetime.timedelta(hours = 2)
                e_time       = e_time_dt.strftime('%H:%M')

            # 対戦相手
            team = parsed_game[2]

            # スタジアム
            stadium = parsed_game[3]

            csvRow = []
            csvRow.append(comp+' '+sec+' '+team)
            csvRow.append(YEAR_NOW+'/'+day)
            csvRow.append(s_time)
            csvRow.append(YEAR_NOW+'/'+day)
            csvRow.append(e_time)
            csvRow.append(all_day_flag)
            csvRow.append('')
            csvRow.append(stadium)

            writer.writerow(csvRow)
    finally:
        csvFile.close()


def main():
    """
    @brief:
      メイン関数
    """
    # Webサイトにgetリクエストで送信し情報を取得
    r = requests.get(URL_ANTLERS_CAL)

    # HTTPレスポンスボディを取得
    html = r.text

    # 取得元のHTMLタグが壊れていて読み込みに失敗するため，パース前にHTMLファイルの該当行を削除
    # (2019/07/07時点)
    html_mod = ''
    for s in html.splitlines():
        if '</a></span></li</ul>' in s:
            pass
        else:
            html_mod += s + os.linesep

    # BeautifulSoupオブジェクトの生成
    soup = BeautifulSoup(html_mod, 'html.parser')

    # 出場大会のリストを構築
    competitions = []
    for c in soup.findAll(name='div', attrs={'class': 'title_name_m0'}):
        # 全角英数字を半角に変換
        c_z2h = jaconv.z2h(c.string, kana=False, digit=True, ascii=True)

        # 除外する大会等
        if c_z2h == '過去の試合結果':
            continue

        competitions.append(c_z2h)

    # ヘッダ行のCSV出力
    csvFile = open(OUTPUT_PATH, 'wt', newline = '', encoding = 'shift_jis')
    writer = csv.writer(csvFile)
    try:
        writer.writerow(['Subject', 'Start Date' , 'Start Time', 'End Date', 'End Time', 'All Day Event', 'Description', 'Location'])
    finally:
        csvFile.close()

    # 試合情報のCSV出力
    for idx_comp in range(len(competitions)):
        output_game_schedule(soup, competitions, idx_comp)


if __name__ == '__main__':
    main()
