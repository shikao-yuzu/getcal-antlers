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

    print(soup.select('.game'))


if __name__ == '__main__':
    main()
