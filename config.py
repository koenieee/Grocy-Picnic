#general login settings
picnic_user = '####'
picnic_passwd = '#####'
grocy_api_key = '####'
grocy_api_url = '####'

#main repository
main_repo = 'https://raw.githubusercontent.com/koenieee/Grocy-Picnic/main/'

#specific picnic settings, recipes and products with their ean code
picnic_product_ean_list = main_repo + 'grocy_data/products.json' #todo share among users.
picnic_recipe_list = main_repo + 'grocy_data/recipes.json' #todo, share among users

#for first grocy setup with picnic data
picnic_quantity_list = main_repo + 'grocy_data/quantities.json'
picnic_location_list = main_repo + 'grocy_data/location.json'
picnic_stores_list = main_repo + 'grocy_data/stores.json'
picnic_userfields_list = main_repo + 'grocy_data/userfields.json'

#picnic database settings
picnic_max_import_products = 1
picnic_img_baseurl = 'https://storefront-prod.nl.picnicinternational.com/static/images/'
picnic_img_size = 'medium'

#grocy settings
default_store_id = 1 #see value in page Stores in Grocy. Add store and find out ID (name Picnic e.g.)
default_location_id = 1 #see value in page Locations in Grocy. Add location and find out ID. (name Home e.g.) 
disable_tht = -1 #disable tenminste houdtbaar tot. -1 to disable. Picnic provides fresh label, but that's way too short, maybe something in the future..