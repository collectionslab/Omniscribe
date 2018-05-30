###
# Bounding Box Classification Module
###


###
# Imports Start
###

from torch.utils.data import Dataset
from torch.utils.data.dataloader import default_collate
from torchvision.datasets.folder import IMG_EXTENSIONS, has_file_allowed_extension, default_loader
from torchvision.transforms.functional import crop
from torchvision.transforms import ToTensor
import torch
import os

import sys
sys.path.append(os.path.abspath('../../../'))

from detection.lib.model.ImageROI import ImageROI

###
# Imports End
###


###
# BoundingBoxClassificationDataset Start
###

def make_dataset_with_meta(dirname):
    dirname = os.path.expanduser(dirname)
    images = [(os.path.join(dirname, f), os.path.join(dirname, os.path.splitext(f)[0] + '-meta.csv'))
               for f in sorted(os.listdir(dirname))
              if has_file_allowed_extension(f, IMG_EXTENSIONS)]
    return images

def read_metadata(metafile):
    # TODO: read in metadata csv from metafile, return list of dicts as follows:
    
    return [{'bottom_y' : 0, 'left_x' : 0, 'height' : 1346, 'width' : 1000, 'class' : 'unknown'},
            {'bottom_y' : 0, 'left_x' : 0, 'height' : 1346, 'width' : 1000, 'class' : 'positive'},
            {'bottom_y' : 150, 'left_x' : 150, 'height' : 50, 'width' : 50, 'class' : 'negative'}
           ]

class BoundingBoxClassificationDataset(Dataset):
    def __init__(self, root, transform = None):
        self.transform = transform
        self.images_and_meta = make_dataset_with_meta(root)
    
    def __getitem__(self, index):
        image_file, meta_file = self.images_and_meta[index]
        bounding_boxes = read_metadata(meta_file)
        raw_image = default_loader(image_file)
        cropped_images = []
        
        i = 0
        for box in bounding_boxes:
            img = crop(raw_image, box['bottom_y'], box['left_x'], box['height'], box['width'])
            if self.transform is not None:
                img = self.transform(img)
            cropped_images.append(img)
            
            i += 1
            if index < 10 and i <= 1:
                break
            
        cropped_images = default_collate(cropped_images)
        return cropped_images

    def __len__(self):
        return len(self.images_and_meta)

###
# BoundingBoxClassificationDataset End
###


###
# Prediction function Start
###

def predict_on_boxes(model, images):
    model.train(False)
    all_preds = []
    for inputs in images:
        with torch.set_grad_enabled(False):
            outputs = model(inputs)
            _, preds = torch.max(outputs.data, 1)
            all_preds.append(any(preds))
        
    return all_preds

###
# Prediction function End
###


###
# ROI Prediction function Start
# Only predicts on ROIs for one page
###

def get_pos_rois(model, page_info, model_transform = None, model_input_size = (32, 32), stride = (8,8)):
    model.train(False)
    # todo
    
    # Get page image and ROIs
    page_img, page_rois = page_info
    
    # If page_img is actually an image location, load the PIL image
    if isinstance(page_img, str):
        page_img = default_loader(page_img)
        
    if isinstance(stride, int):
        stride = (stride, stride)
        
    all_pos_locs = []
        
    # For each ROI, perform predictions on squares of model_input_size
    for roi in page_rois:
        
        # Create all possible sub-ROIs in the given ROI
        sub_roi_locs = [ImageROI(y, x, model_input_size[1], model_input_size[0])
                        for y in range(roi.y, roi.y + roi.height - model_input_size[1], stride[1])
                        for x in range(roi.x, roi.x + roi.width - model_input_size[0], stride[0])
                       ]
        
        # If no model transform is given, create a basic ToTensor() that can be passed into a model
        # TODO: decide if this necessary
        if not model_transform:
            model_transform = ToTensor()
            
        # Create cropped images for each sub-ROI
        sub_rois = [model_transform(crop(page_img, sr.y, sr.x, sr.height, sr.width)) for sr in sub_roi_locs]
        
        # Concatenate all sub-ROI cropped images into a tensor for batched input to a model
        sub_rois = default_collate(sub_rois)
        
        # Obtain predictions from model for sub-ROI images
        outputs = model(sub_rois)
        _, roi_preds = torch.max(outputs.data, 1)
        
        # Extract sub-ROIs with positive predictions, and their outputs (confidence)
        pos_roi_items = [(loc, conf[pred].item())  for (loc, pred, conf) in zip(sub_roi_locs, roi_preds, outputs) if pred == 1]
        
        # Modify each positive ROI appropriately
        for loc, conf  in pos_roi_items:
            loc.isAnnotation = True
            loc.confidence = conf
        
        # Add these new positive ROIs to the overall list of positive ROIs for this page
        all_pos_locs.append([sub_roi for (sub_roi, conf) in pos_roi_items])
        
    # Return a list of all positive ROIs in this image
    return all_pos_locs

###
# ROI Prediction function End
###
