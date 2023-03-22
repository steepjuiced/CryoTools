"""
Steep Juiced
This script uses the 'mrcfile' library to read and write MRC files. 
It prompts the user to enter the number of chunks to split the stack into,
calculates the length of each chunk, and hen bins the data into the desired number 
of chunks using 'np.mean()'. 
Finally, it saves each chunk as a new MRC stack using 'mrcfile.new()'. Note that this script assumes that the input MRC stack
has dimensions '(N, X, Y)', where 'N' is the number of images and 'x' and 'y' are the image dimensions. If you MRC stack has a 
different shape, you may need to modify the scipt accordingly.

permissive=True is used to allow reading of non-standard MRC files. If your MRC stack is a standard file, you can oomit this argument.
"""

import argparse
import os
import mrcfile
import numpy as np

# Parse command line argument
parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help='Input MRCS file')
parser.add_argument('--chunks', required=True, type=int, help='Number of chunks to bin the images into')
args = parser.parse_args()

# Open the MRC stack
with mrcfile.open(args.input, permissive=True) as mrc:
    # Read the data and shape
    # Debug :
    # mrc.print_header()
    data = mrc.data
    nx, ny, nz = mrc.data.shape
    mrc_header = mrc.header

    # Calculate the number of images in each chunk
    chunk_size = nz // args.chunks

    # Create the output directory if it does not exist
    output_dir = os.path.splitext(args.input)[0]
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Loop through each chunk
    for i in range(args.chunks):
        # Calculate start and end indices for current chunk
        start_index = i * chunk_size
        end_index = start_index + chunk_size
        chunk_data = data[:, :, start_index:end_index]
        chunk_filename = os.path.join(output_dir, f"chunk_{i+1}.mrcs")
        with mrcfile.new(chunk_filename, overwrite=True) as mrc:
            mrc.set_data(np.squeeze(chunk_data))
            #mrc.set_header(mrc_header)
            #mrc.header.nz = chunk_size