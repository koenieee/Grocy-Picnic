from python_picnic_api import PicnicAPI
import appdaemon.plugins.hass.hassapi as hass
import json
from supermarktconnector.jumbo import JumboConnector
from supermarktconnector.ah import AHConnector
import requests


#
# PicNic Api app voor Grocey
#
# Args:
#
# 40097138 => donne huttenkase
# 8718796026464 => ontbijtspek
# 



class PicNic(hass.Hass):
  picnic_user = '####'
  picnic_passwd = '###'
  grocy_api_key = '####'
  grocy_api_url = 'https://####/api/'
  
  picnic = PicnicAPI(username=self.picnic_user, password=self.picnic_passwd, country_code="NL", store=False)
 # connector = JumboConnector()
  #connector = AHConnector()
  
  def initialize(self):
     self.log("PicNic Api AppDeamon")
     picnic = self.picnic
    # searchResFound = picnic.search('Cottage Cheese.')
     #
    #koppeling maken tussen api, picnic en albert heijn
     #searchResFound = self.connector.get_product_details(self.connector.get_product_by_barcode('40097138'))["title"]

     
     
    # searchResFound = json.dumps(self.connector.get_product_details(self.connector.get_product_by_barcode('8718796026464')),sort_keys=True, indent=4)
     
    # for x in picnic.get_deliveries()[0]["orders"][0]["items"]:
    #    name = x["items"][0]["name"]
    #    id = x["items"][0]["id"]
    #    image_ids = x["items"][0]["image_ids"][0]
    #    price = x["items"][0]["price"]
    #    self.addProductToGrocy(name, id, image_ids, price)




     
     #[1]
     #res = ' '.join(map(str, searchResFound)) #//picnic
     #res = searchResFound
    # self.log("PicNic: " + res)

  def postToGrocy(self, apiPart: str, postData: str):
    url = self.grocy_api_url + apiPart
    header = {'GROCY-API-KEY': self.grocy_api_key}
    header["Content-Type"] = 'application/json'
    header["accept"] = 'application/json'
    x = requests.post( url, data = postData, headers=header, verify=False)
    print(x.content)

  def addProductToGrocy(self, name: str, shop_id: str, imgId: str, price: str):
    postData = """
    {
      "name": \""""+name+"""\",
      "qu_id_purchase": \""""+shop_id+"""\",
      "qu_id_stock": "1",
      "qu_factor_purchase_to_stock": "1.0",
      "shopping_location_id": "3",
      "location_id":"1",
      "picture_file_name":"https://storefront-prod.nl.picnicinternational.com/static/images/"""+imgId+"""/tiny.png"
    }"""

    self.postToGrocy("objects/products", postData)

  def get_delivery(self, deliveryId: str):
     self.log("DeliveryID: " + deliveryId)
     path = "/product/" + deliveryId
     return self.picnic._get(path)
     
  def importLastPicnicDelivery(self):
    for x in picnic.get_deliveries()[0]["orders"][0]["items"]:
        name = x["items"][0]["name"]
        id = x["items"][0]["id"]
        image_ids = x["items"][0]["image_ids"][0]
        price = x["items"][0]["price"]
        self.addProductToGrocy(name, id, image_ids, price)

    
  def pretty_print_POST(self,req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
     
     
     
