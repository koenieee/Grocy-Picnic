# Grocy-Picnic
Picnic (online supermarket) connection between Grocy (ERP fridge/house management tool)

## Requirements
- https://github.com/MikeBrink/python-picnic-api
- - Inspired by: https://github.com/MikeBrink/python-picnic-api/issues/7
- https://github.com/grocy/grocy (ofc)

## Getting Started

1. Make sure you have pip3 and python3 installed
2. And make sure you have a grocy instance up & running.
3. Run this command: `pip3 install -r requirements.txt`
4. Change `config.py` to your needs (fill in user and grocy settings). Change max number of import product (limit if you want to)
   
   Note: don't change the json files for some default grocy settings (these are needed by the picnic import script) Change them only if you know what you do...
5. Run `main.py` (with install as argument  for first time importing some data into grocy) 
   
   `main.py install`
6. Run `main.py` (with import as argument, to import last picnic delivery into database)
   
   `main.py import`
7. Importing can be run every time you make a new picnic order.


## Some ideas
- Use machine vision (Tensorflow) to recongize vegatables with webcam)
- Minimize effort to keep track of own stock supply
   - E.g. with webcam and vision algorithm
   - Or always use the order as stock resupply and when selecting a recipe, consume everything from that recipe
- Order food via Google Assistant to add to picnic basket (Via IFTTT and variables, no support for Dutch although :()
- Add recipes from leukerecepten.nl and scrape them to add them to the grocy database
- Share recipes and ean product codes from picnic among other users.
- Create as Hasiio addon.
  

## Product Data Picnic -> Grocy
- picnic ID (userfield)
- name of product
- image 
- weight
- quantity
- price
  
Add to stock if item is allready in database

## Stock management Grocy -> Picnic
TODO
- When out of stock in Grocy, add to basket in Picnic
- Select a few recipes for the week in Grocy, add all to basket in Picnic
