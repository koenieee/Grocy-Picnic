from fuzzywuzzy import fuzz


ignore_tags_for_grocy = [ #ignore these ingriedienst in grocy, but add them in the list of benodigdheden.
    "water",
    "zout",
    "peper",
    "olijfolie",
    "boter"
]

cut_these_words = [ #filter out these words. to get better product match
    "gesnipperd",
    "fijngesneden",
    "in parten",
    "geschild",
    "in blokjes",
    "uit blik",
    "optioneel",
    "garneren",
    "sap van",
    "blaadjes",
    "ongezouten",
    "kleine",
    "grote",
    "verse",
    "om te",
    "snuf",
    "theelepel",
    "eetlepel",
    "bosje",
    "teentjes", #only knoflook haha
    "tenen",
    "vlokken",
    "handje",
    "scheutje",
    "scheut"
    "paar",
    "zakje",
    "stukje",
    "doses",
    "druppels",
    "blik",
    "plakjes",
    "vellen",
    "achter",
    "naast",
    "in",
    "op",
    "door",
    "over",
    "boven",
    "onder",
    "om",
    "tegen",
    "binnen",
    "buiten",
    "langs",
    "tijdens",
    "sinds",
    "tot",
    "zonder",
    "met",
    "behalve",
    "naar",
    "via",
    "tegen",
    "volgens",
    "en",
    "te",
    "voor",
    "hartig",
    "warme",
    "koude",
    "gedroogde",
    "middelgrote",
    "mini",
    "bakken"
]



def checkIfIsInList(theList: [], what:str, percentage: int):
    for list_item in theList:
        match_pecentage = fuzz.ratio(list_item, what)
      #  print(match_pecentage)
        if(match_pecentage > percentage): 
            return list_item
    return None


def ignoreIngriedientAsProduct(ingriedient: str):
    if any(ext in ingriedient for ext in ignore_tags_for_grocy):
        return True
    return False


def removeUselessWords(ingriedient: str):
    original_word = ingriedient.lower().strip()
    real_product = original_word.split(' ')
    for word in original_word.split(' '):
        wasInList = checkIfIsInList(cut_these_words, word, 75)
        if wasInList != None: #it looked like it, so remove the word
            real_product.remove(word)
        #    print(real_product)
    s = " "
    return s.join(real_product) # else case
    
