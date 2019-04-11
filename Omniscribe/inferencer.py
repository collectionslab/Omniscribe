"""
Mask R-CNN
Trained on annotations found in old printed books
Copyright (c) 2018 Matterport, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Jonathan Quach of BuildUCLA
------------------------------------------------------------
"""
import argparse
import os
import sys
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import skimage.draw
import cv2
import requests
import urllib
from mrcnn.visualize import display_instances
from mrcnn.config import Config
from mrcnn import model as modellib, utils
from tqdm import tqdm
from exportFiles import exportHTML, exportManifest

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Path to trained weights file
WEIGHTS_PATH = "model.h5"

parser = argparse.ArgumentParser(
    'Detects Images containing annotations from mainfest files. Default output is a text file containing the list of images')
parser.add_argument("--confidence", default=0.95, type=float,
                    help="A score from 0 to 1 that serves as a threshold for detecting annotations. Inferences at or above this score count as detections.")
parser.add_argument("--html", action='store_true',
                    help='Saves images in a HTML gallery.')
parser.add_argument("--text", action='store_true',
                    help='Saves image links in a text file.')
parser.add_argument("--manifest", action='store_true',
                    help='Saves images in a IIIF-compliant manifest.')

ARGS, manifestURLs = parser.parse_known_args()
############################################################
#  Configurations
############################################################


class CustomConfig(Config):
    # Give the configuration a recognizable name
    NAME = "handwriting"

    # faster to train than using resnet101 as backbone
    BACKBONE = "resnet50"

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + handwriting

    # Skip detections with < confidence
    DETECTION_MIN_CONFIDENCE = ARGS.confidence


def detected(model, image_path=None):
    assert image_path

    # Run model detection and generate the color splash effect
    print()
    print("RUNNING ON IMAGE: {}".format(image_path))

    image = skimage.io.imread(image_path)

    # Detect objects
    r = model.detect([image], verbose=0)[0]

    if len(r['scores']) == 0:
        print('NO ANNOTATIONS DETECTED')
        return None
    else:
        print('ANNOTATIONS FOUND')
        return image_path

############################################################
#  Load a trained model
############################################################


def load_model(weights_path):
    assert weights_path

    class InferenceConfig(CustomConfig):

        GPU_COUNT = 1
        IMAGES_PER_GPU = 1

    config = InferenceConfig()

    model = modellib.MaskRCNN(mode="inference", config=config,
                              model_dir="logs/")

    # Load weights
    model.load_weights(weights_path, by_name=True)

    return model


def getImages(manifestURL=None):

    data = None

    # accessing a manifest URL hosted on another server
    if urllib.parse.urlparse(manifestURL).scheme != "":
        r = requests.get(manifestURL, verify=False)
        data = json.loads(r.content)
    else:  # accessing a local manifest file
        with open(manifestURL, encoding='utf-8') as dataFile:
            data = json.loads(dataFile.read())

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

    CURRENT_DIRECTORY = os.getcwd()

    if ARGS.confidence < 0 or ARGS.confidence > 1:
        print('Please provide a confidence level between 0 and 1.')
        exit()

    model = load_model(WEIGHTS_PATH)

    results = set()

    imageURIs = []
    for man in manifests:
        imageURIs += getImages(man)

    for img in tqdm(imageURIs):
        if detected(model, img):
            results.add(img)

    if ARGS.html:
        with open("resultsImages.html", "w") as htmlFile:
            htmlFile.write(exportHTML(results))
            print("SAVED resultsImages.html TO {}".format(CURRENT_DIRECTORY))

    # create a text file that contains all image URIS of the images
    # that contain handwriting (each line contains one image URI)
    if ARGS.text:
        with open("resultsURIs.txt", "w") as imgsFile:
            lines = sorted(results)
            imgsFile.write(lines[0])
            for img in lines[1:]:
                imgsFile.write('\n' + img)

            print("SAVED resultsURIS.txt TO {}".format(CURRENT_DIRECTORY))

    if ARGS.manifest or not (ARGS.html and ARGS.text and ARGS.manifest):
        with open("resultsManifest.json", "w") as manifestFile:
            manifestFile.write(exportManifest(results))
            print("SAVED resultsManifest.json TO {}".format(CURRENT_DIRECTORY))


def main():
    infer(manifestURLs)


if __name__ == '__main__':
    main()
