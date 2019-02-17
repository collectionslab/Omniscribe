"""
Mask R-CNN
Train on the toy Balloon dataset and implement color splash effect.
Copyright (c) 2018 Matterport, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Waleed Abdulla
------------------------------------------------------------
Usage: import the module (see Jupyter notebooks for examples), or run from
       the command line as such:
    # Train a new model starting from pre-trained COCO weights
    python3 balloon.py train --dataset=/path/to/balloon/dataset --weights=coco
    # Resume training a model that you had trained earlier
    python3 balloon.py train --dataset=/path/to/balloon/dataset --weights=last
    # Train a new model starting from ImageNet weights
    python3 balloon.py train --dataset=/path/to/balloon/dataset --weights=imagenet
    # Apply color splash to an image
    python3 balloon.py splash --weights=/path/to/weights/file.h5 --image=<URL or path to file>
    # Apply color splash to video using the last weights you trained
    python3 balloon.py splash --weights=last --video=<URL or path to file>
"""

import os
import sys
import json
import datetime
import numpy as np
import skimage.draw
import cv2
from mrcnn.visualize import display_instances
import matplotlib.pyplot as plt

# frowned upon because of security breaches
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# Root directory of the project
ROOT_DIR = os.path.abspath("../../")

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
from mrcnn.config import Config
from mrcnn import model as modellib, utils

# Path to trained weights file
COCO_WEIGHTS_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# Directory to save logs and model checkpoints, if not provided
# through the command line argument --logs
DEFAULT_LOGS_DIR = "/Users/silver/Desktop/mask-rcnn/Annotation-Detector/logs/"

WEIGHTS_PATH = '/Users/silver/Desktop/mask-rcnn/Annotation-Detector/mask_rcnn_handwriting_0007.h5'
MANIFEST_PATH  = 'https://marinus.library.ucla.edu/iiif/annotated/uclaclark_SB322S53.json'
############################################################
#  Configurations
############################################################


class CustomConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "handwriting"

    #should be faster to train as opposed to resnet101
    BACKBONE = "resnet50"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 2

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # Background + handwriting

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 50

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.90


def color_splash(image, mask):
    """Apply color splash effect.
    image: RGB image [height, width, 3]
    mask: instance segmentation mask [height, width, instance count]
    Returns result image.
    """
    # Make a grayscale copy of the image. The grayscale copy still
    # has 3 RGB channels, though.
    

    gray = skimage.color.gray2rgb(skimage.color.rgb2gray(image)) * 255
    
    # We're treating all instances as one, so collapse the mask into one layer
    mask = (np.sum(mask, -1, keepdims=True) >= 1)
    # Copy color pixels from the original color image where mask is set
    if mask.shape[0] > 0:
        splash = np.where(mask, image, gray).astype(np.uint8)
    else:
        splash = gray
    return splash


def detect_and_color_splash(model, image_path=None):
    assert image_path

    # Run model detection and generate the color splash effect
    print("Running on {}".format(image_path))
    # Read image
    image = skimage.io.imread(image_path)

    # import requests
    # from PIL import Image
    # from io import BytesIO

    # response = requests.get(image_path, verify=False)
    # print(response)
    # image = Image.open(BytesIO(response.content))


    # Detect objects
    r = model.detect([image], verbose=1)[0]

    for e in r['scores']:
    	print(e)

    if len(r['scores']) == 0:
    	print('NO ROIS!')
    	return None
    else:

        # Color splash
        splash = color_splash(image, r['masks'])
        # Save output
        file_name = "splash_{:%Y%m%dT%H%M%S}.png".format(datetime.datetime.now())
        skimage.io.imsave(file_name, splash)
        print("Saved to ", file_name)

    




############################################################
#  Load a trained model
############################################################

def load_model(weights_path):
    assert weights_path

    class InferenceConfig(CustomConfig):
        # Set batch size to 1 since we'll be running inference on
        # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1
    config = InferenceConfig()
    config.display()

    model = modellib.MaskRCNN(mode="inference", config=config, model_dir=DEFAULT_LOGS_DIR)

    # Load weights
    print("Loading weights ", weights_path)
    
    model.load_weights(weights_path, by_name=True)

    return model




def getImageURIs(manifestURL=None):
    import requests
    # retrieve a manifest.json file from url

    url = 'https://marinus.library.ucla.edu/iiif/annotated/uclaclark_SB322S53.json'
    r = requests.get(url, verify=False)
    data = json.loads(r.content)

    imageURIs = []


    someSequence = data['sequences'][0] # since we do not care about the order, we can just arbitrarily choose the first one

    canvases = someSequence['canvases']

    for c in canvases:
        imgs = c['images']

        for i in imgs:
            #imageURIs.append(i['resource']['@id'] + '/full/full/0/default.jpg')
            imageURIs.append(i['resource']['@id'])

    # with open(manifestURL) as data_file:    
    #     data = json.load(data_file)

    #     someSequence = data['sequences'][0] # since we do not care about the order, we can just arbitrarily choose the first one

    #     canvases = someSequence['canvases']

    #     for c in canvases:
    #         imgs = c['images']

    #         for i in imgs:
    #             imageURIs.append(i['resource']['@id'] + '/full/full/0/default.jpg')

    return imageURIs


def detect_annotations_from_manifest(model,manifest_path):
    assert model and manifest_path


    annotatedPages = []
    imageURIs = getImageURIs(manifest_path)


    print(imageURIs )

    print('Looking into this manifest ', manifest_path)
    print('Inferencing with model ', model)

    for img in imageURIs:
        prediction = detect_and_color_splash(model,img)
        if prediction is not None:
            annotatedPages.append((img,prediction))

    return annotatedPages


    



if __name__ == '__main__':

    import time
    t0 = time.time()

    m = load_model(WEIGHTS_PATH)

    results = detect_annotations_from_manifest(m,MANIFEST_PATH)

    for r in results:
        print(r)
    


    t1 = time.time()

    print((t1-t0)/3600) #prints how many hours it took