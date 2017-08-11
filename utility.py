import httplib2
import json
import string

def getGeoCodeLocation(inputString):
    google_api_key='AIzaSyDqScH7XDNT11svhIMwZ0sCBmTYgaLFgxU'
    locationString = inputString.replace(' ','+')
    url = ('''https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'''%(locationString,google_api_key))
    print(url)
    h = httplib2.Http()
    response,content = h.request(url,'GET')
    content = json.loads(content.decode('utf-8'))
    lat = content['results'][0]['geometry']['location']['lat']
    lng = content['results'][0]['geometry']['location']['lng']
    return [lat,lng]


def getReviewsfromZomato(restaurant):
    zomato_api_key = '8a9a6581b4db84e04e8031307b122f83'
    lat,lng = getGeoCodeLocation(restaurant)
    print(lat,lng)
    reviews = {'lat':lat,'lng':lng,
                'review':['Sorry no reviews exists for the given restaurant, kindly check some other restaurant.',
                'Sorry no reviews.']}
    return reviews

# reviews = getReviewsfromZomato('Chulha Chauki Marathalli, Bangalore')