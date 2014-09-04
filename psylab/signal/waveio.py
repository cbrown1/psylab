# -*- coding: utf-8 -*-

# Copyright (c) 2008-2010 Christopher Brown; All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
#    * Redistributions of source code must retain the above copyright 
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright 
#      notice, this list of conditions and the following disclaimer in 
#      the documentation and/or other materials provided with the distribution
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
# POSSIBILITY OF SUCH DAMAGE.
#
# Comments and/or additions are welcome (send e-mail to: c-b@asu.edu).
# 

import numpy as np
import struct
import warnings

class WavFileWarning(UserWarning):
    pass

_big_endian = False

# assumes file pointer is immediately
#  after the 'fmt ' id
def _read_fmt_chunk(fid):
    if _big_endian:
        fmt = '>'
    else:
        fmt = '<'
    res = struct.unpack(fmt+'ihHIIHH',fid.read(20))
    size, comp, noc, rate, sbytes, ba, bits = res
    if (comp != 1 or size > 16):
        warnings.warn("Unfamiliar format bytes", WavFileWarning)
        if (size>16):
            fid.read(size-16)
    return size, comp, noc, rate, sbytes, ba, bits

# assumes file pointer is immediately
#   after the 'data' id
def _read_data_chunk(fid, noc, bits):
    if _big_endian:
        fmt = '>i'
    else:
        fmt = '<i'
    size = struct.unpack(fmt,fid.read(4))[0]
    if bits == 8:
        data = np.fromfile(fid, dtype=np.ubyte, count=size)
        if noc > 1:
            data = data.reshape(-1,noc)
    else:
        bytes = bits//8
        if _big_endian:
            dtype = '>i%d' % bytes
        else:
            dtype = '<i%d' % bytes
        data = np.fromfile(fid, dtype=dtype, count=size//bytes)
        if noc > 1:
            data = data.reshape(-1,noc)
    return data

def _read_riff_chunk(fid):
    global _big_endian
    str1 = fid.read(4)
    if str1 == 'RIFX':
        _big_endian = True
    elif str1 != 'RIFF':
        raise ValueError("Not a WAV file.")
    if _big_endian:
        fmt = '>I'
    else:
        fmt = '<I'
    fsize = struct.unpack(fmt, fid.read(4))[0] + 8
    str2 = fid.read(4)
    if (str2 != 'WAVE'):
        raise ValueError("Not a WAV file.")
    if str1 == 'RIFX':
        _big_endian = True
    return fsize

# open a wave-file
def read(file):
    """Return the sample rate (in samples/sec) and data from a WAV file

    The file can be an open file or a filename.
    The returned sample rate is a Python integer
    The data is returned as a numpy array with a
        data-type determined from the file.
    """
    if hasattr(file,'read'):
        fid = file
    else:
        fid = open(file, 'rb')

    fsize = _read_riff_chunk(fid)
    noc = 1
    bits = 8
    while (fid.tell() < fsize):
        # read the next chunk
        chunk_id = fid.read(4)
        if chunk_id == 'fmt ':
            size, comp, noc, rate, sbytes, ba, bits = _read_fmt_chunk(fid)
        elif chunk_id == 'data':
            data = _read_data_chunk(fid, noc, bits)
        else:
            warnings.warn("chunk not understood", WavFileWarning)
            size = struct.unpack('I',fid.read(4))[0]
            bytes = fid.read(size)
    fid.close()
    return rate, data

# Write a wave-file
# sample rate, data
def write(filename, rate, data):
    """Write a numpy array as a WAV file

    filename -- The name of the file to write (will be over-written)
    rate -- The sample rate (in samples/sec).
    data -- A 1-d or 2-d numpy array of integer data-type.
            The bits-per-sample will be determined by the data-type
            To write multiple-channels, use a 2-d array of shape
            (Nsamples, Nchannels)

    Writes a simple uncompressed WAV file.
    """
    fid = open(filename, 'wb')
    fid.write('RIFF')
    fid.write('\x00\x00\x00\x00')
    fid.write('WAVE')
    # fmt chunk
    fid.write('fmt ')
    if data.ndim == 1:
        noc = 1
    else:
        noc = data.shape[1]
    bits = data.dtype.itemsize * 8
    sbytes = rate*(bits / 8)*noc
    ba = noc * (bits / 8)
    fid.write(struct.pack('<ihHIIHH', 16, 1, noc, rate, sbytes, ba, bits))
    # data chunk
    fid.write('data')
    fid.write(struct.pack('<i', data.nbytes))
    import sys
    if data.dtype.byteorder == '>' or (data.dtype.byteorder == '=' and sys.byteorder == 'big'):
        data = data.byteswap()
    data.tofile(fid)
    # Determine file size and place it in correct
    #  position at start of the file.
    size = fid.tell()
    fid.seek(4)
    fid.write(struct.pack('<i', size-8))
    fid.close()

def wavread(filename):
    '''Reads wavefiles 
        
        A Matlab-style wavefile reader

        Parameters
        ----------
        filename : string
            Path to the wavefile to read

        Returns
        -------
        y : array
            The wave data
    '''
    
    fs,data = read(filename)
    return np.float64(data/32768.),fs

def wavwrite(data,fs,filename):
    '''Writes wavefiles 
        
        A Matlab-style wavefile writer

        Parameters
        ----------
        data : array
            Audio data to write
        fs : Scalar
            The sampling frequency
        filename : string
            Path to the wavefile to write
    '''
    write(filename, fs, np.int16(data*32768))


def pcm2float(sig, dtype=np.float64):
    """Convert PCM signal to floating point with a range from -1 to 1.
        Use dtype=np.float32 for single precision.

        Parameters
        ----------
        sig : array_like
            Input array, must have (signed) integral type.
        dtype : data-type, optional
            Desired (floating point) data type.
        
        Returns
        -------
        ndarray
            normalized floating point data.

        See Also
        --------
        dtype
    """
    # TODO: allow unsigned (e.g. 8-bit) data
    sig = np.asarray(sig) # make sure it's a NumPy array
    assert sig.dtype.kind == 'i', "'sig' must be an array of signed integers!"
    dtype = np.dtype(dtype) # allow string input (e.g. 'f')
    # Note that 'min' has a greater (by 1) absolute value than 'max'!
    # Therefore, we use 'min' here to avoid clipping.
    return sig.astype(dtype) / dtype.type(-np.iinfo(sig.dtype).min)
    
