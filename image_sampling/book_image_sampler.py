from image_sample_generator import subsample_images

def subsample_books(input_dir_loc, output_dir_loc, sample_dimensions, stride = (1,1), num_samples = None):
    # import necessary packages
    import os
    import math
    
    # read all book
    input_books = [d for d in os.listdir(input_dir_loc)
                   if os.path.isdir(os.path.join(input_dir_loc, d))]
    
    # if output directory doesn't exist, create it
    if not os.path.exists(output_dir_loc):
        os.makedirs(output_dir_loc)
    
    # label folder names
    label_pairs = [('positive', 'unlabeled'), ('negative', 'negative')]
    
    # total number of samples divided by number of books
    samples_per_label = None
    if num_samples is not None:
        samples_per_label = int(math.ceil(float(num_samples)
                                         /float(len(input_books))
                                         /float(len(label_pairs)) ))
        
    for book in input_books:
        book_dir = os.path.join(input_dir_loc, book)
        
        # subsample for each label pair
        for pair in label_pairs:
            input_label_dir = os.path.join(book_dir, pair[0])
            
            samples_per_image = None
            if samples_per_label is not None:
                # get the number of images in the input label
                num_images = len([f for f in os.listdir(input_label_dir)
                                  if os.path.isfile(os.path.join(input_label_dir, f))])
                
                samples_per_image = int(math.ceil(float(samples_per_label) / float(num_images)))
            
            # create output directory
            output_label_dir = os.path.join(output_dir_loc, book, pair[1])
            print('input: ', input_label_dir)
            print('output: ', output_label_dir)
            print('samples: ', samples_per_image)
            print()
            
            subsample_images(input_loc = input_label_dir,
                             output_dir_loc = output_label_dir,
                             sample_dimensions = sample_dimensions,
                             stride = stride,
                             num_samples = samples_per_image)
    
    
    

if __name__ == '__main__':
    """
    This script has one function: Generate and save random subsamples of an image.
    
    Required Parameters:
        - input directory
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
                       help = 'input directory containing all books, each of which contains a positive and negative folder')
    parser.add_argument('-o', '--output', action = 'store', required = True,
                       help = 'directory where image samples should be output, with unlabeled and negative folders per book')
    parser.add_argument('-d', '--dimensions', action = 'store', required = True,
                       help = 'dimensions of each image subsample. in format xdim,ydim or just one number dim used to create squares')
    
    parser.add_argument('-s', '--stride', action = 'store', required = False, default = '1,1',
                        help = 'stride to use when creating image subsamples. in format xstride,ystride or just one number stride for both x and y. defaults to 1 pixel stride.')
    parser.add_argument('-n', '--number', action = 'store', required = False, default = None,
                       help = 'number of total random subsamples (approximate).')
    
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
    
    subsample_books(input_dir_loc = args.input,
                     output_dir_loc = args.output,
                     sample_dimensions = dims,
                     stride = stride,
                     num_samples = number)
    
    print('completed subsampling images from ' + str(args.input) + '. Images output to ' + str(args.output) + '.')
    