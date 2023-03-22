"""
Steep Juiced
This script uses the 'mrcfile' library to read and display MRC header.
"""

import argparse
import os
import mrcfile
import numpy as np

# Parse command line argument
parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, help='Input MRCS file')
args = parser.parse_args()

# Open the MRC stack
with mrcfile.open(args.input, permissive=True) as mrc:
    # print the header information
    print(f'nx : {mrc.header.nx}')