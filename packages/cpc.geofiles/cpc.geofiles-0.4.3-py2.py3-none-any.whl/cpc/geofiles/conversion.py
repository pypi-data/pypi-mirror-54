"""
Contains methods for converting between different file formats
"""


import numpy
from bisect import bisect

from cpc.geogrids import Geogrid
from cpc.geogrids.manipulation import interpolate

from cpc.stats import full_fields_to_ptiles


def fcst_bin_to_txt(bin_file, grid, fcst_ptiles,
                    desired_output_thresholds, txt_file,
                    output_threshold_type='ptile', terciles=False,
                    output_grid=None, out_missing_val='-999'):
    """
    Converts a forecast binary file to a text file

    The forecast binary file must contain probabilities of exceeding certain
    percentiles (AKA a POE file), where the percentiles are ascending in the
    file. The dimensions of the file should be (P x L), where:

      - P is the percentile
      - L is the location

    If `output_threshold_type` is set to 'ptile' ('raw'), then the
    probability  of exceeding the given ptiles (raw values) will be written
    to the output file under the headers ptileXX, ptileYY (rawvalXX,
    rawvalYY), etc.

    If `terciles=True`, then headers will be different (see the Parameters
    section
    below)

    Parameters
    ----------

    - bin_file (string)
        - Binary file containing the forecast, with the dimensions (ptile x Y x
        X)
    - grid (Grid)
        - Grid that the binary file maps to
    - fcst_ptiles (list)
        - 1-dimensional list of ptiles found in the forecast file
    - desired_output_thresholds (list)
        - 1-dimensional list of ptiles or raw values to include in the output
        file
    - txt_file (string)
        - Text file to write data to (will be overwritten)
    - output_threshold_type (string, optional)
        - Type of thresholds to write out ('ptile' or 'raw')
    - terciles (bool, optional)
        - If True, will output tercile probabilities (with headers below, normal
          , and above)
        - If False (default), will output probabilities of exceeding percentiles
          (with headers ptileXX, ptileYY, etc.)
        - Can only be set when 2 percentiles are supplied
    - output_grid (Grid, optional))
        - `data_utils.gridded.grid` to interpolate to before converting to a
        txt file
    - out_missing_val (string, optional)
        - value to write out to text file indicating missing data (defaults to '-999')

    Raises
    ------

    - ValueError
        - If arguments are incorrect
    """

    # If terciles=True, make sure there are only 2 percentiles
    if terciles:
        if len(desired_output_thresholds) != 2:
            raise ValueError('To output terciles, you must pass exactly 2 '
                             'desired thresholds')

    # Open binary file
    data = numpy.fromfile(bin_file, dtype='float32')

    # Reshape data
    data = numpy.reshape(data, (len(fcst_ptiles), grid.num_y, grid.num_x))

    # Interpolate, if necessary
    if output_grid:
        data_new = numpy.zeros((len(fcst_ptiles), output_grid.num_y, output_grid.num_x))
        for p in range(len(fcst_ptiles)):
            data_new[p] = interpolate(data[p, :, :], grid, output_grid)
        data = data_new
    else:
        output_grid = grid

    # Make sure desired percentiles are part of the forecast percentiles
    if set(fcst_ptiles).issuperset(set(desired_output_thresholds)):

        # Find the indexes of the desired_output_thresholds within fcst_ptiles
        fcst_ptiles.sort()
        ptile_indexes = numpy.searchsorted(fcst_ptiles, desired_output_thresholds)

        # Open the output file
        file = open(txt_file, 'w')

        # Get the number of digits in num_x and num_y for formatting below
        num_digits = max(len(str(output_grid.num_y)), len(str(output_grid.num_x)))

        # Establish the format for the grid point column and the data column(s)
        gridpoint_col_fmt = '{:0' + str(num_digits) + 'd}{:0' + str(num_digits) + 'd}'
        data_col_fmt = '{:>7.5f}'
        data_col_fmt_missing = '{:>7s}'

        # ----------------------------------------------------------------------
        # Create a header string
        #
        # The word 'id' is used for the first column (which contains
        # gridpoints). This is the typical header used in the other VWT text
        # files.
        #
        # Also note that the header of each column is designed to match the
        # length of the data in that column, so they are aligned.
        header_string = ('{:<' + str(len(gridpoint_col_fmt.format(0, 0))) +
                         's}  ').format('id')
        if terciles:
            header_string = ('{:<' + str(len(gridpoint_col_fmt.format(0, 0))) +
                             's}  ').format('id')
            for temp_str in ['below', 'normal', 'above']:
                header_string += ('{:>' + str(len(data_col_fmt.format(0))) +
                                  's}  ').format(temp_str)
        else:
            for ptile_index in ptile_indexes:
                header_string += ('{:>' + str(len(data_col_fmt.format(0))) +
                                  's}  ').format('ptile{:02d}'.format(
                    fcst_ptiles[ptile_index]))

        # Write header to file
        file.write(header_string + '\n')

        # Loop over grid
        for x in range(numpy.shape(data)[2]):
            for y in range(numpy.shape(data)[1]):
                # Create a data string consisting of the desired ptiles
                if terciles:
                    probs = []
                    probs.append(1.0 - data[ptile_indexes[0], y, x])
                    probs.append(data[ptile_indexes[0], y, x] -
                                 data[ptile_indexes[1], y, x])
                    probs.append(data[ptile_indexes[1], y, x])
                    data_string = ''
                    for prob in probs:
                        if numpy.isnan(prob):
                            data_string += (data_col_fmt_missing + '  ').format(out_missing_val)
                        else:
                            data_string += (data_col_fmt + '  ').format(prob)
                else:
                    data_string = ''
                    for ptile_index in ptile_indexes:
                        if numpy.isnan(data[ptile_index, y, x]):
                            data_string += (data_col_fmt_missing + '  ').format(out_missing_val)
                        else:
                            data_string += (data_col_fmt + '  ').format(
                                data[ptile_index, y, x])
                # Write the grid point and data to the file
                file.write((gridpoint_col_fmt + '  {}\n').format(
                    x+1, y+1, data_string))

        # Close the output file
        file.close()
    else:
        raise ValueError('Desired percentiles must all be found in fcst '
                         'percentiles')


def obs_bin_to_txt(bin_file, grid, desired_output_thresholds, txt_file,
                   output_threshold_type='ptile', climo_file=None,
                   climo_ptiles=None, output_grid=None):
    """
    Converts an observation binary file to a text file

    The observation binary file must contain raw values of the given variable.
    The file should be a single dimension (locations).

    A climatology file is necessary if output_threshold_type='ptile', in which
    case the raw values in the observation file needs to first be converted to
    ptiles. The climatology file must have probabilities of exceeding a given
    set of percentiles, and be of dimensions (P x L) where:

      - P is the percentile
      - L is the location

    climo_ptiles must also be provided specifying the percentiles in the file.

    Parameters
    ----------

    - bin_file (string)
        - Binary file containing the observation, with the dimensions (Y x X)
    - grid (Grid)
        - `data_utils.gridded.grid.Grid` that the binary file maps to
    - desired_output_thresholds (array_like)
        - 1-dimensional list of thresholds (either ptiles or raw values) to
        include in the output file
    - txt_file (string)
        - Text file to write data to (will be overwritten)
    - output_threshold_type (string, optional)
        - Type of thresholds to write out ('ptile' or 'raw')
    - climo_file (string, optional)
        - Binary file containing the climatology (needed to convert raw observations to a
          category), with the dimensions (Y x X)
    - climo_ptiles (array_like, optional)
        - List of percentiles found in the climatology file
    - output_grid (Grid, optional)
        - `data_utils.gridded.grid.Grid` to interpolate to before
        converting to a txt file

    Raises
    ------

    - ValueError
        - If arguments are incorrect
    """

    # Currently only supports 3 categories
    if len(desired_output_thresholds) != 2:
        raise ValueError('Currently only supports 3 categories')

    # Convert ptiles and thresholds into NumPy arrays
    desired_output_thresholds = numpy.array(desired_output_thresholds)
    try:
        climo_ptiles = numpy.array(climo_ptiles)
    except ValueError:
        raise ValueError('climo_ptiles must be defined as a list (or NumPy '
                         'array) of percentiles between 0 and 100')

    # Open obs binary file
    obs_data = numpy.fromfile(bin_file, dtype='float32')
    obs_data[obs_data <= -999] = numpy.nan

    # Open climo binary file
    climo_data = numpy.fromfile(climo_file, dtype='float32')
    climo_data[climo_data <= -999] = numpy.nan

    # Make sure desired percentiles are part of the forecast percentiles
    if set(climo_ptiles).issuperset(set(desired_output_thresholds)):

        # Reshape climo data
        climo_data = numpy.reshape(climo_data, (len(climo_ptiles), grid.num_y*grid.num_x))  # Reshape data

        # Convert observations to percentiles
        k = 1.343
        obs_ptile_data = 100 * full_fields_to_ptiles(obs_data, climo_data,
                                                     climo_ptiles/100, k)

        # Reshape obs data
        obs_ptile_data = numpy.reshape(obs_ptile_data, (grid.num_y, grid.num_x))  # Reshape data

        # Interpolate, if necessary
        if output_grid:
            obs_ptile_data = interpolate(
                obs_ptile_data,
                grid,
                output_grid)
        else:
            output_grid = grid

        # Open the output file
        file = open(txt_file, 'w')

        # Get the number of digits in num_x and num_y for formatting below
        num_digits = max(len(str(output_grid.num_y)), len(str(output_grid.num_x)))

        # Establish the format for the grid point column and the data column(s)
        gridpoint_col_fmt = '{:0' + str(num_digits) + 'd}{:0' + str(num_digits) + 'd}'
        data_col_fmt = {'category': '{:>12.0f}', 'percentile': '{:>12.2f}'}

        # ----------------------------------------------------------------------
        # Create a header string
        #
        # The word 'id' is used for the first column (which contains
        # gridpoints). This is the typical header used in the other VWT text
        # files.
        header_string = ('{:<' + str(len(gridpoint_col_fmt.format(0, 0))) + 's}  ').format('id')
        for temp_str in ['category', 'percentile']:
            header_string += ('{:>' + str(len(data_col_fmt[temp_str].format(0))) + 's}  ').format(temp_str)

        # Write header to file
        file.write(header_string + '\n')

        # Loop over grid
        for x in range(numpy.shape(obs_ptile_data)[1]):
            for y in range(numpy.shape(obs_ptile_data)[0]):
                # Create a data string consisting of the desired data columns
                if numpy.isnan(obs_ptile_data[y, x]):
                    data_string = (data_col_fmt['category'] + '  ' + data_col_fmt['category']).format(-999, -999)
                else:
                    data_string = ''
                    data_string += (data_col_fmt['category'] + '  ').format(
                        bisect(desired_output_thresholds, obs_ptile_data[y, x])+1)
                    data_string += (data_col_fmt['percentile'] + '  ').format(
                        obs_ptile_data[y, x])
                # Write the grid point and data to the file
                file.write((gridpoint_col_fmt + '  {}\n').format(x + 1, y + 1,
                                                                 data_string))
        # Close the output file
        file.close()
    else:
        raise ValueError('Desired percentiles must all be found in fcst '
                         'percentiles')
