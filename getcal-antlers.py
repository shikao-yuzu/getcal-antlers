import csv
from bs4 import BeautifulSoup
import requests


# 取得対象のWebサイト
URL_ANTLERS_CAL = 'http://www.so-net.ne.jp/antlers/games'


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

    # 出場大会一覧のリスト
    competitions = soup.findAll(name='div', attrs={'class': 'title_name_m0'})
    for c in competitions:
        print(c.string)

    # とりあえずCSV出力
    table = soup.findAll(name="table")[0]
    rows = table.findAll(name="tr")

    csvFile = open("test.csv", 'wt', newline = '', encoding = 'shift_jis')
    writer = csv.writer(csvFile)

    try:
        for row in rows:
            csvRow = []
            for cell in row.findAll(name=['td', 'th']):
                csvRow.append(cell.get_text().strip())
            writer.writerow(csvRow)
    finally:
        csvFile.close()


if __name__ == '__main__':
    main()
