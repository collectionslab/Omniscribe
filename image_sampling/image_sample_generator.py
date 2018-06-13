
def subsample_images(input_loc, output_dir_loc, sample_dimensions, stride = (1,1), num_samples = None, do_crop = False):
    # import necessary packages
    import sys
    import os
    sys.path.append(os.path.abspath('..'))
    from detection.lib.model.ImageROI import ImageROI, roi_to_csv
    from PIL import Image
    import numpy as np
    
    # compile list of all files to read
    input_files = []
    if os.path.isfile(input_loc):
        input_files.append(input_loc)
    elif os.path.isdir(input_loc):
        for f in os.listdir(input_loc):
            input_files.append(os.path.join(input_loc, f))
    else:
        print('Unknown location: ', input_loc)
        return
    
    # if output directory doesn't exist, create it
    if not os.path.exists(output_dir_loc):
        os.makedirs(output_dir_loc)
        
    # iterate for each file name
    for fname in input_files:
        
        # get info about image file path
        f_full_basename = os.path.basename(fname)
        f_basename, f_ext = os.path.splitext(f_full_basename)
        
        # get image PIL
        img = Image.open(fname)
        w, h = img.size
        
        # create list of ImageROIs for this image
        rois = [ImageROI(x, y, sample_dimensions[0], sample_dimensions[1])
                   for x in range(0, w - sample_dimensions[0], stride[0])
                   for y in range(0, h - sample_dimensions[1], stride[1])]
        
        # randomly choose num_samples number of ImageROIs from rois
        if (num_samples is not None) and (num_samples < len(rois)):
            rois = np.random.choice(rois, num_samples, replace=False)
        
        if do_crop:
            # for each ROI, crop the image and save it
            for i in range(len(rois)):
                roi = rois[i]
                im = img.crop((roi.x, roi.y, roi.x + roi.width, roi.y + roi.height))
                outfilename = os.path.join(output_dir_loc, f_basename + '-' + str(i) + f_ext)
                im.convert('RGB').save(outfilename)
        else:
            # copy the entire page to the output directory
            outfilename = os.path.join(output_dir_loc, f_full_basename)
            img.convert('RGB').save(outfilename)
            
            # write each ImageROI out to a csv with the format (ex.) 'outputdir/f_full_basename(includes .png)-roi_5.csv'
            # so, when generating labels, for each ROI csv, we remove everything including and after the last '-' to get the image filename
            for i in range(len(rois)):
                roi = rois[i]
                outfilename = os.path.join(output_dir_loc, f_full_basename + '-roi_' + str(i) + '.csv')
                roi_to_csv(roi, outfilename)

    
if __name__ == '__main__':
    """
    This script has one function: Generate and save random subsamples of an image.
    
    Required Parameters:
        - input file or directory
        - output directory
        - output image sizes, in format xsize,ysize
        
    Optional Parameters:
        - stride, in format xstride,ystride
            - if stride is unintialized, it will be default to 1 pixel 
        - number of output images. if not set, it defaults to all the images
    """
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', action = 'store', required = True,
                       help = 'input file or directory')
    parser.add_argument('-o', '--output', action = 'store', required = True,
                       help = 'directory where image samples should be output')
    parser.add_argument('-d', '--dimensions', action = 'store', required = True,
                       help = 'dimensions of each image subsample. in format xdim,ydim or just one number dim used to create squares')
    
    parser.add_argument('-s', '--stride', action = 'store', required = False, default = '1,1',
                        help = 'stride to use when creating image subsamples. in format xstride,ystride or just one number stride for both x and y. defaults to 1 pixel stride.')
    parser.add_argument('-n', '--number', action = 'store', required = False, default = None,
                       help = 'number of random subsamples of each image to generate and save. defaults to all possible samples.')
    
    parser.add_argument('-c', '--crop', action = 'store_true', required = False, default = False,
                        help = 'setting this flag will save the actual cropped images, instead of bounding boxes, in the output directory.')
    
    args = parser.parse_args()
    
    # preprocess a few formatted arguments
    
    # dimensions
    dims = tuple(int(i) for i in args.dimensions.split(','))
    if len(dims) == 1:
        dims = dims*2
    
    # stride
    stride = tuple(int(i) for i in args.stride.split(','))
    if len(stride) == 1:
        stride = stride*2
    
    # number
    if args.number is not None:
        number = int(args.number)
    else:
        number = None
    
    subsample_images(input_loc = args.input,
                     output_dir_loc = args.output,
                     sample_dimensions = dims,
                     stride = stride,
                     num_samples = number,
                     do_crop = args.crop)
    
    print('completed subsampling images from ' + str(args.input) + '. Images output to ' + str(args.output) + '.')
    