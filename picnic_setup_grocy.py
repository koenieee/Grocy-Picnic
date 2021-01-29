from python_picnic_api import PicnicAPI
import json
from grocy import GrocyAPI
import requests
import re
import config


class PicnicSetupGrocy():

    picnic = PicnicAPI(username=config.picnic_user,
                       password=config.picnic_passwd, country_code="NL", store=False)
    grocy = GrocyAPI(config.picnic_img_size, config.picnic_img_baseurl)
    json_picnic_data = {}

    def importIntoGrocy(self, url: str, api_url: str, key: str):
        print("Starting importing: " + url)
        json_data = json.loads(requests.get(url).text)
        for obj in json_data[key]:
            print("Importing: " + obj["name"] + " into grocy database...")
            res = self.grocy.postToGrocy(api_url, obj)
            if not res.ok:
                print("failed importing: " + res.text)

    def setupQuantities(self):
        self.importIntoGrocy(config.picnic_quantity_list,
                             "objects/quantity_units", "data")

    def setupUserfields(self):
        self.importIntoGrocy(config.picnic_userfields_list,
                             "objects/userfields", "data")

    def setupStoreAndLocation(self):
        self.importIntoGrocy(config.picnic_stores_list,
                             "objects/shopping_locations", "data")
        self.importIntoGrocy(config.picnic_location_list,
                             "objects/locations", "data")

    def installAll(self):  # make sure to have an empty grocy database.
        self.setupUserfields()
        self.setupStoreAndLocation()
        self.setupQuantities()
