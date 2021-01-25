import picnic

p = picnic.PicNic()

p.getAllGrocyProducts() #first load all existiing grocy products.
p.getQuantityUnits() #import all grocy quantities.

#p.setInStock("73", "10", "1.56")
p.importLastPicnicDelivery()

#TODO
## Setup grocy using picnic items, import quantities from github repo
## Increase stock picnic ID
## Set stock date right
## check if order is already processed, then don't add to stock
## Todo ml to Miliiters quantitiy
## Fill in kcal, product details.
## TOdo import 'vers na aantal dagen, minimum' picnic, count the real delivery date + numOfDays.


    
    # searchResFound = picnic.search('Cottage Cheese.')
     #
    #koppeling maken tussen api, picnic en albert heijn
     #searchResFound = self.connector.get_product_details(self.connector.get_product_by_barcode('40097138'))["title"]
   # self.addPicnicIDToProduct(40, "900")
   # print(self.getProductInformation("10764022"))
    #self.grocy.changePictureFileNameProduct("45", self.grocy.uploadProductPictureToGrocy("d3176c7b1cd82af60db515e93679768449919709c1e3a2525a3e0a3a9a7460f8"))

  #   self.matchPicnicQuantityByGrocyQuantity("stuks")
    # self.fillQuantity("60 gram")
    # searchResFound = json.dumps(self.connector.get_product_details(self.connector.get_product_by_barcode('8718796026464')),sort_keys=True, indent=4)

     
     #[1]
     #searchResFound = json.dumps(self.get_delivery("10761823"),sort_keys=True, indent=4)
     #res = ' '.join(map(str, searchResFound)) #//picnic
     #res = searchResFound
    # self.log("PicNic: " + res)