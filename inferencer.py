"""
Mask R-CNN
Trained on annotations found in old printed books
Copyright (c) 2018 Matterport, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Jonathan Quach of BuildUCLA
------------------------------------------------------------
"""

import os
import json
import requests
import ssl
import skimage.draw
import urllib3
from tqdm import tqdm
from argparse import ArgumentParser
from mrcnn.config import Config
from mrcnn import model as modellib, utils
from exportFiles import exportHTML, exportManifest

parser = ArgumentParser(
    'Detects images containing annotations from manifest files. Default output is a manifest json file compliant with IIIF.')
parser.add_argument("--confidence", default=0.95, type=float,
                    help="A score from 0 to 1 that serves as a threshold for detecting annotations. Inferences at or above this score are inferred as an annotation.")
parser.add_argument("--html", action='store_true',
                    help='Saves images in a HTML gallery.')
parser.add_argument("--text", action='store_true',
                    help='Saves image links in a text file.')
parser.add_argument("--manifest", action='store_true',
                    help='Saves image data to a IIIF-compliant manifest.')
parser.add_argument("--annotate", action='store_true',
                    help='Saves detected annotations to IIIF AnnotationList file(s), linked from the manifest.')
parser.add_argument("--iiif_root", default="http://127.0.0.1/iiif", type=str,
                    help='Web-accessible address from which output IIIF manifests and annotations will be served.')
parser.add_argument("--max_pages", default=-1, type=int,
                    help='Maximum number of images (IIIF canvases) to process.')

ARGS, manifestURLs = parser.parse_known_args()
WEIGHTS_PATH = "model.h5"
ssl._create_default_https_context = ssl._create_unverified_context

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class CustomConfig(Config):

    NAME = "annotation"
    BACKBONE = "resnet50"
    NUM_CLASSES = 2
    DETECTION_MIN_CONFIDENCE = ARGS.confidence


def detected(model, image_path):
    assert image_path

    print("\nFinding annotations on image: {}".format(image_path))

    image = skimage.io.imread(image_path)
    #print("shape of image is ", image.shape)

    r = model.detect([image], verbose=0)[0]

    if len(r['scores']) == 0:
        print('No annotations were detected.')
        return None
    else:
        print('Annotations were found!')
        return [r, image.shape[1], image.shape[0]]


def load_model(weights_path):
    assert weights_path

    class InferenceConfig(CustomConfig):

        GPU_COUNT = 1
        IMAGES_PER_GPU = 1

    config = InferenceConfig()
    model = modellib.MaskRCNN(mode="inference", config=config,
                              model_dir="logs/")

    model.load_weights(weights_path, by_name=True)

    return model


def getImages(manifestURL=None):
    data = None

    if os.path.isfile(manifestURL):
        with open(manifestURL, encoding='utf-8') as dataFile:
            data = json.loads(dataFile.read())
    else:
        try:
            res = requests.get(manifestURL, verify=False)
            data = json.loads(res.content)
        except:
            print('Could not connect to {}. Please check if the URL provided is correctly typed.'.format(
                manifestURL))
            print('Exiting now.')
            exit()

    # This should be a dictionary keyed on the image service @id,
    # with width and height as the values
    imageURIs = {}
    someSequence = data['sequences'][0]
    canvases = someSequence['canvases']

    # Example of a manifest that indicates that the "full" sized
    # image from the "resource" entry is smaller than max
    # http://iiif.gdmrdigital.com/nlw/4004562-cutdown.json
    # @id: "http://dams.llgc.org.uk/iiif/2.0/image/4004566/full/1024,/0/default.jpg"

    for c in canvases:
        imgs = c['images']
        height = c['height']
        width = c['width']
        for i in imgs:

            # ASSUMPTION: Each image takes up the entire canvas.
            # This assumes a simplified use of the IIIF Presentation API,
            # which explicitly states that multiple images can exist on
            # the same canvas.
            # In the future, this should be supported by checking for and
            # parsing any "canvas fragment" #xywh= coordinates that are
            # specified at the end of the "on" parameter of each image.
            # In that case, the output of the handwriting detection would need
            # to be projected into these spaces, rather than onto the full
            # canvas.

            resourceID = i['resource']['@id']

            serviceID = i['resource']['service']['@id']

            # Just in case the image server URL is in the
            # servide @id parameter
            if (len(serviceID) > len(resourceID)):
                imageURL = serviceID
            else:
                imageURL = resourceID

            if (imageURL.find('/default.jpg') < 0):
                if (imageURL[-1] != '/'):
                    imageURL += '/'
                imageURL += 'full/full/0/default.jpg'
        
            #print("looking at image " + imageURL)
            imageURIs[imageURL] = [width, height]

    return imageURIs


def infer(manifests):

    if ARGS.confidence < 0 or ARGS.confidence > 1:
        print('Please provide a confidence level between 0 and 1.')
        exit()

    model = load_model(WEIGHTS_PATH)
    currentDirectory = os.getcwd()
    results = set()
    annotations = {}
    imageURIs = {}

    total_images = 0

    for man in manifests:
        image_info = getImages(man)
        # imageURIs is a dict keyed on the @id value from the resource section
        # Its value is a [width, height] tuple
        for image_url in image_info:
            if ((ARGS.max_pages < 0) or (total_images < ARGS.max_pages)):
                imageURIs[image_url] = [image_info[image_url][0], image_info[image_url][1]]
                total_images += 1

    print('Finding annotations on {} images collected from the manifest(s).'.format(
        len(imageURIs)))
    for img in tqdm(imageURIs):
        detection_results = detected(model, img)
        if detection_results:
            results.add(img)
            if ARGS.annotate:

                canvas_width = imageURIs[img][0]
                canvas_height = imageURIs[img][1]

                image_width = detection_results[1]
                image_height = detection_results[2]

                width_ratio = 1
                height_ratio = 1

                #if (img.find('full/full/0/default') == -1):
                #if ((canvas_width != image_width) or (canvas_height != image_height)):

                #    width_ratio = float(canvas_width) / float(image_width)
                #    height_ratio = float(canvas_height) / float(image_height)

                #print("canvas dims are " + str(canvas_width) + ", " + str(canvas_height))
                #print("scaling ratios are " + str(width_ratio) + ", " + str(height_ratio))

                annotations[img] = [detection_results[0], image_width, image_height, width_ratio, height_ratio]

            # DEV: only consider the first matching image
            continue

    print()
    if ARGS.html:
        with open("resultsImages.html", "w") as htmlFile:
            htmlFile.write(exportHTML(results))
            print("Saved resultsImages.html to {}".format(currentDirectory))

    if ARGS.text:
        with open("resultsURIs.txt", "w") as imgsFile:
            lines = sorted(results)
            imgsFile.write(lines[0])
            for img in lines[1:]:
                imgsFile.write('\n' + img)

            print("Saved resultsURIS.txt to {}".format(currentDirectory))

    if ARGS.manifest or not (ARGS.html or ARGS.text):
        if ARGS.annotate:
            [manifestJSON, annotations_data] = exportManifest(results, ARGS.iiif_root, annotations, True)
            for anno_path in annotations_data:
                anno_dir = '/'.join(anno_path.split('/')[:-1])
                os.makedirs(anno_dir, 0o755, True)
                with open(anno_path, "w") as annotations_file:
                    annotations_file.write(annotations_data[anno_path])
                    print("Saved annotations file to {}".format(anno_path))

        else:
            manifestJSON = exportManifest(results, ARGS.iiif_root, annotations, False)

        with open("resultsManifest.json", "w") as manifestFile:
            manifestFile.write(manifestJSON)
            print("Saved resultsManifest.json to {}".format(currentDirectory))

    print('Finished detecting annotations.')


def main():
    #infer(manifestURLs)
    infer(["uclaclark_SB322S53-short.json"])
    #infer(["http://iiif.gdmrdigital.com/nlw/4004562-cutdown.json"])


if __name__ == '__main__':
    main()
