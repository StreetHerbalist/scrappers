
import requests
import json
from lxml import html
from typing import List, Any, Dict
import time
import re

class ScraperAndExtraction():
    HOST = "https://www.werstreamt.es"
    providers_list = []
    providers_info_list = []

    @staticmethod
    def read_it(link_to_site):
        response = requests.get(link_to_site)
        tree = html.fromstring(response.content)
        return tree
    @staticmethod
    def cleaning(text):
        cleaned_text = re.sub(r'[()]', '', text)
        return cleaned_text
    
    @staticmethod
    def save_data(name_of_provider,link_f,counted_series,counted_films):
        final_dict = {
                            "provider_name": name_of_provider,
                            "url": link_f,
                            "serie_count": counted_series,
                            "movie_count": counted_films
                        }
        with open(r'C:\Users\pvtru\Desktop\Programy Itd\Testing\providers_info.json', 'a+') as file:
            json.dump(final_dict, file, indent=4)
    
    @staticmethod
    def counting(tree_last): 
        counted_films = "".join(tree_last.xpath('//a[contains (text(), "Filme")]//span//text()'))
        counted_series = "".join(tree_last.xpath('//a[contains (text(), "Serien")]//span//text()'))
        name_of_provider = 
        
        return counted_films, counted_series, name_of_provider
         
    
    def get_providers(self):
        tree = self.read_it(self.HOST)
        providers_slug = tree.xpath('//ul[@class="providers"]//@href')
        for slug in providers_slug:
            link = (f'https://www.werstreamt.es{slug}')
            self.providers_list.append(link)
     
    def page_load(self):
        for link_f in self.providers_list:
            tree = self.read_it(link_f)
            slug_to_films = tree.xpath('//span[@class="read-more"]//@href')
            # link_to_f = 
            links_to_chan =[]
            if not slug_to_films : 
                slug_to_channels = tree.xpath("//a[@class='right small']//@href")
                for slugx in slug_to_channels:
                    link_to_f = f'https://www.werstreamt.es{slugx}'
                    tree_last = self.read_it(link_to_f)
                    slug_to_more = tree_last.xpath('//span[@class="read-more"]//@href')
                    if not slug_to_more:
                        name_of_provider = "".join(tree_last.xpath('//h1[@class="clearfix"]//a//text()'))
                        counted_films = self.cleaning("".join(tree_last.xpath('//a[contains (text(), "Filme")]//span//text()')))
                        counted_series = self.cleaning("".join(tree_last.xpath('//a[contains (text(), "Serien")]//span//text()')))                   
                        save = self.save_data(name_of_provider,link_f,counted_series,counted_films)
                    else : 
                        link_to_f = f'https://www.werstreamt.es{slug_to_more[0]}'
                        tree_last = self.read_it(link_to_f)
                        name_of_provider = "".join(tree_last.xpath('//h1[@class="clearfix"]//a//text()'))
                        counted_films = self.cleaning("".join(tree_last.xpath('//a[contains (text(), "Filme")]//span//text()')))
                        counted_series = self.cleaning("".join(tree_last.xpath('//a[contains (text(), "Serien")]//span//text()')))
                        save = self.save_data(name_of_provider,link_f,counted_series,counted_films)
            else:
                link_to_f = f'https://www.werstreamt.es{slug_to_films[0]}'
                tree_last = self.read_it(link_to_f)
                slug_to_alle = tree_last.xpath('//ul[@class="dropdown"]//a[contains(text(), "Alle")]//@href')
                counted_films = tree_last.xpath('//a[contains (text(), "Filme")]//span//text()')
                if counted_films:
                    name_of_provider = "".join(tree_last.xpath('//h1[@class="clearfix"]//a//text()'))
                    counted_films = self.cleaning("".join(tree_last.xpath('//a[contains (text(), "Filme")]//span//text()')))
                    counted_series = self.cleaning("".join(tree_last.xpath('//a[contains (text(), "Serien")]//span//text()')))
                    save = self.save_data(name_of_provider,link_f,counted_series,counted_films)   
                else:
                    link_for_counting = f'https://www.werstreamt.es{slug_to_alle[2]}'
                    tree_las = self.read_it(link_for_counting)
                    name_of_provider = "".join(tree_las.xpath('//h1[@class="clearfix"]//a//text()'))
                    counted_films = self.cleaning("".join(tree_las.xpath('//a[contains (text(), "Filme")]//span//text()')))
                    counted_series = self.cleaning("".join(tree_las.xpath('//a[contains (text(), "Serien")]//span//text()')))
                    save = self.save_data(name_of_provider,link_f,counted_series,counted_films)
instance = ScraperAndExtraction()
instance.get_providers()
instance.page_load()