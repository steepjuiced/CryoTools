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

# Get the desired number of chunks from the user
num_chunks = int(input('Enter the number of chunks to split the stack into: '))

# Open the MRC stack
with mrcfile.open('input.mrcs', permissive=True) as mrc:
    # Read the data and shape
    # Debug :
    # mrc.print_header()
    data = mrc.data
    shape = mrc.data.shape

    # Get the number of images in the mrc file and image dimensions
    if shape[1] == shape[2]:
        print('The X and Y dimensions are equal')
        print(f"The images are {shape[1]} x {shape[2]}")
        print(f"The number of images in the MRC stack is {shape[0]}")
        x_size = shape[1]
        y_size = x_size
        num_images = shape[0]
    else:
        num_images = shape[2]
        x_size = shape[0]
        y_size = x_size
        print(f"The number of images in the MRC stack is {shape[2]}")

    # Calculate the length of each chunk
    chunk_length = num_images // num_chunks

    # Loop through each chunk
    for i in range(num_chunks):
        # Calculate start and end indices for current chunk
        start_index = i * chunk_length
        end_index = start_index + chunk_length

        # Read images for current chunk
        images = mrc.data[start_index:end_index]

        # Bin images
        binned_images = np.mean(images.reshape((-1, x_size, y_size)), axis=1)

        # Write binned images to new MRC stack file
        with mrcfile.new(f'chunk_{i}.mrcs', overwrite=True) as new_mrc:
            new_mrc.set_data(binned_images.astype(np.float16))
