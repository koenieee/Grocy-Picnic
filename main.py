import picnic

p = picnic.PicNic()

p.getAllGrocyProducts() #first load all existiing grocy products.
p.getQuantityUnits() #import all grocy quantities.

#p.setupGrocyPicnicSettings()
#p.importLastPicnicDelivery()

#TODO
## Set stock date right
## check if order is already processed, then don't add to stock
## Todo ml to Miliiters quantitiy
## Check for updated ean codes in products.list
## Check for updates recipes in recipes.list, and import


## Future ideas:
# Import 'vers na aantal dagen, minimum' picnic, count the real delivery date + numOfDays. Picnic has really short THT dates...
# Fill in kcal, product details. Loop through every product and append information (not sure how interesting this is though...)


