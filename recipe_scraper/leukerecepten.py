


import requests
from bs4 import BeautifulSoup

from fuzzywuzzy import fuzz
from process_ingriedients import *

#pip3 install beautifulsoup4

URL = 'https://www.leukerecepten.nl/recepten/nasi/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find("div", {"class": "page-content__ingredients-list js-ingredients-list"})#.findAll('li')

ingriedients = []




#### Order of processing ingriedient:
# removeUselessWords, match product but  
# Strip and remove numbers
# strip and remove quantity
# 

# 1 ignoreIngriedientAsProduct
# # How much is needed?
# 2 removeUselessWords
# 3 removeCutterTechnique

#['1  ui (gesnipperd)', '2  tenen knoflook (fijngesneden)', '750 gr romatomaten (in parten)', '750 ml water', '1  groentebouillontablet', '1  klein blikje tomatenpuree', '  Scheutje kookroom', '2 eetlepels olijfolie', '  Optioneel: verse basilicum']




for label in results.find_all('label'):
    ingriedients.append(label.text.replace('\n','').replace('\t','').replace('\r',''))


for ingriedient in ingriedients:
    if ignoreIngriedientAsProduct(ingriedient):
        print("Not for grocy picnic id: " + ingriedient)
    else: 
        print(removeUselessWords(ingriedient))

#print(ingriedients)
#exit()


#print(results)


#page-content__ingredients-list js-ingredients-list 