nfc_uri={
    "1" :  "spotify:track:2DwUdMJ5uxv20EhAildreg", # cookie
    "2" : "spotify:track:4Li2WHPkuyCdtmokzW2007", # jayz and kanye
    "3" : "spotify:track:1zxfRSZcaonV1VXcY0PgY5", # jakarta
    "4" : "spotify:track:2pg2TiYo9Rb8KeB5JjP7jS" # sativa
}

def getURI(tagid : str) -> str:
    return nfc_uri[tagid]
