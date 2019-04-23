# Proof of Concept

The goal of this project is to investigate the learnability of some of the data that is owned by the Collections Lab team at UCLA. Over one year later, we have concluded that the data we have has machine learning applications when the data is transformed appropriately. The following files were used to verify the feasibility of our project and what our project can achieve.

## The Pipeline

### 1. Gathering Data

To gather labeled data, we used [Zooniverse](https://www.zooniverse.org/), a crowd-sourcing platform where anyone can help draw bounding boxes on our collection of printed books. In total we had **4143** annotations across 1079 images. These annotations were exported and stored in `rawData.csv`.

### 2. Formatting the Raw Data

In order to leverage [Mask R-CNN](https://github.com/matterport/Mask_RCNN) to detect annotations, we need to provide the training data and validation data in a JSON of this form:

```javascript
{
    "Image1": {
        "imgName": "Image1.png",
        "regions": {
            "0": {
                "shape_attributes": {
                    "name": "polygon",
                    "all_points_x": [X1, X2, X2, X1],
                    "all_points_y": [Y1, Y1, Y2, Y2]
                }
            },
            "1": {
                "shape_attributes": {
                    "name": "polygon",
                    "all_points_x": [X1, X2, X2, X1],
                    "all_points_y": [Y1, Y1, Y2, Y2]
                }
            },
            "2": {
                "shape_attributes": {
                    "name": "polygon",
                    "all_points_x": [X1, X2, X2, X1],
                    "all_points_y": [Y1, Y1, Y2, Y2]
                }
            }
        }
    },
    "Image2": {
        "imgName": "Image2.png",
        "regions": {
            "0": {
                "shape_attributes": {
                    "name": "polygon",
                    "all_points_x": [X1, X2, X2, X1],
                    "all_points_y": [Y1, Y1, Y2, Y2]
                }
            },
            "1": {
                "shape_attributes": {
                    "name": "polygon",
                    "all_points_x": [X1, X2, X2, X1],
                    "all_points_y": [Y1, Y1, Y2, Y2]
                }
            }
        }
    }
    // ...
}
```

This JSON will have images as keys, where each image has a name and one or more regions (labeled bounding boxes) on that image.
While every region is labeled as a polygon, `all_points_x` and `all_points_y` store x and y coordinates that form a rectangle, which are the coordinates of the bounding boxes that Zooniverse volunteers have drawn for us.

In short, our data was presented like this: ![snippet of raw data](./images/t4.png)

and we wrote `extractROIs.py` that generated a `data.json` file that formats the data to look more like this:
 ![snippet of formatted data](./images/formattedData.png)

### 3. Generating the datasets

 We wrote `datasetGenerator.py` to split `data.json` to have a roughly 70/15/15 split (70% of the annotations are for training, 15% of the annotations are for validation, and 15% of the annotations are for testing). This split is necessary in order to tune hyperparameters and ultimately prevent overfitting. With `SEED = 42`, we had **2901** annotations for training, **627** annotations for validation, and **615** annotations for testing.

### 4. Training the Model

 TODO
#### Training Loss Curve

![training loss curve](images/trainingLoss.png)

#### Validation Loss Curve

![validation loss curve](images/validationLoss.png)

## Files and Directories (Requires Python 3.6.x)

### `data.json`

The resulting file generated from `extractROIs.py`. It contains all the images with their labeled annotations from `rawData.csv`. It is to be used with `datasetGenerator.py` in order to generate datasets that are ready for training.

### `datasetGenerator.py`

This scripts reads `data.json` and generates three JSON files for training, validation, and testing. Each of these files have to be renamed to `via_region_data.json` and are to be placed in the same directory where the images they represent are located. Note that changing the `SEED` value will create different datasets.

### `extractROIs.py`

This script takes the `rawData.csv` file (hard-coded) and generates `data.json`, a JSON file that contains all the images listed on zooniverse along with all the regions that they may have. The JSON itself is a relatively complex object that stores many images, and those images may themselves have lists of ROIs.

To put it simply, every image has a list of ROIs, and every ROI is made up of an `all_points_x"`
array and an `all_points_y` array such that `all_points_x[i]` and `all_points_y[i]` make up a
coordinate point, where every region would have four of these coordinate points (to make a
rectangle that captures the ROI).

These ROIs are constructed as such due to the fact that the Mask R-CNN as released
on GitHub require that structure in order to do training.

`$ python3 extractROIs.py`

### handwriting/

Contains a training set and a validation set for images that contain handwriting. These images come from the Collections Lab database. Note that training the model assumes daughter directories "train" and " val" where those directories contain only images.

### `inferencer.py`

This script is the engine that does all the handwriting detection. It currently takes a list of manifests via command line and will save all images referred by the manifest that it predicts has at least one region that contains handwriting.

The script will display information of its configuration for Mask R-CNN, the weights of the models it will use to infer, the manifest URI it is currently running on, the image URI it is currently inferring on, and confidence scores in range [0.96, 1] of any region it picks up (the higher the score, the more confident the model believes a region contains handwriting).

`$ python3 inferencer.py https://marinus.library.ucla.edu/iiif/annotated/uclaclark_SB322S53.json`

#### mask-rcnn/

This is the vanilla Mask-RCNN that is re-purposed for detecting handwriting. For more information, please refer to <https://github.com/matterport/Mask_RCNN>.

### rawData.csv

This csv files stores all the labeled data created from zooniverse users. The data includes
regions of interests that were labeled and provides some information of the user who marked
them. Further processing of this data is needed before it can be trained.

### requirements.txt

A list of dependencies needed to run this package. To be used as follows:

$ pip3 install -r requirements.txt