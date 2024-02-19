import requests 
import lxml 
import json
from lxml import  html
import re 


class scraper():
    HOST = 'https://www.bluesky.pl/'
   
    @staticmethod
    def read_it(link_to_site):
        response = requests.get(link_to_site)
        tree = html.fromstring(response.content)
        return tree
    
    def extraction(self):
        tree = self.read_it(self.HOST)
        cheap_flights_slug = tree.xpath('//a[@title="Tanie loty z Polski"]//@href')
        tree_for_list_of_flights = self.read_it(f'https://www.bluesky.pl/{cheap_flights_slug}')
        conteners_with_info = tree_for_list_of_flights.xpath('//div[@class="best-flights__data-container with__price"]')
        for contener in conteners_with_info:
            destination = contener.xpath('//span[@class="best-flights__country-text"]/text()')
            link_to_details = contener.xpath('//div[@class="best-flights__btn-wrapper"]//a//@href')
            tree_details_no_date = self.read_it(link_to_details)
            link_to_final_details = tree_details_no_date.xpath('//div[@class="best-flights__btn-wrapper"]//a//@href')
            tree_details_final = self.read_it(link_to_final_details)
            final_conteners = tree_details_final.xpath('//div[@class="best-flights__data-container with__price"]')
            details = []
            for f_contener in final_conteners:
                departure_place = f_contener.xpath('//span[@class="best-flights__country-text"]/text()')
                price = f_contener.xpath('//span[@class="best-flights__price"]/text()')
                flight_details = {
                        "price" : price,
                        "departure" : departure_place                
                        }
                details.append(flight_details)
            flight_final_details = {
                "destination": destination,
                "prices_and_departure": flight_details
            }
            with open('StreetHerbalist/scrappers/flying_sites/info.json', "a+") as file:
                json.dumps(file)




instance = scraper()
instance.extraction(self)
