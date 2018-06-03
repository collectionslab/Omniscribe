"""
This script has one function: make labeling images easier.

Required Parameters:
    - input directory
    - positive output directory
    - negative output directory
"""

def generate_labels(input_dir, pos_output_dir, neg_output_dir):
    import sys
    import os
    import shutil
    
    import matplotlib
    import matplotlib.pyplot as plt
    plt.ion()

    # get list of files from input_dir
    input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    # if pos_output_dir doesn't exist, create it
    if not os.path.exists(pos_output_dir):
        os.makedirs(pos_output_dir)

    # if neg_output_dir doesn't exist, create it
    if not os.path.exists(neg_output_dir):
        os.makedirs(neg_output_dir)
    
    # button press to output directory mappings
    key_to_dir = {'left' : neg_output_dir,
                  'right' : pos_output_dir,
                  'down' : None}
    
    # disable toolbar
    matplotlib.rcParams['toolbar'] = 'None'
    
    # setup figure
    fig = plt.figure()
    plt.suptitle("Use arrows to label: 'left'=negative, 'down'=delete, 'right'=positive",
                fontweight='bold')
    pltobj = None
    key_connection = None
    
    for fname in input_files:
        print("Labeling file '" + str(fname) + "'")
        
        # read image from file
        img_arr = plt.imread(fname)
        
        # title the image plot
        plt.title(fname)
        
        # update plot image
        if pltobj is None:
            pltobj = plt.imshow(img_arr)
        pltobj.set_data(img_arr)
        plt.pause(0.1)
        
        # setup key press event callback
        lock = {}
        def on_key(event):
            lock['key'] = event.key
        
        # register key press connection
        if key_connection is not None:
            fig.canvas.mpl_disconnect(key_connection)
        key_connection = fig.canvas.mpl_connect('key_press_event', on_key)
        
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
                    shutil.move(fname, outdir)
                    print("Moved '" + str(fname) + "' to '" + str(outdir) + "'")
                else:
                    os.remove(fname)
                    print("Deleted '" + str(fname) + "'")
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

    args = parser.parse_args()

    generate_labels(args.input, args.positive, args.negative)
    print('generated labels for images from ' + str(args.input)
          + '. Positive images output to ' + str(args.positive)
          + '. Negative images output to ' + str(args.negative))