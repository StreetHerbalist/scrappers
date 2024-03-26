import requests
import lxml
from lxml import html
import re
import pprint
import re

class __MAIN__ ():
    HOST = "https://books.toscrape.com/"
    links_to_books = []
    def ekstrakcja():
        page = requests.get(__MAIN__.HOST)
        tree = html.fromstring(page.content)
        slugs_to_books = tree.xpath("//li[@class='col-xs-6 col-sm-4 col-md-3 col-lg-3']//@href")
        for xp in slugs_to_books:
            link = "".join(f'{__MAIN__.HOST}/{xp}')
            __MAIN__.links_to_books.append(link)
        for final_link in __MAIN__.links_to_books:
            page_fin=requests.get(final_link)
            final_tree = html.fromstring(page_fin.content)
            price = ('//p[@class="price_color"]//text()')
            table = "".join(final_tree.xpath('//table[@class="table table-striped"]//text()')).split()
            id = table[0]
            breadcrumbs = final_tree.xpath('//ul[@class="breadcrumb"]//text()')
            cleand = re.sub(r'[ [\]\n]', '', str(breadcrumbs))
            clean = re.sub(r'[\n]', '', cleand)
            categories = clean[-1]
            table_set = """{
                       "PRODUCT_INFO": "{table}"
               }"""
            with open("C:\Users\pvtru\Desktop\ProgramyItd\data_set.json", "+a") as file:
                file.json.dump(table_set)

instance = __MAIN__
instance.ekstrakcja()

