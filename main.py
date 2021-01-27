import picnic
import picnic_setup_grocy


#Firt time run this. Make sure you have an empty Grocy database (or not, but prepare for conflicts then)
#install = picnic_setup_grocy.PicnicSetupGrocy()
#install.installAll()

#To import picnic products run these, comment above setup: 
pp = picnic.PicNic()
pp.importLastPicnicDelivery()

#TODO
## Set stock date right
## check if order is already processed, then don't add to stock
## Todo ml to Miliiters quantitiy
## Check for updated ean codes in products.list
## Check for updates recipes in recipes.list, and import


## Future ideas:
# Import 'vers na aantal dagen, minimum' picnic, count the real delivery date + numOfDays. Picnic has really short THT dates...
# Fill in kcal, product details. Loop through every product and append information (not sure how interesting this is though...)


