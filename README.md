# Grocy-Picnic
Picnic (online supermarket) connection between Grocy (ERP fridge management tool)

# Requirements
- https://github.com/bartmachielsen/SupermarktConnector
- https://github.com/MikeBrink/python-picnic-api
- - Inspired by: https://github.com/MikeBrink/python-picnic-api/issues/7
- Hassio (Homeassistant) and AppDeamon


# Future work
I want to create a grocy database with ID's from PicNic products and their barcode (if there is one) and fill the database with their products and images.
So this tool will be an easy way to import your order from picnic into grocy, but you still have to specify details on your own.

Also an idea to enable machine vision to detects products without barcode.

# Some ideas
- Match barcodes of picnic products with AHConnector, or JumboConnector (See project Bart)
- Make own database with recipes
- Keep track of prices, if cheaper order by Albert heijn or Jumbo
- Use machine vision (Tensorflow) to recongize vegatables with webcam)
- Minimize effort to keep track of own stock supply
- - E.g. with webcam and vision algorithm
- - Or always use the order as stock resupply and when selecting a recipe, consume everything from that recipe
- Order food via Google Assistant to add to picnic basket
- Maybe also add other supermarkets one day. 
  For example if you buy in the Albert Heijn and scan your bonus card, you can retrieve the order and also add this to grocy. So no manual input for products...

# Product Data Picnic -> Grocy
- picnic ID (userfield)
- name of product
- image 
- weight
- quantity
- price
- detailed information, for later:
- - energy kcal
- - ingriedients e.g.
- - maybe more

Add to stock if item is allready in database

# Stock management Grocy -> Picnic
- When out of stock in Grocy, add to basket in Picnic
- Select a few recipes for the week in Grocy, add all to basket in Picnic
