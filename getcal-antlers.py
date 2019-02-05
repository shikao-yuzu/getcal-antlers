import csv
from bs4 import BeautifulSoup
import requests
import jaconv


# 取得対象のWebサイト
URL_ANTLERS_CAL = 'http://www.so-net.ne.jp/antlers/games'

# 出力ファイル名
OUTPUT_PATH = 'antlers.csv'


def output_game_schedule(soup: BeautifulSoup, competitions: list, idx_comp: int) -> None:
    """
    @brief:
      試合情報をCSVに出力
    """
    tables = soup.findAll(name='table')
    if (idx_comp >= len(tables)):
        return

    comp = competitions[idx_comp]

    rows = tables[idx_comp].findAll(name='tr')

    csvFile = open(OUTPUT_PATH, 'at', newline = '', encoding = 'shift_jis')
    writer = csv.writer(csvFile)

    try:
        for idx_row, row in enumerate(rows):
            # 表ラベルは不要
            if idx_row == 0:
                continue

            rowTmp = []
            for idx_cell, cell in enumerate(row.findAll(name=['td', 'th'])):
                s = cell.get_text().strip().replace('\n','')

                # 中継以降の列は飛ばす
                if idx_cell > 3:
                    continue

                rowTmp.append(s)

            csvRow = []
            csvRow.append(comp+' '+rowTmp[0]+' '+rowTmp[2])
            csvRow.append(rowTmp[1])
            csvRow.append('')
            csvRow.append('')
            csvRow.append('')
            csvRow.append('')
            csvRow.append(rowTmp[3])

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

    # BeautifulSoupオブジェクトの生成
    soup = BeautifulSoup(html, 'html.parser')

    # 出場大会のリストを構築
    competitions = []
    for c in soup.findAll(name='div', attrs={'class': 'title_name_m0'}):
        competitions.append(jaconv.z2h(c.string, kana=False, digit=True, ascii=True))

    # タイトル行の出力
    csvFile = open(OUTPUT_PATH, 'wt', newline = '', encoding = 'shift_jis')
    writer = csv.writer(csvFile)
    try:
        writer.writerow(['件名', '開始日' , '開始時刻', '終了日', '終了時刻', '終日イベント', '場所'])
    finally:
        csvFile.close()

    # 試合情報の追記
    for idx_comp in range(len(competitions)):
        output_game_schedule(soup, competitions, idx_comp)


if __name__ == '__main__':
    main()
