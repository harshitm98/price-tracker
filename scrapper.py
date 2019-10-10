import requests
from lxml import html, etree
import json


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
url = []
url.append("https://www.amazon.in/HP-X3500-Wireless-Mouse-Black/dp/B00EZ3OPX6/ref=sr_1_14?crid=3P0LNG1GLI5KG&keywords=ergonomic+mouse&qid=1570210070&sprefix=ergo%2Caps%2C361&sr=8-14")
url.append("https://www.amazon.in/gp/product/B07HZ8JWCL/ref=s9_acss_bw_cg_J19W1Hp5_2b1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-4&pf_rd_r=T7E7VVSA61ZBTR2JD5MA&pf_rd_t=101&pf_rd_p=fc8cf619-f105-4895-8e09-357ba5b665ae&pf_rd_i=1388921031")
url.append("https://www.amazon.in/Logitech-Silent-Wireless-Large-Mouse/dp/B01JPOLKDW/ref=sr_1_17?crid=3P0LNG1GLI5KG&keywords=ergonomic+mouse&qid=1570210070&smid=A2FE28HTZZT4DB&sprefix=ergo%2Caps%2C361&sr=8-17")
url.append("https://www.amazon.in/gp/product/B07G8C2SG5/ref=s9_acss_bw_cg_Jupiter_5c1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-3&pf_rd_r=FX9PKDQ9GQQHMV350J7A&pf_rd_t=101&pf_rd_p=b8418346-10cd-4a9d-8140-c5aa93651ec6&pf_rd_i=1389401031")
url.append('https://www.amazon.in/gp/product/B07HGH3G46/ref=s9_acss_bw_cg_Topbann_2c1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-4&pf_rd_r=87HV9NERA664RNVRESB6&pf_rd_t=101&pf_rd_p=6c0e5a1a-a9c2-441c-968c-513e0354b7a3&pf_rd_i=16613114031')


def fetch_offers(tree):
    list_of_offers = []
    try:
        print("The length of list is {}".format(
            len(tree.xpath("//li[@class='a-spacing-small a-spacing-top-small']"))))
        for elem in tree.xpath("//span[@class='a-list-item']/text()"):
            if str(elem).strip() != "":
                if not str(elem).replace("\n", "").replace("\t", "").replace("  ", "").__contains__("Check eligibility here!"):
                    list_of_offers.append(str(elem).replace("\n", "").replace(
                        "\t", "").replace("  ", ""))
        print(list_of_offers[-len(tree.xpath("//li[@class='a-spacing-small a-spacing-top-small']")):])
                    
    except Exception as e:
        print(Exception, e)


i = 0
retry_count = 0
while(i < len(url)):
    resultPage = requests.get(url[i], headers=headers)
    if resultPage.status_code == 200:
        tree = html.fromstring(resultPage.content)
        if str(resultPage.content).find("Robot Check") != -1:
            # print("Robot check...")
            retry_count += 1
            continue
        list_dict_keys_of_images_url = list(json.loads(tree.xpath(
            '//*[@id="landingImage"]/@data-a-dynamic-image')[0]).keys())
        list_dict_keys_of_images_url.sort()
        try:
            price = str(tree.xpath(
                '//*[@id="priceblock_ourprice"]/text()')[0]).replace("\xa0", "")
        except Exception as e:
            price = str(tree.xpath(
                '//*[@id="priceblock_dealprice"]/text()')[0]).replace("\xa0", "")
        print("Title: {}\nPrice: {}\nImage Url: {}".format(str(tree.xpath(
            '//*[@id="productTitle"]/text()')[0]).strip(), price, list_dict_keys_of_images_url[0]))
        fetch_offers(tree)
        i += 1
    else:
        print("Error fetching the page. Error code: {}".format(resultPage))

print("Total Retries : {}".format(retry_count))
