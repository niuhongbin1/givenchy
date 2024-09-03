import requests

url = 'https://api.louisvuitton.com/eco-eu/search-merch-eapi/v1/fra-fr/stores/query'

hs = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'client_id':'607e3016889f431fb8020693311016c9',
    'client_secret':'60bbcdcD722D411B88cBb72C8246a22F',
    # 'content-type': 'application/json',
    'origin': 'chrome-extension://ieoejemkppmjcdfbnfphhpbfmallhfnc',
    'cookie': 'lv-dispatch=fra-fr'
}


j = {
    "country": "FR",
    "latitudeCenter": "48.85883390050193",
    "longitudeCenter": "2.347035000000006",
    "latitudeA": "48.92185373401864",
    "longitudeA": "2.1770902368164124",
    "latitudeB": "48.795814066985216",
    "longitudeB": "2.5169797631836",
    "query": "Paris,France",
    "clickAndCollect": False,
    "skuId": "1AB7SG",
    "pageType": "productsheet"
}


rep = requests.post(url = url,headers=hs,json=j,timeout=5)

p = rep.json()


