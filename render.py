import argparse

from collections import namedtuple

import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

Point = namedtuple('Point', ['x', 'y'])

def render(data_file, axis_max = None, line_thickness = 1):
    data = pd.read_csv(
        data_file,                # The file we are reading
        sep = ' ',                # Columns are separated by spaces
        header = None,            # There is no header row to name the columns
        names = [                 # Name the columns
            'command',            # First columns is the command
            'x',                  # Second column is the X value
            'y'                   # Third column is the Y value
        ],
        comment = '#',            # Comment lines start with # so ignore them.
        skip_blank_lines = True,  # Ignore lines with nothing on them
    )

    # Remove the X/Y in front of the number and tell Python it is a number
    def __parse_col(x):
        if x is np.nan or x.startswith('Z'):
            return None
        elif x.startswith('X'):
            return float(x.replace('X', ''))
        elif x.startswith('Y'):
            return float(x.replace('Y', ''))
        else:
            raise ValueError("Unknown column value: {0}".format(x))

    data.x = data.x.apply(__parse_col)
    data.y = data.y.apply(__parse_col)

    # Create a plot figure that is 8 inches by 8 inches
    fig, ax = plt.subplots(figsize=(8, 8))

    # Start at X0, Y0
    curr_xy = Point(0,0)

    # Go through each of the commands
    for i, next_xy in data.iterrows():

        if next_xy.command.upper() == 'G0':
            # G0 is lift up and go to point, so update the starting point
            curr_xy = Point(next_xy.x, next_xy.y)
        elif next_xy.command.upper() == 'G1':
            # G1 is put down and move to point, so draw a line from the current point to the next point
            line = plt.plot([curr_xy.x, next_xy.x], [curr_xy.y, next_xy.y], color = 'k')
            # Make the drawn line thicker
            plt.setp(line, linewidth = line_thickness)

        # Update the current point from the 'next' point
        curr_xy = Point(next_xy.x, next_xy.y)

    # Default to fitting the largest X or Y value plotted if axis_max wasn't supplied
    if axis_max is None:
        ax.set_xlim(0, data.x.max())
        ax.set_ylim(0, data.y.max())
    else: # Otherwise set the axis to range from 0 to axis_max
        ax.set_xlim(0, axis_max)
        ax.set_ylim(0, axis_max)

    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Render a set of commands into an image.')
    parser.add_argument(
        'filename',
        metavar = 'FILENAME',
        type = str,
        help = 'Input file to render'
    )

    parser.add_argument(
        '--axis-size',
        metavar = 'AXIS_SIZE',
        type = float,
        help = 'Set the X,Y axes to range from zero to AXIS_SIZE'
    )

    parser.add_argument(
        '--linewidth',
        metavar = 'LINE_WIDTH',
        type = float,
        default = 1,
        help = 'Set the line width to LINE_WIDTH'
    )

    args = parser.parse_args()
    render(args.filename, args.axis_size, args.linewidth)

if __name__ == '__main__':
    main()
