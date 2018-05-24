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
import torch
import os

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
    
    return [{'bottom_y' : 0, 'left_x' : 0, 'height' : 1346, 'width' : 1000},
#             {'bottom_y' : 150, 'left_x' : 150, 'height' : 50, 'width' : 50}
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
        for box in bounding_boxes:
            img = crop(raw_image, box['bottom_y'], box['left_x'], box['height'], box['width'])
            if self.transform is not None:
                img = self.transform(img)
            cropped_images.append(img)
            
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
