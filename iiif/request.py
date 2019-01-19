from PIL import Image
import requests
from io import BytesIO
import json

def getImage(url):
    #NOTE verify = False is bad practice as per https://stackoverflow.com/questions/10667960/python-requests-throwing-sslerror
    response = requests.get(url, verify=False)
    print(response)
    img = Image.open(BytesIO(response.content))
    img.show()


def getImageURIs(manifestURL=None):
    
    # retrieve a manifest.json file from url

    #url = 'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
    #r = requests.get(url)
    #print(json.loads(r.content))

    imageURIs = []

    with open('toganoo_1.json') as data_file:    
        data = json.load(data_file)

        someSequence = data['sequences'][0] # since we do not care about the order, we can just arbitrarily choose the first one

        canvases = someSequence['canvases']

        for c in canvases:
            imgs = c['images']

            for i in imgs:
                imageURIs.append(i['resource']['@id'])

    return imageURIs


def main():
    url='https://marinus.library.ucla.edu/cantaloupe-4.0.1/iiif/2/toganoo%7C1%7Cucla_1564390_002.tif/full/full/0/default.jpg'

    #getImage(url)

    someList = getImageURIs('asd')

    for e in someList:
        print(e)
        #getImage(e)

if __name__ == '__main__':
    main()  