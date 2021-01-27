from python_picnic_api import PicnicAPI
import json
from supermarktconnector.jumbo import JumboConnector
from supermarktconnector.ah import AHConnector
from grocy import GrocyAPI
import requests
import urllib.request
import re 
import config
from picnic_grocy_item import GrocyPicnicProduct



class PicnicSetupGrocy():

  picnic = PicnicAPI(username=picnic_user, password=picnic_passwd, country_code="NL", store=False)
  grocy = GrocyAPI(picnic_image_size, picnic_img_baseurl)
  json_picnic_data = {}
  
  def importIntoGrocy(self, url: str, api_url: str, key:str):
    print("Starting importing: " + url)
    json_data = json.loads(requests.get(url).text)
    for obj in json_data[key]:
      print("Importing: " + obj["name"] + " into grocy database...")
      res = self.grocy.postToGrocy(api_url, obj)
      if not res.ok:
        print("failed importing: " + res.text)

  def setupQuantities(self):
      importIntoGrocy(config.picnic_quantity_list, "objects/quantity_units", "data")

  def setupUserfields(self):
      importIntoGrocy(config.picnic_userfields_list, "objects/userfields", "data")

  def setupStoreAndLocation(self):
      importIntoGrocy(config.picnic_stores_list, "objects/shopping_locations", "data")
      importIntoGrocy(config.picnic_location_list, "objects/locations", "data")

  