import requests
from lxml import html, etree
import json


class AmazonScrapper:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Host': 'www.amazon.in',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    def __init__(self, url):
        print('Running Amazon Scrapper...')
        self.url = url

    def is_robot_check(self, result_page, retry_count):
        if str(result_page.content).find("Robot Check") != -1:
            print("Robot check...")
            retry_count += 1
            return True


    def get_title(self, tree):
        return str(tree.xpath(
                '//*[@id="productTitle"]/text()')[0]).strip()

    def get_price(self, tree):
        try:
            normal_price = 0  # if exception occurs while fetching normal price below, because there is a deal - then normal price would be 0
            normal_price = str(tree.xpath(
                '//*[@id="priceblock_ourprice"]/text()')[0]).replace("\xa0", "")
            deal_price = 0
            return normal_price
        except Exception as e:
            deal_price = str(tree.xpath(
                '//*[@id="priceblock_dealprice"]/text()')[0]).replace("\xa0", "")
            return deal_price

    def get_image(self, tree):
        list_dict_keys_of_images_url = list(json.loads(tree.xpath(
                '//*[@id="landingImage"]/@data-a-dynamic-image')[0]).keys())
        list_dict_keys_of_images_url.sort()
        return list_dict_keys_of_images_url[0]

    def get_ratings(self, tree):
        # TODO: Get the ratings
        return

    def get_details(self, tree):
        title = self.get_title(tree)
        price = self.get_price(tree)
        image_url = self.get_image(tree)
        offers_list = self.get_offers_list(tree)
        print("Title: {}\nPrice: {}\nImage Url: {}\nOffers: {}\n\n".format(title, price, image_url, offers_list))


    # returns a list of offers and deals
    def get_offers_list(self, tree):
        list_of_offers = []
        try:
            # print("The length of list is {}".format(
            #     len(tree.xpath("//li[@class='a-spacing-small a-spacing-top-small']"))))
            for elem in tree.xpath("//span[@class='a-list-item']/text()"):
                if str(elem).strip() != "":
                    if not str(elem).replace("\n", "").replace("\t", "").replace("  ", "").__contains__("Check eligibility here!"):
                        list_of_offers.append(str(elem).replace("\n", "").replace(
                            "\t", "").replace("  ", ""))

            list_of_offers = list_of_offers[-len(tree.xpath(
                "//li[@class='a-spacing-small a-spacing-top-small']")):]
            return list_of_offers

        except Exception as e:
            print(Exception, e)
            return []

    def load_url(self, retry_count=0):
        result_page = requests.get(url, headers=self.headers)
        if result_page.status_code == 200:
            tree = html.fromstring(result_page.content)
            if self.is_robot_check(result_page, retry_count):
                return
            self.get_details(tree)

        else:
            print("Error fetching the page. Error code: {}".format(result_page))

    def search_by_title(self):
        # TODO: Search by title for comparision
        return

    def search_by_category(self):
        # TODO: To be implemented for searching by category
        return

    def cleaning_offers(self):
        # TODO: Sanitizing the offers
        return


if __name__ == '__main__':
    urls = []
    urls.append("https://www.amazon.in/HP-X3500-Wireless-Mouse-Black/dp/B00EZ3OPX6/ref=sr_1_14?crid=3P0LNG1GLI5KG&keywords=ergonomic+mouse&qid=1570210070&sprefix=ergo%2Caps%2C361&sr=8-14")
    urls.append("https://www.amazon.in/gp/product/B07HZ8JWCL/ref=s9_acss_bw_cg_J19W1Hp5_2b1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-4&pf_rd_r=T7E7VVSA61ZBTR2JD5MA&pf_rd_t=101&pf_rd_p=fc8cf619-f105-4895-8e09-357ba5b665ae&pf_rd_i=1388921031")
    urls.append("https://www.amazon.in/Logitech-Silent-Wireless-Large-Mouse/dp/B01JPOLKDW/ref=sr_1_17?crid=3P0LNG1GLI5KG&keywords=ergonomic+mouse&qid=1570210070&smid=A2FE28HTZZT4DB&sprefix=ergo%2Caps%2C361&sr=8-17")
    urls.append("https://www.amazon.in/gp/product/B07G8C2SG5/ref=s9_acss_bw_cg_Jupiter_5c1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-3&pf_rd_r=FX9PKDQ9GQQHMV350J7A&pf_rd_t=101&pf_rd_p=b8418346-10cd-4a9d-8140-c5aa93651ec6&pf_rd_i=1389401031")
    urls.append('https://www.amazon.in/gp/product/B07HGH3G46/ref=s9_acss_bw_cg_Topbann_2c1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-4&pf_rd_r=87HV9NERA664RNVRESB6&pf_rd_t=101&pf_rd_p=6c0e5a1a-a9c2-441c-968c-513e0354b7a3&pf_rd_i=16613114031')

    for url in urls:
        AmazonScrapper(url).load_url()
