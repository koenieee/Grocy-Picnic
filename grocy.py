import requests
import config
import json
import urllib3.request
import base64 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GrocyAPI():
  grocy_api_key = config.grocy_api_key
  grocy_api_url = config.grocy_api_url
  verify_ssl = False
  image_size = "" 
  img_baseurl = "" 

  def __init__(self, img_size: str, img_baseurl: str):
    self.image_size = img_size
    self.img_baseurl = img_baseurl
 

  def makeHeader(self):
    header = {'GROCY-API-KEY': self.grocy_api_key}
    header["Content-Type"] = 'application/json'
    header["accept"] = 'application/json'
    return header


  def getFromGrocy(self, apiPart: str):
    url = self.grocy_api_url + apiPart
    x = requests.get( url, headers=self.makeHeader(), verify=self.verify_ssl)
    return json.loads(x.text)

  def putToGrocy(self, apiPart: str, postData: str):
    url = self.grocy_api_url + apiPart
    x = requests.put( url, data = postData, headers=self.makeHeader(), verify=self.verify_ssl)
    return x

  def postToGrocy(self, apiPart: str, postData: str):
    url = self.grocy_api_url + apiPart
    x = requests.post( url, data = json.dumps(postData), headers=self.makeHeader(), verify=self.verify_ssl)
    return x

  def addUserFieldToProduct(self, product_id: str, userfield_data:str):
    return self.putToGrocy("userfields/products/" + product_id, userfield_data)


  def changePictureFileNameProduct(self, product_id: str, filename:str):
      self.putToGrocy('objects/products/' + product_id, ("{\"picture_file_name\":\""+filename+"\"}"))

  def addPictureToProduct(self, img_id:str):
    header = {'GROCY-API-KEY': self.grocy_api_key}
    header["Content-Type"] = 'application/octet-stream'
    header["accept"] = '*/*'

    img_filename = img_id+".png"
    encode_bytes = img_filename.encode("ascii") 
    base64_bytes = base64.b64encode(encode_bytes) 

    url = self.grocy_api_url + 'files/productpictures/' + base64_bytes.decode("ascii")
    data_url = self.img_baseurl + img_id + "/"+self.image_size+".png"

    html = requests.get(data_url)

    x = requests.put( url, data = html, headers=self.makeHeader(), verify=self.verify_ssl)
    if x.ok:
        return img_filename
    else:
        print("Failure img uploading" + x.response)
        return ""
    
