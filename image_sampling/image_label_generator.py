"""
This script has one function: make labeling images easier.

Required Parameters:
    - input directory
    - positive output directory
    - negative output directory
"""

def generate_labels(input_dir, pos_output_dir, neg_output_dir, precropped = False):
    import sys
    import os
    import shutil
    from PIL import Image
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    plt.ion()
    
    sys.path.append(os.path.abspath('..'))
    from detection.lib.model.ImageROI import csv_to_roi
    

    # get list of files from input_dir
    input_files = []
    if precropped:
        input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    else:
        input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir)
                       if (os.path.isfile(os.path.join(input_dir, f)) and f.endswith('.csv'))]

    # if pos_output_dir doesn't exist, create it
    if not os.path.exists(pos_output_dir):
        os.makedirs(pos_output_dir)

    # if neg_output_dir doesn't exist, create it
    if not os.path.exists(neg_output_dir):
        os.makedirs(neg_output_dir)
    
    # button press to output directory mappings
    key_to_dir = {'left' : neg_output_dir,
                  'right' : pos_output_dir,
                  'down' : None,
                  'up' : None
                 }
    
    # disable toolbar
    matplotlib.rcParams['toolbar'] = 'None'
    
    # setup figure
    fig, axes = plt.subplots(1)
    
    plt.suptitle("'left'=negative, 'right'=positive, 'down'=delete, 'up'=skip",
                fontweight='bold')
    pltobj = None
    key_connection = None
    rect = None
    
    for fname in input_files:
        print("Labeling file '" + str(fname) + "'")
        
        # setup key press event callback
        lock = {}
        def on_key(event):
            lock['key'] = event.key
        
        # register key press connection
        if key_connection is not None:
            fig.canvas.mpl_disconnect(key_connection)
        key_connection = fig.canvas.mpl_connect('key_press_event', on_key)
        
        # get info about file path
        f_full_basename = os.path.basename(fname)
        f_basename, f_ext = os.path.splitext(f_full_basename)
        
        imgname = fname
        if not precropped:
            imgname = os.path.join(input_dir, f_full_basename[:f_full_basename.rfind('-')])
        
        # read image from file
        pilimg = Image.open(imgname)
        img_arr = np.asarray(pilimg)
        
        # title the image plot
        plt.title(imgname)
        
        # update plot image
        if pltobj is None:
            pltobj = plt.imshow(img_arr)
        pltobj.set_data(img_arr)
        
        roi = None
        if not precropped:
            # get ROI
            roi = csv_to_roi(fname)

            if rect is not None:
                rect.remove()
            rect = patches.Rectangle((roi.x,roi.y),roi.width, roi.height,
                                     linewidth=2,
                                     edgecolor='r',
                                     facecolor='none')
            axes.add_patch(rect)
        
        plt.pause(0.1)
        
        # wait for key press
        while True:
            # wait for keypress (plt.waitforbuttonpress() == True)
            while (not plt.waitforbuttonpress()):
                continue
            
            # move or delete file accordingly
            keyval = lock['key']
            if keyval in key_to_dir:
                outdir = key_to_dir[keyval]
                if outdir is not None:
                    if precropped:
                        shutil.move(imgname, outdir)
                        print("Moved '" + str(imgname) + "' to '" + str(outdir) + "'")
                    else:
                        # crop and save
                        cropimg = pilimg.crop((roi.x, roi.y, roi.x + roi.width, roi.y + roi.height))
                        outloc = os.path.join(outdir, f_basename + '.png')
                        cropimg.convert('RGB').save(outloc)
                        os.remove(fname)
                        
                elif keyval == 'down':
                    os.remove(fname)
                    print("Deleted '" + str(fname) + "'")
                else:
                    print("Skipped '" + str(fname) + "'")
                break
            else:
                print("Key '" + str(keyval) + "' is not accepted. Only left, right, and down arrows are allowed.")
        
        print()

    return


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', action = 'store', required = True,
                       help = 'input directory')
    parser.add_argument('-p', '--positive', action = 'store', required = True,
                       help = 'directory where positive image samples should be output')
    parser.add_argument('-n', '--negative', action = 'store', required = True,
                       help = 'directory where negative image samples should be output')
    parser.add_argument('-c', '--cropped', action = 'store_true', required = False, default = False,
                        help = 'flag, if set, tells the generator to assume images are precropped.')

    args = parser.parse_args()

    generate_labels(args.input, args.positive, args.negative, args.cropped)
    print('generated labels for images from ' + str(args.input)
          + '. Positive images output to ' + str(args.positive)
          + '. Negative images output to ' + str(args.negative))