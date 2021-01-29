# general login settings
picnic_user = '##'
picnic_passwd = '##'
grocy_api_key = '##'
grocy_api_url = 'https://###/api/'

# grocy settings
# disable tenminste houdtbaar tot. -1 to disable. Picnic provides fresh label, but that's way too short, maybe something in the future..
disable_tht = -1
# change this number to limit max num of imports.
picnic_max_import_products = 2


#####Don't change the following data unless you know what your doing...#####
# main repository
main_repo = 'https://raw.githubusercontent.com/koenieee/Grocy-Picnic/main/'

# specific picnic settings, recipes and products with their ean code
# todo share among users.
picnic_product_ean_list = main_repo + 'grocy_data/products.json'
picnic_recipe_list = main_repo + 'grocy_data/recipes.json'  # todo, share among users

# for first grocy setup with picnic data
picnic_quantity_list = main_repo + 'grocy_data/quantities.json'
picnic_location_list = main_repo + 'grocy_data/location.json'
picnic_stores_list = main_repo + 'grocy_data/stores.json'
picnic_userfields_list = main_repo + 'grocy_data/userfields.json'

# picnic database settings
picnic_img_baseurl = 'https://storefront-prod.nl.picnicinternational.com/static/images/'
picnic_img_size = 'medium'
