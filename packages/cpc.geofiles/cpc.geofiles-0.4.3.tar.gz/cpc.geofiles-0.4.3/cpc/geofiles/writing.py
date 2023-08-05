import numpy as np


def stn_terciles_to_txt(below, near, above, stn_ids, output_file, in_missing_val=None,
                        out_missing_val='nan'):
    """
    Writes station tercile data to a text file

    ### Parameters

    - below - *NumPy array* - array of below normal values
    - near - *NumPy array* - array of near normal values
    - above - *NumPy array* - array of above normal values
    - output_file - *string* - text file to write values to
    - in_missing_val - *float or None* - value to consider missing - if None then don't consider
      anything missing (except for None), otherwise just write the in_missing_val in all columns
    - output_missing_val - *string* - value to write to text file signifying missing data (defaults
    """
    # Open output file
    f = open(output_file, 'w')
    # Loop over all stations
    f.write('id      below    near   above\n'.format())
    for i in range(len(stn_ids)):
        # If below, near, and above are equal to the missing value
        # specified, do not format them (leave them as is)
        if in_missing_val is None:
            is_missing = all([x is None for x in [below[i], near[i], above[i]]])
        elif np.isnan(in_missing_val):
            is_missing = all([np.isnan(x) for x in [below[i], near[i], above[i]]])
        else:
            is_missing = all([x == in_missing_val for x in [below[i], near[i], above[i]]])
        if is_missing:
            f.write(
                '{:5s}   {:>5s}   {:>5s}   {:>5s}\n'.format(
                    stn_ids[i], out_missing_val, out_missing_val, out_missing_val
                )
            )
        else:
            f.write(
                '{:5s}   {:>4.3f}   {:>4.3f}   {:>4.3f}\n'.format(
                    stn_ids[i], below[i], near[i], above[i]
                )
            )
    # Close output file
    f.close()


def grd_terciles_to_txt(below, near, above, grid, output_file, missing_val=None):
    # Reshape data from one to two dimensions
    if below.ndim == near.ndim == above.ndim == 1:
        below = np.reshape(below, (grid.num_y, grid.num_x))
        near = np.reshape(near, (grid.num_y, grid.num_x))
        above = np.reshape(above, (grid.num_y, grid.num_x))
    # Open output file
    f = open(output_file, 'w')
    # Loop over all grid points
    f.write('XXYY   below    near   above\n'.format())
    for x in range(grid.num_x):
        for y in range(grid.num_y):
            # TODO: Make the num X and Y sizes dynamic - ex. XXYY vs XXXYYY
            # If below, near, and above are equal to the missing value
            # specified, do not format them (leave them as is)
            if missing_val is not None and \
                    all([x == missing_val for x in[below[y, x],
                                                   near[y, x],
                                                   above[y, x]]]):
                f.write(
                    '{:02.0f}{:02.0f}    {:4s}    {:4s}    {:4s}\n'.format(
                        x + 1,
                        y + 1,
                        str(missing_val), str(missing_val), str(missing_val)
                    )
                )
            # If below, near, and above are not equal to the missing value
            # specified, proceed with formatting them as floats
            else:
                f.write(
                    '{:02.0f}{:02.0f}   {:4.3f}   {:4.3f}   {:4.3f}\n'.format(
                        x+1, y+1,
                        below[y, x],
                        near[y, x],
                        above[y, x])
                )
    # Close output file
    f.close()
