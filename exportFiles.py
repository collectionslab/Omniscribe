import json
import urllib.request
import uuid
from yattag import Doc
from imantics import Mask, Polygons
from shapely.geometry import Polygon

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

def slash_join(*args):
    return "/".join(arg.strip("/") for arg in args)

def exportManifest(urls, iiif_root, annotations=None, ):

    manifest_id = slash_join(iiif_root + "/resultsManifest.json")

    manifest = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": manifest_id,
        "@type": "sc:Manifest",
        "label": "Annotations",
        "sequences": [{
            "@type": "sc:Sequence",
            "canvases": []
            }
        ]
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

    if (annotations):
        annotations_data = {}

    annolist_count = 0

    for url in urls:

        image_template = json.loads(jsonObj)
        # Retrive main image url
        img_url = url.split('/')[:-4]
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

        canvas_id = img_url + '.json'

        image['@id'] = canvas_id
        image['height'] = height
        image['width'] = width
        image['images'][0]['on'] = canvas_id
        image['images'][0]['resource']['@id'] = img_url + \
            '/full/full/0/default.jpg'
        image['images'][0]['resource']['service']['@id'] = img_url

        if (annotations and (url in annotations)):
            # Annotation lists are generated *per canvas (image)*
            # See https://iiif.io/api/presentation/2.1/#annotation-list
            # also https://github.com/UCLAXLabs/iiif-annotation-converter/blob/master/iiif_face_annotator.py

            annolist_count += 1

            anno_id = slash_join(iiif_root, "annotations", "image" + str(annolist_count))
            anno_list_filename = slash_join("annotations", "image" + str(annolist_count))

            anno_data = { "@id": anno_id,
                          "@context": "http://iiif.io/api/presentation/2/context.json",
                          "@type": "sc:AnnotationList",
                          "resources": []
            }

            for i, roi in enumerate(annotations[url]['rois']):

                # This is the actual bitmap mask of the annotation region
                mask = annotations[url]["masks"][:, :, i]

                polygons = Mask(mask).polygons()
                points = polygons.points[0]

                poly = Polygon(points)

                hull = poly.convex_hull

                hull_coords = list(hull.exterior.coords)
                #print(hull_coords)
                #print(hull_coords[0])

                # ROI: [1413, 1988, 1592, 2244]

                roi_width = roi[3] - roi[1]
                roi_height = roi[2] - roi[0]

                xywh = [roi[1], roi[0], roi_width, roi_height]

                xywh_string = ','.join(list(map(str,xywh)))

                #print(xywh_string)

                # This code makes a rectangular path:
                
                # This is what a polygon annotation region looks like:
                # First it includes the fragmentSelector with the xywh bounding box, then
                # "value": "<svg xmlns='http://www.w3.org/2000/svg'><path xmlns=\"http://www.w3.org/2000/svg\" d=\"M369.34609,1260.26646l-28.38438,51.09188l-5.67688,136.24502l62.44564,22.7075l210.04441,17.03063l45.41501,-68.12251l51.09188,-113.53752l-181.66003,-39.73813l-147.59877,-5.67688z\" data-paper-data=\"{&quot;strokeWidth&quot;:1,&quot;editable&quot;:true,&quot;deleteIcon&quot;:null,&quot;annotation&quot;:null}\" id=\"rough_path_271150e9-b7b7-48df-9fd2-daeadaabb9c9\" fill=\"#3f3fa3\" fill-rule=\"nonzero\" stroke=\"#00bfff\" stroke-width=\"1\" stroke-linecap=\"butt\" stroke-linejoin=\"miter\" stroke-miterlimit=\"10\" stroke-dasharray=\"\" stroke-dashoffset=\"0\" font-family=\"none\" font-weight=\"none\" font-size=\"none\" text-anchor=\"none\" style=\"mix-blend-mode: normal\"/></svg>"
                # After initial M startX, startY, X and Y movements seem to be prefaced by 'l'; z finishes the path.

                confidence_string = "confidence: " + "{:.0%}".format(annotations[url]['scores'][i])
                #print(confidence_string)

                box_uuid = str(uuid.uuid4())
                pathTopLeft = [ str(float(xywh[0])), str(float(xywh[1])) ]
                pathHalfWidth = str(float(xywh[2]) / 2)
                pathHalfHeight = str(float(xywh[3]) / 2)
                svgPath = "M" + pathTopLeft[0] + "," + pathTopLeft[1] + 'h' + pathHalfWidth + 'h' + pathHalfWidth + 'v' + pathHalfHeight + 'v' + pathHalfHeight + 'h-' + pathHalfWidth + 'h-' + pathHalfWidth + 'v-' + pathHalfHeight + 'z'
                svg_string = "<svg xmlns='http://www.w3.org/2000/svg'>" + '<path xmlns="http://www.w3.org/2000/svg" d="' + svgPath + '" data-paper-data="{&quot;strokeWidth&quot;:1,&quot;rotation&quot;:0,&quot;deleteIcon&quot;:null,&quot;rotationIcon&quot;:null,&quot;group&quot;:null,&quot;editable&quot;:true,&quot;annotation&quot;:null}" id="rectangle_' + box_uuid + '" fill-opacity="0" fill="#00bfff" fill-rule="nonzero" stroke="#003366" stroke-width="2" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray="8" stroke-dashoffset="0" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode: normal"/></svg>'

                box_annotation = { '@type': "oa:Annotation",
                                    'motivation': [ "oa:commenting", "oa:tagging" ],
                                    "resource": [ { '@id': "_:b2", '@type': "dctypes:Text", 'http://dev.llgc.org.uk/sas/full_text': confidence_string, 'format': "text/html", 'chars': confidence_string } ],
                                    "on": [ { '@id': "_:b0", '@type': "oa:SpecificResource", 
                                        'within': { '@id': manifest_id,
                                                    '@type': "sc:Manifest" },
                                                    'selector': { '@id': "_:b1", '@type': "oa:Choice", 'default': { '@id': "_:b4", '@type': "oa:FragmentSelector", 'value': "xywh=" + xywh_string },
                                                                  'item': { '@id': "_:b5", '@type': "oa:SvgSelector", 'value': svg_string } }, 'full': canvas_id} ], 
                                                    "@context": "http://iiif.io/api/presentation/2/context.json" }

                anno_data["resources"].append(box_annotation)

                mask_uuid = str(uuid.uuid4())

                svg_path = "M" + str(hull_coords[0][0]) + "," + str(hull_coords[0][1])

                for j in range(1,len(hull_coords)):
                    delta_x = hull_coords[j][0] - hull_coords[j-1][0]
                    delta_y = hull_coords[j][1] - hull_coords[j-1][1]

                    svg_path += 'l' + str(delta_x) + "," + str(delta_y)

                svg_path += 'z'
                svg_string = "<svg xmlns='http://www.w3.org/2000/svg'><path xmlns=\"http://www.w3.org/2000/svg\" d=\"" + svg_path + "\" data-paper-data=\"{&quot;strokeWidth&quot;:1,&quot;editable&quot;:true,&quot;deleteIcon&quot;:null,&quot;annotation&quot;:null}\" id=\"rough_path_" + mask_uuid + "\" fill-opacity=\"0.2\" fill=\"#3f3fa3\" fill-rule=\"nonzero\" stroke=\"#00bfff\" stroke-width=\"1\" stroke-linecap=\"butt\" stroke-linejoin=\"miter\" stroke-miterlimit=\"10\" stroke-dasharray=\"\" stroke-dashoffset=\"0\" font-family=\"none\" font-weight=\"none\" font-size=\"none\" text-anchor=\"none\" style=\"mix-blend-mode: normal\"/></svg>"
                #print(svg_string)

                mask_annotation = { '@type': "oa:Annotation",
                                    'motivation': [ "oa:commenting", "oa:tagging" ],
                                    "resource": [ { '@id': "_:b2", '@type': "dctypes:Text", 'http://dev.llgc.org.uk/sas/full_text': "", 'format': "text/html", 'chars': "" },
                                                  { '@id': "_:b3", '@type': "oa:Tag", 'http://dev.llgc.org.uk/sas/full_text': "handwriting", 'chars': "handwriting" } ],
                                    "on": [ { '@id': "_:b0", '@type': "oa:SpecificResource", 
                                        'within': { '@id': manifest_id,
                                                    '@type': "sc:Manifest" },
                                                    'selector': { '@id': "_:b1", '@type': "oa:Choice", 'default': { '@id': "_:b4", '@type': "oa:FragmentSelector", 'value': "xywh=" + xywh_string },
                                                                  'item': { '@id': "_:b5", '@type': "oa:SvgSelector", 'value': svg_string } }, 'full': canvas_id} ], 
                                                    "@context": "http://iiif.io/api/presentation/2/context.json" }

                anno_data["resources"].append(mask_annotation)

            annotations_data[anno_list_filename] = json.dumps(anno_data, indent=4)

            # Need to add a link to the annotations list to the canvas otherContent attribute
            anno_list_link = { "@id": anno_id, "@type": "sc:Annotationlist" }
            image["otherContent"] = [anno_list_link]

        manifest['sequences'][0]['canvases'].append(image)

    if (annotations):
        return [json.dumps(manifest, indent=4), annotations_data]
    else:
        return json.dumps(manifest, indent=4)
