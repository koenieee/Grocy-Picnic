import requests
import config
import json
import urllib.request
import base64 


class GrocyAPI():
  grocy_api_key = config.grocy_api_key
  grocy_api_url = config.grocy_api_url
  verify_ssl = False
  image_size = "medium"

  def makeHeader(self):
    header = {'GROCY-API-KEY': self.grocy_api_key}
    header["Content-Type"] = 'application/json'
    header["accept"] = 'application/json'
    return header


  def getFromGrocy(self, apiPart: str):
    url = self.grocy_api_url + apiPart
    x = requests.get( url, headers=self.makeHeader(), verify=self.verify_ssl)
    return x

  def putToGrocy(self, apiPart: str, postData: str):
    url = self.grocy_api_url + apiPart
    x = requests.put( url, data = postData, headers=self.makeHeader(), verify=self.verify_ssl)
    return x

  def postToGrocy(self, apiPart: str, postData: str):
    url = self.grocy_api_url + apiPart
    x = requests.post( url, data = postData, headers=self.makeHeader(), verify=self.verify_ssl)
    return x

  def addUserFieldToProduct(self, product_id: str, userfield_data:str):
    return self.putToGrocy("userfields/products/" + product_id, userfield_data)


  def changePictureFileNameProduct(self, product_id: str, filename:str):
      self.putToGrocy('objects/products/' + product_id, ("{\"picture_file_name\":\""+filename+"\"}"))

  #todo split this into picnic and grocy fileupload.
  def uploadProductPictureToGrocy(self, img_id:str):
    header = {'GROCY-API-KEY': self.grocy_api_key}
    header["Content-Type"] = 'application/octet-stream'
    header["accept"] = '*/*'

    img_filename = img_id+".png"
    encode_bytes = img_filename.encode("ascii") 
    base64_bytes = base64.b64encode(encode_bytes) 

    url = self.grocy_api_url + 'files/productpictures/' + base64_bytes.decode("ascii")
    print("Http url: " + url)
    data_url = "https://storefront-prod.nl.picnicinternational.com/static/images/" + img_id + "/"+self.image_size+".png"

    with urllib.request.urlopen(data_url) as f:
        html = f.read()

    x = requests.put( url, data = html, headers=self.makeHeader(), verify=self.verify_ssl)
    if x.ok:
        return img_filename
    else:
        print("Failure img uploading" + x.response)
        return ""
    
