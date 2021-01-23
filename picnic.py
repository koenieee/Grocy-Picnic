from python_picnic_api import PicnicAPI
#import appdaemon.plugins.hass.hassapi as hass
import json
from supermarktconnector.jumbo import JumboConnector
from supermarktconnector.ah import AHConnector
from grocy import GrocyAPI
import requests
import urllib.request
import re 
import config


class PicNic():
  picnic_user = config.picnic_user
  picnic_passwd = config.picnic_passwd

  quantities=dict()
  
  
  picnic = PicnicAPI(username=picnic_user, password=picnic_passwd, country_code="NL", store=False)
  grocy = GrocyAPI()
 # connector = JumboConnector()
  #connector = AHConnector()
  
  def initialize(self):
    
    # searchResFound = picnic.search('Cottage Cheese.')
     #
    #koppeling maken tussen api, picnic en albert heijn
     #searchResFound = self.connector.get_product_details(self.connector.get_product_by_barcode('40097138'))["title"]
   # self.addPicnicIDToProduct(40, "900")
   # print(self.getProductInformation("10764022"))
    #self.grocy.changePictureFileNameProduct("45", self.grocy.uploadProductPictureToGrocy("d3176c7b1cd82af60db515e93679768449919709c1e3a2525a3e0a3a9a7460f8"))
     self.getQuantityUnits()
     self.importLastPicnicDelivery()
  #   self.matchPicnicQuantityByGrocyQuantity("stuks")
    # self.fillQuantity("60 gram")
    # searchResFound = json.dumps(self.connector.get_product_details(self.connector.get_product_by_barcode('8718796026464')),sort_keys=True, indent=4)

     
     #[1]
     #searchResFound = json.dumps(self.get_delivery("10761823"),sort_keys=True, indent=4)
     #res = ' '.join(map(str, searchResFound)) #//picnic
     #res = searchResFound
    # self.log("PicNic: " + res)


  def addPicnicIDToProduct(self, product_id:str, picnic_id:str):
    self.grocy.addUserFieldToProduct(str(product_id), "{\"picnic\":\""+picnic_id+"\"}")


  def addPicNicProductToGrocy(self, name: str, tara_weight: str, qu_id:str, picnic_id: str, imgId: str, price: str):
    postData = """
    {
      "name": \""""+name+"""\",
      "qu_id_purchase": \""""+qu_id+"""\",
      "qu_id_stock": \""""+qu_id+"""\",
      "qu_factor_purchase_to_stock": "1.0",
      "shopping_location_id": "1",
      "location_id":"2",
      "tare_weight": \""""+tara_weight+"""\"
    }"""

    result = self.grocy.postToGrocy("objects/products", postData)
    if result.ok:
        json_result = json.loads(result.text)
        grocy_product_id = json_result["created_object_id"]
        print("Product toegevoegd, nu picnicID toevoegen, grocy_id: " + grocy_product_id + ", picnic_id: " + picnic_id)
        self.addPicnicIDToProduct(grocy_product_id, picnic_id)
        print("Afbeelding uploaden.")
        self.grocy.changePictureFileNameProduct(grocy_product_id, self.grocy.uploadProductPictureToGrocy(imgId))
    else:
        print("product NIET toegevoegd, want: " + result.text)

  def getProductInformation(self, productID: str):
    # path = "/product/" + productID, just a test.
     path = '/my_store/'
     return self.picnic._get(path)
     
  def importLastPicnicDelivery(self):
    for x in self.picnic.get_deliveries()[0]["orders"][0]["items"]:
       x = self.picnic.get_deliveries()[0]["orders"][0]["items"]
       name = x["items"][0]["name"]
       id = x["items"][0]["id"]
       image_ids = x["items"][0]["image_ids"][0]
       price = x["items"][0]["price"]
       unit_quantity = x["items"][0]["unit_quantity"]
       converted_quantity = self.fillQuantity(unit_quantity)
       self.addPicNicProductToGrocy(name, converted_quantity[0], converted_quantity[1], id, image_ids, price)
        
  def fillQuantity(self, quantity_text: str):
      replaced_text = quantity_text.replace(",", ".")
      temp = re.compile("([\d.]*\d+) ([a-zA-Z]+)") 
      res = temp.match(replaced_text).groups() 
      if res[1] == "x":
          temp = re.compile("([\d.]*\d+) x ([\d.]*\d+) ([a-zA-Z]+)") 
          res = temp.match(replaced_text).groups() 
          calculatie = int(res[0]) * int(res[1])
          new = [calculatie, res[2]]
          
          return [str(new[0]), str(self.matchPicnicQuantityByGrocyQuantity(new[1]))]
      else:    
          return [str(res[0]), str(self.matchPicnicQuantityByGrocyQuantity(res[1]))] #returns HOW_MUCH, WHAT_KIND_OF
      
  def matchPicnicQuantityByGrocyQuantity(self, picnicQuantity: str):
     #print("picnicquanitity: " + picnicQuantity)
     found_quantity = ([self.quantities[key] for key in self.quantities if picnicQuantity in key.lower()])
     if len(found_quantity) > 0:
         return found_quantity[0]
     else:
         return 0
     #return self.quantities[picnicQuantity]["id"]
    # for quantity in self.quantities:
         
    #     if picnicQuantity == quantity["name"):
     #        return quantity["id"]
      


  def getQuantityUnits(self):
      x = self.grocy.getFromGrocy('objects/quantity_units')
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
     
     
     
