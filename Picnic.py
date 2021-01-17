from python_picnic_api import PicnicAPI
import appdaemon.plugins.hass.hassapi as hass
import json
from supermarktconnector.jumbo import JumboConnector
from supermarktconnector.ah import AHConnector
import requests
import urllib.request
import re 

#
# PicNic Api app voor Grocey
#
# Args:
#
# 40097138 => donne huttenkase
# 8718796026464 => ontbijtspek
# 




class PicNic(hass.Hass):
  picnic_user = ''
  picnic_passwd = ''
  grocy_api_key = ''
  grocy_api_url = ''
  quantities=dict()
  
  picnic = PicnicAPI(username=picnic_user, password=picnic_passwd, country_code="NL", store=False)
 # connector = JumboConnector()
  #connector = AHConnector()
  
  def initialize(self):
     self.log("PicNic Api AppDeamon")
     
    # searchResFound = picnic.search('Cottage Cheese.')
     #
    #koppeling maken tussen api, picnic en albert heijn
     #searchResFound = self.connector.get_product_details(self.connector.get_product_by_barcode('40097138'))["title"]

     self.getQuantityUnits()
    # self.importLastPicnicDelivery()
     self.matchPicnicQuantityByGrocyQuantity("stuks")
    # self.fillQuantity("60 gram")
    # searchResFound = json.dumps(self.connector.get_product_details(self.connector.get_product_by_barcode('8718796026464')),sort_keys=True, indent=4)

     
     #[1]
     #searchResFound = json.dumps(self.get_delivery("10761823"),sort_keys=True, indent=4)
     #res = ' '.join(map(str, searchResFound)) #//picnic
     #res = searchResFound
    # self.log("PicNic: " + res)

  def getFromGrocy(self, apiPart: str):
    url = self.grocy_api_url + apiPart
    header = {'GROCY-API-KEY': self.grocy_api_key}
    header["Content-Type"] = 'application/json'
    header["accept"] = 'application/json'
    x = requests.get( url, headers=header, verify=False)
    return x


  def postToGrocy(self, apiPart: str, postData: str):
    url = self.grocy_api_url + apiPart
    header = {'GROCY-API-KEY': self.grocy_api_key}
    header["Content-Type"] = 'application/json'
    header["accept"] = 'application/json'
    x = requests.post( url, data = postData, headers=header, verify=False)
    return x

  def addProductToGrocy(self, name: str, shop_id: str, imgId: str, price: str):
    postData = """
    {
      "name": \""""+name+"""\",
      "qu_id_purchase": \""""+shop_id+"""\",
      "qu_id_stock": "1",
      "qu_factor_purchase_to_stock": "1.0",
      "shopping_location_id": "3",
      "location_id":"2",
      "picture_file_name":\""""+imgId+""".png\"
    }"""

    result = self.postToGrocy("objects/products", postData)
    if result.ok:
        print("Product toegevoegd")
    else:
        print("product NIET toegevoegd")

  def get_delivery(self, deliveryId: str):
     self.log("DeliveryID: " + deliveryId)
     path = "/product/" + deliveryId
     return self.picnic._get(path)
     
  def importLastPicnicDelivery(self):
    for x in self.picnic.get_deliveries()[0]["orders"][0]["items"]:
        name = x["items"][0]["name"]
        id = x["items"][0]["id"]
        image_ids = x["items"][0]["image_ids"][0]
        price = x["items"][0]["price"]
        unit_quantity = x["items"][0]["unit_quantity"]
        self.fillQuantity(unit_quantity)
       # self.addProductToGrocy(name, id, image_ids, price)
        
  def fillQuantity(self, quantity_text: str):
      print(quantity_text.replace(",", "."))
      replaced_text = quantity_text.replace(",", ".")
      temp = re.compile("([\d.]*\d+) ([a-zA-Z]+)") 
      res = temp.match(replaced_text).groups() 
      if res[1] == "x":
          temp = re.compile("([\d.]*\d+) x ([\d.]*\d+) ([a-zA-Z]+)") 
          res = temp.match(replaced_text).groups() 
          calculatie = int(res[0]) * int(res[1])
          new = {calculatie, res[2]}
          print("Speciale actie: " + str(new))
          
      
      print("Qantitiy: " + str(res[0]) + " ID: " + str(self.matchPicnicQuantityByGrocyQuantity(res[1])))
      
  def matchPicnicQuantityByGrocyQuantity(self, picnicQuantity: str):
     print("picnicquanitity: " + picnicQuantity)
     print([self.quantities[key] for key in self.quantities if picnicQuantity in key.lower()])
     #return self.quantities[picnicQuantity]["id"]
    # for quantity in self.quantities:
         
    #     if picnicQuantity == quantity["name"):
     #        return quantity["id"]
      
  def getQuantityUnits(self):
      x = self.getFromGrocy('objects/quantity_units')
      json_data = json.loads(x.text)
      #print(json_data)
      for quantity in json_data:
         self.quantities[quantity["name"]] = quantity["id"]
      print(self.quantities)
    
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
     
     
     
