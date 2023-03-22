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

import mrcfile
import numpy as np

# Open the MRC stack
with mrcfile.open('input.mrc', permissive=True) as mrc:
    # Read the data and shape
    data = mrc.data
    shape = mrc.data.shape

    # Get the number of images in the mrc file and image dimensions
    if shape[1] == shape[2]:
        print('The X and Y dimensions are equal')
        print('The images are X x Y')
        print(f'The number of images in the MRC stack is {shape[0]}.')
    else:
        print(f'The number of images in the MRC stack is {shape[2]}.')

    # Get the desired number of chunks from the user
    num_chunks = int(input('Enter the number of chunks to split the stack into: '))

    # Calculate the length of each chunk
    chunk_length = shape[0] // num_chunks

    # Bin the data into chunks
    binned_data = np.zeros((chunk_length, shape[1], shape[2], num_chunks))
    for i in range(num_chunks):
        start = i * chunk_length
        end = (i + 1) * chunk_length
        binned_data[:, :, :, i] = np.mean(data[start:end], axis = 0)

    # Save the binned data to a new MRC stack for each chunk
    for i in range(num_chunks):
        with mrcfile.new(f'output_{i}.mrc', overwrite=True) as new_mrc:
            new_mrc.set_data(binned_data[:, :, :, i])
