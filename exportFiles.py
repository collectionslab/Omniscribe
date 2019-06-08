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

            width_ratio = annotations[url][1]
            height_ratio = annotations[url][2]

            annolist_count += 1

            anno_id = slash_join(iiif_root, "annotations", "image" + str(annolist_count))
            anno_list_filename = slash_join("annotations", "image" + str(annolist_count))

            anno_data = { "@id": anno_id,
                          "@context": "http://iiif.io/api/presentation/2/context.json",
                          "@type": "sc:AnnotationList",
                          "resources": []
            }

            for i, roi in enumerate(annotations[url][0]['rois']):

                # This is the actual bitmap mask of the annotation region
                mask = annotations[url][0]["masks"][:, :, i]

                polygons = Mask(mask).polygons()
                points = polygons.points[0]

                poly = Polygon(points)

                hull = poly.convex_hull

                unscaled_hull_coords = list(hull.exterior.coords)

                hull_coords = []

                for coord in unscaled_hull_coords:
                    scaled_coord = [float(coord[0]) * width_ratio, float(coord[1]) * height_ratio]
                    print("Unscaled coord: " + str(coord) + ", scaled coord: " + str(scaled_coord))
                    hull_coords.append(scaled_coord)

                roi_width = (float(roi[3]) - float(roi[1])) * width_ratio
                roi_height = (float(roi[2]) - float(roi[0])) * height_ratio

                xywh = [float(roi[1]) * width_ratio, float(roi[0]) * height_ratio, roi_width, roi_height]

                xywh_string = ','.join(list(map(str,xywh)))

                confidence_string = "confidence: " + "{:.0%}".format(annotations[url][0]['scores'][i])

                # Colors for the box outline and fill
                box_stroke = "#003366"
                box_fill = "#00bfff"
                # Colors for the path (mask) outline and fill
                path_stroke = "#00bfff"
                path_fill = "#3f3fa3"

                box_uuid = str(uuid.uuid4())
                pathTopLeft = [ str(float(xywh[0])), str(float(xywh[1])) ]
                pathHalfWidth = str(float(xywh[2]) / 2)
                pathHalfHeight = str(float(xywh[3]) / 2)
                svgPath = "M" + pathTopLeft[0] + "," + pathTopLeft[1] + 'h' + pathHalfWidth + 'h' + pathHalfWidth + 'v' + pathHalfHeight + 'v' + pathHalfHeight + 'h-' + pathHalfWidth + 'h-' + pathHalfWidth + 'v-' + pathHalfHeight + 'z'
                svg_string = "<svg xmlns='http://www.w3.org/2000/svg'>" + '<path xmlns="http://www.w3.org/2000/svg" d="' + svgPath + '" data-paper-data="{&quot;strokeWidth&quot;:1,&quot;rotation&quot;:0,&quot;deleteIcon&quot;:null,&quot;rotationIcon&quot;:null,&quot;group&quot;:null,&quot;editable&quot;:true,&quot;annotation&quot;:null}" id="rectangle_' + box_uuid + '" fill-opacity="0" fill="' + box_fill + '" fill-rule="nonzero" stroke="' + box_stroke + '" stroke-width="2" stroke-linecap="butt" stroke-linejoin="miter" stroke-miterlimit="10" stroke-dasharray="8" stroke-dashoffset="0" font-family="none" font-weight="none" font-size="none" text-anchor="none" style="mix-blend-mode: normal"/></svg>'

                box_annotation = { '@type': "oa:Annotation",
                                    'motivation': [ "oa:commenting", "oa:tagging" ],
                                    "resource": [ { '@id': "_:b2", '@type': "oa:Tag", 'http://dev.llgc.org.uk/sas/full_text': "handwriting", 'chars': "handwriting" },
                                                  { '@id': "_:b3", '@type': "dctypes:Text", 'http://dev.llgc.org.uk/sas/full_text': "", 'format': "text/html", 'chars': "" } ],
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
                svg_string = "<svg xmlns='http://www.w3.org/2000/svg'><path xmlns=\"http://www.w3.org/2000/svg\" d=\"" + svg_path + "\" data-paper-data=\"{&quot;strokeWidth&quot;:1,&quot;editable&quot;:true,&quot;deleteIcon&quot;:null,&quot;annotation&quot;:null}\" id=\"rough_path_" + mask_uuid + "\" fill-opacity=\"0.2\" fill=\"" + path_fill + "\" fill-rule=\"nonzero\" stroke=\"" + path_stroke + "\" stroke-width=\"1\" stroke-linecap=\"butt\" stroke-linejoin=\"miter\" stroke-miterlimit=\"10\" stroke-dasharray=\"\" stroke-dashoffset=\"0\" font-family=\"none\" font-weight=\"none\" font-size=\"none\" text-anchor=\"none\" style=\"mix-blend-mode: normal\"/></svg>"

                mask_annotation = { '@type': "oa:Annotation",
                                    'motivation': [ "oa:commenting" ],
                                    "resource": [ { '@id': "_:b2", '@type': "dctypes:Text", 'http://dev.llgc.org.uk/sas/full_text': confidence_string, 'format': "text/html", 'chars': confidence_string } ],
                                    "on": [ { '@id': "_:b0", '@type': "oa:SpecificResource", 
                                        'within': { '@id': manifest_id,
                                                    '@type': "sc:Manifest" },
                                                    'selector': { '@id': "_:b1", '@type': "oa:Choice", 'default': { '@id': "_:b3", '@type': "oa:FragmentSelector", 'value': "xywh=" + xywh_string },
                                                                  'item': { '@id': "_:b4", '@type': "oa:SvgSelector", 'value': svg_string } }, 'full': canvas_id} ], 
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
