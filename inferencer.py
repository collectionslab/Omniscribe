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
    'Detects images containing annotations from mainfest files. Default output is a manifest json file compliant with IIIF.')
parser.add_argument("--confidence", default=0.95, type=float,
                    help="A score from 0 to 1 that serves as a threshold for detecting annotations. Inferences at or above this score are inferred as an annotation.")
parser.add_argument("--html", action='store_true',
                    help='Saves images in a HTML gallery.')
parser.add_argument("--text", action='store_true',
                    help='Saves image links in a text file.')
parser.add_argument("--manifest", action='store_true',
                    help='Saves images in a IIIF-compliant manifest.')

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
    r = model.detect([image], verbose=0)[0]

    if len(r['scores']) == 0:
        print('No annotations were detected.')
        return None
    else:
        print('Annotations were found!')
        return image_path


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

    imageURIs = []
    someSequence = data['sequences'][0]
    canvases = someSequence['canvases']

    for c in canvases:
        imgs = c['images']
        height = c['height']
        width = c['width']
        for i in imgs:

            resourceID = i['resource']['@id']
            potentialFileExtension = resourceID[-3:].lower()

            fileExtensions = set(['jpg', 'peg', 'png', 'iff'])
            if potentialFileExtension not in fileExtensions:
                if potentialFileExtension[-1] == '/':
                    imageURIs.append(resourceID + 'full/full/0/default.jpg')
                else:
                    imageURIs.append(resourceID + '/full/full/0/default.jpg')
            else:
                imageURIs.append(i['resource']['@id'])

    return imageURIs


def infer(manifests):

    if ARGS.confidence < 0 or ARGS.confidence > 1:
        print('Please provide a confidence level between 0 and 1.')
        exit()

    model = load_model(WEIGHTS_PATH)
    currentDirectory = os.getcwd()
    results = set()
    imageURIs = []

    for man in manifests:
        imageURIs += getImages(man)

    imageURIs = set(imageURIs)

    print('Finding annotations on {} images collected from the manifest(s).'.format(
        len(imageURIs)))
    for img in tqdm(imageURIs):
        if detected(model, img):
            results.add(img)

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
        with open("resultsManifest.json", "w") as manifestFile:
            manifestFile.write(exportManifest(results))
            print("Saved resultsManifest.json to {}".format(currentDirectory))

    print('Finished detecting annotations.')


def main():
    infer(manifestURLs)


if __name__ == '__main__':
    main()
