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



class PicNic():
  picnic_user = config.picnic_user
  picnic_passwd = config.picnic_passwd
  picnic_image_size = config.picnic_img_size
  picnic_img_baseurl = config.picnic_img_baseurl
  picnic_numofelementsimport = config.picnic_max_import_products
  picnic_ean_codes_url = config.picnic_product_ean_list
  quantities=dict()
  grocy_items = []
  
  picnic = PicnicAPI(username=picnic_user, password=picnic_passwd, country_code="NL", store=False)
  grocy = GrocyAPI(picnic_image_size, picnic_img_baseurl)
  json_picnic_data = {}


  def __init__(self):
    json_data = json.loads(requests.get(self.picnic_ean_codes_url).text)     #download all json ean products from file
    self.json_picnic_data = json_data["data"]
    self.getAllGrocyProducts() #first load all existing grocy products.
    self.getQuantityUnits() #import all grocy quantities.
  #  print(self.getProductInformation(10465898))


  def getEANFromPicnicID(self, picnic_id:str):
    for json_item in self.json_picnic_data:
      if str(json_item["picnic_id"]) == picnic_id:
        return str(json_item["ean"])
    return ""

  def addPicnicIDToProduct(self, product_id:str, picnic_id:str):
    self.grocy.addUserFieldToProduct(str(product_id), "{\"picnic\":\""+picnic_id+"\"}")

  def addPicNicProductToGrocy(self, name: str, qu_id:str, picnic_id: str, imgId: str, price: str):
    postData = {}
    postData["name"] = name
    postData["qu_id_purchase"] = qu_id
    postData["qu_id_stock"] = qu_id
    postData["qu_factor_purchase_to_stock"] = 1.0
    postData["shopping_location_id"] = config.default_store_id
    postData["location_id"] = config.default_location_id
    postData["barcode"] = self.getEANFromPicnicID(picnic_id)
    postData["default_best_before_days"] = config.disable_tht #disable tenminste houdtbaar tot

    result = self.grocy.postToGrocy("objects/products", postData)
    if result.ok:
        json_result = json.loads(result.text)
        grocy_product_id = json_result["created_object_id"]
        print("Added picnic product to grocy: " + grocy_product_id + ", picnic_id: " + picnic_id)
        self.addPicnicIDToProduct(grocy_product_id, picnic_id)
        print("Uploading picnic image to grocy...")
        self.grocy.changePictureFileNameProduct(grocy_product_id, self.grocy.addPictureToProduct(imgId))
        return grocy_product_id
    else:
        print("Failed to add picnic product to grocy: " + result.text)
        return 0

  def getProductInformation(self, productID: str):
     path = "/product/" + str(productID) #, just a test.
     return self.picnic._get(path)
     
  def importLastPicnicDelivery(self):
    last_delivery_index = -1
    order_data = self.picnic.get_deliveries()[0]["orders"][last_delivery_index]["creation_time"]
    delivery_date = self.picnic.get_deliveries()[0]["delivery_time"]["start"]

    print(json.dumps(delivery_date))
    for picnic_item in self.picnic.get_deliveries()[0]["orders"][last_delivery_index]["items"][:self.picnic_numofelementsimport]: # last order of picnic
       #picnic data:
       name = picnic_item["items"][0]["name"]
       id = picnic_item["items"][0]["id"]
       image_ids = picnic_item["items"][0]["image_ids"][0]
       price = (picnic_item["items"][0]["price"] / 100)  #used in stock data
       unit_quantity = picnic_item["items"][0]["unit_quantity"]
       converted_quantity = self.fillQuantity(unit_quantity)
       sort_of_quantity = converted_quantity[1]
       how_much =  converted_quantity[0]
       
       #grocy_data:
       grocy_id_existing_product = self.getPicnicProductInGrocy(id)
       if grocy_id_existing_product != 0:
       #   print("picnic item already in grocy..." + price)
          print("Increasing stock: " + how_much + " with id: " + sort_of_quantity)
          self.setInStock(grocy_id_existing_product, how_much, price, order_data)
       else: 
          new_grocy_id = self.addPicNicProductToGrocy(name, sort_of_quantity, id, image_ids, price)
          if new_grocy_id != 0:
            self.setInStock(new_grocy_id, how_much, price, order_data)

          #todo increase stock after adding product.

        
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
      json_data = self.grocy.getFromGrocy('objects/quantity_units')
      for quantity in json_data:
         self.quantities[quantity["name"]] = quantity["id"]
      print(self.quantities)

  def setInStock(self, grocy_id: str, stock: str, price: str, order_date):
      post_data = {}
      post_data["amount"] = str(stock)
      post_data["price"] = str(price)
      post_data["purchased_date"] = str(order_date)#order_date
      print("grocy_id: " + grocy_id)
      result = self.grocy.postToGrocy('stock/products/'+grocy_id+'/add', post_data)
      if result.ok:
         print("setInStock: succes")
      else:
         print("Failed to add stock: " + result.text)

  def getPicnicProductInGrocy(self, picnic_id: str):
      for grocy_item in self.grocy_items:
        if grocy_item.picnic_id == picnic_id:
          return grocy_item.grocy_id
      return 0

  def getAllGrocyProducts(self):
      json_data = self.grocy.getFromGrocy('objects/products')
    
      for product in json_data:
        grocy_product = GrocyPicnicProduct(product["userfields"]["picnic"], product["id"], product["name"], product["picture_file_name"], product["tare_weight"], product["qu_id_stock"])
        self.grocy_items.append(grocy_product)

      #print(self.grocy_items)

     
     
     
