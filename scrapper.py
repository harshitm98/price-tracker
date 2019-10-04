import requests
from lxml import html


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
url = []
url.append("https://www.amazon.in/HP-X3500-Wireless-Mouse-Black/dp/B00EZ3OPX6/ref=sr_1_14?crid=3P0LNG1GLI5KG&keywords=ergonomic+mouse&qid=1570210070&sprefix=ergo%2Caps%2C361&sr=8-14")
url.append("https://www.amazon.in/gp/product/B07HZ8JWCL/ref=s9_acss_bw_cg_J19W1Hp5_2b1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-4&pf_rd_r=T7E7VVSA61ZBTR2JD5MA&pf_rd_t=101&pf_rd_p=fc8cf619-f105-4895-8e09-357ba5b665ae&pf_rd_i=1388921031")
url.append("https://www.amazon.in/Logitech-Silent-Wireless-Large-Mouse/dp/B01JPOLKDW/ref=sr_1_17?crid=3P0LNG1GLI5KG&keywords=ergonomic+mouse&qid=1570210070&smid=A2FE28HTZZT4DB&sprefix=ergo%2Caps%2C361&sr=8-17")
url.append("https://www.amazon.in/gp/product/B07G8C2SG5/ref=s9_acss_bw_cg_Jupiter_5c1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-3&pf_rd_r=FX9PKDQ9GQQHMV350J7A&pf_rd_t=101&pf_rd_p=b8418346-10cd-4a9d-8140-c5aa93651ec6&pf_rd_i=1389401031")

i = 0
while(i < len(url)):
    resultPage = requests.get(url[i], headers=headers)
    resultPage.cookies.clear()
    if resultPage.status_code == 200:
        tree = html.fromstring(resultPage.content)
        with open("text.html", "w+") as f:
            f.write(str(resultPage.content))
        if str(resultPage.content).find("Robot Check") != -1:
            print("Robot check...")
            continue
        print("Normal price", tree.xpath(
            '//*[@id="priceblock_ourprice"]/text()'))
        print("Deal price", tree.xpath(
            '//*[@id="priceblock_dealprice"]/text()'))
        i += 1

    else:
        print(resultPage.status_code)
