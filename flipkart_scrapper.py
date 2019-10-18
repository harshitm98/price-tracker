import requests
from lxml import html, etree
import json


class FlipkartScrapper:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Host': 'www.flipkart.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    def __init__(self, url):
        print('Running Flipkart scrapper...')

    def get_title_price_image_ratings(self, retry_count=0):
        resultPage = requests.get(url, headers=self.headers)
        if resultPage.status_code == 200:
            tree = html.fromstring(resultPage.content)
            title = ""
            # Title
            for elem in tree.xpath('//span[@class="_35KyD6"]/text()'):
                title += elem
            # Price
            for elem in tree.xpath('//div[@class="_1vC4OE _3qQ9m1"]/text()'):
                price = elem
            # Images
            image_urls = []
            for elem in tree.xpath('//div[@class="_2_AcLJ"]/@style'):
                elem = str(elem)
                if elem.find("url(") != -1:
                    image_url = elem[elem.find("url(") + 4:elem.find(
                        ")", elem.find("url(") + 4)]
                    image_urls.append(image_url)
            if len(image_urls) == 0:
                for elem in tree.xpath('//div[@class="_2_AcLJ _3_yGjX"]/@style'):
                    elem = str(elem)
                    if elem.find("url(") != -1:
                        image_url = elem[elem.find("url(") + 4:elem.find(
                            ")", elem.find("url(") + 4)]
                        image_urls.append(image_url)
            # Ratings
            ratings = ""
            for elem in tree.xpath('//div[@class="hGSR34"]'):
                 ratings = elem.text
            if ratings == "":
                for elem in tree.xpath('//div[@class="hGSR34 bqXGTW"]'):
                    ratings = elem.text

            # Offers
            offers = []
            for elem in tree.xpath('//li["_2-n-Lg col"]/span'):
                # To avoid <span class="_2YJn2R">Bank Offer</span>
                if elem.get("class") != "_2YJn2R":
                    etree.strip_tags(elem,'strong')
                    offers.append(elem.text)
                    
            print("Title: {}\tPrice: {}\tImage Url: {}\tNumber of Images: {}\tRating: {}\tOffers: {}".format(
                title, price, image_urls[0], len(image_urls), ratings, offers))


if __name__ == '__main__':
    urls = []
    urls.append('https://www.flipkart.com/kraasa-boys-lace-running-shoes/p/itmfg6fwgn7z8mfh?pid=KSSFG5NZCHQRKZHM&lid=LSTKSSFG5NZCHQRKZHMSBRJFO&marketplace=FLIPKART&srno=b_1_1&otracker=nmenu_sub_Baby%20%26%20Kids_0_Sport%20Shoes&fm=organic&iid=en_TOqF4xV%2F2sGPk8wDEMDFFL1Wp7qLxmo6HlcoglvTKZ1I3oytCtY1kOIHV2mGoOSdIGj51WcqgqwRyjstF%2Fxx2g%3D%3D&ppt=browse&ppn=browse&ssid=f3mpjm8u0o5lz8qo1570910705601')
    urls.append('https://www.flipkart.com/azacus-analog-multicolor-clock/p/itmfhz7yzkqb4hws?pid=TCKFHZ3QUNQF3UVG&lid=LSTTCKFHZ3QUNQF3UVGGN8CZO&marketplace=FLIPKART&spotlightTagId=BestvalueId_arb%2Fkjw&srno=b_1_3&otracker=browse&iid=cf728cd1-0de3-483e-a544-5467d8f8bac7.TCKFHZ3QUNQF3UVG.SEARCH&ppt=browse&ppn=browse&ssid=e9q6zqmlgdh3d7uo1570910676931')
    urls.append('https://www.flipkart.com/redmi-note-7s-astro-moonlight-white-32-gb/p/itm5e8bac3bcf4c4?pid=MOBFJFZDP9R3Z7YK&lid=LSTMOBFJFZDP9R3Z7YKQJSH2X&marketplace=FLIPKART&sattr[]=color&sattr[]=storage&sattr[]=ram&st=ram&otracker=hp_omu_Top%252BOffers_2_3.dealCard.OMU_88559FM66S42_3')

    for url in urls:
        FlipkartScrapper(url).get_title_price_image_ratings()
