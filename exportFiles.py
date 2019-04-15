import json
import urllib.request
from yattag import Doc

def exportHTML(urls):
    div = ('{display:inline-block;'
           'width: 15%;'
           'height: 40%;'
           'margin: 2%;}')

    img = ('{height: 100%;'
           'width: 100%;'
           'object-fit: contain;}')

    doc, tag, text = Doc().tagtext()

    with tag('html'):
        with tag('style'):
            text('div' + div + 'img' + img)
        with tag('body'):
            with tag('h1'):
                text('Pages Containing Annotations')
            with tag('p'):
                text('Click on an image to view')
            # generate each image 'box'
            for url in urls:
                with tag('div'):
                    with tag('a', ('href', url)):
                        doc.stag('img', src=url)

    return doc.getvalue()


def exportManifest(urls):
    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": "http://localhost/manifest.json",
        "@type": "sc:Manifest",
        "label": "Annotations",
        "sequences": [{
            "@type": "sc:Sequence",
            "canvases": [

            ]
        }]
    }

    image_template_id = '{"@id": "[image url].json",'
    image_template_type = '"@type": "sc:Canvas",'
    image_template_height = '"height": 0,'
    image_template_width = '"width": 0,'
    image_template_images = '"images": [{'

    images_type = '"@type": "oa:Annotation",'
    images_motivation = '"motivation": "sc:painting",'
    images_on = '"on": "[image url].json",'
    images_resource = '"resource": {'

    resource_id = '"@id": "[image url]/full/full/0/default.jpg",'
    resource_type = '"@type": "dctypes:Image",'
    resource_format = '"format": "image/jpeg",'
    resource_service = '"service": {'

    service_context = '"@context": "http://iiif.io/api/image/2/context.json",'
    service_id = '"@id": "[image url]",'
    service_profile = '"profile": "http://iiif.io/api/image/2/level1.json"'

    image_template_string = image_template_id
    image_template_string += image_template_type + image_template_height
    image_template_string += image_template_width + image_template_images
    image_template_string += images_type + images_motivation + images_on
    image_template_string += images_resource + resource_id + resource_type
    image_template_string += resource_format + resource_service
    image_template_string += service_context + \
        service_id + service_profile + '} } } ] }'

    jsonObj = eval(json.dumps(image_template_string))

    for url in urls:

        image_template = json.loads(jsonObj)
        # Retrive main image url
        url = url.split('/')
        img_url = url[:-4]
        img_url = '/'.join(img_url)

        # get height width metadata
        info_request = urllib.request.urlopen(img_url + '/info.json')
        info = info_request.read()
        info = info.decode("utf8")
        info_request.close()

        info = json.loads(info)
        height = info['height']
        width = info['width']

        image = dict(image_template)

        image['@id'] = img_url + '.json'
        image['height'] = height
        image['width'] = width
        image['images'][0]['on'] = img_url + '.json'
        image['images'][0]['resource']['@id'] = img_url + \
            '/full/full/0/default.jpg'
        image['images'][0]['resource']['service']['@id'] = img_url

        manifest['sequences'][0]['canvases'].append(image)

    return json.dumps(manifest, indent=4)
