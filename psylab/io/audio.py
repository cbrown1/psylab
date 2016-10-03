# -*- coding: utf-8 -*-

# Copyright (c) 2014 Christopher Brown
#
# This file is part of Psylab.
#
# Psylab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Psylab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Psylab.  If not, see <http://www.gnu.org/licenses/>.
#
# Bug reports, bug fixes, suggestions, enhancements, or other
# contributions are welcome. Go to http://code.google.com/p/psylab/
# for more information and to contribute. Or send an e-mail to:
# cbrown1@pitt.edu.
#

"""
Helper functions for working with audio data in less typical ways

"""

import os
import glob
import numpy as np
import medussa as m

def read_multi_file (folder, file_base, file_ext):
    """Reads audio data split across multiple files

        A typical use case is audio with more than 8 channels
        saved in flac format, which is limited to 8 channels per
        file. So these data would thus be saved to multiple files.

        Function assumes a file format similar to:

            track01_1.flac
            track01_2.flac
            track01_3.flac

        That is, assumes that the file counter is the last part
        of the file base name, and that the first file contains
        the first set of audio channels, etc.. In the example,
        the function will read in all three of these files, and
        you would pass 'track01' as the file_base parameter, and
        '.flac' as the file_ext parameter.

        Dependencies
        ------------
        Medussa [http://medussa.googlecode.com]

    """
    files = glob.glob(os.path.join(folder,file_base+'*'+file_ext))
    files.sort()
    y = np.array(())
    for file_path in files:
        this_data,fs = m.read_file(file_path)
        if y.ndim==1:
            y = this_data
        else:
            y = np.concatenate((y,this_data),axis=1)
    return y

def read_audio_file(file_path):
    data,fs = m.read_file(file_path)
    return data,fs

def assign_to_output_channels(data, channels):
    """Zero-pads columns to assign multi-channel audio data to desired output channels

        Intended for multi-channel playback situations in which non-contiguous
        output channels are to be used. Columns of zeros will be inserted between channels
        as needed, so that each channel of audio data will be assigned to the correct output
        channel upon playback.

        Remember, channel IDs are zero-based.

        Parameters
        ----------
        data : 2-d array
            The audio data, with each channel in a column (2nd numpy dim)
        channels : list
            The output channels to assign each audio channel to. The list length must be
            equal to data.shape[1]. Eg., if you have 2 columns of audio, and you pass the
            list [2,5], then the first column of audio will be assigned to output channel
            2 (the third channel; two columns of zeros will be prepended), and the second
            column of audio data will be assigned to output channel 5 (three more columns
            of zeros will be inserted)

        Returns
        -------
        out : 2-d array
            The output array

        Example
        -------

        >>> c1 = np.ones(4)
        >>> c2 = np.ones(4)*2
        >>> ar = np.column_stack((c1,c2)) # Two channels of fake audio
        >>> out = assign_to_output_channels(ar, [2,6]) # Assign to channels 2 and 6
        >>> out
        array([[ 0.,  0.,  1.,  0.,  0.,  0.,  2.],
               [ 0.,  0.,  1.,  0.,  0.,  0.,  2.],
               [ 0.,  0.,  1.,  0.,  0.,  0.,  2.],
               [ 0.,  0.,  1.,  0.,  0.,  0.,  2.]])
        >>> 
    """

    out = np.zeros((data.shape[0], np.max(channels)+1))
    for i in range(len(channels)):
            out[:,channels[i]] = data[:,i]

    return out
